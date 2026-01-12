"""
Schema definitions for the update_task MCP tool
"""
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class UpdateTaskInput(BaseModel):
    """
    Input schema for the update_task MCP tool
    """
    user_id: str = Field(..., description="Unique identifier of the user", max_length=255)
    task_id: str = Field(..., description="Unique identifier of the task to update")
    title: Optional[str] = Field(None, description="New title for the task", max_length=255)
    description: Optional[str] = Field(None, description="New description for the task")
    status: Optional[str] = Field(None, description="New status (pending, completed)")
    priority: Optional[str] = Field(None, description="New priority level (low, medium, high)")
    due_date: Optional[str] = Field(None, description="New due date in ISO 8601 format (YYYY-MM-DDTHH:mm:ss.sssZ)")

    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "task_id": "task456",
                "title": "Updated task title",
                "description": "Updated task description",
                "status": "completed",
                "priority": "high",
                "due_date": "2026-01-15T00:00:00.000Z"
            }
        }


class UpdateTaskOutput(BaseModel):
    """
    Output schema for the update_task MCP tool
    """
    success: bool = Field(..., description="Indicates if the request was successful")
    task: Optional['TaskDetail'] = Field(None, description="The updated task details if successful")
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
                "title": "Updated task title",
                "description": "Updated task description",
                "status": "completed",
                "created_at": "2026-01-12T15:00:00.000Z",
                "updated_at": "2026-01-12T16:00:00.000Z",
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
                "code": "TASK_NOT_FOUND",
                "message": "Task not found or not owned by user"
            }
        }