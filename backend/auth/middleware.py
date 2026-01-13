"""
Authentication Middleware for the Todo AI Chatbot
"""
import jwt
from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.auth.config import AuthConfig
from backend.auth.session_manager import session_manager
from typing import Optional, Dict, Any
import httpx


class AuthMiddleware:
    """
    Authentication middleware to handle user authentication and session management
    """

    def __init__(self):
        self.config = AuthConfig()
        self.security = HTTPBearer(auto_error=True)

    async def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify the authentication token and return user information.

        Args:
            token: JWT token to verify

        Returns:
            User information dictionary if token is valid, None otherwise
        """
        return session_manager.validate_session_token(token)

    async def get_current_user(self, request: Request) -> Optional[Dict[str, Any]]:
        """
        Get the current user from the request based on authentication.

        Args:
            request: FastAPI request object

        Returns:
            User information dictionary if authenticated, None otherwise
        """
        # First, try to get the token from the Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

            # Try to refresh the token if needed
            refreshed_token = session_manager.refresh_session_token(token)
            if refreshed_token and refreshed_token != token:
                # In a real implementation, we'd update the token in the response
                pass

            return await self.verify_token(refreshed_token or token)

        # If not in header, try to get from cookies (Better Auth pattern)
        session_token = request.cookies.get(self.config.AUTH_COOKIE_NAME)
        if session_token:
            # Try to refresh the token if needed
            refreshed_token = session_manager.refresh_session_token(session_token)
            if refreshed_token and refreshed_token != session_token:
                # In a real implementation, we'd update the token in the response
                pass

            return await self.verify_token(refreshed_token or session_token)

        # If no token is found, return None
        return None

    async def authenticate_request(self, request: Request) -> Dict[str, Any]:
        """
        Authenticate the incoming request and return user information.

        Args:
            request: FastAPI request object

        Returns:
            User information dictionary

        Raises:
            HTTPException: If authentication fails
        """
        user = await self.get_current_user(request)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )

        return user

    async def validate_user_access(self, user: Dict[str, Any], resource_user_id: str) -> bool:
        """
        Validate that the authenticated user has access to a specific resource.

        Args:
            user: User information dictionary
            resource_user_id: ID of the user who owns the resource

        Returns:
            True if user has access, False otherwise
        """
        return user.get("user_id") == resource_user_id

    async def handle_session_expiry(self, request: Request) -> Optional[str]:
        """
        Handle session expiry and redirect if needed.

        Args:
            request: FastAPI request object

        Returns:
            Redirect URL if session expired, None otherwise
        """
        user = await self.get_current_user(request)
        if not user:
            # Session has expired or is invalid
            return "/login"  # Return login page URL

        return None

    def get_csrf_token(self) -> str:
        """
        Generate a CSRF token for security.

        Returns:
            CSRF token string
        """
        return session_manager.generate_csrf_token()


# Global instance of the auth middleware
auth_middleware = AuthMiddleware()