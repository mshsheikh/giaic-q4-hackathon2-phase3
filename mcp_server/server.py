"""
MCP Server implementation for the Todo AI Chatbot
"""
import asyncio
from typing import Dict, Any, List
from uuid import UUID
from backend.database.connection import get_session_context
from backend.services.db_task_service import DBTaskService
from backend.services.db_conversation_service import DBConversationService
from backend.services.db_message_service import DBMessageService
from .config import MCPConfig


class MCPServer:
    """
    Main MCP Server class that handles all tool registrations and execution
    """

    def __init__(self):
        self.tools: Dict[str, callable] = {}
        self.config = MCPConfig()

        # Validate configuration
        self.config.validate()

        # Initialize database connection
        self._setup_database()

    def _setup_database(self):
        """
        Setup database connection and initialize tables if needed
        """
        from backend.database.connection import create_db_and_tables
        create_db_and_tables()

    def register_tool(self, name: str, handler: callable):
        """
        Register a tool with the MCP server

        Args:
            name: Name of the tool
            handler: Callable function that handles the tool
        """
        self.tools[name] = handler

    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a registered tool with the given parameters

        Args:
            tool_name: Name of the tool to execute
            parameters: Parameters to pass to the tool

        Returns:
            Result of the tool execution
        """
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": {
                    "code": "TOOL_NOT_FOUND",
                    "message": f"Tool '{tool_name}' not found"
                }
            }

        try:
            # Execute the tool
            result = await self.tools[tool_name](parameters)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": {
                    "code": "EXECUTION_ERROR",
                    "message": str(e)
                }
            }

    async def get_tool_list(self) -> List[str]:
        """
        Get a list of all registered tools

        Returns:
            List of tool names
        """
        return list(self.tools.keys())

    async def add_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        MCP tool to add a new task
        """
        user_id = params.get("user_id")
        description = params.get("description")
        title = params.get("title", description)  # Use description as title if not provided
        priority = params.get("priority", "medium")
        due_date = params.get("due_date")

        if not user_id or not description:
            return {
                "success": False,
                "error": {
                    "code": "INVALID_INPUT",
                    "message": "user_id and description are required"
                }
            }

        try:
            with get_session_context() as session:
                task = DBTaskService.create_task(
                    session=session,
                    user_id=user_id,
                    title=title,
                    description=description
                )

                # Convert task to dictionary for response
                task_dict = {
                    "id": str(task.id),
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status.value,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }

                return {
                    "success": True,
                    "task": task_dict
                }
        except Exception as e:
            return {
                "success": False,
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": str(e)
                }
            }

    async def list_tasks(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        MCP tool to list tasks
        """
        user_id = params.get("user_id")
        status_filter = params.get("status_filter")
        limit = params.get("limit", 100)
        offset = params.get("offset", 0)

        if not user_id:
            return {
                "success": False,
                "error": {
                    "code": "INVALID_INPUT",
                    "message": "user_id is required"
                }
            }

        try:
            with get_session_context() as session:
                from backend.models.task import TaskStatus
                status_enum = None
                if status_filter:
                    try:
                        status_enum = TaskStatus(status_filter.lower())
                    except ValueError:
                        return {
                            "success": False,
                            "error": {
                                "code": "INVALID_STATUS",
                                "message": f"Invalid status: {status_filter}. Must be 'pending' or 'completed'"
                            }
                        }

                tasks = DBTaskService.get_tasks_by_user(
                    session=session,
                    user_id=user_id,
                    status=status_enum
                )

                # Apply limit and offset
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

                return {
                    "success": True,
                    "tasks": task_dicts,
                    "pagination": {
                        "total": len(tasks),
                        "limit": limit,
                        "offset": offset
                    }
                }
        except Exception as e:
            return {
                "success": False,
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": str(e)
                }
            }

    async def complete_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        MCP tool to complete a task
        """
        user_id = params.get("user_id")
        task_id_str = params.get("task_id")

        if not user_id or not task_id_str:
            return {
                "success": False,
                "error": {
                    "code": "INVALID_INPUT",
                    "message": "user_id and task_id are required"
                }
            }

        try:
            task_id = UUID(task_id_str)
        except ValueError:
            return {
                "success": False,
                "error": {
                    "code": "INVALID_TASK_ID",
                    "message": "task_id must be a valid UUID"
                }
            }

        try:
            with get_session_context() as session:
                task = DBTaskService.complete_task(
                    session=session,
                    task_id=task_id,
                    user_id=user_id
                )

                if not task:
                    return {
                        "success": False,
                        "error": {
                            "code": "TASK_NOT_FOUND",
                            "message": "Task not found or not owned by user"
                        }
                    }

                # Convert task to dictionary for response
                task_dict = {
                    "id": str(task.id),
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status.value,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }

                return {
                    "success": True,
                    "task": task_dict
                }
        except Exception as e:
            return {
                "success": False,
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": str(e)
                }
            }

    async def delete_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        MCP tool to delete a task
        """
        user_id = params.get("user_id")
        task_id_str = params.get("task_id")

        if not user_id or not task_id_str:
            return {
                "success": False,
                "error": {
                    "code": "INVALID_INPUT",
                    "message": "user_id and task_id are required"
                }
            }

        try:
            task_id = UUID(task_id_str)
        except ValueError:
            return {
                "success": False,
                "error": {
                    "code": "INVALID_TASK_ID",
                    "message": "task_id must be a valid UUID"
                }
            }

        try:
            with get_session_context() as session:
                success = DBTaskService.delete_task(
                    session=session,
                    task_id=task_id,
                    user_id=user_id
                )

                if not success:
                    return {
                        "success": False,
                        "error": {
                            "code": "TASK_NOT_FOUND",
                            "message": "Task not found or not owned by user"
                        }
                    }

                return {
                    "success": True,
                    "deleted_task_id": task_id_str
                }
        except Exception as e:
            return {
                "success": False,
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": str(e)
                }
            }

    async def update_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        MCP tool to update a task
        """
        user_id = params.get("user_id")
        task_id_str = params.get("task_id")
        title = params.get("title")
        status = params.get("status")
        priority = params.get("priority")
        due_date = params.get("due_date")

        if not user_id or not task_id_str:
            return {
                "success": False,
                "error": {
                    "code": "INVALID_INPUT",
                    "message": "user_id and task_id are required"
                }
            }

        try:
            task_id = UUID(task_id_str)
        except ValueError:
            return {
                "success": False,
                "error": {
                    "code": "INVALID_TASK_ID",
                    "message": "task_id must be a valid UUID"
                }
            }

        # Validate status if provided
        if status:
            try:
                from backend.models.task import TaskStatus
                status = TaskStatus(status.lower())
            except ValueError:
                return {
                    "success": False,
                    "error": {
                        "code": "INVALID_STATUS",
                        "message": f"Invalid status: {status}. Must be 'pending' or 'completed'"
                    }
                }

        try:
            with get_session_context() as session:
                task = DBTaskService.update_task(
                    session=session,
                    task_id=task_id,
                    user_id=user_id,
                    title=title,
                    status=status
                )

                if not task:
                    return {
                        "success": False,
                        "error": {
                            "code": "TASK_NOT_FOUND",
                            "message": "Task not found or not owned by user"
                        }
                    }

                # Convert task to dictionary for response
                task_dict = {
                    "id": str(task.id),
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status.value,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }

                return {
                    "success": True,
                    "task": task_dict
                }
        except Exception as e:
            return {
                "success": False,
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": str(e)
                }
            }


# Global server instance
server = MCPServer()


async def initialize_server():
    """
    Initialize the MCP server and register all tools
    """
    # Register all tools with the server
    server.register_tool("add_task", server.add_task)
    server.register_tool("list_tasks", server.list_tasks)
    server.register_tool("complete_task", server.complete_task)
    server.register_tool("delete_task", server.delete_task)
    server.register_tool("update_task", server.update_task)

    return server