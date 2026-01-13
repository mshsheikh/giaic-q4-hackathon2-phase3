"""
Rate Limit Service for Backend
"""
import time
from typing import Dict, Optional, List
from collections import defaultdict, deque
from config.rate_limit_config import get_rate_limit_config


class RateLimitService:
    """
    Service class for managing rate limiting across the application
    """
    def __init__(self):
        self.config = get_rate_limit_config()
        # Store request timestamps for each identifier
        self.requests: Dict[str, deque] = defaultdict(deque)

    def is_allowed(self, identifier: str, endpoint: str = "default") -> bool:
        """
        Check if a request is allowed based on rate limits

        Args:
            identifier: Unique identifier for the requester (user ID or IP)
            endpoint: The endpoint being accessed

        Returns:
            True if allowed, False if rate limit exceeded
        """
        # Get the current time
        now = time.time()

        # Get requests for this identifier
        requests = self.requests[identifier]

        # Remove old requests that are outside the time window
        time_window = self.config.get_time_window()
        while requests and (now - requests[0]) > time_window:
            requests.popleft()

        # Get the limit based on the endpoint
        limit = self.config.get_limit_for_endpoint(endpoint)

        # Check if we've exceeded the limit
        if len(requests) >= limit:
            return False

        # Add the current request
        self.add_request(identifier)

        return True

    def add_request(self, identifier: str) -> None:
        """
        Add a request to the rate limit tracking

        Args:
            identifier: Unique identifier for the requester
        """
        self.requests[identifier].append(time.time())

    def get_remaining_requests(self, identifier: str, endpoint: str = "default") -> int:
        """
        Get the number of remaining requests for an identifier

        Args:
            identifier: Unique identifier for the requester
            endpoint: The endpoint being accessed

        Returns:
            Number of remaining requests
        """
        # Get the current time
        now = time.time()

        # Get requests for this identifier
        requests = self.requests[identifier]

        # Remove old requests that are outside the time window
        time_window = self.config.get_time_window()
        while requests and (now - requests[0]) > time_window:
            requests.popleft()

        # Get the limit based on the endpoint
        limit = self.config.get_limit_for_endpoint(endpoint)

        return limit - len(requests)

    def get_reset_time(self, identifier: str, endpoint: str = "default") -> float:
        """
        Get the time when the rate limit will reset for an identifier

        Args:
            identifier: Unique identifier for the requester
            endpoint: The endpoint being accessed

        Returns:
            Unix timestamp when the rate limit will reset
        """
        # Find the earliest request in the current window
        requests = self.requests[identifier]

        if not requests:
            return time.time()

        # The reset time is the time of the oldest request plus the time window
        time_window = self.config.get_time_window()
        return requests[0] + time_window

    def get_usage_stats(self, identifier: str, endpoint: str = "default") -> Dict[str, int]:
        """
        Get usage statistics for an identifier

        Args:
            identifier: Unique identifier for the requester
            endpoint: The endpoint being accessed

        Returns:
            Dictionary with usage statistics
        """
        remaining = self.get_remaining_requests(identifier, endpoint)
        limit = self.config.get_limit_for_endpoint(endpoint)
        used = limit - remaining

        return {
            "limit": limit,
            "used": used,
            "remaining": remaining,
            "reset_time": self.get_reset_time(identifier, endpoint)
        }

    def clear_identifier(self, identifier: str) -> None:
        """
        Clear rate limit tracking for an identifier

        Args:
            identifier: Unique identifier to clear
        """
        if identifier in self.requests:
            del self.requests[identifier]

    def cleanup_old_records(self) -> None:
        """
        Clean up old rate limit records that are outside the time window
        """
        now = time.time()
        time_window = self.config.get_time_window()

        # Create a list of keys to remove to avoid modifying dict during iteration
        keys_to_remove = []

        for identifier, requests in self.requests.items():
            # Remove old requests
            while requests and (now - requests[0]) > time_window:
                requests.popleft()

            # If no requests left, mark for removal
            if not requests:
                keys_to_remove.append(identifier)

        # Remove identifiers with no requests
        for key in keys_to_remove:
            del self.requests[key]