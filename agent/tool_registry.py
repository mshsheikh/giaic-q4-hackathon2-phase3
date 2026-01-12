"""
Tool Registry for the TodoAgent
Handles the registration and management of MCP tools available to the agent.
"""
from typing import Dict, Any, Callable, Awaitable
import httpx
import json
from .config import AgentConfig


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
        # Register all available tools
        self.register_tool("add_task", self._call_add_task)
        self.register_tool("list_tasks", self._call_list_tasks)
        self.register_tool("complete_task", self._call_complete_task)
        self.register_tool("delete_task", self._call_delete_task)
        self.register_tool("update_task", self._call_update_task)

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

    async def _call_add_task(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call the add_task MCP tool.
        """
        try:
            # In a real implementation, this would make an HTTP request to the MCP server
            # For now, we'll return a simulated response
            return {
                "success": True,
                "task": {
                    "id": "simulated_task_id",
                    "user_id": parameters.get("user_id"),
                    "title": parameters.get("title"),
                    "description": parameters.get("description", ""),
                    "status": "pending",
                    "created_at": "2026-01-12T16:00:00.000Z",
                    "updated_at": "2026-01-12T16:00:00.000Z"
                },
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "task": None,
                "error": {
                    "code": "EXECUTION_ERROR",
                    "message": str(e)
                }
            }

    async def _call_list_tasks(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call the list_tasks MCP tool.
        """
        try:
            # In a real implementation, this would make an HTTP request to the MCP server
            # For now, we'll return a simulated response
            return {
                "success": True,
                "tasks": [
                    {
                        "id": "task1",
                        "user_id": parameters.get("user_id"),
                        "title": "Sample task",
                        "description": "This is a sample task",
                        "status": "pending",
                        "created_at": "2026-01-12T15:00:00.000Z",
                        "updated_at": "2026-01-12T15:00:00.000Z"
                    }
                ],
                "pagination": {"total": 1, "limit": 100, "offset": 0},
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "tasks": [],
                "pagination": None,
                "error": {
                    "code": "EXECUTION_ERROR",
                    "message": str(e)
                }
            }

    async def _call_complete_task(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call the complete_task MCP tool.
        """
        try:
            # In a real implementation, this would make an HTTP request to the MCP server
            # For now, we'll return a simulated response
            return {
                "success": True,
                "task": {
                    "id": parameters.get("task_id"),
                    "user_id": parameters.get("user_id"),
                    "title": "Sample task",
                    "description": "This is a sample task",
                    "status": "completed",
                    "created_at": "2026-01-12T15:00:00.000Z",
                    "updated_at": "2026-01-12T16:00:00.000Z"
                },
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "task": None,
                "error": {
                    "code": "EXECUTION_ERROR",
                    "message": str(e)
                }
            }

    async def _call_delete_task(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call the delete_task MCP tool.
        """
        try:
            # In a real implementation, this would make an HTTP request to the MCP server
            # For now, we'll return a simulated response
            return {
                "success": True,
                "deleted_task_id": parameters.get("task_id"),
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "deleted_task_id": None,
                "error": {
                    "code": "EXECUTION_ERROR",
                    "message": str(e)
                }
            }

    async def _call_update_task(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call the update_task MCP tool.
        """
        try:
            # In a real implementation, this would make an HTTP request to the MCP server
            # For now, we'll return a simulated response
            return {
                "success": True,
                "task": {
                    "id": parameters.get("task_id"),
                    "user_id": parameters.get("user_id"),
                    "title": parameters.get("title", "Updated task"),
                    "description": parameters.get("description", "Updated description"),
                    "status": parameters.get("status", "pending"),
                    "created_at": "2026-01-12T15:00:00.000Z",
                    "updated_at": "2026-01-12T16:00:00.000Z"
                },
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "task": None,
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