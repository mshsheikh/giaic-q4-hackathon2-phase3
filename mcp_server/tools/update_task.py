"""
Implementation of the update_task MCP tool for the Todo AI Chatbot
"""
from typing import Dict, Any
from uuid import UUID
from backend.database.connection import get_session_context
from backend.services.db_task_service import DBTaskService
from backend.models.task import TaskStatus
from ..config import MCPConfig


async def update_task_tool(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP tool to update a task according to the specification.

    Args:
        parameters: Dictionary containing the parameters for the tool
                   - user_id (str): User identifier
                   - task_id (str): Unique identifier of the task to update
                   - description (str, optional): New description for the task
                   - status (str, optional): New status (pending, completed)
                   - priority (str, optional): New priority level (low, medium, high)
                   - due_date (str, optional): New due date in ISO format

    Returns:
        Dictionary with success status and task information or error details
    """
    user_id = parameters.get("user_id")
    task_id_str = parameters.get("task_id")
    title = parameters.get("title")
    description = parameters.get("description")
    status = parameters.get("status")
    priority = parameters.get("priority")
    due_date = parameters.get("due_date")

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

    # Validate status if provided
    if status:
        try:
            status = TaskStatus(status.lower())
        except ValueError:
            return {
                "success": False,
                "task": None,
                "error": {
                    "code": "INVALID_STATUS",
                    "message": f"Invalid status: {status}. Must be 'pending' or 'completed'"
                }
            }

    # Use status for update (status takes precedence over status)
    update_status = status

    try:
        with get_session_context() as session:
            # Update the task using the database service
            task = DBTaskService.update_task(
                session=session,
                task_id=task_id,
                user_id=user_id,
                title=title,
                description=description,
                status=update_status
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
                    "updated_at": task.updated_at.isoformat(),
                    "due_date": due_date  # Include due_date if provided
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
tool_function = update_task_tool