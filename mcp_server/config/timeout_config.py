"""
Timeout Configuration for MCP Server
"""
import os
from typing import Optional


class MCPServerTimeoutConfig:
    """
    Configuration class for MCP server timeout settings
    """
    def __init__(self):
        # Default timeout values (in seconds)
        self.DEFAULT_TOOL_TIMEOUT = int(os.getenv('MCP_DEFAULT_TOOL_TIMEOUT', '15'))
        self.DATABASE_QUERY_TIMEOUT = int(os.getenv('MCP_DATABASE_QUERY_TIMEOUT', '10'))
        self.EXTERNAL_SERVICE_TIMEOUT = int(os.getenv('MCP_EXTERNAL_SERVICE_TIMEOUT', '30'))
        self.LONG_RUNNING_TASK_TIMEOUT = int(os.getenv('MCP_LONG_RUNNING_TASK_TIMEOUT', '60'))

    def get_default_tool_timeout(self) -> int:
        """
        Get the default tool timeout value

        Returns:
            Timeout value in seconds
        """
        return self.DEFAULT_TOOL_TIMEOUT

    def get_database_query_timeout(self) -> int:
        """
        Get the database query timeout value

        Returns:
            Timeout value in seconds
        """
        return self.DATABASE_QUERY_TIMEOUT

    def get_external_service_timeout(self) -> int:
        """
        Get the external service timeout value

        Returns:
            Timeout value in seconds
        """
        return self.EXTERNAL_SERVICE_TIMEOUT

    def get_long_running_task_timeout(self) -> int:
        """
        Get the long running task timeout value

        Returns:
            Timeout value in seconds
        """
        return self.LONG_RUNNING_TASK_TIMEOUT


# Global MCP server timeout configuration instance
mcp_timeout_config = MCPServerTimeoutConfig()


def get_mcp_timeout_config() -> MCPServerTimeoutConfig:
    """
    Get the global MCP server timeout configuration instance

    Returns:
        MCPServerTimeoutConfig instance
    """
    return mcp_timeout_config