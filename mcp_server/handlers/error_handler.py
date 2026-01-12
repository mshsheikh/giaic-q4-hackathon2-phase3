"""
Error Handler for MCP Server
"""
from typing import Dict, Any, Optional
import logging
from datetime import datetime
from ..logging.config import log_with_context


class MCPServerErrorHandler:
    """
    Centralized error handling for MCP server operations
    """

    @staticmethod
    def handle_tool_error(
        tool_name: str,
        error: Exception,
        user_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle errors that occur during tool execution

        Args:
            tool_name: Name of the tool that failed
            error: The exception that occurred
            user_id: User ID associated with the operation
            correlation_id: Correlation ID for request tracing
            parameters: Parameters that were passed to the tool

        Returns:
            Dictionary with error response structure
        """
        # Log the error with context
        logger = logging.getLogger()
        log_data = log_with_context(
            correlation_id=correlation_id,
            tool_name=tool_name,
            user_id=user_id,
            error=str(error),
            error_type=type(error).__name__
        )

        logger.error(f"MCP Tool Error in {tool_name}: {str(error)}", extra=log_data)

        # Determine error code based on error type
        error_code = MCPServerErrorHandler._get_error_code(error)

        # Create error response
        error_response = {
            "success": False,
            "error": {
                "code": error_code,
                "message": str(error),
                "type": type(error).__name__,
                "timestamp": datetime.utcnow().isoformat(),
                "correlation_id": correlation_id,
                "tool_name": tool_name
            }
        }

        # Add additional context if available
        if parameters:
            error_response["error"]["parameters"] = parameters

        return error_response

    @staticmethod
    def _get_error_code(error: Exception) -> str:
        """
        Determine appropriate error code based on exception type

        Args:
            error: The exception that occurred

        Returns:
            Appropriate error code string
        """
        error_type = type(error).__name__

        # Map common exception types to error codes
        error_code_map = {
            "DatabaseError": "DATABASE_ERROR",
            "ConnectionError": "CONNECTION_ERROR",
            "TimeoutError": "TIMEOUT_ERROR",
            "ValueError": "INVALID_INPUT",
            "PermissionError": "PERMISSION_DENIED",
            "NotFoundError": "NOT_FOUND",
            "IntegrityError": "INTEGRITY_ERROR",
            "OperationalError": "OPERATIONAL_ERROR",
        }

        return error_code_map.get(error_type, "INTERNAL_ERROR")

    @staticmethod
    def handle_graceful_failure(
        tool_name: str,
        user_id: str,
        correlation_id: str,
        fallback_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Handle graceful failure when a tool cannot complete its operation

        Args:
            tool_name: Name of the tool that failed
            user_id: User ID associated with the operation
            correlation_id: Correlation ID for request tracing
            fallback_message: Optional fallback message to return

        Returns:
            Dictionary with graceful failure response
        """
        logger = logging.getLogger()
        log_data = log_with_context(
            correlation_id=correlation_id,
            tool_name=tool_name,
            user_id=user_id,
            status="graceful_failure"
        )

        logger.warning(f"Graceful failure for {tool_name}", extra=log_data)

        return {
            "success": False,
            "result": None,
            "error": {
                "code": "GRACEFUL_FAILURE",
                "message": fallback_message or f"The {tool_name} operation could not be completed at this time. Please try again later.",
                "timestamp": datetime.utcnow().isoformat(),
                "correlation_id": correlation_id,
                "tool_name": tool_name
            }
        }

    @staticmethod
    def log_tool_execution(
        tool_name: str,
        user_id: str,
        correlation_id: str,
        parameters: Dict[str, Any],
        result: Optional[Dict[str, Any]] = None,
        success: bool = True
    ) -> None:
        """
        Log tool execution for monitoring and debugging

        Args:
            tool_name: Name of the tool executed
            user_id: User ID associated with the operation
            correlation_id: Correlation ID for request tracing
            parameters: Parameters passed to the tool
            result: Result from the tool execution
            success: Whether the execution was successful
        """
        logger = logging.getLogger()
        log_data = log_with_context(
            correlation_id=correlation_id,
            tool_name=tool_name,
            user_id=user_id,
            success=success
        )

        if success:
            logger.info(f"Successfully executed {tool_name}", extra=log_data)
        else:
            logger.warning(f"Tool {tool_name} executed with issues", extra=log_data)