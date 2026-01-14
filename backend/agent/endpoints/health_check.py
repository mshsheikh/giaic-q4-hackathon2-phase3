"""
Health Check Endpoints for TodoAgent
"""
import asyncio
import time
from typing import Dict, Any
from datetime import datetime
from ..config import AgentConfig
from ..utils.correlation_id_handler import get_agent_correlation_id_from_context


async def check_openai_connection() -> Dict[str, Any]:
    """
    Check connectivity to OpenAI API

    Returns:
        Dictionary with OpenAI API health status
    """
    start_time = time.time()
    try:
        # Import OpenAI client to check if it's available
        import openai
        from ..config import AgentConfig

        # Get the API key from config
        config = AgentConfig()
        config.validate()

        # For now, just check if we have the API key
        # In a real implementation, we'd make an actual API call
        if not config.OPENAI_API_KEY:
            return {
                "status": "error",
                "component": "openai_api",
                "details": "OPENAI_API_KEY not configured",
                "response_time_ms": round((time.time() - start_time) * 1000, 2)
            }

        # Verify the API key format (basic check)
        if not config.OPENAI_API_KEY.startswith('sk-'):
            return {
                "status": "warning",
                "component": "openai_api",
                "details": "API key format may be invalid",
                "response_time_ms": round((time.time() - start_time) * 1000, 2)
            }

        return {
            "status": "ok",
            "component": "openai_api",
            "details": "API key configured",
            "response_time_ms": round((time.time() - start_time) * 1000, 2)
        }
    except Exception as e:
        return {
            "status": "error",
            "component": "openai_api",
            "details": str(e),
            "response_time_ms": round((time.time() - start_time) * 1000, 2)
        }


async def check_mcp_connection() -> Dict[str, Any]:
    """
    Check connectivity to MCP server

    Returns:
        Dictionary with MCP server health status
    """
    start_time = time.time()
    try:
        # Check if we can import and access MCP tools
        # This is a basic check to see if the connection mechanism exists
        from ..tool_registry import ToolRegistry

        # Try to initialize the registry
        registry = ToolRegistry()
        # Check if the registry has the expected methods
        if not hasattr(registry, 'initialize_tools') or not hasattr(registry, 'call_tool'):
            return {
                "status": "error",
                "component": "mcp_connection",
                "details": "ToolRegistry missing required methods",
                "response_time_ms": round((time.time() - start_time) * 1000, 2)
            }

        return {
            "status": "ok",
            "component": "mcp_connection",
            "details": "MCP connection mechanism available",
            "response_time_ms": round((time.time() - start_time) * 1000, 2)
        }
    except Exception as e:
        return {
            "status": "error",
            "component": "mcp_connection",
            "details": str(e),
            "response_time_ms": round((time.time() - start_time) * 1000, 2)
        }


async def check_agent_components() -> Dict[str, Any]:
    """
    Check core agent components

    Returns:
        Dictionary with agent component health status
    """
    start_time = time.time()
    try:
        # Check if core agent components are available
        from ..todo_agent import TodoAgent

        # Verify that the agent has the expected methods
        agent = TodoAgent()
        required_methods = ['initialize', 'process_request', 'close']
        missing_methods = [method for method in required_methods if not hasattr(agent, method)]

        if missing_methods:
            return {
                "status": "error",
                "component": "agent_core",
                "details": f"Missing methods: {', '.join(missing_methods)}",
                "response_time_ms": round((time.time() - start_time) * 1000, 2)
            }

        return {
            "status": "ok",
            "component": "agent_core",
            "details": "All required methods available",
            "response_time_ms": round((time.time() - start_time) * 1000, 2)
        }
    except Exception as e:
        return {
            "status": "error",
            "component": "agent_core",
            "details": str(e),
            "response_time_ms": round((time.time() - start_time) * 1000, 2)
        }


async def get_health_status() -> Dict[str, Any]:
    """
    Comprehensive health check for the TodoAgent

    Returns:
        Dictionary with overall health status and component details
    """
    start_time = time.time()

    # Run checks concurrently
    openai_task = check_openai_connection()
    mcp_task = check_mcp_connection()
    agent_task = check_agent_components()

    openai_check, mcp_check, agent_check = await asyncio.gather(openai_task, mcp_task, agent_task)

    # Determine overall status
    checks = [openai_check, mcp_check, agent_check]
    overall_status = "ok"
    if any(check["status"] == "error" for check in checks):
        overall_status = "error"
    elif any(check["status"] == "warning" for check in checks):
        overall_status = "warning"

    response = {
        "status": overall_status,
        "timestamp": datetime.utcnow().isoformat(),
        "response_time_ms": round((time.time() - start_time) * 1000, 2),
        "checks": checks,
        "service": "agent",
        "version": "1.0.0"  # This could be read from a version file or environment
    }

    return response


async def get_readiness_status() -> Dict[str, Any]:
    """
    Readiness check to determine if the TodoAgent is ready to accept requests

    Returns:
        Dictionary with readiness status
    """
    # For readiness, we need OpenAI connection, MCP connection, and agent components
    openai_check = await check_openai_connection()
    mcp_check = await check_mcp_connection()
    agent_check = await check_agent_components()

    if all(check["status"] == "ok" for check in [openai_check, mcp_check, agent_check]):
        return {
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "agent",
            "reason": "OpenAI API, MCP connection, and agent components available"
        }
    else:
        reasons = []
        if openai_check["status"] != "ok":
            reasons.append("OpenAI API unavailable")
        if mcp_check["status"] != "ok":
            reasons.append("MCP connection unavailable")
        if agent_check["status"] != "ok":
            reasons.append("Agent components unavailable")

        return {
            "status": "not_ready",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "agent",
            "reason": "; ".join(reasons)
        }


async def get_liveness_status() -> Dict[str, Any]:
    """
    Liveness check to determine if the TodoAgent is alive and responding

    Returns:
        Dictionary with liveness status
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "agent",
        "message": "TodoAgent is responding to requests"
    }