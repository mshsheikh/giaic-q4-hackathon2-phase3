"""
Conversation Management Service
"""
from typing import List, Tuple, Optional
from datetime import datetime
from uuid import UUID
from sqlmodel import Session, select
from ..models.conversation import Conversation
from ..models.message import Message, MessageRole
from ..schemas.conversation_management_schemas import (
    ConversationCreateRequest,
    ConversationResponse,
    MessageResponse
)


class ConversationManagementService:
    """
    Service class for managing conversations with full CRUD operations
    """

    def create_conversation(
        self,
        session: Session,
        user_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> ConversationResponse:
        """
        Create a new conversation

        Args:
            session: Database session
            user_id: User ID for the conversation owner
            name: Optional name for the conversation
            description: Optional description for the conversation

        Returns:
            Created conversation as ConversationResponse
        """
        from uuid import uuid4

        # Create new conversation
        conversation = Conversation(
            id=uuid4(),
            user_id=user_id,
            name=name,
            description=description,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Add to session and commit
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        # Return as response object
        return ConversationResponse(
            id=str(conversation.id),
            user_id=conversation.user_id,
            name=conversation.name,
            description=conversation.description,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at
        )

    def get_user_conversations(
        self,
        session: Session,
        user_id: str,
        skip: int = 0,
        limit: int = 50
    ) -> Tuple[List[ConversationResponse], int]:
        """
        Get all conversations for a user with pagination

        Args:
            session: Database session
            user_id: User ID to filter conversations
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            Tuple of (list of conversations, total count)
        """
        # Count total conversations for this user
        count_statement = select(Conversation).where(Conversation.user_id == user_id)
        total_count = len(session.exec(count_statement).all())

        # Get paginated conversations
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(Conversation.updated_at.desc())
        )
        conversations = session.exec(statement).all()

        # Convert to response objects
        conversation_responses = [
            ConversationResponse(
                id=str(conv.id),
                user_id=conv.user_id,
                name=conv.name,
                description=conv.description,
                created_at=conv.created_at,
                updated_at=conv.updated_at
            )
            for conv in conversations
        ]

        return conversation_responses, total_count

    def get_conversation_by_id(
        self,
        session: Session,
        conversation_id: str,
        user_id: str
    ) -> Optional[ConversationResponse]:
        """
        Get a specific conversation by ID for a user

        Args:
            session: Database session
            conversation_id: ID of the conversation to retrieve
            user_id: User ID to verify ownership

        Returns:
            ConversationResponse if found and owned by user, None otherwise
        """
        try:
            uuid_id = UUID(conversation_id)
        except ValueError:
            return None

        statement = select(Conversation).where(
            Conversation.id == uuid_id,
            Conversation.user_id == user_id
        )
        conversation = session.exec(statement).first()

        if not conversation:
            return None

        return ConversationResponse(
            id=str(conversation.id),
            user_id=conversation.user_id,
            name=conversation.name,
            description=conversation.description,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at
        )

    def update_conversation(
        self,
        session: Session,
        conversation_id: str,
        user_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> Optional[ConversationResponse]:
        """
        Update a conversation

        Args:
            session: Database session
            conversation_id: ID of the conversation to update
            user_id: User ID to verify ownership
            name: New name (optional)
            description: New description (optional)

        Returns:
            Updated conversation as ConversationResponse if successful, None otherwise
        """
        try:
            uuid_id = UUID(conversation_id)
        except ValueError:
            return None

        statement = select(Conversation).where(
            Conversation.id == uuid_id,
            Conversation.user_id == user_id
        )
        conversation = session.exec(statement).first()

        if not conversation:
            return None

        # Update fields if provided
        if name is not None:
            conversation.name = name
        if description is not None:
            conversation.description = description

        conversation.updated_at = datetime.utcnow()

        # Commit changes
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        return ConversationResponse(
            id=str(conversation.id),
            user_id=conversation.user_id,
            name=conversation.name,
            description=conversation.description,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at
        )

    def delete_conversation(
        self,
        session: Session,
        conversation_id: str,
        user_id: str
    ) -> bool:
        """
        Delete a conversation

        Args:
            session: Database session
            conversation_id: ID of the conversation to delete
            user_id: User ID to verify ownership

        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            uuid_id = UUID(conversation_id)
        except ValueError:
            return False

        statement = select(Conversation).where(
            Conversation.id == uuid_id,
            Conversation.user_id == user_id
        )
        conversation = session.exec(statement).first()

        if not conversation:
            return False

        # Delete the conversation
        session.delete(conversation)
        session.commit()

        return True

    def get_conversation_messages(
        self,
        session: Session,
        conversation_id: str,
        user_id: str,
        skip: int = 0,
        limit: int = 50
    ) -> List[MessageResponse]:
        """
        Get messages for a conversation

        Args:
            session: Database session
            conversation_id: ID of the conversation
            user_id: User ID to verify ownership
            skip: Number of messages to skip
            limit: Maximum number of messages to return

        Returns:
            List of messages in the conversation
        """
        try:
            uuid_id = UUID(conversation_id)
        except ValueError:
            return []

        # Verify that the conversation belongs to the user
        conv_statement = select(Conversation).where(
            Conversation.id == uuid_id,
            Conversation.user_id == user_id
        )
        conversation = session.exec(conv_statement).first()

        if not conversation:
            return []

        # Get messages for this conversation
        message_statement = (
            select(Message)
            .where(Message.conversation_id == uuid_id)
            .offset(skip)
            .limit(limit)
            .order_by(Message.created_at.asc())
        )
        messages = session.exec(message_statement).all()

        # Convert to response objects
        message_responses = [
            MessageResponse(
                id=str(msg.id),
                user_id=msg.user_id,
                conversation_id=str(msg.conversation_id),
                role=msg.role.value,
                content=msg.content,
                created_at=msg.created_at
            )
            for msg in messages
        ]

        return message_responses

    def clear_conversation_messages(
        self,
        session: Session,
        conversation_id: str,
        user_id: str
    ) -> bool:
        """
        Clear all messages in a conversation while keeping the conversation

        Args:
            session: Database session
            conversation_id: ID of the conversation to clear
            user_id: User ID to verify ownership

        Returns:
            True if cleared successfully, False otherwise
        """
        try:
            uuid_id = UUID(conversation_id)
        except ValueError:
            return False

        # Verify that the conversation belongs to the user
        conv_statement = select(Conversation).where(
            Conversation.id == uuid_id,
            Conversation.user_id == user_id
        )
        conversation = session.exec(conv_statement).first()

        if not conversation:
            return False

        # Delete all messages in this conversation
        message_statement = select(Message).where(Message.conversation_id == uuid_id)
        messages = session.exec(message_statement).all()

        for message in messages:
            session.delete(message)

        session.commit()
        return True