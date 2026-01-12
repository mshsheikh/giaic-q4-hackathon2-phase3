"""
Conversation model for the Todo AI Chatbot
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from datetime import datetime

if TYPE_CHECKING:
    from .message import Message


class Conversation(SQLModel, table=True):
    """
    Represents a user's chat session with unique identifier, user association, and timestamps.
    """
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    name: Optional[str] = Field(default=None, max_length=255, nullable=True)
    description: Optional[str] = Field(default=None, max_length=1000, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship to messages
    messages: list["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure updated_at is set to current time on creation/update
        if 'updated_at' not in kwargs or kwargs['updated_at'] is None:
            self.updated_at = datetime.utcnow()