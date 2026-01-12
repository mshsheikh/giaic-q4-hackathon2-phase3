"""
Logout Handler for the Todo AI Chatbot
Handles user logout and session cleanup.
"""
from fastapi import Response
from .config import AuthConfig
from .session_manager import session_manager
from typing import Dict, Any


class LogoutHandler:
    """
    Handler for logout operations and session cleanup.
    """

    def __init__(self):
        self.config = AuthConfig()

    def logout_user(self, response: Response, token: str = None) -> Dict[str, Any]:
        """
        Log out the user and clean up their session.

        Args:
            response: FastAPI response object to set cookies
            token: JWT token to revoke (optional)

        Returns:
            Dictionary with logout result
        """
        # Revoke the session token if provided
        if token:
            session_manager.revoke_session(token)

        # Clear the authentication cookie
        response.set_cookie(
            key=self.config.AUTH_COOKIE_NAME,
            value="",
            httponly=True,
            secure=self.config.SECURE_COOKIES,
            samesite="lax",
            max_age=0,  # Expire immediately
            expires="Thu, 01 Jan 1970 00:00:00 GMT"  # Past date to ensure deletion
        )

        # In a real implementation, we might also:
        # - Add the token to a blacklist to prevent reuse
        # - Clear server-side session data
        # - Trigger cleanup of any user-specific resources

        return {
            "success": True,
            "message": "User logged out successfully"
        }

    def handle_session_expiry(self, response: Response) -> Dict[str, Any]:
        """
        Handle session expiry by cleaning up the expired session.

        Args:
            response: FastAPI response object to set cookies

        Returns:
            Dictionary with expiry handling result
        """
        # Clear the expired authentication cookie
        response.set_cookie(
            key=self.config.AUTH_COOKIE_NAME,
            value="",
            httponly=True,
            secure=self.config.SECURE_COOKIES,
            samesite="lax",
            max_age=0,  # Expire immediately
            expires="Thu, 01 Jan 1970 00:00:00 GMT"  # Past date to ensure deletion
        )

        return {
            "success": True,
            "message": "Session expired and cleared",
            "redirect_url": "/login"  # Suggest redirect to login page
        }


# Global instance of the logout handler
logout_handler = LogoutHandler()