"""
Health Check Endpoints for Backend Service
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from datetime import datetime
import time
import subprocess
import socket
from sqlalchemy import text
from backend.database.connection import get_session_context
from backend.config.debug_config import get_debug_config


router = APIRouter(tags=["health"])


def check_database_connection() -> Dict[str, Any]:
    """
    Check database connectivity and responsiveness

    Returns:
        Dictionary with database health status
    """
    start_time = time.time()
    try:
        with get_session_context() as session:
            # Execute a simple query to test the database connection
            result = session.execute(text("SELECT 1"))
            db_status = "available" if result.fetchone() else "unavailable"
    except Exception as e:
        db_status = "unavailable"
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


def check_external_services() -> Dict[str, Any]:
    """
    Check connectivity to external services (APIs, etc.)

    Returns:
        Dictionary with external service health status
    """
    start_time = time.time()

    # For now, just check if we can reach the OpenAI API endpoint
    # In a real implementation, we'd do an actual API call
    try:
        # Check if we have the necessary environment variables
        import os
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {
                "status": "warning",
                "component": "external_api",
                "details": "OPENAI_API_KEY not configured",
                "response_time_ms": round((time.time() - start_time) * 1000, 2)
            }

        # For now, just check that we have the key - in a real system we'd make an actual API call
        return {
            "status": "ok",
            "component": "external_api",
            "details": "API key configured",
            "response_time_ms": round((time.time() - start_time) * 1000, 2)
        }
    except Exception as e:
        return {
            "status": "error",
            "component": "external_api",
            "details": str(e),
            "response_time_ms": round((time.time() - start_time) * 1000, 2)
        }


@router.get("/health", summary="Overall system health check")
async def health_check() -> Dict[str, Any]:
    """
    Comprehensive health check for the backend service

    Returns:
        Dictionary with overall health status and component details
    """
    start_time = time.time()

    # Check individual components
    db_check = check_database_connection()
    external_check = check_external_services()

    # Determine overall status
    checks = [db_check, external_check]
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
        "service": "backend",
        "version": "1.0.0"  # This could be read from a version file or environment
    }

    # Add debug information if debug mode is enabled
    debug_config = get_debug_config()
    if debug_config.is_debug_mode():
        response["debug_info"] = {
            "debug_mode": True,
            "process_id": str(getattr(subprocess, 'getoutput', lambda: 'N/A')('echo $$')),
            "uptime_seconds": getattr(time, 'perf_counter', lambda: 0)()  # This is a simplified uptime
        }

    return response


@router.get("/health/ready", summary="Readiness check")
async def readiness_check() -> Dict[str, Any]:
    """
    Readiness check to determine if the service is ready to accept traffic

    Returns:
        Dictionary with readiness status
    """
    # For readiness, we're primarily concerned with database connectivity
    db_check = check_database_connection()

    if db_check["status"] == "ok":
        return {
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "backend",
            "reason": "Database connection available"
        }
    else:
        return {
            "status": "not_ready",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "backend",
            "reason": "Database connection unavailable"
        }


@router.get("/health/live", summary="Liveness check")
async def liveness_check() -> Dict[str, Any]:
    """
    Liveness check to determine if the service is alive and responding

    Returns:
        Dictionary with liveness status
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "backend",
        "message": "Service is responding to requests"
    }