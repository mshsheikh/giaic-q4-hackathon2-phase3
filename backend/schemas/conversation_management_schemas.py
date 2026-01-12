"""
Schemas for Conversation Management
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    """
    Role of a message in the conversation
    """
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class ConversationResponse(BaseModel):
    """
    Response schema for conversation data
    """
    id: str
    user_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """
    Response schema for message data
    """
    id: str
    user_id: str
    conversation_id: str
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationCreateRequest(BaseModel):
    """
    Request schema for creating a conversation
    """
    name: Optional[str] = Field(None, max_length=255, description="Name for the conversation")
    description: Optional[str] = Field(None, max_length=1000, description="Description for the conversation")


class ConversationCreateResponse(BaseModel):
    """
    Response schema for conversation creation
    """
    success: bool
    conversation: Optional[ConversationResponse] = None
    error: Optional[dict] = None


class ConversationListResponse(BaseModel):
    """
    Response schema for listing conversations
    """
    success: bool
    conversations: List[ConversationResponse]
    total_count: int
    skip: int
    limit: int
    error: Optional[dict] = None


class ConversationGetResponse(BaseModel):
    """
    Response schema for getting a specific conversation
    """
    success: bool
    conversation: Optional[ConversationResponse] = None
    messages: List[MessageResponse] = []
    error: Optional[dict] = None


class ConversationUpdateRequest(BaseModel):
    """
    Request schema for updating a conversation
    """
    name: Optional[str] = Field(None, max_length=255, description="New name for the conversation")
    description: Optional[str] = Field(None, max_length=1000, description="New description for the conversation")


class ConversationUpdateResponse(BaseModel):
    """
    Response schema for conversation update
    """
    success: bool
    conversation: Optional[ConversationResponse] = None
    error: Optional[dict] = None


class ConversationDeleteResponse(BaseModel):
    """
    Response schema for conversation deletion
    """
    success: bool
    error: Optional[dict] = None