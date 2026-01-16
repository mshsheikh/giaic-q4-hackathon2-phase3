"""
Actual Task Tools Implementation for the TodoAgent
Connects to the database using SQLModel and DBTaskService
"""
from typing import Dict, Any
from database.connection import get_session_context
from services.db_task_service import DBTaskService
from models.task import TaskStatus
from uuid import UUID


class TaskTools:
    """
    Actual implementation of task tools that connect to the database
    """

    @staticmethod
    async def add_task(parameters: Dict[str, Any], session=None) -> Dict[str, Any]:
        """
        Add a new task to the database

        Args:
            parameters: Dictionary containing task details
                       Expected: user_id, title, description (optional)
            session: Optional database session to use (if None, creates a new one for backward compatibility)

        Returns:
            Dictionary with success status and task details
        """
        try:
            user_id = parameters.get("user_id")
            title = parameters.get("title")
            description = parameters.get("description", "")

            if not user_id or not title:
                return {
                    "success": False,
                    "task": None,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "user_id and title are required parameters"
                    }
                }

            # Use provided session or create a new one for backward compatibility
            if session is None:
                with get_session_context() as new_session:
                    task_service = DBTaskService()
                    task = task_service.create_task(
                        session=new_session,
                        user_id=user_id,
                        title=title,
                        description=description
                    )
            else:
                task_service = DBTaskService()
                task = task_service.create_task(
                    session=session,
                    user_id=user_id,
                    title=title,
                    description=description
                )

            # Convert task to dictionary format for response
            task_dict = {
                "id": str(task.id),
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description or "",
                "status": task.status.value,
                "created_at": task.created_at.isoformat() if hasattr(task.created_at, 'isoformat') else str(task.created_at),
                "updated_at": task.updated_at.isoformat() if hasattr(task.updated_at, 'isoformat') else str(task.updated_at)
            }

            return {
                "success": True,
                "task": task_dict,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "task": None,
                "error": {
                    "code": "EXECUTION_ERROR",
                    "message": str(e)
                }
            }

    @staticmethod
    async def list_tasks(parameters: Dict[str, Any], session=None) -> Dict[str, Any]:
        """
        List tasks from the database

        Args:
            parameters: Dictionary containing filter options
                       Expected: user_id, status (optional)
            session: Optional database session to use (if None, creates a new one for backward compatibility)

        Returns:
            Dictionary with success status and list of tasks
        """
        try:
            user_id = parameters.get("user_id")
            status_param = parameters.get("status")

            if not user_id:
                return {
                    "success": False,
                    "tasks": [],
                    "pagination": None,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "user_id is required parameter"
                    }
                }

            # Convert status parameter to TaskStatus enum if provided
            status = None
            if status_param:
                try:
                    status = TaskStatus(status_param.lower())
                except ValueError:
                    return {
                        "success": False,
                        "tasks": [],
                        "pagination": None,
                        "error": {
                            "code": "VALIDATION_ERROR",
                            "message": f"Invalid status: {status_param}. Valid values: {list(TaskStatus.__members__.keys())}"
                        }
                    }

            # Use provided session or create a new one for backward compatibility
            if session is None:
                with get_session_context() as new_session:
                    task_service = DBTaskService()
                    tasks = task_service.get_tasks_by_user(new_session, user_id, status)
            else:
                task_service = DBTaskService()
                tasks = task_service.get_tasks_by_user(session, user_id, status)

            # Convert tasks to dictionary format
            tasks_list = []
            for task in tasks:
                task_dict = {
                    "id": str(task.id),
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description or "",
                    "status": task.status.value,
                    "created_at": task.created_at.isoformat() if hasattr(task.created_at, 'isoformat') else str(task.created_at),
                    "updated_at": task.updated_at.isoformat() if hasattr(task.updated_at, 'isoformat') else str(task.updated_at)
                }
                tasks_list.append(task_dict)

            return {
                "success": True,
                "tasks": tasks_list,
                "pagination": {"total": len(tasks_list), "limit": 100, "offset": 0},
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "tasks": [],
                "pagination": None,
                "error": {
                    "code": "EXECUTION_ERROR",
                    "message": str(e)
                }
            }

    @staticmethod
    async def complete_task(parameters: Dict[str, Any], session=None) -> Dict[str, Any]:
        """
        Mark a task as completed in the database

        Args:
            parameters: Dictionary containing task details
                       Expected: user_id, task_id
            session: Optional database session to use (if None, creates a new one for backward compatibility)

        Returns:
            Dictionary with success status and updated task
        """
        try:
            user_id = parameters.get("user_id")
            task_id_str = parameters.get("task_id")

            if not user_id or not task_id_str:
                return {
                    "success": False,
                    "task": None,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "user_id and task_id are required parameters"
                    }
                }

            try:
                task_id = UUID(task_id_str)
            except ValueError:
                return {
                    "success": False,
                    "task": None,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": f"Invalid task_id format: {task_id_str}"
                    }
                }

            # Use provided session or create a new one for backward compatibility
            if session is None:
                with get_session_context() as new_session:
                    task_service = DBTaskService()
                    task = task_service.complete_task(new_session, task_id, user_id)
            else:
                task_service = DBTaskService()
                task = task_service.complete_task(session, task_id, user_id)

            if task:
                # Convert task to dictionary format
                task_dict = {
                    "id": str(task.id),
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description or "",
                    "status": task.status.value,
                    "created_at": task.created_at.isoformat() if hasattr(task.created_at, 'isoformat') else str(task.created_at),
                    "updated_at": task.updated_at.isoformat() if hasattr(task.updated_at, 'isoformat') else str(task.updated_at)
                }

                return {
                    "success": True,
                    "task": task_dict,
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "task": None,
                    "error": {
                        "code": "TASK_NOT_FOUND",
                        "message": f"Task with id {task_id_str} not found for user {user_id}"
                    }
                }
        except Exception as e:
            return {
                "success": False,
                "task": None,
                "error": {
                    "code": "EXECUTION_ERROR",
                    "message": str(e)
                }
            }

    @staticmethod
    async def delete_task(parameters: Dict[str, Any], session=None) -> Dict[str, Any]:
        """
        Delete a task from the database

        Args:
            parameters: Dictionary containing task details
                       Expected: user_id, task_id
            session: Optional database session to use (if None, creates a new one for backward compatibility)

        Returns:
            Dictionary with success status and deleted task ID
        """
        try:
            user_id = parameters.get("user_id")
            task_id_str = parameters.get("task_id")

            if not user_id or not task_id_str:
                return {
                    "success": False,
                    "deleted_task_id": None,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "user_id and task_id are required parameters"
                    }
                }

            try:
                task_id = UUID(task_id_str)
            except ValueError:
                return {
                    "success": False,
                    "deleted_task_id": None,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": f"Invalid task_id format: {task_id_str}"
                    }
                }

            # Use provided session or create a new one for backward compatibility
            if session is None:
                with get_session_context() as new_session:
                    task_service = DBTaskService()
                    success = task_service.delete_task(new_session, task_id, user_id)
            else:
                task_service = DBTaskService()
                success = task_service.delete_task(session, task_id, user_id)

            if success:
                return {
                    "success": True,
                    "deleted_task_id": task_id_str,
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "deleted_task_id": None,
                    "error": {
                        "code": "TASK_NOT_FOUND",
                        "message": f"Task with id {task_id_str} not found for user {user_id}"
                    }
                }
        except Exception as e:
            return {
                "success": False,
                "deleted_task_id": None,
                "error": {
                    "code": "EXECUTION_ERROR",
                    "message": str(e)
                }
            }

    @staticmethod
    async def update_task(parameters: Dict[str, Any], session=None) -> Dict[str, Any]:
        """
        Update a task in the database

        Args:
            parameters: Dictionary containing task details
                       Expected: user_id, task_id, and at least one of: title, description, status
            session: Optional database session to use (if None, creates a new one for backward compatibility)

        Returns:
            Dictionary with success status and updated task
        """
        try:
            user_id = parameters.get("user_id")
            task_id_str = parameters.get("task_id")

            # Extract optional parameters
            title = parameters.get("title")
            description = parameters.get("description")
            status_param = parameters.get("status")

            if not user_id or not task_id_str:
                return {
                    "success": False,
                    "task": None,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "user_id and task_id are required parameters"
                    }
                }

            # At least one field to update must be provided
            if not any([title is not None, description is not None, status_param is not None]):
                return {
                    "success": False,
                    "task": None,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "At least one field to update is required: title, description, or status"
                    }
                }

            try:
                task_id = UUID(task_id_str)
            except ValueError:
                return {
                    "success": False,
                    "task": None,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": f"Invalid task_id format: {task_id_str}"
                    }
                }

            # Convert status parameter to TaskStatus enum if provided
            status = None
            if status_param:
                try:
                    status = TaskStatus(status_param.lower())
                except ValueError:
                    return {
                        "success": False,
                        "task": None,
                        "error": {
                            "code": "VALIDATION_ERROR",
                            "message": f"Invalid status: {status_param}. Valid values: {list(TaskStatus.__members__.keys())}"
                        }
                    }

            # Use provided session or create a new one for backward compatibility
            if session is None:
                with get_session_context() as new_session:
                    task_service = DBTaskService()
                    task = task_service.update_task(
                        session=new_session,
                        task_id=task_id,
                        user_id=user_id,
                        title=title,
                        description=description,
                        status=status
                    )
            else:
                task_service = DBTaskService()
                task = task_service.update_task(
                    session=session,
                    task_id=task_id,
                    user_id=user_id,
                    title=title,
                    description=description,
                    status=status
                )

            if task:
                # Convert task to dictionary format
                task_dict = {
                    "id": str(task.id),
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description or "",
                    "status": task.status.value,
                    "created_at": task.created_at.isoformat() if hasattr(task.created_at, 'isoformat') else str(task.created_at),
                    "updated_at": task.updated_at.isoformat() if hasattr(task.updated_at, 'isoformat') else str(task.updated_at)
                }

                return {
                    "success": True,
                    "task": task_dict,
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "task": None,
                    "error": {
                        "code": "TASK_NOT_FOUND",
                        "message": f"Task with id {task_id_str} not found for user {user_id}"
                    }
                }
        except Exception as e:
            return {
                "success": False,
                "task": None,
                "error": {
                    "code": "EXECUTION_ERROR",
                    "message": str(e)
                }
            }