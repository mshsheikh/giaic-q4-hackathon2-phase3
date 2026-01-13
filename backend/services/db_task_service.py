"""
Database service for Task operations in the Todo AI Chatbot
"""
from sqlmodel import Session, select, and_, func
from typing import List, Optional
from uuid import UUID
from backend.models.task import Task, TaskStatus
from datetime import datetime


class DBTaskService:
    """
    Service class for handling Task database operations with proper
    multi-user isolation and validation.
    """

    @staticmethod
    def create_task(session: Session, user_id: str, title: str, description: Optional[str] = None) -> Task:
        """
        Create a new task for a user.

        Args:
            session: Database session
            user_id: ID of the user creating the task
            title: Title of the task
            description: Optional description of the task

        Returns:
            The created Task object
        """
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            status=TaskStatus.PENDING
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_task_by_id(session: Session, task_id: UUID, user_id: str) -> Optional[Task]:
        """
        Get a specific task by ID for a specific user.

        Args:
            session: Database session
            task_id: ID of the task to retrieve
            user_id: ID of the user who owns the task

        Returns:
            The Task object if found and owned by the user, None otherwise
        """
        statement = select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
        return session.exec(statement).first()

    @staticmethod
    def get_tasks_by_user(session: Session, user_id: str, status: Optional[TaskStatus] = None) -> List[Task]:
        """
        Get all tasks for a specific user, optionally filtered by status.

        Args:
            session: Database session
            user_id: ID of the user whose tasks to retrieve
            status: Optional status to filter tasks by

        Returns:
            List of Task objects for the user
        """
        statement = select(Task).where(Task.user_id == user_id)
        if status:
            statement = statement.where(Task.status == status)
        statement = statement.order_by(Task.created_at.desc())
        return session.exec(statement).all()

    @staticmethod
    def update_task(session: Session, task_id: UUID, user_id: str,
                    title: Optional[str] = None, description: Optional[str] = None,
                    status: Optional[TaskStatus] = None) -> Optional[Task]:
        """
        Update a task for a specific user.

        Args:
            session: Database session
            task_id: ID of the task to update
            user_id: ID of the user who owns the task
            title: New title (optional)
            description: New description (optional)
            status: New status (optional)

        Returns:
            Updated Task object if successful, None if task not found or not owned by user
        """
        task = DBTaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            return None

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(session: Session, task_id: UUID, user_id: str) -> bool:
        """
        Delete a task for a specific user.

        Args:
            session: Database session
            task_id: ID of the task to delete
            user_id: ID of the user who owns the task

        Returns:
            True if task was deleted, False if not found or not owned by user
        """
        task = DBTaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            return False

        session.delete(task)
        session.commit()
        return True

    @staticmethod
    def complete_task(session: Session, task_id: UUID, user_id: str) -> Optional[Task]:
        """
        Mark a task as completed for a specific user.

        Args:
            session: Database session
            task_id: ID of the task to complete
            user_id: ID of the user who owns the task

        Returns:
            Updated Task object if successful, None if task not found or not owned by user
        """
        return DBTaskService.update_task(session, task_id, user_id, status=TaskStatus.COMPLETED)

    @staticmethod
    def get_task_count_by_status(session: Session, user_id: str) -> dict:
        """
        Get count of tasks by status for a specific user.

        Args:
            session: Database session
            user_id: ID of the user whose tasks to count

        Returns:
            Dictionary with counts for each status
        """
        statement = select(Task.status, func.count(Task.id)).where(
            Task.user_id == user_id
        ).group_by(Task.status)

        results = session.exec(statement).all()
        return {status.value: count for status, count in results}