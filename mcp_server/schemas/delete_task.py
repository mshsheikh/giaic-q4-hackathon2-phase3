"""
Schema definitions for the delete_task MCP tool
"""
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class DeleteTaskInput(BaseModel):
    """
    Input schema for the delete_task MCP tool
    """
    user_id: str = Field(..., description="Unique identifier of the user", max_length=255)
    task_id: str = Field(..., description="Unique identifier of the task to delete")

    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "task_id": "task456"
            }
        }


class DeleteTaskOutput(BaseModel):
    """
    Output schema for the delete_task MCP tool
    """
    success: bool = Field(..., description="Indicates if the request was successful")
    deleted_task_id: Optional[str] = Field(None, description="The ID of the deleted task if successful")
    error: Optional['ErrorDetail'] = Field(None, description="Error information if the request failed")


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