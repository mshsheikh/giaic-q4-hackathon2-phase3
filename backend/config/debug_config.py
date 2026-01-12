"""
Debug Configuration for Backend
"""
import os
from typing import Optional


class DebugConfig:
    """
    Configuration class for debug mode settings
    """
    def __init__(self):
        self.DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
        self.DEBUG_LOG_LEVEL = os.getenv('DEBUG_LOG_LEVEL', 'INFO')
        self.SHOW_INTERMEDIATE_STEPS = os.getenv('SHOW_INTERMEDIATE_STEPS', 'false').lower() == 'true'
        self.EXPOSE_INTERNAL_ERRORS = os.getenv('EXPOSE_INTERNAL_ERRORS', 'false').lower() == 'true'
        self.VERBOSE_TOOL_LOGGING = os.getenv('VERBOSE_TOOL_LOGGING', 'false').lower() == 'true'

    def is_debug_mode(self) -> bool:
        """
        Check if debug mode is enabled

        Returns:
            True if debug mode is enabled, False otherwise
        """
        return self.DEBUG_MODE

    def should_show_intermediate_steps(self) -> bool:
        """
        Check if intermediate steps should be shown

        Returns:
            True if intermediate steps should be shown, False otherwise
        """
        return self.SHOW_INTERMEDIATE_STEPS

    def should_expose_internal_errors(self) -> bool:
        """
        Check if internal errors should be exposed to clients

        Returns:
            True if internal errors should be exposed, False otherwise
        """
        return self.EXPOSE_INTERNAL_ERRORS

    def should_verbose_tool_logging(self) -> bool:
        """
        Check if tools should log verbosely

        Returns:
            True if verbose tool logging should be enabled, False otherwise
        """
        return self.VERBOSE_TOOL_LOGGING

    def get_log_level(self) -> str:
        """
        Get the configured log level

        Returns:
            Log level as string (INFO, DEBUG, etc.)
        """
        return self.DEBUG_LOG_LEVEL


# Global debug configuration instance
debug_config = DebugConfig()


def get_debug_config() -> DebugConfig:
    """
    Get the global debug configuration instance

    Returns:
        DebugConfig instance
    """
    return debug_config