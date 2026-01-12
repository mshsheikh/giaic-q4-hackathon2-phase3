"""
Tests for the TodoAgent
"""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from agent.todo_agent import TodoAgent


@pytest.mark.asyncio
async def test_agent_initialization():
    """
    Test successful agent initialization
    """
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
        agent = TodoAgent()
        await agent.initialize()

        assert agent.config.OPENAI_API_KEY == 'test-key'
        assert agent.tool_registry is not None


@pytest.mark.asyncio
async def test_process_request_success():
    """
    Test successful request processing
    """
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
        agent = TodoAgent()
        await agent.initialize()

        # Mock the OpenAI client response
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()

        mock_choice.message = mock_message
        mock_message.content = "I've added your task."
        mock_message.tool_calls = None

        mock_response.choices = [mock_choice]

        with patch.object(agent.client.chat.completions, 'create', return_value=mock_response):
            result = await agent.process_request(
                user_message="Add buy groceries to my list",
                user_id="user123"
            )

            assert result["response"] == "I've added your task."
            assert result["tool_calls"] == []


@pytest.mark.asyncio
async def test_process_request_with_tool_calls():
    """
    Test request processing with tool calls
    """
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
        agent = TodoAgent()
        await agent.initialize()

        # Mock the OpenAI client response with tool calls
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_tool_call = MagicMock()
        mock_function = MagicMock()

        mock_function.name = "add_task"
        mock_function.arguments = '{"title": "buy groceries", "user_id": "user123"}'

        mock_tool_call.function = mock_function
        mock_tool_call.id = "call_123"

        mock_choice.message = mock_message
        mock_message.content = "I've added your task."
        mock_message.tool_calls = [mock_tool_call]

        mock_response.choices = [mock_choice]

        # Mock the final response after tool execution
        mock_final_response = MagicMock()
        mock_final_choice = MagicMock()
        mock_final_message = MagicMock()
        mock_final_message.content = "I've added 'buy groceries' to your list."
        mock_final_response.choices = [mock_final_choice]
        mock_final_choice.message = mock_final_message

        with patch.object(agent.client.chat.completions, 'create', side_effect=[mock_response, mock_final_response]):
            with patch.object(agent.tool_registry, 'call_tool', return_value={
                "success": True,
                "task": {
                    "id": "task123",
                    "user_id": "user123",
                    "title": "buy groceries",
                    "status": "pending"
                },
                "error": None
            }):
                result = await agent.process_request(
                    user_message="Add buy groceries to my list",
                    user_id="user123"
                )

                assert result["response"] == "I've added 'buy groceries' to your list."
                assert len(result["tool_calls"]) == 1
                assert result["tool_calls"][0]["tool_name"] == "add_task"


@pytest.mark.asyncio
async def test_process_request_error():
    """
    Test request processing with error
    """
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
        agent = TodoAgent()
        await agent.initialize()

        with patch.object(agent.client.chat.completions, 'create', side_effect=Exception("API Error")):
            result = await agent.process_request(
                user_message="Add buy groceries to my list",
                user_id="user123"
            )

            assert "I'm sorry, I encountered an error" in result["response"]
            assert result["error"] == "API Error"


@pytest.mark.asyncio
async def test_agent_close():
    """
    Test agent cleanup
    """
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
        agent = TodoAgent()
        await agent.initialize()

        with patch.object(agent.tool_registry, 'close') as mock_close:
            await agent.close()

            mock_close.assert_called_once()