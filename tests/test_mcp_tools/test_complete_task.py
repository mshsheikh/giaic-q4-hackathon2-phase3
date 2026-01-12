"""
Tests for the complete_task MCP tool
"""
import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4, UUID
from mcp_server.tools.complete_task import complete_task_tool
from backend.models.task import Task, TaskStatus


@pytest.mark.asyncio
async def test_complete_task_success():
    """
    Test successful task completion
    """
    mock_session = MagicMock()
    mock_task = Task(
        id=uuid4(),
        user_id="user123",
        title="Test Task",
        description="Test Description",
        status=TaskStatus.COMPLETED
    )

    with patch('mcp_server.tools.complete_task.get_session_context') as mock_context:
        mock_context.return_value.__enter__.return_value = mock_session
        with patch('mcp_server.tools.complete_task.DBTaskService') as mock_service:
            mock_service.complete_task.return_value = mock_task

            params = {
                "user_id": "user123",
                "task_id": str(uuid4())
            }

            result = await complete_task_tool(params)

            assert result["success"] is True
            assert result["task"]["user_id"] == "user123"
            assert result["task"]["status"] == "completed"
            assert result["error"] is None


@pytest.mark.asyncio
async def test_complete_task_missing_user_id():
    """
    Test complete_task with missing user_id
    """
    params = {
        "task_id": str(uuid4())
    }

    result = await complete_task_tool(params)

    assert result["success"] is False
    assert result["error"]["code"] == "MISSING_USER_ID"
    assert "user_id is required" in result["error"]["message"]


@pytest.mark.asyncio
async def test_complete_task_missing_task_id():
    """
    Test complete_task with missing task_id
    """
    params = {
        "user_id": "user123"
    }

    result = await complete_task_tool(params)

    assert result["success"] is False
    assert result["error"]["code"] == "MISSING_TASK_ID"
    assert "task_id is required" in result["error"]["message"]


@pytest.mark.asyncio
async def test_complete_task_invalid_task_id():
    """
    Test complete_task with invalid task_id
    """
    params = {
        "user_id": "user123",
        "task_id": "invalid-uuid"
    }

    result = await complete_task_tool(params)

    assert result["success"] is False
    assert result["error"]["code"] == "INVALID_TASK_ID"
    assert "task_id must be a valid UUID" in result["error"]["message"]


@pytest.mark.asyncio
async def test_complete_task_not_found():
    """
    Test complete_task when task doesn't exist
    """
    mock_session = MagicMock()

    with patch('mcp_server.tools.complete_task.get_session_context') as mock_context:
        mock_context.return_value.__enter__.return_value = mock_session
        with patch('mcp_server.tools.complete_task.DBTaskService') as mock_service:
            mock_service.complete_task.return_value = None

            params = {
                "user_id": "user123",
                "task_id": str(uuid4())
            }

            result = await complete_task_tool(params)

            assert result["success"] is False
            assert result["task"] is None
            assert result["error"]["code"] == "TASK_NOT_FOUND"
            assert "Task not found or not owned by user" in result["error"]["message"]


@pytest.mark.asyncio
async def test_complete_task_database_error():
    """
    Test complete_task when database operation fails
    """
    with patch('mcp_server.tools.complete_task.get_session_context') as mock_context:
        mock_context.side_effect = Exception("Database error")

        params = {
            "user_id": "user123",
            "task_id": str(uuid4())
        }

        result = await complete_task_tool(params)

        assert result["success"] is False
        assert result["task"] is None
        assert result["error"]["code"] == "DATABASE_ERROR"
        assert "Database error" in result["error"]["message"]