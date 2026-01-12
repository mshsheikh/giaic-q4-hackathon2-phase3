"""
Tests for Tool Call Tracking in the Chat API
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from backend.main import app
from backend.services.tool_call_service import ToolCallService


@pytest.mark.asyncio
async def test_log_single_tool_call():
    """
    Test logging a single tool call.
    """
    with patch('backend.services.tool_call_service.DBMessageService') as mock_message_service_class:
        mock_message_service = MagicMock()
        mock_message_service.create_message = MagicMock()
        mock_message_service_class.return_value = mock_message_service

        # Test the service method directly
        await ToolCallService.log_tool_call(
            user_id="user123",
            conversation_id="conv456",
            tool_name="add_task",
            parameters={"title": "buy groceries"},
            result={"success": True, "task_id": "task789"}
        )

        # Verify that create_message was called with the right parameters
        mock_message_service.create_message.assert_called_once()
        args, kwargs = mock_message_service.create_message.call_args
        assert kwargs["user_id"] == "user123"
        assert kwargs["role"].value == "tool"  # Assuming MessageRole.TOOL.value is "tool"
        assert "add_task" in kwargs["content"]
        assert "buy groceries" in kwargs["content"]


@pytest.mark.asyncio
async def test_log_multiple_tool_calls():
    """
    Test logging multiple tool calls.
    """
    tool_calls = [
        {
            "tool_name": "add_task",
            "parameters": {"title": "buy groceries"},
            "result": {"success": True, "task_id": "task789"}
        },
        {
            "tool_name": "list_tasks",
            "parameters": {"user_id": "user123"},
            "result": {"success": True, "tasks": []}
        }
    ]

    with patch('backend.services.tool_call_service.ToolCallService.log_tool_call') as mock_log_tool_call:
        mock_log_tool_call.return_value = None  # Mock as async but return nothing

        # Test the service method directly
        await ToolCallService.log_multiple_tool_calls(
            user_id="user123",
            conversation_id="conv456",
            tool_calls=tool_calls
        )

        # Verify that log_tool_call was called twice (once for each tool call)
        assert mock_log_tool_call.call_count == 2


@pytest.mark.asyncio
async def test_tool_call_tracking_in_chat_endpoint():
    """
    Test that tool calls are properly tracked when using the chat endpoint.
    """
    tool_calls_result = [
        {
            "tool_name": "add_task",
            "parameters": {"title": "buy groceries", "user_id": "user123"},
            "result": {"success": True, "task": {"id": "task789", "title": "buy groceries"}}
        }
    ]

    with patch('backend.routers.chat_router.TodoAgent') as mock_agent_class:
        # Create a mock agent instance
        mock_agent = AsyncMock()
        mock_agent.initialize = AsyncMock()
        mock_agent.process_request = AsyncMock(return_value={
            "response": "I've added 'buy groceries' to your list.",
            "tool_calls": tool_calls_result,
            "error": None
        })

        mock_agent_class.return_value = mock_agent

        with patch('backend.routers.chat_router.ConversationService') as mock_conversation_service_class:
            mock_conversation_service = MagicMock()
            mock_conversation_service.get_conversation_history = AsyncMock(return_value=[])
            mock_conversation_service_class.return_value = mock_conversation_service

            with patch('backend.routers.chat_router.DBMessageService') as mock_message_service_class:
                mock_message_service = MagicMock()
                mock_message_service.create_message = MagicMock()
                mock_message_service_class.return_value = mock_message_service

                with patch('backend.routers.chat_router.ToolCallService') as mock_tool_call_service:
                    mock_tool_call_service.log_multiple_tool_calls = AsyncMock()

                    with TestClient(app) as client:
                        # Test the chat endpoint
                        response = client.post(
                            "/api/user123/chat",
                            json={"message": "Add buy groceries to my list"}
                        )

                        assert response.status_code == 200
                        data = response.json()
                        assert data["success"] is True
                        assert len(data["tool_calls"]) == 1
                        assert data["tool_calls"][0]["tool_name"] == "add_task"

                        # Verify that log_multiple_tool_calls was called
                        mock_tool_call_service.log_multiple_tool_calls.assert_called_once()


@pytest.mark.asyncio
async def test_tool_call_tracking_empty():
    """
    Test that no tool calls are logged when agent returns no tool calls.
    """
    with patch('backend.routers.chat_router.TodoAgent') as mock_agent_class:
        # Create a mock agent instance
        mock_agent = AsyncMock()
        mock_agent.initialize = AsyncMock()
        mock_agent.process_request = AsyncMock(return_value={
            "response": "Hello!",
            "tool_calls": [],  # No tool calls
            "error": None
        })

        mock_agent_class.return_value = mock_agent

        with patch('backend.routers.chat_router.ConversationService') as mock_conversation_service_class:
            mock_conversation_service = MagicMock()
            mock_conversation_service.get_conversation_history = AsyncMock(return_value=[])
            mock_conversation_service_class.return_value = mock_conversation_service

            with patch('backend.routers.chat_router.DBMessageService') as mock_message_service_class:
                mock_message_service = MagicMock()
                mock_message_service.create_message = MagicMock()
                mock_message_service_class.return_value = mock_message_service

                with patch('backend.routers.chat_router.ToolCallService') as mock_tool_call_service:
                    mock_tool_call_service.log_multiple_tool_calls = AsyncMock()

                    with TestClient(app) as client:
                        # Test the chat endpoint
                        response = client.post(
                            "/api/user123/chat",
                            json={"message": "Say hello"}
                        )

                        assert response.status_code == 200
                        data = response.json()
                        assert data["success"] is True
                        assert len(data["tool_calls"]) == 0

                        # Verify that log_multiple_tool_calls was NOT called since there were no tool calls
                        mock_tool_call_service.log_multiple_tool_calls.assert_not_called()


@pytest.mark.asyncio
async def test_get_tool_calls_for_conversation():
    """
    Test retrieving tool calls for a conversation.
    """
    # Mock messages returned by DBMessageService
    mock_tool_messages = [
        MagicMock(
            created_at="2026-01-12T15:00:00Z",
            content="Tool 'add_task' called with parameters: {'title': 'buy groceries'}\nResult: {'success': True}"
        )
    ]

    with patch('backend.services.tool_call_service.DBMessageService') as mock_message_service_class:
        mock_message_service = MagicMock()
        mock_message_service.get_messages_by_role = MagicMock(return_value=mock_tool_messages)
        mock_message_service_class.return_value = mock_message_service

        # Test the service method directly
        result = await ToolCallService.get_tool_calls_for_conversation(
            conversation_id="conv456",
            user_id="user123"
        )

        assert len(result) == 1
        assert result[0]["timestamp"] == "2026-01-12T15:00:00Z"
        assert "add_task" in result[0]["content"]

        # Verify that get_messages_by_role was called with the right parameters
        mock_message_service.get_messages_by_role.assert_called_once()