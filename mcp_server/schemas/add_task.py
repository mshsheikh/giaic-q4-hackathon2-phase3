"""
Schema definitions for the add_task MCP tool
"""
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class AddTaskInput(BaseModel):
    """
    Input schema for the add_task MCP tool
    """
    user_id: str = Field(..., description="Unique identifier of the user", max_length=255)
    title: Optional[str] = Field(None, description="Title of the task", max_length=255)
    description: Optional[str] = Field(None, description="Description of the task")
    priority: Optional[str] = Field("medium", description="Priority level (low, medium, high)")
    due_date: Optional[str] = Field(None, description="Due date in ISO 8601 format (YYYY-MM-DDTHH:mm:ss.sssZ)")

    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "title": "Buy groceries",
                "description": "Buy milk, bread, and eggs",
                "priority": "high",
                "due_date": "2026-01-15T00:00:00.000Z"
            }
        }


class AddTaskOutput(BaseModel):
    """
    Output schema for the add_task MCP tool
    """
    success: bool = Field(..., description="Indicates if the request was successful")
    task: Optional['TaskDetail'] = Field(None, description="The created task details if successful")
    error: Optional['ErrorDetail'] = Field(None, description="Error information if the request failed")


class TaskDetail(BaseModel):
    """
    Schema for task details in the response
    """
    id: str = Field(..., description="Unique identifier of the task")
    user_id: str = Field(..., description="User identifier associated with the task")
    title: str = Field(..., description="Title of the task", max_length=255)
    description: Optional[str] = Field(None, description="Description of the task")
    status: str = Field(..., description="Status of the task (pending, completed)")
    created_at: str = Field(..., description="Creation timestamp in ISO format")
    updated_at: str = Field(..., description="Last update timestamp in ISO format")
    due_date: Optional[str] = Field(None, description="Due date in ISO 8601 format (if specified)")

    class Config:
        schema_extra = {
            "example": {
                "id": "task456",
                "user_id": "user123",
                "title": "Buy groceries",
                "description": "Buy milk, bread, and eggs",
                "status": "pending",
                "created_at": "2026-01-12T15:00:00.000Z",
                "updated_at": "2026-01-12T15:00:00.000Z",
                "due_date": "2026-01-15T00:00:00.000Z"
            }
        }


class ErrorDetail(BaseModel):
    """
    Schema for error details in the response
    """
    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Human-readable error message")

    class Config:
        schema_extra = {
            "example": {
                "code": "MISSING_USER_ID",
                "message": "user_id is required"
            }
        }