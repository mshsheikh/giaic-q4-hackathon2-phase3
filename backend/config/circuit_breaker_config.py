"""
Circuit Breaker Configuration for Backend
"""
import os
from typing import Optional


class CircuitBreakerConfig:
    """
    Configuration class for circuit breaker settings
    """
    def __init__(self):
        # Default values
        self.FAILURE_THRESHOLD = int(os.getenv('CB_FAILURE_THRESHOLD', '5'))  # failures before opening
        self.RESET_TIMEOUT = int(os.getenv('CB_RESET_TIMEOUT', '60'))  # seconds to wait before half-open
        self.TIMEOUT_DURATION = int(os.getenv('CB_TIMEOUT_DURATION', '10'))  # seconds for individual calls
        self.HALF_OPEN_ATTEMPTS = int(os.getenv('CB_HALF_OPEN_ATTEMPTS', '3'))  # attempts when half-open
        self.ENABLED = os.getenv('CB_ENABLED', 'true').lower() == 'true'  # whether CB is enabled

    def get_failure_threshold(self) -> int:
        """
        Get the failure threshold for opening the circuit

        Returns:
            Number of failures before opening the circuit
        """
        return self.FAILURE_THRESHOLD

    def get_reset_timeout(self) -> int:
        """
        Get the reset timeout for transitioning from OPEN to HALF_OPEN

        Returns:
            Timeout in seconds
        """
        return self.RESET_TIMEOUT

    def get_timeout_duration(self) -> int:
        """
        Get the timeout duration for individual calls

        Returns:
            Timeout duration in seconds
        """
        return self.TIMEOUT_DURATION

    def get_half_open_attempts(self) -> int:
        """
        Get the number of attempts allowed when in HALF_OPEN state

        Returns:
            Number of attempts
        """
        return self.HALF_OPEN_ATTEMPTS

    def is_enabled(self) -> bool:
        """
        Check if circuit breakers are enabled

        Returns:
            True if enabled, False otherwise
        """
        return self.ENABLED


# Global circuit breaker configuration instance
circuit_breaker_config = CircuitBreakerConfig()


def get_circuit_breaker_config() -> CircuitBreakerConfig:
    """
    Get the global circuit breaker configuration instance

    Returns:
        CircuitBreakerConfig instance
    """
    return circuit_breaker_config