"""
Correlation ID Handler for TodoAgent
"""
import uuid
from typing import Dict, Any, Optional
from contextlib import contextmanager
from contextvars import ContextVar


# Context variable to store correlation ID for the current agent execution
_agent_correlation_id_ctx: ContextVar[Optional[str]] = ContextVar('_agent_correlation_id_ctx', default=None)


def generate_agent_correlation_id() -> str:
    """
    Generate a new correlation ID for agent operations

    Returns:
        String representation of a UUID4
    """
    return str(uuid.uuid4())


def set_agent_correlation_id(correlation_id: str) -> None:
    """
    Set the correlation ID in the current agent execution context

    Args:
        correlation_id: The correlation ID to set
    """
    _agent_correlation_id_ctx.set(correlation_id)


def get_agent_correlation_id_from_context() -> Optional[str]:
    """
    Get the correlation ID from the current agent execution context

    Returns:
        Correlation ID if set, otherwise None
    """
    return _agent_correlation_id_ctx.get()


@contextmanager
def agent_correlation_id_context(correlation_id: str):
    """
    Context manager for temporarily setting a correlation ID in agent context

    Args:
        correlation_id: The correlation ID to set for the context
    """
    token = _agent_correlation_id_ctx.set(correlation_id)
    try:
        yield
    finally:
        _agent_correlation_id_ctx.reset(token)


def add_correlation_id_to_tool_parameters(parameters: Dict[str, Any], correlation_id: str) -> Dict[str, Any]:
    """
    Add correlation ID to tool call parameters

    Args:
        parameters: Tool call parameters
        correlation_id: The correlation ID to add

    Returns:
        Updated parameters dictionary with correlation ID
    """
    updated_params = parameters.copy()
    updated_params["correlation_id"] = correlation_id
    return updated_params