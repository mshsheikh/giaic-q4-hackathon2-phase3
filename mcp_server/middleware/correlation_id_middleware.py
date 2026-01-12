"""
Correlation ID Middleware for MCP Server
"""
import uuid
from typing import Dict, Any, Optional


def extract_correlation_id_from_headers(headers: Dict[str, str]) -> str:
    """
    Extract correlation ID from headers, generating a new one if not present

    Args:
        headers: Dictionary of headers

    Returns:
        Correlation ID string
    """
    correlation_id = headers.get("x-correlation-id") or str(uuid.uuid4())
    return correlation_id


def add_correlation_id_to_response(response: Dict[str, Any], correlation_id: str) -> Dict[str, Any]:
    """
    Add correlation ID to response metadata

    Args:
        response: The response dictionary
        correlation_id: The correlation ID to add

    Returns:
        Updated response dictionary with correlation ID
    """
    # Add correlation ID to response metadata if not already present
    if not response.get("metadata"):
        response["metadata"] = {}

    response["metadata"]["correlation_id"] = correlation_id
    return response


def get_correlation_id_for_tool_call(parameters: Dict[str, Any]) -> str:
    """
    Get correlation ID from tool call parameters or generate new one

    Args:
        parameters: Tool call parameters

    Returns:
        Correlation ID string
    """
    correlation_id = parameters.get("correlation_id") or str(uuid.uuid4())
    return correlation_id