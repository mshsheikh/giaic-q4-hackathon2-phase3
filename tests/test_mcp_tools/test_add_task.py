"""
Tests for the add_task MCP tool
"""
import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4
from mcp_server.tools.add_task import add_task_tool
from backend.models.task import Task, TaskStatus


@pytest.mark.asyncio
async def test_add_task_success():
    """
    Test successful task creation
    """
    mock_session = MagicMock()
    mock_task = Task(
        id=uuid4(),
        user_id="user123",
        title="Test Task",
        description="Test Description",
        status=TaskStatus.PENDING
    )

    with patch('mcp_server.tools.add_task.get_session_context') as mock_context:
        mock_context.return_value.__enter__.return_value = mock_session
        with patch('mcp_server.tools.add_task.DBTaskService') as mock_service:
            mock_service.create_task.return_value = mock_task

            params = {
                "user_id": "user123",
                "title": "Test Task",
                "description": "Test Description"
            }

            result = await add_task_tool(params)

            assert result["success"] is True
            assert result["task"]["user_id"] == "user123"
            assert result["task"]["title"] == "Test Task"
            assert result["task"]["status"] == "pending"
            assert result["error"] is None


@pytest.mark.asyncio
async def test_add_task_missing_user_id():
    """
    Test add_task with missing user_id
    """
    params = {
        "title": "Test Task",
        "description": "Test Description"
    }

    result = await add_task_tool(params)

    assert result["success"] is False
    assert result["error"]["code"] == "MISSING_USER_ID"
    assert "user_id is required" in result["error"]["message"]


@pytest.mark.asyncio
async def test_add_task_missing_description_and_title():
    """
    Test add_task with missing description and title
    """
    params = {
        "user_id": "user123"
    }

    result = await add_task_tool(params)

    assert result["success"] is False
    assert result["error"]["code"] == "MISSING_DESCRIPTION"
    assert "Either description or title is required" in result["error"]["message"]


@pytest.mark.asyncio
async def test_add_task_database_error():
    """
    Test add_task when database operation fails
    """
    with patch('mcp_server.tools.add_task.get_session_context') as mock_context:
        mock_context.side_effect = Exception("Database error")

        params = {
            "user_id": "user123",
            "title": "Test Task",
            "description": "Test Description"
        }

        result = await add_task_tool(params)

        assert result["success"] is False
        assert result["task"] is None
        assert result["error"]["code"] == "DATABASE_ERROR"
        assert "Database error" in result["error"]["message"]