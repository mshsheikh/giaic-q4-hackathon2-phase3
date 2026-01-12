"""
Configuration for the TodoAgent
"""
import os
from typing import Optional


class AgentConfig:
    """
    Configuration class for TodoAgent settings
    """

    # OpenAI configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")

    # Agent configuration
    AGENT_NAME: str = os.getenv("AGENT_NAME", "TodoAgent")
    AGENT_DESCRIPTION: str = os.getenv("AGENT_DESCRIPTION", "An AI assistant for managing your todo list.")

    # MCP Server configuration
    MCP_SERVER_URL: str = os.getenv("MCP_SERVER_URL", "http://localhost:8000")

    # Timeout settings
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))

    # Debug mode
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    @classmethod
    def validate(cls) -> None:
        """
        Validate the configuration settings
        """
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY must be set")

        if not cls.AGENT_NAME:
            raise ValueError("AGENT_NAME must be set")