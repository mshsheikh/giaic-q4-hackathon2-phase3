"""
Structured Logging Middleware for FastAPI
"""
import time
import logging
from typing import Callable, Awaitable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from ..logging.config import log_with_context


class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add structured logging to all requests
    """
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Get start time
        start_time = time.time()

        # Process the request
        response = await call_next(request)

        # Calculate duration
        duration = time.time() - start_time

        # Log the request
        logger = logging.getLogger()
        log_data = log_with_context(
            request=request,
            method=request.method,
            url=str(request.url),
            status_code=response.status_code,
            duration_ms=round(duration * 1000, 2)
        )

        # Log based on status code
        if response.status_code >= 400:
            logger.error(f"Request completed with error", extra=log_data)
        elif response.status_code >= 300:
            logger.warning(f"Request completed with redirect", extra=log_data)
        else:
            logger.info(f"Request completed successfully", extra=log_data)

        return response


# Create a helper function to get logger with proper configuration
def get_structured_logger() -> logging.Logger:
    """
    Get a configured logger instance

    Returns:
        Configured logger instance
    """
    return logging.getLogger()