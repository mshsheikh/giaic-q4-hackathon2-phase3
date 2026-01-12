"""
User model for the Todo AI Chatbot
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime


class User(SQLModel, table=True):
    """
    Represents a user in the system with authentication information.
    """
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    name: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    is_active: bool = Field(default=True, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure updated_at is set to current time on initialization
        if 'updated_at' not in kwargs or kwargs['updated_at'] is None:
            self.updated_at = datetime.utcnow()