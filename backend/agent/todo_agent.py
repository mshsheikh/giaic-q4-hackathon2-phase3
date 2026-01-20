"""
TodoAgent implementation for the Todo AI Chatbot
"""
import asyncio
from openai import AsyncOpenAI
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from .config import AgentConfig
from .tool_registry import ToolRegistry
import json
import logging
import httpx


class TodoAgent:
    """
    TodoAgent class that uses OpenAI's API to process natural language requests
    and calls MCP tools to manage tasks.
    """

    def __init__(self):
        self.config = AgentConfig()

        # Validate configuration
        self.config.validate()

        # Set up OpenAI-compatible client for Gemini
        self.client = AsyncOpenAI(
            api_key=self.config.MODEL_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        # Add masked logging for verification
        masked_key = self.config.MODEL_API_KEY[:4] + "****" if len(self.config.MODEL_API_KEY) >= 4 else "****"
        logging.info(f"Initialized model client with base_url: {self.config.MODEL_BASE_URL or 'DEFAULT'}, masked_api_key: {masked_key}")

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
        # Prepare the messages for the agent
        messages = [{"role": "system", "content": self.system_prompt}]

        # Add conversation history if provided, but limit to last 15 messages to prevent unbounded growth
        if conversation_history:
            # Limit conversation history to prevent memory issues
            limited_history = conversation_history[-15:]  # Take only last 15 messages
            for msg in limited_history:
                # Exclude tool-call metadata to keep prompt clean
                if msg.get("role") != "tool":
                    messages.append(msg)

        # Add the current user message
        messages.append({"role": "user", "content": user_message})

        # Define available functions/tools
        functions = [
            {
                "name": "add_task",
                "description": "Add a new task to the user's list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user's ID"},
                        "title": {"type": "string", "description": "Title of the task"},
                        "description": {"type": "string", "description": "Description of the task"},
                    },
                    "required": ["user_id", "title"],
                },
            },
            {
                "name": "list_tasks",
                "description": "Get all tasks for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user's ID"},
                    },
                    "required": ["user_id"],
                },
            },
            {
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
            {
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
            {
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
        ]

        # Execute the chat completion with function calling
        try:
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model="gemini-2.5-flash",
                    messages=messages,
                    tools=[{"type": "function", "function": func} for func in functions],
                    tool_choice="auto",
                ),
                timeout=60  # 60 seconds timeout
            )

            # Process the response
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            tool_results = []

            if tool_calls:
                # Execute ALL tool calls sequentially and collect results
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Add user_id to function args if not present
                    if "user_id" not in function_args:
                        function_args["user_id"] = user_id

                    # Call the appropriate tool
                    result = await self.tool_registry.call_tool(function_name, function_args, session)
                    tool_results.append({
                        "tool_name": function_name,
                        "parameters": function_args,
                        "result": result,
                        "tool_call_id": tool_call.id  # Store tool call ID for linking
                    })

                # Add tool results to messages for the final response
                messages.append(response_message)
                for tool_result in tool_results:
                    messages.append({
                        "role": "tool",
                        "content": json.dumps(tool_result["result"]),
                        "tool_call_id": tool_result["tool_call_id"]
                    })

                # Get final response from the model after tool results
                final_response = await asyncio.wait_for(
                    self.client.chat.completions.create(
                        model="gemini-2.5-flash",
                        messages=messages,
                    ),
                    timeout=30
                )
                final_content = final_response.choices[0].message.content
            else:
                final_content = response_message.content

            return {
                "response": final_content or "I processed your request successfully.",
                "tool_calls": tool_results,
                "tool_results": tool_results
            }

        except asyncio.TimeoutError:
            logging.error(f"Timeout processing request for user_id: {user_id}")
            return {
                "response": "The AI model timed out. Please try again.",
                "tool_calls": [],
                "tool_results": []
            }
        except Exception as e:
            logging.exception(f"Error processing request for user_id: {user_id}", exc_info=True)
            return {
                "response": "Sorry, I encountered an error processing your request. Please try again.",
                "tool_calls": [],
                "tool_results": []
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