"""
Tests for the Conversation Handler
"""
import pytest
from unittest.mock import patch, MagicMock
from agent.conversation_handler import ConversationHandler
from agent.todo_agent import TodoAgent


@pytest.mark.asyncio
async def test_conversation_handler_initialization():
    """
    Test successful conversation handler initialization
    """
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
        agent = TodoAgent()
        conversation_handler = ConversationHandler(agent)

        assert conversation_handler.agent == agent
        assert conversation_handler.conversations == {}


@pytest.mark.asyncio
async def test_process_message_new_conversation():
    """
    Test processing a message in a new conversation
    """
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
        agent = TodoAgent()
        await agent.initialize()

        conversation_handler = ConversationHandler(agent)

        # Mock the agent's process_request method
        with patch.object(agent, 'process_request', return_value={
            "response": "I've added your task.",
            "tool_calls": [],
            "error": None
        }):
            result = await conversation_handler.process_message(
                user_id="user123",
                message="Add buy groceries to my list"
            )

            # Check that a conversation was created
            assert result["conversation_id"] == "user123_new"
            assert result["response"] == "I've added your task."
            assert result["tool_calls"] == []

            # Check that the conversation was stored
            assert "user123_new" in conversation_handler.conversations


@pytest.mark.asyncio
async def test_process_message_existing_conversation():
    """
    Test processing a message in an existing conversation
    """
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
        agent = TodoAgent()
        await agent.initialize()

        conversation_handler = ConversationHandler(agent)

        # Pre-populate a conversation
        conversation_id = "test_conv_123"
        conversation_handler.conversations[conversation_id] = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]

        # Mock the agent's process_request method
        with patch.object(agent, 'process_request', return_value={
            "response": "I've added your task.",
            "tool_calls": [],
            "error": None
        }):
            result = await conversation_handler.process_message(
                user_id="user123",
                message="Add buy groceries to my list",
                conversation_id=conversation_id
            )

            # Check the response
            assert result["conversation_id"] == conversation_id
            assert result["response"] == "I've added your task."
            assert result["tool_calls"] == []

            # Check that the conversation history was updated
            assert len(conversation_handler.conversations[conversation_id]) == 4


@pytest.mark.asyncio
async def test_get_conversation_history():
    """
    Test retrieving conversation history
    """
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
        agent = TodoAgent()
        conversation_handler = ConversationHandler(agent)

        # Add some messages to a conversation
        conversation_id = "test_conv_456"
        conversation_handler.conversations[conversation_id] = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]

        # Get the history
        history = conversation_handler.get_conversation_history(conversation_id)

        assert len(history) == 2
        assert history[0]["role"] == "user"
        assert history[0]["content"] == "Hello"
        assert history[1]["role"] == "assistant"
        assert history[1]["content"] == "Hi there!"


@pytest.mark.asyncio
async def test_clear_conversation():
    """
    Test clearing a conversation
    """
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
        agent = TodoAgent()
        conversation_handler = ConversationHandler(agent)

        # Add a conversation
        conversation_id = "test_conv_789"
        conversation_handler.conversations[conversation_id] = [
            {"role": "user", "content": "Hello"}
        ]

        # Verify it exists
        assert conversation_id in conversation_handler.conversations

        # Clear the conversation
        result = conversation_handler.clear_conversation(conversation_id)

        # Check that it was cleared
        assert result is True
        assert conversation_id not in conversation_handler.conversations

        # Try to clear a non-existent conversation
        result = conversation_handler.clear_conversation("nonexistent")
        assert result is False


@pytest.mark.asyncio
async def test_get_all_conversations_for_user():
    """
    Test getting all conversations for a user
    """
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
        agent = TodoAgent()
        conversation_handler = ConversationHandler(agent)

        # Add some conversations for different users
        conversation_handler.conversations["user123_conv1"] = []
        conversation_handler.conversations["user123_conv2"] = []
        conversation_handler.conversations["user456_conv1"] = []

        # Get conversations for user123
        user_convs = conversation_handler.get_all_conversations_for_user("user123")

        assert len(user_convs) == 2
        assert "user123_conv1" in user_convs
        assert "user123_conv2" in user_convs
        assert "user456_conv1" not in user_convs