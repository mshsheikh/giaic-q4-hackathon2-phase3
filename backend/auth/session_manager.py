"""
Session Manager for the Todo AI Chatbot
Handles session creation, validation, and management.
"""
import jwt
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from .config import AuthConfig
import secrets
import hashlib


class SessionManager:
    """
    Manages user sessions for the authentication system.
    """

    def __init__(self):
        self.config = AuthConfig()

    def create_session_token(self, user_id: str, email: str, name: str) -> str:
        """
        Create a new session token for the user.

        Args:
            user_id: ID of the user
            email: Email of the user
            name: Name of the user

        Returns:
            JWT token string
        """
        # Calculate expiry time
        expiry_time = datetime.utcnow() + timedelta(hours=self.config.SESSION_EXPIRY_HOURS)

        # Create payload
        payload = {
            "sub": user_id,
            "email": email,
            "name": name,
            "iat": datetime.utcnow(),
            "exp": expiry_time
        }

        # Encode the JWT token
        token = jwt.encode(payload, self.config.AUTH_JWT_SECRET, algorithm="HS256")
        return token

    def validate_session_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Validate a session token and return user information.

        Args:
            token: JWT token to validate

        Returns:
            User information dictionary if valid, None otherwise
        """
        try:
            # Decode and verify the token
            payload = jwt.decode(token, self.config.AUTH_JWT_SECRET, algorithms=["HS256"])

            # Check if token is expired
            exp_time = datetime.fromtimestamp(payload.get("exp", 0))
            if exp_time < datetime.utcnow():
                return None

            return {
                "user_id": payload.get("sub", ""),
                "email": payload.get("email", ""),
                "name": payload.get("name", ""),
                "exp": payload.get("exp", 0)
            }
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def refresh_session_token(self, token: str) -> Optional[str]:
        """
        Refresh a session token if it's close to expiration.

        Args:
            token: Current JWT token to refresh

        Returns:
            New JWT token string if refreshed, None if invalid
        """
        try:
            # Decode the current token
            payload = jwt.decode(token, self.config.AUTH_JWT_SECRET, algorithms=["HS256"])

            # Check if the token is close to expiration (within 1 hour)
            exp_time = datetime.fromtimestamp(payload.get("exp", 0))
            if exp_time - datetime.utcnow() < timedelta(hours=1):
                # Create a new token with extended expiry
                new_payload = {
                    "sub": payload.get("sub", ""),
                    "email": payload.get("email", ""),
                    "name": payload.get("name", ""),
                    "iat": datetime.utcnow(),
                    "exp": datetime.utcnow() + timedelta(hours=self.config.SESSION_EXPIRY_HOURS)
                }

                return jwt.encode(new_payload, self.config.AUTH_JWT_SECRET, algorithm="HS256")
            else:
                # Token is not close to expiration, return the original
                return token
        except jwt.InvalidTokenError:
            return None

    def revoke_session(self, token: str) -> bool:
        """
        Revoke a session token (in a real implementation, this would add to a blacklist).

        Args:
            token: JWT token to revoke

        Returns:
            True if successfully revoked, False otherwise
        """
        # In a real implementation, this would add the token to a blacklist
        # For now, we'll just validate that it's a valid token
        return self.validate_session_token(token) is not None

    def generate_csrf_token(self) -> str:
        """
        Generate a CSRF token for security.

        Returns:
            CSRF token string
        """
        return secrets.token_urlsafe(32)

    def validate_csrf_token(self, token: str, expected_token: str) -> bool:
        """
        Validate a CSRF token.

        Args:
            token: Token to validate
            expected_token: Expected token value

        Returns:
            True if valid, False otherwise
        """
        # Use constant time comparison to prevent timing attacks
        return secrets.compare_digest(token, expected_token)


# Global instance of the session manager
session_manager = SessionManager()