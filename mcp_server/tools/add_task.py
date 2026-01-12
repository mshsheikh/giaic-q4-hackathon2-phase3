"""
Implementation of the add_task MCP tool for the Todo AI Chatbot
"""
from typing import Dict, Any
from uuid import UUID
from backend.database.connection import get_session_context
from backend.services.db_task_service import DBTaskService
from ..config import MCPConfig


async def add_task_tool(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP tool to add a new task according to the specification.

    Args:
        parameters: Dictionary containing the parameters for the tool
                   - user_id (str): User identifier
                   - title (str): Title of the task
                   - description (str, optional): Description of the task
                   - priority (str, optional): Priority level (default: "medium")
                   - due_date (str, optional): Due date in ISO format

    Returns:
        Dictionary with success status and task information or error details
    """
    user_id = parameters.get("user_id")
    description = parameters.get("description")
    title = parameters.get("title", description)  # Use description as title if not provided
    priority = parameters.get("priority", "medium")
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

    if not description and not title:
        return {
            "success": False,
            "task": None,
            "error": {
                "code": "MISSING_DESCRIPTION",
                "message": "Either description or title is required"
            }
        }

    try:
        with get_session_context() as session:
            # Create the task using the database service
            task = DBTaskService.create_task(
                session=session,
                user_id=user_id,
                title=title,
                description=description
            )

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
# The server.py already has an add_task method, so we'll just export this function
# to allow it to be used as a standalone tool if needed
tool_function = add_task_tool