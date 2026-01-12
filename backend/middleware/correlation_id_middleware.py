"""
Correlation ID Middleware for FastAPI applications
"""
import uuid
from typing import Callable, Awaitable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add correlation ID to all requests for tracing
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Get correlation ID from header if provided, otherwise generate new one
        correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())

        # Add correlation ID to request state
        request.state.correlation_id = correlation_id

        # Add correlation ID to response headers
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id

        return response


def get_correlation_id(request: Request) -> str:
    """
    Helper function to get correlation ID from request

    Args:
        request: FastAPI request object

    Returns:
        Correlation ID string
    """
    return getattr(request.state, 'correlation_id', str(uuid.uuid4()))