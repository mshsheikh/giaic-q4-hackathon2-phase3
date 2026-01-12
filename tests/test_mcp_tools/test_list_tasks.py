"""
Tests for the list_tasks MCP tool
"""
import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4
from mcp_server.tools.list_tasks import list_tasks_tool
from backend.models.task import Task, TaskStatus


@pytest.mark.asyncio
async def test_list_tasks_success():
    """
    Test successful task listing
    """
    mock_session = MagicMock()
    mock_tasks = [
        Task(
            id=uuid4(),
            user_id="user123",
            title="Test Task 1",
            description="Test Description 1",
            status=TaskStatus.PENDING
        ),
        Task(
            id=uuid4(),
            user_id="user123",
            title="Test Task 2",
            description="Test Description 2",
            status=TaskStatus.COMPLETED
        )
    ]

    with patch('mcp_server.tools.list_tasks.get_session_context') as mock_context:
        mock_context.return_value.__enter__.return_value = mock_session
        with patch('mcp_server.tools.list_tasks.DBTaskService') as mock_service:
            mock_service.get_tasks_by_user.return_value = mock_tasks

            params = {
                "user_id": "user123"
            }

            result = await list_tasks_tool(params)

            assert result["success"] is True
            assert len(result["tasks"]) == 2
            assert result["pagination"]["total"] == 2
            assert result["error"] is None


@pytest.mark.asyncio
async def test_list_tasks_with_status_filter():
    """
    Test task listing with status filter
    """
    mock_session = MagicMock()
    mock_tasks = [
        Task(
            id=uuid4(),
            user_id="user123",
            title="Test Task",
            description="Test Description",
            status=TaskStatus.PENDING
        )
    ]

    with patch('mcp_server.tools.list_tasks.get_session_context') as mock_context:
        mock_context.return_value.__enter__.return_value = mock_session
        with patch('mcp_server.tools.list_tasks.DBTaskService') as mock_service:
            mock_service.get_tasks_by_user.return_value = mock_tasks

            params = {
                "user_id": "user123",
                "status_filter": "pending"
            }

            result = await list_tasks_tool(params)

            assert result["success"] is True
            assert len(result["tasks"]) == 1
            assert result["tasks"][0]["status"] == "pending"
            assert result["error"] is None


@pytest.mark.asyncio
async def test_list_tasks_missing_user_id():
    """
    Test list_tasks with missing user_id
    """
    params = {}

    result = await list_tasks_tool(params)

    assert result["success"] is False
    assert result["error"]["code"] == "MISSING_USER_ID"
    assert "user_id is required" in result["error"]["message"]


@pytest.mark.asyncio
async def test_list_tasks_invalid_status_filter():
    """
    Test list_tasks with invalid status filter
    """
    params = {
        "user_id": "user123",
        "status_filter": "invalid_status"
    }

    result = await list_tasks_tool(params)

    assert result["success"] is False
    assert result["error"]["code"] == "INVALID_STATUS_FILTER"
    assert "Invalid status filter" in result["error"]["message"]


@pytest.mark.asyncio
async def test_list_tasks_database_error():
    """
    Test list_tasks when database operation fails
    """
    with patch('mcp_server.tools.list_tasks.get_session_context') as mock_context:
        mock_context.side_effect = Exception("Database error")

        params = {
            "user_id": "user123"
        }

        result = await list_tasks_tool(params)

        assert result["success"] is False
        assert result["tasks"] == []
        assert result["error"]["code"] == "DATABASE_ERROR"
        assert "Database error" in result["error"]["message"]