"""
Debug Configuration for TodoAgent
"""
import os
from typing import Optional


class AgentDebugConfig:
    """
    Configuration class for agent debug mode settings
    """
    def __init__(self):
        self.DEBUG_MODE = os.getenv('AGENT_DEBUG_MODE', 'false').lower() == 'true'
        self.DEBUG_LOG_LEVEL = os.getenv('AGENT_DEBUG_LOG_LEVEL', 'INFO')
        self.SHOW_THOUGHT_PROCESS = os.getenv('SHOW_THOUGHT_PROCESS', 'false').lower() == 'true'
        self.LOG_TOOL_CALLS_VERBOSE = os.getenv('LOG_TOOL_CALLS_VERBOSE', 'false').lower() == 'true'
        self.RETURN_DEBUG_INFO = os.getenv('RETURN_DEBUG_INFO', 'false').lower() == 'true'

    def is_debug_mode(self) -> bool:
        """
        Check if agent debug mode is enabled

        Returns:
            True if debug mode is enabled, False otherwise
        """
        return self.DEBUG_MODE

    def should_show_thought_process(self) -> bool:
        """
        Check if thought process should be shown

        Returns:
            True if thought process should be shown, False otherwise
        """
        return self.SHOW_THOUGHT_PROCESS

    def should_log_tool_calls_verbose(self) -> bool:
        """
        Check if tool calls should be logged verbosely

        Returns:
            True if verbose tool logging should be enabled, False otherwise
        """
        return self.LOG_TOOL_CALLS_VERBOSE

    def should_return_debug_info(self) -> bool:
        """
        Check if debug info should be returned to client

        Returns:
            True if debug info should be returned, False otherwise
        """
        return self.RETURN_DEBUG_INFO

    def get_log_level(self) -> str:
        """
        Get the configured log level

        Returns:
            Log level as string (INFO, DEBUG, etc.)
        """
        return self.DEBUG_LOG_LEVEL


# Global agent debug configuration instance
agent_debug_config = AgentDebugConfig()


def get_agent_debug_config() -> AgentDebugConfig:
    """
    Get the global agent debug configuration instance

    Returns:
        AgentDebugConfig instance
    """
    return agent_debug_config