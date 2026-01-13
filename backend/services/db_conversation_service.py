"""
Database service for Conversation operations in the Todo AI Chatbot
"""
from sqlmodel import Session, select, and_
from typing import List, Optional
from uuid import UUID
from backend.models.conversation import Conversation
from datetime import datetime


class DBConversationService:
    """
    Service class for handling Conversation database operations with proper
    multi-user isolation and validation.
    """

    @staticmethod
    def create_conversation(session: Session, user_id: str) -> Conversation:
        """
        Create a new conversation for a user.

        Args:
            session: Database session
            user_id: ID of the user creating the conversation

        Returns:
            The created Conversation object
        """
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    def get_conversation_by_id(session: Session, conversation_id: UUID, user_id: str) -> Optional[Conversation]:
        """
        Get a specific conversation by ID for a specific user.

        Args:
            session: Database session
            conversation_id: ID of the conversation to retrieve
            user_id: ID of the user who owns the conversation

        Returns:
            The Conversation object if found and owned by the user, None otherwise
        """
        statement = select(Conversation).where(
            and_(Conversation.id == conversation_id, Conversation.user_id == user_id)
        )
        return session.exec(statement).first()

    @staticmethod
    def get_conversations_by_user(session: Session, user_id: str) -> List[Conversation]:
        """
        Get all conversations for a specific user.

        Args:
            session: Database session
            user_id: ID of the user whose conversations to retrieve

        Returns:
            List of Conversation objects for the user
        """
        statement = select(Conversation).where(Conversation.user_id == user_id)
        statement = statement.order_by(Conversation.created_at.desc())
        return session.exec(statement).all()

    @staticmethod
    def update_conversation(session: Session, conversation_id: UUID, user_id: str) -> Optional[Conversation]:
        """
        Update a conversation's updated_at timestamp for a specific user.

        Args:
            session: Database session
            conversation_id: ID of the conversation to update
            user_id: ID of the user who owns the conversation

        Returns:
            Updated Conversation object if successful, None if conversation not found or not owned by user
        """
        conversation = DBConversationService.get_conversation_by_id(session, conversation_id, user_id)
        if not conversation:
            return None

        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    def delete_conversation(session: Session, conversation_id: UUID, user_id: str) -> bool:
        """
        Delete a conversation for a specific user.

        Args:
            session: Database session
            conversation_id: ID of the conversation to delete
            user_id: ID of the user who owns the conversation

        Returns:
            True if conversation was deleted, False if not found or not owned by user
        """
        conversation = DBConversationService.get_conversation_by_id(session, conversation_id, user_id)
        if not conversation:
            return False

        session.delete(conversation)
        session.commit()
        return True

    @staticmethod
    def get_conversation_count(session: Session, user_id: str) -> int:
        """
        Get count of conversations for a specific user.

        Args:
            session: Database session
            user_id: ID of the user whose conversations to count

        Returns:
            Count of conversations for the user
        """
        from sqlalchemy import func
        statement = select(func.count(Conversation.id)).where(Conversation.user_id == user_id)
        return session.exec(statement).one()