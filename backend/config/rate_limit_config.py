"""
Rate Limit Configuration for Backend
"""
import os
from typing import Dict, List, Optional


class RateLimitConfig:
    """
    Configuration class for rate limiting settings
    """
    def __init__(self):
        # Default values
        self.DEFAULT_RATE_LIMIT = int(os.getenv('DEFAULT_RATE_LIMIT', '100'))  # requests per window
        self.RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', '3600'))  # seconds
        self.IP_RATE_LIMIT = int(os.getenv('IP_RATE_LIMIT', '1000'))  # requests per window for IPs
        self.USER_RATE_LIMIT = int(os.getenv('USER_RATE_LIMIT', '500'))  # requests per window for users
        self.BURST_LIMIT = int(os.getenv('BURST_LIMIT', '10'))  # requests per second for bursts

        # Endpoints that are exempt from rate limiting
        self.EXEMPT_ENDPOINTS = os.getenv('EXEMPT_ENDPOINTS', '/health,/health/ready,/health/live').split(',')

        # Specific rate limits for different endpoints
        self.ENDPOINT_LIMITS = {
            '/api/chat': int(os.getenv('CHAT_RATE_LIMIT', '10')),  # per minute
            '/api/tasks': int(os.getenv('TASKS_RATE_LIMIT', '50')),
            '/api/conversations': int(os.getenv('CONVERSATIONS_RATE_LIMIT', '30')),
        }

    def get_default_limit(self) -> int:
        """
        Get the default rate limit

        Returns:
            Default rate limit value
        """
        return self.DEFAULT_RATE_LIMIT

    def get_time_window(self) -> int:
        """
        Get the time window for rate limiting

        Returns:
            Time window in seconds
        """
        return self.RATE_LIMIT_WINDOW

    def get_ip_limit(self) -> int:
        """
        Get the rate limit for IP addresses

        Returns:
            IP rate limit value
        """
        return self.IP_RATE_LIMIT

    def get_user_limit(self) -> int:
        """
        Get the rate limit for users

        Returns:
            User rate limit value
        """
        return self.USER_RATE_LIMIT

    def get_burst_limit(self) -> int:
        """
        Get the burst rate limit

        Returns:
            Burst rate limit value
        """
        return self.BURST_LIMIT

    def is_endpoint_exempt(self, endpoint: str) -> bool:
        """
        Check if an endpoint is exempt from rate limiting

        Args:
            endpoint: Endpoint path to check

        Returns:
            True if exempt, False otherwise
        """
        return endpoint in self.EXEMPT_ENDPOINTS

    def get_limit_for_endpoint(self, endpoint: str) -> int:
        """
        Get the rate limit for a specific endpoint

        Args:
            endpoint: Endpoint path

        Returns:
            Rate limit value for the endpoint
        """
        return self.ENDPOINT_LIMITS.get(endpoint, self.DEFAULT_RATE_LIMIT)


# Global rate limit configuration instance
rate_limit_config = RateLimitConfig()


def get_rate_limit_config() -> RateLimitConfig:
    """
    Get the global rate limit configuration instance

    Returns:
        RateLimitConfig instance
    """
    return rate_limit_config