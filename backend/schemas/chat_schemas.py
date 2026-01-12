"""
Schema definitions for the Chat API
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class ChatRequest(BaseModel):
    """
    Request schema for the chat endpoint
    """
    message: str = Field(..., description="Natural language message from the user", max_length=1000)
    conversation_id: Optional[str] = Field(None, description="Unique identifier of the conversation (optional)")

    class Config:
        schema_extra = {
            "example": {
                "message": "Add 'buy groceries' to my todo list",
                "conversation_id": "abc123-def456-ghi789"
            }
        }


class ToolCall(BaseModel):
    """
    Schema for representing a tool call made by the agent
    """
    tool_name: str = Field(..., description="Name of the MCP tool called")
    parameters: dict = Field(..., description="Parameters passed to the tool")
    result: dict = Field(..., description="Result returned by the tool")
    timestamp: datetime = Field(..., description="Timestamp when the tool was called")

    class Config:
        schema_extra = {
            "example": {
                "tool_name": "add_task",
                "parameters": {
                    "user_id": "user123",
                    "description": "buy groceries",
                    "priority": "medium"
                },
                "result": {
                    "success": True,
                    "task": {
                        "id": "task789",
                        "user_id": "user123",
                        "description": "buy groceries",
                        "status": "pending",
                        "created_at": "2026-01-12T15:00:00.000Z",
                        "updated_at": "2026-01-12T15:00:00.000Z"
                    }
                },
                "timestamp": "2026-01-12T15:00:00.000Z"
            }
        }


class ChatResponse(BaseModel):
    """
    Response schema for the chat endpoint
    """
    success: bool = Field(..., description="Indicates if the request was successful")
    conversation_id: str = Field(..., description="Unique identifier of the conversation (new or existing)")
    response: str = Field(..., description="The assistant's response to the user's message")
    tool_calls: List[ToolCall] = Field([], description="List of MCP tool calls made by the agent")
    error: Optional[dict] = Field(None, description="Error information if the request failed")

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "conversation_id": "abc123-def456-ghi789",
                "response": "I've added 'buy groceries' to your todo list.",
                "tool_calls": [
                    {
                        "tool_name": "add_task",
                        "parameters": {
                            "user_id": "user123",
                            "description": "buy groceries",
                            "priority": "medium"
                        },
                        "result": {
                            "success": True,
                            "task": {
                                "id": "task789",
                                "user_id": "user123",
                                "description": "buy groceries",
                                "status": "pending",
                                "created_at": "2026-01-12T15:00:00.000Z",
                                "updated_at": "2026-01-12T15:00:00.000Z"
                            }
                        },
                        "timestamp": "2026-01-12T15:00:00.000Z"
                    }
                ],
                "error": None
            }
        }