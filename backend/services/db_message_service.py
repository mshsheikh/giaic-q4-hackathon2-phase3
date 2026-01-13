"""
Database service for Message operations in the Todo AI Chatbot
"""
from sqlmodel import Session, select, and_
from typing import List, Optional
from uuid import UUID
from backend.models.message import Message, MessageRole
from datetime import datetime


class DBMessageService:
    """
    Service class for handling Message database operations with proper
    multi-user isolation and validation.
    """

    @staticmethod
    def create_message(session: Session, user_id: str, conversation_id: UUID,
                      role: MessageRole, content: str) -> Message:
        """
        Create a new message in a conversation.

        Args:
            session: Database session
            user_id: ID of the user creating the message
            conversation_id: ID of the conversation to add the message to
            role: Role of the message sender (user, assistant, tool)
            content: Content of the message

        Returns:
            The created Message object
        """
        message = Message(
            user_id=user_id,
            conversation_id=conversation_id,
            role=role,
            content=content
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    @staticmethod
    def get_message_by_id(session: Session, message_id: UUID, user_id: str) -> Optional[Message]:
        """
        Get a specific message by ID for a specific user.

        Args:
            session: Database session
            message_id: ID of the message to retrieve
            user_id: ID of the user who owns the message

        Returns:
            The Message object if found and owned by the user, None otherwise
        """
        statement = select(Message).where(
            and_(Message.id == message_id, Message.user_id == user_id)
        )
        return session.exec(statement).first()

    @staticmethod
    def get_messages_by_conversation(session: Session, conversation_id: UUID,
                                   user_id: str) -> List[Message]:
        """
        Get all messages for a specific conversation and user.

        Args:
            session: Database session
            conversation_id: ID of the conversation whose messages to retrieve
            user_id: ID of the user who owns the conversation

        Returns:
            List of Message objects for the conversation
        """
        # First verify the user owns the conversation
        from backend.services.db_conversation_service import DBConversationService
        conversation = DBConversationService.get_conversation_by_id(session, conversation_id, user_id)
        if not conversation:
            return []

        statement = select(Message).where(
            and_(Message.conversation_id == conversation_id, Message.user_id == user_id)
        )
        statement = statement.order_by(Message.created_at.asc())
        return session.exec(statement).all()

    @staticmethod
    def get_messages_by_user(session: Session, user_id: str, limit: int = 100) -> List[Message]:
        """
        Get recent messages for a specific user.

        Args:
            session: Database session
            user_id: ID of the user whose messages to retrieve
            limit: Maximum number of messages to return

        Returns:
            List of Message objects for the user
        """
        statement = select(Message).where(Message.user_id == user_id)
        statement = statement.order_by(Message.created_at.desc()).limit(limit)
        return session.exec(statement).all()

    @staticmethod
    def get_messages_by_role(session: Session, conversation_id: UUID,
                            user_id: str, role: MessageRole) -> List[Message]:
        """
        Get messages of a specific role for a conversation and user.

        Args:
            session: Database session
            conversation_id: ID of the conversation whose messages to retrieve
            user_id: ID of the user who owns the conversation
            role: Role to filter messages by

        Returns:
            List of Message objects with the specified role
        """
        # First verify the user owns the conversation
        from backend.services.db_conversation_service import DBConversationService
        conversation = DBConversationService.get_conversation_by_id(session, conversation_id, user_id)
        if not conversation:
            return []

        statement = select(Message).where(
            and_(
                Message.conversation_id == conversation_id,
                Message.user_id == user_id,
                Message.role == role
            )
        )
        statement = statement.order_by(Message.created_at.asc())
        return session.exec(statement).all()

    @staticmethod
    def delete_message(session: Session, message_id: UUID, user_id: str) -> bool:
        """
        Delete a message for a specific user.

        Args:
            session: Database session
            message_id: ID of the message to delete
            user_id: ID of the user who owns the message

        Returns:
            True if message was deleted, False if not found or not owned by user
        """
        message = DBMessageService.get_message_by_id(session, message_id, user_id)
        if not message:
            return False

        session.delete(message)
        session.commit()
        return True

    @staticmethod
    def get_message_count(session: Session, conversation_id: UUID, user_id: str) -> int:
        """
        Get count of messages for a specific conversation and user.

        Args:
            session: Database session
            conversation_id: ID of the conversation whose messages to count
            user_id: ID of the user who owns the conversation

        Returns:
            Count of messages in the conversation for the user
        """
        from sqlalchemy import func
        # First verify the user owns the conversation
        from backend.services.db_conversation_service import DBConversationService
        conversation = DBConversationService.get_conversation_by_id(session, conversation_id, user_id)
        if not conversation:
            return 0

        statement = select(func.count(Message.id)).where(
            and_(Message.conversation_id == conversation_id, Message.user_id == user_id)
        )
        return session.exec(statement).one()