"""
Circuit Breaker Implementation for TodoAgent
"""
import time
import threading
from enum import Enum
from typing import Callable, Any, Optional, Dict
from functools import wraps
from ..config import AgentConfig


class AgentCircuitState(Enum):
    """
    Circuit breaker states for the agent
    """
    CLOSED = "closed"      # Normal operation, requests pass through
    OPEN = "open"         # Tripped, requests fail immediately
    HALF_OPEN = "half_open"  # Testing if service recovered


class AgentCircuitBreaker:
    """
    Circuit breaker implementation for agent operations
    """
    def __init__(self, name: str):
        self.name = name
        self.config = AgentConfig()

        # State management
        self._state = AgentCircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time = None

        # Thread safety
        self._lock = threading.RLock()

        # Statistics
        self._success_count = 0
        self._total_requests = 0

        # Configuration defaults
        self.failure_threshold = 5
        self.reset_timeout = 60  # seconds
        self.timeout_duration = 10  # seconds for individual calls

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
            if self._state == AgentCircuitState.OPEN:
                # Check if it's time to attempt reset
                if self._should_attempt_reset():
                    self._state = AgentCircuitState.HALF_OPEN
                else:
                    raise Exception(f"Agent circuit breaker '{self.name}' is OPEN. Request rejected.")

            self._total_requests += 1

        # Execute the function with timeout
        import asyncio
        try:
            # For async functions, we need to handle them differently
            if asyncio.iscoroutinefunction(func):
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(lambda: asyncio.run(func(*args, **kwargs)))
                    result = future.result(timeout=self.timeout_duration)
            else:
                # For sync functions, execute normally
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

        return (time.time() - self._last_failure_time) >= self.reset_timeout

    def _on_success(self) -> None:
        """
        Handle successful operation
        """
        self._success_count += 1
        self._failure_count = 0  # Reset failure count on success
        self._state = AgentCircuitState.CLOSED

    def _on_failure(self) -> None:
        """
        Handle failed operation
        """
        self._failure_count += 1
        self._last_failure_time = time.time()

        # Check if we should trip the circuit
        if self._failure_count >= self.failure_threshold:
            self._state = AgentCircuitState.OPEN

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
                "can_attempt_reset": self._should_attempt_reset() if self._state == AgentCircuitState.OPEN else False
            }

    def reset(self) -> None:
        """
        Manually reset the circuit breaker
        """
        with self._lock:
            self._state = AgentCircuitState.CLOSED
            self._failure_count = 0
            self._success_count = 0
            self._total_requests = 0
            self._last_failure_time = None

    def force_open(self) -> None:
        """
        Manually force the circuit breaker to open
        """
        with self._lock:
            self._state = AgentCircuitState.OPEN
            self._last_failure_time = time.time()


def agent_circuit_breaker(name: str):
    """
    Decorator to apply circuit breaker pattern to agent functions

    Args:
        name: Name for the circuit breaker instance

    Returns:
        Decorator function
    """
    cb = AgentCircuitBreaker(name)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return cb.call(func, *args, **kwargs)
        return wrapper
    return decorator


class AgentCircuitBreakerManager:
    """
    Manager for multiple agent circuit breakers
    """
    def __init__(self):
        self._circuit_breakers: Dict[str, AgentCircuitBreaker] = {}
        self._lock = threading.Lock()

    def get_circuit_breaker(self, name: str) -> AgentCircuitBreaker:
        """
        Get or create an agent circuit breaker by name

        Args:
            name: Name of the circuit breaker

        Returns:
            AgentCircuitBreaker instance
        """
        with self._lock:
            if name not in self._circuit_breakers:
                self._circuit_breakers[name] = AgentCircuitBreaker(name)
            return self._circuit_breakers[name]

    def get_all_states(self) -> Dict[str, Dict[str, Any]]:
        """
        Get state information for all agent circuit breakers

        Returns:
            Dictionary mapping names to state information
        """
        states = {}
        for name, cb in self._circuit_breakers.items():
            states[name] = cb.get_state_info()
        return states

    def reset_all(self) -> None:
        """
        Reset all agent circuit breakers
        """
        for cb in self._circuit_breakers.values():
            cb.reset()


# Global agent circuit breaker manager instance
agent_circuit_breaker_manager = AgentCircuitBreakerManager()


def get_agent_circuit_breaker(name: str) -> AgentCircuitBreaker:
    """
    Get an agent circuit breaker instance by name

    Args:
        name: Name of the circuit breaker

    Returns:
        AgentCircuitBreaker instance
    """
    return agent_circuit_breaker_manager.get_circuit_breaker(name)