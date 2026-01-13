"""
Circuit Breaker Implementation for Backend Services
"""
import time
import threading
from enum import Enum
from typing import Callable, Any, Optional, Dict, Tuple
from functools import wraps
from config.circuit_breaker_config import get_circuit_breaker_config


class CircuitState(Enum):
    """
    Circuit breaker states
    """
    CLOSED = "closed"      # Normal operation, requests pass through
    OPEN = "open"         # Tripped, requests fail immediately
    HALF_OPEN = "half_open"  # Testing if service recovered


class CircuitBreaker:
    """
    Circuit breaker implementation to prevent cascade failures
    """
    def __init__(self, name: str):
        self.name = name
        self.config = get_circuit_breaker_config()

        # State management
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time = None

        # Thread safety
        self._lock = threading.RLock()

        # Statistics
        self._success_count = 0
        self._total_requests = 0

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute a function with circuit breaker protection

        Args:
            func: Function to execute
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function

        Returns:
            Result of the function call

        Raises:
            Exception: If circuit breaker is open or function fails
        """
        with self._lock:
            if self._state == CircuitState.OPEN:
                # Check if it's time to attempt reset
                if self._should_attempt_reset():
                    self._state = CircuitState.HALF_OPEN
                else:
                    raise Exception(f"Circuit breaker '{self.name}' is OPEN. Request rejected.")

            self._total_requests += 1

        # Execute the function
        try:
            result = func(*args, **kwargs)

            with self._lock:
                self._on_success()

            return result

        except Exception as e:
            with self._lock:
                self._on_failure()

            raise e

    def _should_attempt_reset(self) -> bool:
        """
        Check if it's time to attempt resetting the circuit

        Returns:
            True if reset should be attempted, False otherwise
        """
        if self._last_failure_time is None:
            return False

        return (time.time() - self._last_failure_time) >= self.config.get_reset_timeout()

    def _on_success(self) -> None:
        """
        Handle successful operation
        """
        self._success_count += 1
        self._failure_count = 0  # Reset failure count on success
        self._state = CircuitState.CLOSED

    def _on_failure(self) -> None:
        """
        Handle failed operation
        """
        self._failure_count += 1
        self._last_failure_time = time.time()

        # Check if we should trip the circuit
        if self._failure_count >= self.config.get_failure_threshold():
            self._state = CircuitState.OPEN

    def get_state_info(self) -> Dict[str, Any]:
        """
        Get current state information

        Returns:
            Dictionary with state information
        """
        with self._lock:
            return {
                "name": self.name,
                "state": self._state.value,
                "failure_count": self._failure_count,
                "success_count": self._success_count,
                "total_requests": self._total_requests,
                "last_failure_time": self._last_failure_time,
                "can_attempt_reset": self._should_attempt_reset() if self._state == CircuitState.OPEN else False
            }

    def reset(self) -> None:
        """
        Manually reset the circuit breaker
        """
        with self._lock:
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._success_count = 0
            self._total_requests = 0
            self._last_failure_time = None

    def force_open(self) -> None:
        """
        Manually force the circuit breaker to open
        """
        with self._lock:
            self._state = CircuitState.OPEN
            self._last_failure_time = time.time()


def circuit_breaker(name: str):
    """
    Decorator to apply circuit breaker pattern to functions

    Args:
        name: Name for the circuit breaker instance

    Returns:
        Decorator function
    """
    cb = CircuitBreaker(name)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return cb.call(func, *args, **kwargs)
        return wrapper
    return decorator


class CircuitBreakerManager:
    """
    Manager for multiple circuit breakers
    """
    def __init__(self):
        self._circuit_breakers: Dict[str, CircuitBreaker] = {}
        self._lock = threading.Lock()

    def get_circuit_breaker(self, name: str) -> CircuitBreaker:
        """
        Get or create a circuit breaker by name

        Args:
            name: Name of the circuit breaker

        Returns:
            CircuitBreaker instance
        """
        with self._lock:
            if name not in self._circuit_breakers:
                self._circuit_breakers[name] = CircuitBreaker(name)
            return self._circuit_breakers[name]

    def get_all_states(self) -> Dict[str, Dict[str, Any]]:
        """
        Get state information for all circuit breakers

        Returns:
            Dictionary mapping names to state information
        """
        states = {}
        for name, cb in self._circuit_breakers.items():
            states[name] = cb.get_state_info()
        return states

    def reset_all(self) -> None:
        """
        Reset all circuit breakers
        """
        for cb in self._circuit_breakers.values():
            cb.reset()


# Global circuit breaker manager instance
circuit_breaker_manager = CircuitBreakerManager()


def get_circuit_breaker(name: str) -> CircuitBreaker:
    """
    Get a circuit breaker instance by name

    Args:
        name: Name of the circuit breaker

    Returns:
        CircuitBreaker instance
    """
    return circuit_breaker_manager.get_circuit_breaker(name)