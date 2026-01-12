"""
Tests for the delete_task MCP tool
"""
import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4
from mcp_server.tools.delete_task import delete_task_tool


@pytest.mark.asyncio
async def test_delete_task_success():
    """
    Test successful task deletion
    """
    mock_session = MagicMock()

    with patch('mcp_server.tools.delete_task.get_session_context') as mock_context:
        mock_context.return_value.__enter__.return_value = mock_session
        with patch('mcp_server.tools.delete_task.DBTaskService') as mock_service:
            mock_service.delete_task.return_value = True

            task_id = str(uuid4())
            params = {
                "user_id": "user123",
                "task_id": task_id
            }

            result = await delete_task_tool(params)

            assert result["success"] is True
            assert result["deleted_task_id"] == task_id
            assert result["error"] is None


@pytest.mark.asyncio
async def test_delete_task_missing_user_id():
    """
    Test delete_task with missing user_id
    """
    params = {
        "task_id": str(uuid4())
    }

    result = await delete_task_tool(params)

    assert result["success"] is False
    assert result["error"]["code"] == "MISSING_USER_ID"
    assert "user_id is required" in result["error"]["message"]


@pytest.mark.asyncio
async def test_delete_task_missing_task_id():
    """
    Test delete_task with missing task_id
    """
    params = {
        "user_id": "user123"
    }

    result = await delete_task_tool(params)

    assert result["success"] is False
    assert result["error"]["code"] == "MISSING_TASK_ID"
    assert "task_id is required" in result["error"]["message"]


@pytest.mark.asyncio
async def test_delete_task_invalid_task_id():
    """
    Test delete_task with invalid task_id
    """
    params = {
        "user_id": "user123",
        "task_id": "invalid-uuid"
    }

    result = await delete_task_tool(params)

    assert result["success"] is False
    assert result["error"]["code"] == "INVALID_TASK_ID"
    assert "task_id must be a valid UUID" in result["error"]["message"]


@pytest.mark.asyncio
async def test_delete_task_not_found():
    """
    Test delete_task when task doesn't exist
    """
    mock_session = MagicMock()

    with patch('mcp_server.tools.delete_task.get_session_context') as mock_context:
        mock_context.return_value.__enter__.return_value = mock_session
        with patch('mcp_server.tools.delete_task.DBTaskService') as mock_service:
            mock_service.delete_task.return_value = False

            params = {
                "user_id": "user123",
                "task_id": str(uuid4())
            }

            result = await delete_task_tool(params)

            assert result["success"] is False
            assert result["deleted_task_id"] is None
            assert result["error"]["code"] == "TASK_NOT_FOUND"
            assert "Task not found or not owned by user" in result["error"]["message"]


@pytest.mark.asyncio
async def test_delete_task_database_error():
    """
    Test delete_task when database operation fails
    """
    with patch('mcp_server.tools.delete_task.get_session_context') as mock_context:
        mock_context.side_effect = Exception("Database error")

        params = {
            "user_id": "user123",
            "task_id": str(uuid4())
        }

        result = await delete_task_tool(params)

        assert result["success"] is False
        assert result["deleted_task_id"] is None
        assert result["error"]["code"] == "DATABASE_ERROR"
        assert "Database error" in result["error"]["message"]