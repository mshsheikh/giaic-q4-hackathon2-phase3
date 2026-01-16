"""
Tool Call Service for the Todo AI Chatbot
Tracks and logs tool calls made by the agent.
"""
from typing import Dict, Any, List
from uuid import UUID
from datetime import datetime
from database.connection import get_session_context
from models.message import MessageRole
from services.db_message_service import DBMessageService


class ToolCallService:
    """
    Service class for tracking and logging tool calls made by the agent.
    """

    @staticmethod
    async def log_tool_call(
        user_id: str,
        conversation_id: str,
        tool_name: str,
        parameters: Dict[str, Any],
        result: Dict[str, Any],
        session=None
    ) -> None:
        """
        Log a tool call made by the agent.

        Args:
            user_id: ID of the user who initiated the conversation
            conversation_id: ID of the conversation where the tool was called
            tool_name: Name of the tool that was called
            parameters: Parameters passed to the tool
            result: Result returned by the tool
            session: Optional database session to use (if None, creates a new one for backward compatibility)
        """
        # Create a message to represent the tool call in the conversation
        if session is None:
            with get_session_context() as new_session:
                # Create a message representing the tool call
                tool_message_content = f"Tool '{tool_name}' called with parameters: {parameters}\nResult: {result}"

                DBMessageService.create_message(
                    session=new_session,
                    user_id=user_id,
                    conversation_id=UUID(conversation_id),
                    role=MessageRole.TOOL,
                    content=tool_message_content
                )
        else:
            # Create a message representing the tool call
            tool_message_content = f"Tool '{tool_name}' called with parameters: {parameters}\nResult: {result}"

            DBMessageService.create_message(
                session=session,
                user_id=user_id,
                conversation_id=UUID(conversation_id),
                role=MessageRole.TOOL,
                content=tool_message_content
            )

    @staticmethod
    async def log_multiple_tool_calls(
        user_id: str,
        conversation_id: str,
        tool_calls: List[Dict[str, Any]],
        session=None
    ) -> None:
        """
        Log multiple tool calls made by the agent in a single request.

        Args:
            user_id: ID of the user who initiated the conversation
            conversation_id: ID of the conversation where the tools were called
            tool_calls: List of tool call dictionaries with name, parameters, and result
            session: Optional database session to use (if None, tools will create their own)
        """
        for tool_call in tool_calls:
            await ToolCallService.log_tool_call(
                user_id=user_id,
                conversation_id=conversation_id,
                tool_name=tool_call.get("tool_name", "unknown"),
                parameters=tool_call.get("parameters", {}),
                result=tool_call.get("result", {}),
                session=session
            )

    @staticmethod
    async def get_tool_calls_for_conversation(
        conversation_id: str,
        user_id: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all tool calls for a specific conversation.

        Args:
            conversation_id: ID of the conversation to retrieve tool calls for
            user_id: ID of the user who owns the conversation

        Returns:
            List of tool call dictionaries
        """
        with get_session_context() as session:
            # Get all messages with role 'tool' for the conversation
            tool_messages = DBMessageService.get_messages_by_role(
                session=session,
                conversation_id=UUID(conversation_id),
                user_id=user_id,
                role=MessageRole.TOOL
            )

            tool_calls = []
            for message in tool_messages:
                # Parse the tool call information from the message content
                # In a real implementation, we might store tool calls in a separate table
                tool_call = {
                    "timestamp": message.created_at,
                    "content": message.content
                }
                tool_calls.append(tool_call)

            return tool_calls