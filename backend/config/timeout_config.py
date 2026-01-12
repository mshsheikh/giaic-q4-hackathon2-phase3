"""
Timeout Configuration for Backend
"""
import os
from typing import Optional


class TimeoutConfig:
    """
    Configuration class for timeout settings
    """
    def __init__(self):
        # Default timeout values (in seconds)
        self.DEFAULT_REQUEST_TIMEOUT = int(os.getenv('DEFAULT_REQUEST_TIMEOUT', '30'))
        self.DATABASE_QUERY_TIMEOUT = int(os.getenv('DATABASE_QUERY_TIMEOUT', '10'))
        self.EXTERNAL_API_TIMEOUT = int(os.getenv('EXTERNAL_API_TIMEOUT', '30'))
        self.MCP_TOOL_TIMEOUT = int(os.getenv('MCP_TOOL_TIMEOUT', '15'))
        self.AGENT_PROCESSING_TIMEOUT = int(os.getenv('AGENT_PROCESSING_TIMEOUT', '60'))
        self.FILE_UPLOAD_TIMEOUT = int(os.getenv('FILE_UPLOAD_TIMEOUT', '120'))

    def get_default_request_timeout(self) -> int:
        """
        Get the default request timeout value

        Returns:
            Timeout value in seconds
        """
        return self.DEFAULT_REQUEST_TIMEOUT

    def get_database_query_timeout(self) -> int:
        """
        Get the database query timeout value

        Returns:
            Timeout value in seconds
        """
        return self.DATABASE_QUERY_TIMEOUT

    def get_external_api_timeout(self) -> int:
        """
        Get the external API timeout value

        Returns:
            Timeout value in seconds
        """
        return self.EXTERNAL_API_TIMEOUT

    def get_mcp_tool_timeout(self) -> int:
        """
        Get the MCP tool timeout value

        Returns:
            Timeout value in seconds
        """
        return self.MCP_TOOL_TIMEOUT

    def get_agent_processing_timeout(self) -> int:
        """
        Get the agent processing timeout value

        Returns:
            Timeout value in seconds
        """
        return self.AGENT_PROCESSING_TIMEOUT

    def get_file_upload_timeout(self) -> int:
        """
        Get the file upload timeout value

        Returns:
            Timeout value in seconds
        """
        return self.FILE_UPLOAD_TIMEOUT


# Global timeout configuration instance
timeout_config = TimeoutConfig()


def get_timeout_config() -> TimeoutConfig:
    """
    Get the global timeout configuration instance

    Returns:
        TimeoutConfig instance
    """
    return timeout_config