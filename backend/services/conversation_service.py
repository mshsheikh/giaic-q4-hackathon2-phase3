"""
Conversation Service for the Todo AI Chatbot
"""
from typing import Optional, List, Dict
from uuid import UUID
from ..models.conversation import Conversation
from ..models.message import Message
from ..database.connection import get_session_context
from ..services.db_conversation_service import DBConversationService
from ..services.db_message_service import DBMessageService


class ConversationService:
    """
    Service class for handling conversation-related operations.
    """

    def __init__(self):
        pass

    async def create_conversation(self, user_id: str) -> Conversation:
        """
        Create a new conversation for a user.

        Args:
            user_id: ID of the user creating the conversation

        Returns:
            The created Conversation object
        """
        with get_session_context() as session:
            conversation = DBConversationService.create_conversation(session, user_id)
            return conversation

    async def get_conversation_by_id(self, conversation_id: str, user_id: str) -> Optional[Conversation]:
        """
        Get a conversation by its ID for a specific user.

        Args:
            conversation_id: ID of the conversation to retrieve
            user_id: ID of the user who owns the conversation

        Returns:
            The Conversation object if found and owned by the user, None otherwise
        """
        with get_session_context() as session:
            conversation = DBConversationService.get_conversation_by_id(
                session,
                UUID(conversation_id),
                user_id
            )
            return conversation

    async def update_conversation(self, conversation_id: str, user_id: str) -> Optional[Conversation]:
        """
        Update a conversation's last activity timestamp.

        Args:
            conversation_id: ID of the conversation to update
            user_id: ID of the user who owns the conversation

        Returns:
            The updated Conversation object if successful, None if not found
        """
        with get_session_context() as session:
            conversation = DBConversationService.update_conversation(
                session,
                UUID(conversation_id),
                user_id
            )
            return conversation

    async def get_conversation_history(self, conversation_id: str, user_id: str) -> List[Dict[str, str]]:
        """
        Get the full conversation history for a specific conversation.

        Args:
            conversation_id: ID of the conversation to retrieve history for
            user_id: ID of the user who owns the conversation

        Returns:
            List of message dictionaries with role and content
        """
        with get_session_context() as session:
            # First verify the user owns the conversation
            conversation = DBConversationService.get_conversation_by_id(
                session,
                UUID(conversation_id),
                user_id
            )

            if not conversation:
                return []

            # Get all messages for the conversation
            messages = DBMessageService.get_messages_by_conversation(
                session,
                UUID(conversation_id),
                user_id
            )

            # Convert messages to the format expected by the agent
            history = []
            for message in messages:
                history.append({
                    "role": message.role.value,
                    "content": message.content
                })

            return history

    async def get_user_conversations(self, user_id: str) -> List[Conversation]:
        """
        Get all conversations for a specific user.

        Args:
            user_id: ID of the user whose conversations to retrieve

        Returns:
            List of Conversation objects for the user
        """
        with get_session_context() as session:
            conversations = DBConversationService.get_conversations_by_user(session, user_id)
            return conversations