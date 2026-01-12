"""
Implementation of the list_tasks MCP tool for the Todo AI Chatbot
"""
from typing import Dict, Any, List
from uuid import UUID
from backend.database.connection import get_session_context
from backend.services.db_task_service import DBTaskService
from backend.models.task import TaskStatus
from ..config import MCPConfig


async def list_tasks_tool(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP tool to list tasks according to the specification.

    Args:
        parameters: Dictionary containing the parameters for the tool
                   - user_id (str): User identifier
                   - status_filter (str, optional): Filter by status (pending, completed)
                   - limit (int, optional): Maximum number of tasks to return (default: 100)
                   - offset (int, optional): Number of tasks to skip for pagination (default: 0)

    Returns:
        Dictionary with success status and task list or error details
    """
    user_id = parameters.get("user_id")
    status_filter = parameters.get("status_filter")
    limit = parameters.get("limit", 100)
    offset = parameters.get("offset", 0)

    # Validate required parameters
    if not user_id:
        return {
            "success": False,
            "tasks": [],
            "pagination": None,
            "error": {
                "code": "MISSING_USER_ID",
                "message": "user_id is required"
            }
        }

    # Validate limit and offset
    if not isinstance(limit, int) or limit <= 0:
        limit = 100
    if not isinstance(offset, int) or offset < 0:
        offset = 0

    # Validate status filter if provided
    status_enum = None
    if status_filter:
        try:
            status_enum = TaskStatus(status_filter.lower())
        except ValueError:
            return {
                "success": False,
                "tasks": [],
                "pagination": None,
                "error": {
                    "code": "INVALID_STATUS_FILTER",
                    "message": f"Invalid status filter: {status_filter}. Must be 'pending' or 'completed'"
                }
            }

    try:
        with get_session_context() as session:
            # Get tasks using the database service
            tasks = DBTaskService.get_tasks_by_user(
                session=session,
                user_id=user_id,
                status=status_enum
            )

            # Apply pagination
            start_idx = offset
            end_idx = min(start_idx + limit, len(tasks))
            paginated_tasks = tasks[start_idx:end_idx]

            # Convert tasks to dictionaries
            task_dicts = []
            for task in paginated_tasks:
                task_dict = {
                    "id": str(task.id),
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status.value,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
                task_dicts.append(task_dict)

            # Prepare the response according to the specification
            response = {
                "success": True,
                "tasks": task_dicts,
                "pagination": {
                    "total": len(tasks),
                    "limit": limit,
                    "offset": offset
                },
                "error": None
            }

            return response

    except Exception as e:
        return {
            "success": False,
            "tasks": [],
            "pagination": None,
            "error": {
                "code": "DATABASE_ERROR",
                "message": str(e)
            }
        }


# For backward compatibility with the server implementation
tool_function = list_tasks_tool