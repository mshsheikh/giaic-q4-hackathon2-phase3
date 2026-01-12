"""
Task model for the Todo AI Chatbot
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from datetime import datetime
import enum

if TYPE_CHECKING:
    from .conversation import Conversation


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class Task(SQLModel, table=True):
    """
    Represents a user's todo item with properties like id, user_id, title,
    description, completion status, and timestamps.
    """
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    title: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default=None)
    status: TaskStatus = Field(default=TaskStatus.PENDING, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure updated_at is set to current time on creation/update
        if 'updated_at' not in kwargs or kwargs['updated_at'] is None:
            self.updated_at = datetime.utcnow()