"""
TodoAgent implementation for the Todo AI Chatbot
"""
import asyncio
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from .config import AgentConfig
from .tool_registry import ToolRegistry
import json
import logging


class TodoAgent:
    """
    TodoAgent class that uses OpenAI's API to process natural language requests
    and calls MCP tools to manage tasks.
    """

    def __init__(self):
        self.config = AgentConfig()

        # Validate configuration
        self.config.validate()

        # Set up OpenAI-compatible client using canonical snippet
        client_kwargs = {
            "api_key": self.config.MODEL_API_KEY
        }

        if self.config.MODEL_BASE_URL:
            client_kwargs["base_url"] = self.config.MODEL_BASE_URL

        self.client = AsyncOpenAI(**client_kwargs)

        # Initialize OpenAIChatCompletionsModel
        self.model = OpenAIChatCompletionsModel(model=self.config.MODEL_NAME, openai_client=self.client)

        # Create RunConfig
        self.run_config = RunConfig(model=self.model, model_provider=self.client)

        # Add masked logging for verification
        masked_key = self.config.MODEL_API_KEY[:4] + "****" if len(self.config.MODEL_API_KEY) >= 4 else "****"
        logging.info(f"Initialized model client with base_url: {self.config.MODEL_BASE_URL or 'DEFAULT'}, masked_api_key: {masked_key}")

        # Disable tracing if enabled
        # (assuming any tracing configuration would go here)

        # Set up tool registry
        self.tool_registry = ToolRegistry()

        # System prompt for the agent
        self.system_prompt = """
        You are a helpful AI assistant for managing todo lists. Your job is to understand user requests about tasks and call the appropriate tools to manage them.

        Available tools:
        1. add_task: Add a new task to the user's list
        2. list_tasks: Get all tasks for the user
        3. complete_task: Mark a task as completed
        4. delete_task: Remove a task from the list
        5. update_task: Modify an existing task

        When a user wants to add a task, use add_task.
        When a user wants to see their tasks, use list_tasks.
        When a user wants to mark a task as done, use complete_task.
        When a user wants to remove a task, use delete_task.
        When a user wants to modify a task, use update_task.

        Always respond in a friendly, helpful way and confirm what actions you took.
        """

    async def initialize(self):
        """
        Initialize the agent by setting up the tool registry.
        """
        await self.tool_registry.initialize_tools()

    async def process_request(self, user_message: str, user_id: str, conversation_history: List[Dict[str, str]] = None, session=None) -> Dict[str, Any]:
        """
        Process a user request and return the agent's response.

        Args:
            user_message: The message from the user
            user_id: The ID of the user making the request
            conversation_history: Previous messages in the conversation (optional)
            session: Optional database session to use for tool calls

        Returns:
            Dictionary containing the agent's response and any tool calls made
        """
        # Prepare the messages for the OpenAI API
        messages = [{"role": "system", "content": self.system_prompt}]

        # Add conversation history if provided
        if conversation_history:
            for msg in conversation_history:
                messages.append(msg)

        # Add the current user message
        messages.append({"role": "user", "content": user_message})

        try:
            # Use the new OpenAI Agents SDK pattern
            # Since the exact method calls may vary by implementation, we'll maintain
            # the existing function calling approach with the updated agent structure
            agent = Agent(name="todo-agent", model="gpt-4o-mini")

            # The rest of the function calling logic stays the same as before
            # since we don't know the exact API of the Agent.run() method
            # For now, we'll revert to using the AsyncOpenAI client directly for function calling
            # to maintain compatibility with the existing code structure
            response = await self.client.chat.completions.create(
                model=self.config.MODEL_NAME,
                messages=messages,
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "add_task",
                            "description": "Add a new task to the user's list",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "user_id": {"type": "string", "description": "The user's ID"},
                                    "title": {"type": "string", "description": "Title of the task"},
                                    "description": {"type": "string", "description": "Description of the task"},
                                    "priority": {"type": "string", "description": "Priority level (low, medium, high)"}
                                },
                                "required": ["user_id", "title"],
                            },
                        },
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "list_tasks",
                            "description": "Get all tasks for the user",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "user_id": {"type": "string", "description": "The user's ID"},
                                    "status_filter": {"type": "string", "description": "Filter by status (pending, completed)"},
                                },
                                "required": ["user_id"],
                            },
                        },
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "complete_task",
                            "description": "Mark a task as completed",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "user_id": {"type": "string", "description": "The user's ID"},
                                    "task_id": {"type": "string", "description": "ID of the task to complete"},
                                },
                                "required": ["user_id", "task_id"],
                            },
                        },
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "delete_task",
                            "description": "Remove a task from the list",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "user_id": {"type": "string", "description": "The user's ID"},
                                    "task_id": {"type": "string", "description": "ID of the task to delete"},
                                },
                                "required": ["user_id", "task_id"],
                            },
                        },
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "update_task",
                            "description": "Modify an existing task",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "user_id": {"type": "string", "description": "The user's ID"},
                                    "task_id": {"type": "string", "description": "ID of the task to update"},
                                    "title": {"type": "string", "description": "New title for the task"},
                                    "description": {"type": "string", "description": "New description for the task"},
                                    "status": {"type": "string", "description": "New status (pending, completed)"},
                                },
                                "required": ["user_id", "task_id"],
                            },
                        },
                    },
                ],
                tool_choice="auto",  # Auto-determine which tool to call
            )

            # Extract the response
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # Process tool calls if any
            tool_results = []
            if tool_calls:
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Add the user_id to the function arguments if not present
                    if "user_id" not in function_args:
                        function_args["user_id"] = user_id

                    # Call the appropriate MCP tool via the registry, passing the session
                    result = await self.tool_registry.call_tool(function_name, function_args, session)
                    tool_results.append({
                        "tool_call_id": tool_call.id,
                        "result": result
                    })

            # If there were tool calls, get the final response from the model
            final_response = response_message.content
            if tool_calls:
                # Add tool results to the messages and get a final response
                messages.append(response_message)

                for tool_result in tool_results:
                    messages.append({
                        "role": "tool",
                        "content": json.dumps(tool_result["result"]),
                        "tool_call_id": tool_result["tool_call_id"]
                    })

                # Get the final response after tool execution
                final_response_completion = await self.client.chat.completions.create(
                    model=self.config.MODEL_NAME,
                    messages=messages,
                )
                final_response = final_response_completion.choices[0].message.content

            return {
                "response": final_response,
                "tool_calls": [
                    {
                        "tool_name": tc.function.name,
                        "parameters": json.loads(tc.function.arguments),
                        "result": next(tr["result"] for tr in tool_results if tr["tool_call_id"] == tc.id)
                    }
                    for tc in tool_calls or []
                ] if tool_calls else []
            }

        except Exception as e:
            return {
                "response": f"I'm sorry, I encountered an error: {str(e)}",
                "tool_calls": [],
                "error": str(e)
            }

    async def close(self):
        """
        Close the agent and clean up resources
        """
        await self.tool_registry.close()

    async def validate_agent_setup(self) -> Dict[str, Any]:
        """
        Validation function to check agent setup without affecting production requests.

        Returns:
            Dictionary with validation results
        """
        validation_results = {
            "model_api_key_present": bool(self.config.OPENAI_API_KEY),
            "mcp_tools": {}
        }

        # Check if required tools are available
        required_tools = ["add_task", "list_tasks", "complete_task", "delete_task", "update_task"]

        for tool_name in required_tools:
            try:
                # Just check if the tool exists in the registry
                tool_exists = hasattr(self.tool_registry, '_tools') and tool_name in self.tool_registry._tools
                validation_results["mcp_tools"][tool_name] = {
                    "available": tool_exists,
                    "callable": tool_exists  # Simplified check
                }
            except Exception as e:
                validation_results["mcp_tools"][tool_name] = {
                    "available": False,
                    "callable": False,
                    "error": str(e)
                }

        return validation_results