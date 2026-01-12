"""
Schema definitions for the list_tasks MCP tool
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class ListTasksInput(BaseModel):
    """
    Input schema for the list_tasks MCP tool
    """
    user_id: str = Field(..., description="Unique identifier of the user", max_length=255)
    status_filter: Optional[str] = Field(None, description="Filter by status (pending, completed)")
    limit: Optional[int] = Field(100, description="Maximum number of tasks to return", ge=1, le=1000)
    offset: Optional[int] = Field(0, description="Number of tasks to skip for pagination", ge=0)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "status_filter": "pending",
                "limit": 10,
                "offset": 0
            }
        }


class ListTasksOutput(BaseModel):
    """
    Output schema for the list_tasks MCP tool
    """
    success: bool = Field(..., description="Indicates if the request was successful")
    tasks: List['TaskDetail'] = Field([], description="List of tasks matching the criteria")
    pagination: Optional['PaginationDetail'] = Field(None, description="Pagination information")
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

    class Config:
        schema_extra = {
            "example": {
                "id": "task456",
                "user_id": "user123",
                "title": "Buy groceries",
                "description": "Buy milk, bread, and eggs",
                "status": "pending",
                "created_at": "2026-01-12T15:00:00.000Z",
                "updated_at": "2026-01-12T15:00:00.000Z"
            }
        }


class PaginationDetail(BaseModel):
    """
    Schema for pagination details in the response
    """
    total: int = Field(..., description="Total number of tasks matching the criteria")
    limit: int = Field(..., description="Maximum number of tasks returned in this response")
    offset: int = Field(..., description="Number of tasks skipped for pagination")

    class Config:
        schema_extra = {
            "example": {
                "total": 5,
                "limit": 10,
                "offset": 0
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