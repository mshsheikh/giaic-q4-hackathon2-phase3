"""
Tests for Conversation Management in the Chat API
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from backend.main import app
from backend.services.conversation_service import ConversationService


@pytest.mark.asyncio
async def test_create_conversation():
    """
    Test creating a new conversation.
    """
    with patch('backend.routers.chat_router.ConversationService') as mock_conversation_service_class:
        mock_conversation_service = MagicMock()
        mock_conversation_service.create_conversation = AsyncMock(return_value=MagicMock(id="new_conv_123"))
        mock_conversation_service_class.return_value = mock_conversation_service

        with patch('backend.routers.chat_router.DBMessageService') as mock_message_service_class:
            mock_message_service = MagicMock()
            mock_message_service.create_message = MagicMock()
            mock_message_service_class.return_value = mock_message_service

            with patch('backend.routers.chat_router.TodoAgent') as mock_agent_class:
                mock_agent = AsyncMock()
                mock_agent.initialize = AsyncMock()
                mock_agent.process_request = AsyncMock(return_value={
                    "response": "Hello!",
                    "tool_calls": [],
                    "error": None
                })
                mock_agent_class.return_value = mock_agent

                with TestClient(app) as client:
                    response = client.post(
                        "/api/user123/chat",
                        json={"message": "Start a new conversation"}
                    )

                    assert response.status_code == 200
                    data = response.json()
                    assert data["success"] is True
                    assert data["conversation_id"] is not None
                    assert data["response"] == "Hello!"


@pytest.mark.asyncio
async def test_get_conversation_history():
    """
    Test retrieving conversation history.
    """
    mock_history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]

    with patch('backend.routers.chat_router.ConversationService') as mock_conversation_service_class:
        mock_conversation_service = MagicMock()
        mock_conversation_service.get_conversation_history = AsyncMock(return_value=mock_history)
        mock_conversation_service_class.return_value = mock_conversation_service

        with patch('backend.routers.chat_router.DBMessageService') as mock_message_service_class:
            mock_message_service = MagicMock()
            mock_message_service.create_message = MagicMock()
            mock_message_service_class.return_value = mock_message_service

            with patch('backend.routers.chat_router.TodoAgent') as mock_agent_class:
                mock_agent = AsyncMock()
                mock_agent.initialize = AsyncMock()
                mock_agent.process_request = AsyncMock(return_value={
                    "response": "Thanks for the context!",
                    "tool_calls": [],
                    "error": None
                })
                mock_agent_class.return_value = mock_agent

                with TestClient(app) as client:
                    response = client.post(
                        "/api/user123/chat",
                        json={
                            "message": "What did I say before?",
                            "conversation_id": "existing_conv_456"
                        }
                    )

                    assert response.status_code == 200
                    data = response.json()
                    assert data["success"] is True
                    assert data["response"] == "Thanks for the context!"
                    # Verify that get_conversation_history was called with the right parameters
                    mock_conversation_service.get_conversation_history.assert_called_once_with(
                        "existing_conv_456", "user123"
                    )


@pytest.mark.asyncio
async def test_get_user_conversations():
    """
    Test retrieving all conversations for a user.
    """
    mock_conversations = [
        MagicMock(id="conv1", user_id="user123", created_at="2026-01-12T10:00:00Z"),
        MagicMock(id="conv2", user_id="user123", created_at="2026-01-12T11:00:00Z")
    ]

    with patch('backend.services.conversation_service.DBConversationService') as mock_db_service:
        mock_db_service.get_conversations_by_user = MagicMock(return_value=mock_conversations)

        conversation_service = ConversationService()
        result = await conversation_service.get_user_conversations("user123")

        assert len(result) == 2
        assert result[0].id == "conv1"
        assert result[1].id == "conv2"


@pytest.mark.asyncio
async def test_conversation_validation():
    """
    Test that conversations are properly validated for the correct user.
    """
    with patch('backend.routers.chat_router.ConversationService') as mock_conversation_service_class:
        mock_conversation_service = MagicMock()
        # Simulate that the conversation doesn't belong to the user
        mock_conversation_service.get_conversation_by_id = AsyncMock(return_value=None)
        mock_conversation_service_class.return_value = mock_conversation_service

        with TestClient(app) as client:
            response = client.post(
                "/api/user123/chat",
                json={
                    "message": "Continue conversation",
                    "conversation_id": "other_users_conv"
                }
            )

            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert "does not belong to user" in data["detail"]