"""
Base Tool Class for MCP Server with Error Handling
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import asyncio
from ..handlers.error_handler import MCPServerErrorHandler
from ..config.timeout_config import get_mcp_timeout_config


class BaseMCPTool(ABC):
    """
    Base class for all MCP tools with standardized error handling and timeout support
    """

    def __init__(self):
        self.error_handler = MCPServerErrorHandler()
        self.timeout_config = get_mcp_timeout_config()

    async def execute_with_error_handling(
        self,
        parameters: Dict[str, Any],
        user_id: str,
        correlation_id: str,
        tool_name: str
    ) -> Dict[str, Any]:
        """
        Execute the tool with standardized error handling and timeout

        Args:
            parameters: Parameters for the tool
            user_id: User ID making the request
            correlation_id: Correlation ID for request tracing
            tool_name: Name of the tool being executed

        Returns:
            Result of the tool execution or error response
        """
        try:
            # Apply timeout to the tool execution
            timeout = self.timeout_config.get_default_tool_timeout()

            # Execute the tool with timeout
            result = await asyncio.wait_for(
                self._execute_tool(parameters, user_id, correlation_id),
                timeout=timeout
            )

            # Log successful execution
            self.error_handler.log_tool_execution(
                tool_name=tool_name,
                user_id=user_id,
                correlation_id=correlation_id,
                parameters=parameters,
                result=result,
                success=True
            )

            return result

        except asyncio.TimeoutError:
            # Handle timeout specifically
            return self.error_handler.handle_graceful_failure(
                tool_name=tool_name,
                user_id=user_id,
                correlation_id=correlation_id,
                fallback_message=f"The {tool_name} operation timed out. Please try again."
            )

        except Exception as e:
            # Handle any other exception with the error handler
            return self.error_handler.handle_tool_error(
                tool_name=tool_name,
                error=e,
                user_id=user_id,
                correlation_id=correlation_id,
                parameters=parameters
            )

    @abstractmethod
    async def _execute_tool(
        self,
        parameters: Dict[str, Any],
        user_id: str,
        correlation_id: str
    ) -> Dict[str, Any]:
        """
        Abstract method to be implemented by subclasses for tool-specific logic

        Args:
            parameters: Parameters for the tool
            user_id: User ID making the request
            correlation_id: Correlation ID for request tracing

        Returns:
            Result of the tool execution
        """
        pass


class ToolExecutionWrapper:
    """
    Wrapper to execute tools with standardized error handling
    """

    @staticmethod
    async def execute(
        tool: BaseMCPTool,
        parameters: Dict[str, Any],
        user_id: str,
        correlation_id: str,
        tool_name: str
    ) -> Dict[str, Any]:
        """
        Execute a tool with standardized error handling

        Args:
            tool: The tool instance to execute
            parameters: Parameters for the tool
            user_id: User ID making the request
            correlation_id: Correlation ID for request tracing
            tool_name: Name of the tool being executed

        Returns:
            Result of the tool execution or error response
        """
        return await tool.execute_with_error_handling(
            parameters=parameters,
            user_id=user_id,
            correlation_id=correlation_id,
            tool_name=tool_name
        )