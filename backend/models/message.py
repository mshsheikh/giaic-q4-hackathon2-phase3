"""
Message model for the Todo AI Chatbot
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from datetime import datetime
import enum

if TYPE_CHECKING:
    from .conversation import Conversation


class MessageRole(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class Message(SQLModel, table=True):
    """
    Represents individual messages in a conversation with role, content, and timestamp.
    """
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    conversation_id: UUID = Field(foreign_key="conversations.id", nullable=False)
    role: MessageRole = Field(nullable=False)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship to conversation
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure created_at is set to current time on initialization
        if 'created_at' not in kwargs or kwargs['created_at'] is None:
            self.created_at = datetime.utcnow()