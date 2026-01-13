"""
Validation Middleware for FastAPI
"""
from typing import Callable, Awaitable
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from pydantic import ValidationError
from backend.logging.config import log_with_context
import logging


class ValidationMiddleware(BaseHTTPMiddleware):
    """
    Middleware to perform input validation on all requests
    """
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Log the request for validation tracking
        logger = logging.getLogger()

        try:
            # Perform validation based on endpoint
            await self.validate_request(request)

            # Continue with the request if validation passes
            response = await call_next(request)
            return response

        except ValidationError as ve:
            # Log validation errors
            log_data = log_with_context(
                request=request,
                error="Validation error",
                validation_errors=ve.errors()
            )
            logger.warning("Request validation failed", extra=log_data)

            # Return a structured error response
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=422,
                content={
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "Request validation failed",
                        "details": ve.errors()
                    }
                }
            )
        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        except Exception as e:
            # Handle any other validation-related exceptions
            log_data = log_with_context(
                request=request,
                error=str(e),
                error_type=type(e).__name__
            )
            logger.error("Unexpected error during validation", extra=log_data)

            # Return a generic error response
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=500,
                content={
                    "error": {
                        "code": "VALIDATION_SYSTEM_ERROR",
                        "message": "An error occurred during request validation"
                    }
                }
            )

    async def validate_request(self, request: Request) -> None:
        """
        Perform validation on the incoming request based on the endpoint

        Args:
            request: FastAPI request object
        """
        # Extract path and method to determine validation requirements
        path = request.url.path
        method = request.method.lower()

        # For now, we'll implement validation based on the endpoint
        # In a real system, this would be more sophisticated and tied to route definitions
        if path.startswith('/api/') and method in ['post', 'put', 'patch']:
            # These endpoints typically require more validation
            await self.validate_api_request(request, path, method)
        elif path.startswith('/health'):
            # Health endpoints might have minimal validation
            await self.validate_health_request(request, path, method)
        # Add more validation rules as needed for different endpoint types

    async def validate_api_request(self, request: Request, path: str, method: str) -> None:
        """
        Validate API requests based on path and method

        Args:
            request: FastAPI request object
            path: Request path
            method: HTTP method
        """
        # For POST /api/{user_id}/chat
        if 'chat' in path and method == 'post':
            # Validate the chat request body
            body = await request.json()

            # Basic validation for required fields
            if 'message' not in body:
                raise ValidationError("Message is required", "ChatRequest")

            message = body.get('message', '')
            if not message or not message.strip():
                raise ValidationError("Message cannot be empty", "ChatRequest")

            # Validate message length
            if len(message) > 5000:
                raise ValidationError("Message exceeds maximum length of 5000 characters", "ChatRequest")

        # Add more specific validations as needed for other API endpoints

    async def validate_health_request(self, request: Request, path: str, method: str) -> None:
        """
        Validate health check requests

        Args:
            request: FastAPI request object
            path: Request path
            method: HTTP method
        """
        # Health requests typically don't require extensive validation
        # but we can still check for basic requirements if needed
        pass


def validate_input_with_schema(data: dict, schema_class):
    """
    Helper function to validate input data against a Pydantic schema

    Args:
        data: Input data to validate
        schema_class: Pydantic schema class to validate against

    Returns:
        Validated data as a Pydantic model instance

    Raises:
        ValidationError: If validation fails
    """
    return schema_class(**data)