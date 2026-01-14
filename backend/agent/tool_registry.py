"""
Tool Registry for the TodoAgent
Handles the registration and management of MCP tools available to the agent.
"""
from typing import Dict, Any, Callable, Awaitable
import httpx
import json
from .config import AgentConfig
from .tools.task_tools import TaskTools


class ToolRegistry:
    """
    Registry for managing MCP tools available to the TodoAgent.
    """

    def __init__(self):
        self.config = AgentConfig()
        self.tools: Dict[str, Callable] = {}
        self.http_client = httpx.AsyncClient(timeout=self.config.REQUEST_TIMEOUT)

    async def initialize_tools(self):
        """
        Initialize all MCP tools by registering them with the registry.
        """
        # Register all available tools with actual database implementations
        self.register_tool("add_task", TaskTools.add_task)
        self.register_tool("list_tasks", TaskTools.list_tasks)
        self.register_tool("complete_task", TaskTools.complete_task)
        self.register_tool("delete_task", TaskTools.delete_task)
        self.register_tool("update_task", TaskTools.update_task)

    def register_tool(self, name: str, handler: Callable):
        """
        Register a tool with the registry.

        Args:
            name: Name of the tool
            handler: Async function that handles the tool call
        """
        self.tools[name] = handler

    async def call_tool(self, name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a registered tool with the given parameters.

        Args:
            name: Name of the tool to call
            parameters: Parameters to pass to the tool

        Returns:
            Result of the tool call
        """
        if name not in self.tools:
            return {
                "success": False,
                "error": {
                    "code": "TOOL_NOT_FOUND",
                    "message": f"Tool '{name}' not found"
                }
            }

        try:
            result = await self.tools[name](parameters)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": {
                    "code": "EXECUTION_ERROR",
                    "message": str(e)
                }
            }

    async def close(self):
        """
        Close the registry and clean up resources
        """
        await self.http_client.aclose()