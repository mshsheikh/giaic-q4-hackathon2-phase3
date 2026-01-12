"""
Health Check Endpoints for MCP Server
"""
import asyncio
import time
from typing import Dict, Any
from datetime import datetime
from ..config import MCPConfig
from ..middleware.correlation_id_middleware import extract_correlation_id_from_headers


async def check_database_connection() -> Dict[str, Any]:
    """
    Check database connectivity and responsiveness

    Returns:
        Dictionary with database health status
    """
    start_time = time.time()
    try:
        # Import database connection here to avoid circular imports
        from backend.database.connection import get_session_context
        from sqlalchemy import text

        with get_session_context() as session:
            # Execute a simple query to test the database connection
            result = session.execute(text("SELECT 1"))
            db_status = "available" if result.fetchone() else "unavailable"
    except Exception as e:
        return {
            "status": "error",
            "component": "database",
            "details": str(e),
            "response_time_ms": round((time.time() - start_time) * 1000, 2)
        }

    return {
        "status": "ok",
        "component": "database",
        "details": db_status,
        "response_time_ms": round((time.time() - start_time) * 1000, 2)
    }


async def check_tool_availability() -> Dict[str, Any]:
    """
    Check availability of MCP tools

    Returns:
        Dictionary with tool availability status
    """
    start_time = time.time()

    try:
        # Check if tools are properly loaded and available
        # For now, just verify that we can import the tools
        from ..tools.add_task import add_task_tool
        from ..tools.list_tasks import list_tasks_tool
        from ..tools.complete_task import complete_task_tool
        from ..tools.delete_task import delete_task_tool
        from ..tools.update_task import update_task_tool

        # Verify that the functions exist
        tools = [add_task_tool, list_tasks_tool, complete_task_tool, delete_task_tool, update_task_tool]
        available_tools = len([tool for tool in tools if callable(tool)])

        return {
            "status": "ok" if available_tools == 5 else "warning",
            "component": "tools",
            "details": f"{available_tools}/5 tools available",
            "response_time_ms": round((time.time() - start_time) * 1000, 2)
        }
    except Exception as e:
        return {
            "status": "error",
            "component": "tools",
            "details": str(e),
            "response_time_ms": round((time.time() - start_time) * 1000, 2)
        }


async def get_health_status() -> Dict[str, Any]:
    """
    Comprehensive health check for the MCP server

    Returns:
        Dictionary with overall health status and component details
    """
    start_time = time.time()

    # Run checks concurrently
    db_task = check_database_connection()
    tool_task = check_tool_availability()

    db_check, tool_check = await asyncio.gather(db_task, tool_task)

    # Determine overall status
    checks = [db_check, tool_check]
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
        "service": "mcp_server",
        "version": "1.0.0"  # This could be read from a version file or environment
    }

    return response


async def get_readiness_status() -> Dict[str, Any]:
    """
    Readiness check to determine if the MCP server is ready to accept traffic

    Returns:
        Dictionary with readiness status
    """
    # For readiness, we're primarily concerned with database connectivity and tool availability
    db_check = await check_database_connection()
    tool_check = await check_tool_availability()

    if db_check["status"] == "ok" and tool_check["status"] == "ok":
        return {
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "mcp_server",
            "reason": "Database connection and tools available"
        }
    else:
        reasons = []
        if db_check["status"] != "ok":
            reasons.append("Database connection unavailable")
        if tool_check["status"] != "ok":
            reasons.append("MCP tools unavailable")

        return {
            "status": "not_ready",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "mcp_server",
            "reason": "; ".join(reasons)
        }


async def get_liveness_status() -> Dict[str, Any]:
    """
    Liveness check to determine if the MCP server is alive and responding

    Returns:
        Dictionary with liveness status
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "mcp_server",
        "message": "MCP Server is responding to requests"
    }