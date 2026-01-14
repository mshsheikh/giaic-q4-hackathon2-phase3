"""
Tool Failure Handler for TodoAgent
"""
from typing import Dict, Any, Optional
import logging
from datetime import datetime
from ..utils.correlation_id_handler import get_agent_correlation_id_from_context
from ..app_logging.config import log_with_context


class ToolFailureHandler:
    """
    Handler for managing tool call failures in the TodoAgent
    """

    @staticmethod
    def handle_tool_failure(
        tool_name: str,
        error: Exception,
        user_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle failures that occur when calling MCP tools

        Args:
            tool_name: Name of the tool that failed
            error: The exception that occurred
            user_id: User ID associated with the operation
            conversation_id: Conversation ID associated with the operation
            correlation_id: Correlation ID for request tracing
            parameters: Parameters that were passed to the tool

        Returns:
            Dictionary with failure response structure
        """
        # Log the tool failure with context
        logger = logging.getLogger()
        log_data = log_with_context(
            correlation_id=correlation_id or get_agent_correlation_id_from_context(),
            user_id=user_id,
            conversation_id=conversation_id,
            tool_name=tool_name,
            error=str(error),
            error_type=type(error).__name__
        )

        logger.error(f"Agent Tool Call Failure in {tool_name}: {str(error)}", extra=log_data)

        # Create failure response
        failure_response = {
            "success": False,
            "tool_name": tool_name,
            "error": {
                "code": "TOOL_CALL_FAILED",
                "message": f"Failed to execute {tool_name}: {str(error)}",
                "type": type(error).__name__,
                "timestamp": datetime.utcnow().isoformat(),
                "correlation_id": correlation_id or get_agent_correlation_id_from_context(),
                "tool_name": tool_name
            }
        }

        # Add additional context if available
        if parameters:
            failure_response["error"]["parameters"] = parameters

        return failure_response

    @staticmethod
    def handle_graceful_tool_failure(
        tool_name: str,
        user_id: str,
        conversation_id: str,
        correlation_id: str,
        fallback_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Handle graceful tool failure with user-friendly response

        Args:
            tool_name: Name of the tool that failed
            user_id: User ID associated with the operation
            conversation_id: Conversation ID associated with the operation
            correlation_id: Correlation ID for request tracing
            fallback_message: Optional fallback message to return

        Returns:
            Dictionary with graceful failure response
        """
        logger = logging.getLogger()
        log_data = log_with_context(
            correlation_id=correlation_id,
            user_id=user_id,
            conversation_id=conversation_id,
            tool_name=tool_name,
            status="graceful_failure"
        )

        logger.warning(f"Graceful tool failure for {tool_name}", extra=log_data)

        return {
            "success": False,
            "tool_name": tool_name,
            "result": None,
            "error": {
                "code": "GRACEFUL_TOOL_FAILURE",
                "message": fallback_message or f"I'm having trouble with the {tool_name} operation right now. The system is temporarily unavailable. Would you like to try something else?",
                "timestamp": datetime.utcnow().isoformat(),
                "correlation_id": correlation_id,
                "tool_name": tool_name
            }
        }

    @staticmethod
    def log_tool_call_attempt(
        tool_name: str,
        user_id: str,
        conversation_id: str,
        correlation_id: str,
        parameters: Dict[str, Any]
    ) -> None:
        """
        Log tool call attempts for monitoring and debugging

        Args:
            tool_name: Name of the tool being called
            user_id: User ID associated with the operation
            conversation_id: Conversation ID associated with the operation
            correlation_id: Correlation ID for request tracing
            parameters: Parameters being passed to the tool
        """
        logger = logging.getLogger()
        log_data = log_with_context(
            correlation_id=correlation_id,
            user_id=user_id,
            conversation_id=conversation_id,
            tool_name=tool_name,
            parameters=parameters
        )

        logger.info(f"Attempting to call tool {tool_name}", extra=log_data)

    @staticmethod
    def log_tool_call_result(
        tool_name: str,
        user_id: str,
        conversation_id: str,
        correlation_id: str,
        result: Dict[str, Any],
        success: bool = True
    ) -> None:
        """
        Log tool call results for monitoring and debugging

        Args:
            tool_name: Name of the tool that was called
            user_id: User ID associated with the operation
            conversation_id: Conversation ID associated with the operation
            correlation_id: Correlation ID for request tracing
            result: Result from the tool call
            success: Whether the tool call was successful
        """
        logger = logging.getLogger()
        log_data = log_with_context(
            correlation_id=correlation_id,
            user_id=user_id,
            conversation_id=conversation_id,
            tool_name=tool_name,
            success=success
        )

        if success:
            logger.info(f"Tool {tool_name} call succeeded", extra=log_data)
        else:
            logger.warning(f"Tool {tool_name} call failed", extra=log_data)