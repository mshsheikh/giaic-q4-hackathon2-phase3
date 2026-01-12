"""
Tests for the Chat API endpoint
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from backend.main import app
from backend.schemas.chat_schemas import ChatRequest


@pytest.fixture
def client():
    """
    Create a test client for the FastAPI app.
    """
    return TestClient(app)


@pytest.mark.asyncio
async def test_chat_endpoint_success():
    """
    Test successful chat endpoint call.
    """
    with patch('backend.routers.chat_router.TodoAgent') as mock_agent_class:
        # Create a mock agent instance
        mock_agent = AsyncMock()
        mock_agent.initialize = AsyncMock()
        mock_agent.process_request = AsyncMock(return_value={
            "response": "I've added your task.",
            "tool_calls": [],
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

                with TestClient(app) as client:
                    # Test the chat endpoint
                    response = client.post(
                        "/api/user123/chat",
                        json={"message": "Add buy groceries to my list"}
                    )

                    assert response.status_code == 200
                    data = response.json()
                    assert data["success"] is True
                    assert "conversation_id" in data
                    assert data["response"] == "I've added your task."


@pytest.mark.asyncio
async def test_chat_endpoint_with_conversation_id():
    """
    Test chat endpoint with existing conversation ID.
    """
    with patch('backend.routers.chat_router.TodoAgent') as mock_agent_class:
        # Create a mock agent instance
        mock_agent = AsyncMock()
        mock_agent.initialize = AsyncMock()
        mock_agent.process_request = AsyncMock(return_value={
            "response": "I've added your task.",
            "tool_calls": [],
            "error": None
        })

        mock_agent_class.return_value = mock_agent

        with patch('backend.routers.chat_router.ConversationService') as mock_conversation_service_class:
            mock_conversation_service = MagicMock()
            mock_conversation_service.get_conversation_by_id = AsyncMock(return_value=MagicMock())
            mock_conversation_service.get_conversation_history = AsyncMock(return_value=[])
            mock_conversation_service_class.return_value = mock_conversation_service

            with patch('backend.routers.chat_router.DBMessageService') as mock_message_service_class:
                mock_message_service = MagicMock()
                mock_message_service.create_message = MagicMock()
                mock_message_service_class.return_value = mock_message_service

                with TestClient(app) as client:
                    # Test the chat endpoint with conversation ID
                    response = client.post(
                        "/api/user123/chat",
                        json={
                            "message": "Add buy groceries to my list",
                            "conversation_id": "conv456"
                        }
                    )

                    assert response.status_code == 200
                    data = response.json()
                    assert data["success"] is True
                    assert data["conversation_id"] == "conv456"
                    assert data["response"] == "I've added your task."


@pytest.mark.asyncio
async def test_chat_endpoint_with_tool_calls():
    """
    Test chat endpoint with tool calls.
    """
    tool_calls_result = [{
        "tool_name": "add_task",
        "parameters": {"title": "buy groceries", "user_id": "user123"},
        "result": {"success": True, "task": {"id": "task789", "title": "buy groceries"}}
    }]

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


@pytest.mark.asyncio
async def test_chat_endpoint_conversation_not_found():
    """
    Test chat endpoint when conversation is not found.
    """
    with patch('backend.routers.chat_router.ConversationService') as mock_conversation_service_class:
        mock_conversation_service = MagicMock()
        mock_conversation_service.get_conversation_by_id = AsyncMock(return_value=None)
        mock_conversation_service_class.return_value = mock_conversation_service

        with TestClient(app) as client:
            # Test the chat endpoint with non-existent conversation ID
            response = client.post(
                "/api/user123/chat",
                json={
                    "message": "Add buy groceries to my list",
                    "conversation_id": "nonexistent_conv"
                }
            )

            assert response.status_code == 404
            data = response.json()
            assert "detail" in data


@pytest.mark.asyncio
async def test_chat_endpoint_internal_error():
    """
    Test chat endpoint when internal error occurs.
    """
    with patch('backend.routers.chat_router.TodoAgent') as mock_agent_class:
        # Create a mock agent that raises an exception
        mock_agent = AsyncMock()
        mock_agent.initialize = AsyncMock()
        mock_agent.process_request = AsyncMock(side_effect=Exception("API Error"))

        mock_agent_class.return_value = mock_agent

        with patch('backend.routers.chat_router.ConversationService') as mock_conversation_service_class:
            mock_conversation_service = MagicMock()
            mock_conversation_service.get_conversation_history = AsyncMock(return_value=[])
            mock_conversation_service_class.return_value = mock_conversation_service

            with TestClient(app) as client:
                # Test the chat endpoint
                response = client.post(
                    "/api/user123/chat",
                    json={"message": "Add buy groceries to my list"}
                )

                assert response.status_code == 200  # Still returns 200 as error is handled internally
                data = response.json()
                assert data["success"] is False
                assert data["error"] is not None
                assert "INTERNAL_ERROR" in data["error"]["code"]