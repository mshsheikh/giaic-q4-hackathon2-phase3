"""
Validation Schemas for MCP Server
"""
from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional, Dict, Any
from datetime import datetime
import re


class BaseMCPValidationSchema(BaseModel):
    """
    Base validation schema for MCP server with common validation rules
    """
    class Config:
        # Allow extra fields but don't include them in the model
        extra = "ignore"
        # Validate assignments
        validate_assignment = True


class ToolParameterValidationSchema(BaseMCPValidationSchema):
    """
    Schema for validating MCP tool parameters
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


class AddTaskValidationSchema(ToolParameterValidationSchema):
    """
    Schema for validating add_task tool parameters
    """
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    priority: Optional[str] = Field(None, regex=r'^(low|medium|high)$', description="Task priority")
    due_date: Optional[str] = Field(None, description="Due date in ISO format")

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

    @validator('due_date')
    def validate_due_date(cls, v):
        if v is not None:
            try:
                # Attempt to parse the date to ensure it's in a valid format
                datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError('Due date must be in ISO format')
        return v


class ListTasksValidationSchema(ToolParameterValidationSchema):
    """
    Schema for validating list_tasks tool parameters
    """
    status_filter: Optional[str] = Field(None, regex=r'^(pending|completed)$', description="Filter by task status")
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


class CompleteTaskValidationSchema(ToolParameterValidationSchema):
    """
    Schema for validating complete_task tool parameters
    """
    task_id: str = Field(..., min_length=1, max_length=255, description="ID of the task to complete")

    @validator('task_id')
    def validate_task_id(cls, v):
        if not v.strip():
            raise ValueError('Task ID cannot be empty or whitespace only')
        # Basic validation: alphanumeric, hyphens, underscores only
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Task ID contains invalid characters')
        return v.strip()


class DeleteTaskValidationSchema(ToolParameterValidationSchema):
    """
    Schema for validating delete_task tool parameters
    """
    task_id: str = Field(..., min_length=1, max_length=255, description="ID of the task to delete")

    @validator('task_id')
    def validate_task_id(cls, v):
        if not v.strip():
            raise ValueError('Task ID cannot be empty or whitespace only')
        # Basic validation: alphanumeric, hyphens, underscores only
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Task ID contains invalid characters')
        return v.strip()


class UpdateTaskValidationSchema(ToolParameterValidationSchema):
    """
    Schema for validating update_task tool parameters
    """
    task_id: str = Field(..., min_length=1, max_length=255, description="ID of the task to update")
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="New task title")
    description: Optional[str] = Field(None, max_length=1000, description="New task description")
    status: Optional[str] = Field(None, regex=r'^(pending|completed)$', description="New task status")

    @validator('task_id')
    def validate_task_id(cls, v):
        if not v.strip():
            raise ValueError('Task ID cannot be empty or whitespace only')
        # Basic validation: alphanumeric, hyphens, underscores only
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Task ID contains invalid characters')
        return v.strip()

    @validator('title')
    def validate_title(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip() if v else v

    @validator('description')
    def validate_description(cls, v):
        if v is not None:
            if len(v.strip()) == 0:
                return None  # Convert empty descriptions to None
            if len(v) > 1000:
                raise ValueError('Description exceeds maximum length of 1000 characters')
        return v.strip() if v else v


class GenericToolValidationSchema(ToolParameterValidationSchema):
    """
    Generic schema for validating common tool parameters
    """
    correlation_id: Optional[str] = Field(None, max_length=255, description="Correlation ID for request tracing")

    @validator('correlation_id')
    def validate_correlation_id(cls, v):
        if v is not None and len(v.strip()) == 0:
            return None  # Convert empty correlation IDs to None
        return v.strip() if v else v