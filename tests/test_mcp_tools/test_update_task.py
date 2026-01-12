"""
Tests for the update_task MCP tool
"""
import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4
from mcp_server.tools.update_task import update_task_tool
from backend.models.task import Task, TaskStatus


@pytest.mark.asyncio
async def test_update_task_success():
    """
    Test successful task update
    """
    mock_session = MagicMock()
    mock_updated_task = Task(
        id=uuid4(),
        user_id="user123",
        title="Updated Task",
        description="Updated Description",
        status=TaskStatus.COMPLETED
    )

    with patch('mcp_server.tools.update_task.get_session_context') as mock_context:
        mock_context.return_value.__enter__.return_value = mock_session
        with patch('mcp_server.tools.update_task.DBTaskService') as mock_service:
            mock_service.update_task.return_value = mock_updated_task

            params = {
                "user_id": "user123",
                "task_id": str(uuid4()),
                "title": "Updated Task",
                "description": "Updated Description",
                "status": "completed"
            }

            result = await update_task_tool(params)

            assert result["success"] is True
            assert result["task"]["user_id"] == "user123"
            assert result["task"]["title"] == "Updated Task"
            assert result["task"]["status"] == "completed"
            assert result["error"] is None


@pytest.mark.asyncio
async def test_update_task_missing_user_id():
    """
    Test update_task with missing user_id
    """
    params = {
        "task_id": str(uuid4()),
        "title": "Updated Task"
    }

    result = await update_task_tool(params)

    assert result["success"] is False
    assert result["error"]["code"] == "MISSING_USER_ID"
    assert "user_id is required" in result["error"]["message"]


@pytest.mark.asyncio
async def test_update_task_missing_task_id():
    """
    Test update_task with missing task_id
    """
    params = {
        "user_id": "user123",
        "title": "Updated Task"
    }

    result = await update_task_tool(params)

    assert result["success"] is False
    assert result["error"]["code"] == "MISSING_TASK_ID"
    assert "task_id is required" in result["error"]["message"]


@pytest.mark.asyncio
async def test_update_task_invalid_status():
    """
    Test update_task with invalid status
    """
    params = {
        "user_id": "user123",
        "task_id": str(uuid4()),
        "status": "invalid_status"
    }

    result = await update_task_tool(params)

    assert result["success"] is False
    assert result["error"]["code"] == "INVALID_STATUS"
    assert "Invalid status" in result["error"]["message"]


@pytest.mark.asyncio
async def test_update_task_not_found():
    """
    Test update_task when task doesn't exist
    """
    mock_session = MagicMock()

    with patch('mcp_server.tools.update_task.get_session_context') as mock_context:
        mock_context.return_value.__enter__.return_value = mock_session
        with patch('mcp_server.tools.update_task.DBTaskService') as mock_service:
            mock_service.update_task.return_value = None

            params = {
                "user_id": "user123",
                "task_id": str(uuid4()),
                "title": "Updated Task"
            }

            result = await update_task_tool(params)

            assert result["success"] is False
            assert result["task"] is None
            assert result["error"]["code"] == "TASK_NOT_FOUND"
            assert "Task not found or not owned by user" in result["error"]["message"]


@pytest.mark.asyncio
async def test_update_task_database_error():
    """
    Test update_task when database operation fails
    """
    with patch('mcp_server.tools.update_task.get_session_context') as mock_context:
        mock_context.side_effect = Exception("Database error")

        params = {
            "user_id": "user123",
            "task_id": str(uuid4()),
            "title": "Updated Task"
        }

        result = await update_task_tool(params)

        assert result["success"] is False
        assert result["task"] is None
        assert result["error"]["code"] == "DATABASE_ERROR"
        assert "Database error" in result["error"]["message"]