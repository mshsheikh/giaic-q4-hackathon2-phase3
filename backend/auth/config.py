"""
Configuration for the Authentication system
"""
import os
from typing import Optional


class AuthConfig:
    """
    Configuration class for authentication settings
    """

    # Better Auth configuration
    AUTH_JWT_SECRET: str = os.getenv("AUTH_JWT_SECRET", "")
    AUTH_COOKIE_NAME: str = os.getenv("AUTH_COOKIE_NAME", "__Secure-authjs.session-token")
    AUTH_BASE_URL: str = os.getenv("AUTH_BASE_URL", "http://localhost:3000/api/auth")

    # Session configuration
    SESSION_EXPIRY_HOURS: int = int(os.getenv("SESSION_EXPIRY_HOURS", "24"))

    # Security settings
    SECURE_COOKIES: bool = os.getenv("SECURE_COOKIES", "True").lower() == "true"
    CSRF_PROTECTION: bool = os.getenv("CSRF_PROTECTION", "True").lower() == "true"

    # Debug mode
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    @classmethod
    def validate(cls) -> None:
        """
        Validate the authentication configuration
        """
        if not cls.AUTH_JWT_SECRET and not cls.DEBUG:
            raise ValueError("AUTH_JWT_SECRET must be set in production")