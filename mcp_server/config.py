"""
Configuration for the MCP Server
"""
import os
from typing import Optional


class MCPConfig:
    """
    Configuration class for MCP server settings
    """

    # Database configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/todo_chatbot_dev")

    # Server configuration
    SERVER_HOST: str = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("MCP_SERVER_PORT", "8000"))

    # MCP-specific configuration
    MCP_VERSION: str = os.getenv("MCP_VERSION", "1.0")
    MCP_SERVER_NAME: str = os.getenv("MCP_SERVER_NAME", "todo-mcp-server")

    # Database connection pool settings
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "5"))
    DB_POOL_MAX_OVERFLOW: int = int(os.getenv("DB_POOL_MAX_OVERFLOW", "10"))

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

        if not cls.DATABASE_URL:
            raise ValueError("DATABASE_URL must be set")