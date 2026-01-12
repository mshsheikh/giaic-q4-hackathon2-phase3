"""
Implementation of the complete_task MCP tool for the Todo AI Chatbot
"""
from typing import Dict, Any
from uuid import UUID
from backend.database.connection import get_session_context
from backend.services.db_task_service import DBTaskService
from backend.models.task import TaskStatus
from ..config import MCPConfig


async def complete_task_tool(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP tool to mark a task as completed according to the specification.

    Args:
        parameters: Dictionary containing the parameters for the tool
                   - user_id (str): User identifier
                   - task_id (str): Unique identifier of the task to complete

    Returns:
        Dictionary with success status and task information or error details
    """
    user_id = parameters.get("user_id")
    task_id_str = parameters.get("task_id")

    # Validate required parameters
    if not user_id:
        return {
            "success": False,
            "task": None,
            "error": {
                "code": "MISSING_USER_ID",
                "message": "user_id is required"
            }
        }

    if not task_id_str:
        return {
            "success": False,
            "task": None,
            "error": {
                "code": "MISSING_TASK_ID",
                "message": "task_id is required"
            }
        }

    # Validate task_id format
    try:
        task_id = UUID(task_id_str)
    except ValueError:
        return {
            "success": False,
            "task": None,
            "error": {
                "code": "INVALID_TASK_ID",
                "message": "task_id must be a valid UUID"
            }
        }

    try:
        with get_session_context() as session:
            # Complete the task using the database service
            task = DBTaskService.complete_task(
                session=session,
                task_id=task_id,
                user_id=user_id
            )

            if not task:
                return {
                    "success": False,
                    "task": None,
                    "error": {
                        "code": "TASK_NOT_FOUND",
                        "message": "Task not found or not owned by user"
                    }
                }

            # Prepare the response according to the specification
            response = {
                "success": True,
                "task": {
                    "id": str(task.id),
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status.value,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                },
                "error": None
            }

            return response

    except Exception as e:
        return {
            "success": False,
            "task": None,
            "error": {
                "code": "DATABASE_ERROR",
                "message": str(e)
            }
        }


# For backward compatibility with the server implementation
tool_function = complete_task_tool