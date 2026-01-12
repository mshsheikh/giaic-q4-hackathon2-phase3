"""
Timeout Middleware for FastAPI
"""
import asyncio
import time
from typing import Callable, Awaitable
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse
from ..config.timeout_config import get_timeout_config


class TimeoutMiddleware(BaseHTTPMiddleware):
    """
    Middleware to enforce request timeouts
    """
    def __init__(self, app, default_timeout: int = 30):
        super().__init__(app)
        self.default_timeout = default_timeout

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        timeout_config = get_timeout_config()
        timeout = timeout_config.get_default_request_timeout()

        try:
            # Create an async task for the request
            request_task = call_next(request)

            # Wait for the request to complete with timeout
            response = await asyncio.wait_for(request_task, timeout=timeout)
            return response
        except asyncio.TimeoutError:
            # Return a timeout error response
            return JSONResponse(
                status_code=408,
                content={
                    "error": {
                        "code": "REQUEST_TIMEOUT",
                        "message": f"Request timed out after {timeout} seconds"
                    }
                }
            )


def get_timeout_for_endpoint(request: Request) -> int:
    """
    Get the appropriate timeout for a specific endpoint

    Args:
        request: FastAPI request object

    Returns:
        Timeout value in seconds
    """
    timeout_config = get_timeout_config()

    # Different endpoints may have different timeout requirements
    path = request.url.path

    if path.startswith('/api/') and 'upload' in path:
        return timeout_config.get_file_upload_timeout()
    elif path.startswith('/api/') and 'chat' in path:
        return timeout_config.get_agent_processing_timeout()
    else:
        return timeout_config.get_default_request_timeout()