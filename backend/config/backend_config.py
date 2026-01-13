"""
Configuration for the Backend API
"""
import os
from typing import Optional


class BackendConfig:
    """
    Configuration class for Backend API settings
    """

    # Database configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/todo_chatbot_dev")

    # Server configuration
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8000"))
    API_PREFIX: str = os.getenv("API_PREFIX", "/api")

    # Agent configuration
    AGENT_API_KEY: str = os.getenv("AGENT_API_KEY", "")
    AGENT_ENDPOINT: str = os.getenv("AGENT_ENDPOINT", "http://localhost:8001/agent")

    # Database connection pool settings
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "5"))
    DB_POOL_MAX_OVERFLOW: int = int(os.getenv("DB_POOL_MAX_OVERFLOW", "10"))

    # CORS settings
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "*")

    # Debug mode
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    @classmethod
    def validate(cls) -> None:
        """
        Validate the configuration settings
        """
        if cls.DB_POOL_SIZE <= 0:
            raise ValueError("DB_POOL_SIZE must be greater than 0")

        if cls.DB_POOL_MAX_OVERFLOW < 0:
            raise ValueError("DB_POOL_MAX_OVERFLOW must be greater than or equal to 0")