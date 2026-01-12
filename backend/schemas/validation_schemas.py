"""
Validation Schemas for Backend
"""
from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import re


class BaseValidationSchema(BaseModel):
    """
    Base validation schema with common validation rules
    """
    class Config:
        # Allow extra fields but don't include them in the model
        extra = "ignore"
        # Validate assignments
        validate_assignment = True


class UserIdValidationSchema(BaseValidationSchema):
    """
    Schema for validating user IDs
    """
    user_id: str = Field(..., min_length=1, max_length=255, description="Unique identifier for the user")

    @validator('user_id')
    def validate_user_id(cls, v):
        if not v:
            raise ValueError('User ID cannot be empty')
        # Basic validation: alphanumeric, hyphens, underscores only
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('User ID contains invalid characters')
        return v


class TaskValidationSchema(UserIdValidationSchema):
    """
    Schema for validating task-related inputs
    """
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    status: Optional[str] = Field(None, regex=r'^(pending|completed)$', description="Task status")

    @validator('title')
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip()

    @validator('description')
    def validate_description(cls, v):
        if v is not None:
            if len(v.strip()) == 0:
                return None  # Convert empty descriptions to None
            if len(v) > 1000:
                raise ValueError('Description exceeds maximum length of 1000 characters')
        return v.strip() if v else v


class ConversationValidationSchema(UserIdValidationSchema):
    """
    Schema for validating conversation-related inputs
    """
    name: Optional[str] = Field(None, max_length=255, description="Conversation name")


class MessageValidationSchema(UserIdValidationSchema):
    """
    Schema for validating message-related inputs
    """
    conversation_id: str = Field(..., min_length=1, max_length=255, description="Conversation identifier")
    role: str = Field(..., regex=r'^(user|assistant|tool)$', description="Message role")
    content: str = Field(..., min_length=1, max_length=5000, description="Message content")

    @validator('content')
    def validate_content(cls, v):
        if not v.strip():
            raise ValueError('Message content cannot be empty or whitespace only')
        return v.strip()


class ChatRequestValidationSchema(UserIdValidationSchema):
    """
    Schema for validating chat API requests
    """
    message: str = Field(..., min_length=1, max_length=5000, description="User message")
    conversation_id: Optional[str] = Field(None, max_length=255, description="Conversation identifier")

    @validator('message')
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty or whitespace only')
        return v.strip()


class ToolCallValidationSchema(BaseValidationSchema):
    """
    Schema for validating tool call inputs
    """
    tool_name: str = Field(..., min_length=1, max_length=255, description="Name of the tool to call")
    parameters: Dict[str, Any] = Field(..., description="Parameters for the tool call")

    @validator('tool_name')
    def validate_tool_name(cls, v):
        # Allow alphanumeric, hyphens, underscores, and periods
        if not re.match(r'^[a-zA-Z0-9_.-]+$', v):
            raise ValueError('Tool name contains invalid characters')
        return v


class PaginationValidationSchema(BaseValidationSchema):
    """
    Schema for validating pagination parameters
    """
    limit: Optional[int] = Field(None, ge=1, le=1000, description="Maximum number of results to return")
    offset: Optional[int] = Field(None, ge=0, description="Number of results to skip")

    @root_validator
    def validate_pagination(cls, values):
        limit = values.get('limit')
        offset = values.get('offset')

        if limit is not None and limit <= 0:
            raise ValueError('Limit must be greater than 0')
        if limit is not None and limit > 1000:
            raise ValueError('Limit cannot exceed 1000')
        if offset is not None and offset < 0:
            raise ValueError('Offset cannot be negative')

        return values


class SearchValidationSchema(BaseValidationSchema):
    """
    Schema for validating search parameters
    """
    query: Optional[str] = Field(None, min_length=1, max_length=255, description="Search query")
    filters: Optional[Dict[str, Any]] = Field(None, description="Additional filters for the search")

    @validator('query')
    def validate_query(cls, v):
        if v is not None and len(v.strip()) == 0:
            return None  # Convert empty queries to None
        return v.strip() if v else v