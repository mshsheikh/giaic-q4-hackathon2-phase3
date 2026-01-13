"""
Debug Mode Middleware for FastAPI
"""
import time
from typing import Callable, Awaitable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from backend.config.debug_config import get_debug_config
from backend.logging.config import log_with_context


class DebugModeMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle debug mode features
    """
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        debug_config = get_debug_config()

        # Check if debug mode is enabled via header or config
        debug_enabled = debug_config.is_debug_mode() or request.headers.get('X-Debug-Mode', '').lower() == 'true'

        if debug_enabled:
            start_time = time.time()

            # Log request in debug mode
            logger = __import__('logging').getLogger()
            log_data = log_with_context(
                request=request,
                debug_mode=True,
                method=request.method,
                url=str(request.url),
                headers=dict(request.headers),
                query_params=dict(request.query_params)
            )
            logger.debug("Debug: Incoming request", extra=log_data)

        # Process the request
        response = await call_next(request)

        if debug_enabled:
            duration = time.time() - start_time

            # Log response in debug mode
            logger = __import__('logging').getLogger()
            log_data = log_with_context(
                request=request,
                debug_mode=True,
                status_code=response.status_code,
                duration_ms=round(duration * 1000, 2),
                response_headers=dict(response.headers)
            )
            logger.debug("Debug: Outgoing response", extra=log_data)

            # Add debug headers if needed
            response.headers["X-Debug-Mode"] = "enabled"
            response.headers["X-Processing-Time"] = f"{duration:.3f}s"

        return response


def is_debug_enabled(request: Request) -> bool:
    """
    Check if debug mode is enabled for the current request

    Args:
        request: FastAPI request object

    Returns:
        True if debug mode is enabled, False otherwise
    """
    debug_config = get_debug_config()

    # Check both configuration and request header
    return debug_config.is_debug_mode() or request.headers.get('X-Debug-Mode', '').lower() == 'true'