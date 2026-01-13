"""
Rate Limiting Middleware for FastAPI
"""
import time
import hashlib
from typing import Dict, Optional, Callable, Awaitable
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse
from collections import defaultdict, deque
from backend.config.rate_limit_config import get_rate_limit_config
from backend.logging.config import log_with_context
import logging


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware to implement rate limiting based on configurable rules
    """
    def __init__(self, app):
        super().__init__(app)
        self.rate_limit_config = get_rate_limit_config()
        # Store request timestamps for each identifier
        self.requests: Dict[str, deque] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Get the rate limit key for this request
        rate_limit_key = self._get_rate_limit_key(request)

        # Check if rate limit is exceeded
        if self._is_rate_limited(rate_limit_key):
            # Log the rate limit violation
            logger = logging.getLogger()
            log_data = log_with_context(
                request=request,
                rate_limit_key=rate_limit_key,
                status="rate_limit_exceeded"
            )
            logger.warning("Rate limit exceeded", extra=log_data)

            # Return rate limit exceeded response
            return JSONResponse(
                status_code=429,
                content={
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": "Rate limit exceeded. Please try again later."
                    }
                }
            )

        # Add request timestamp
        self._add_request_timestamp(rate_limit_key)

        # Process the request
        response = await call_next(request)

        return response

    def _get_rate_limit_key(self, request: Request) -> str:
        """
        Get the rate limit key for this request based on configuration

        Args:
            request: FastAPI request object

        Returns:
            Rate limit key string
        """
        config = self.rate_limit_config

        # Determine the identifier to use for rate limiting
        identifier = None

        # Check if we have a user ID in the request
        if hasattr(request.state, 'user_id') and request.state.user_id:
            identifier = request.state.user_id
        # Fallback to IP address if no user ID
        elif request.client and request.client.host:
            identifier = request.client.host
        else:
            identifier = "unknown"

        # Create key based on endpoint and identifier
        endpoint = request.url.path
        method = request.method

        # Apply different rate limits based on endpoint
        if config.is_endpoint_exempt(endpoint):
            # Exempt endpoints have no rate limit
            return f"exempt_{identifier}"
        else:
            # Apply standard rate limiting
            return f"{method}:{endpoint}:{identifier}"

    def _is_rate_limited(self, rate_limit_key: str) -> bool:
        """
        Check if the rate limit has been exceeded for this key

        Args:
            rate_limit_key: Rate limit key to check

        Returns:
            True if rate limit is exceeded, False otherwise
        """
        config = self.rate_limit_config

        # Get the current time
        now = time.time()

        # Get requests for this key
        requests = self.requests[rate_limit_key]

        # Remove old requests that are outside the time window
        while requests and (now - requests[0]) > config.get_time_window():
            requests.popleft()

        # Get the limit based on the endpoint
        endpoint = rate_limit_key.split(':')[1] if ':' in rate_limit_key else 'default'
        limit = config.get_limit_for_endpoint(endpoint)

        # Check if we've exceeded the limit
        return len(requests) >= limit

    def _add_request_timestamp(self, rate_limit_key: str) -> None:
        """
        Add the current timestamp to the request log for this key

        Args:
            rate_limit_key: Rate limit key to add timestamp for
        """
        self.requests[rate_limit_key].append(time.time())


def get_client_identifier(request: Request) -> str:
    """
    Get a client identifier for rate limiting purposes

    Args:
        request: FastAPI request object

    Returns:
        Client identifier string
    """
    # Check for user ID first
    if hasattr(request.state, 'user_id') and request.state.user_id:
        return request.state.user_id

    # Fallback to IP address
    if request.client and request.client.host:
        return request.client.host

    # Last resort
    return "unknown"