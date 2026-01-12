"""
Correlation ID Generator Utilities
"""
import uuid
from typing import Optional
from contextlib import contextmanager
from contextvars import ContextVar


# Context variable to store correlation ID for the current execution context
_correlation_id_ctx: ContextVar[Optional[str]] = ContextVar('_correlation_id_ctx', default=None)


def generate_correlation_id() -> str:
    """
    Generate a new correlation ID

    Returns:
        String representation of a UUID4
    """
    return str(uuid.uuid4())


def set_correlation_id(correlation_id: str) -> None:
    """
    Set the correlation ID in the current execution context

    Args:
        correlation_id: The correlation ID to set
    """
    _correlation_id_ctx.set(correlation_id)


def get_correlation_id_from_context() -> Optional[str]:
    """
    Get the correlation ID from the current execution context

    Returns:
        Correlation ID if set, otherwise None
    """
    return _correlation_id_ctx.get()


@contextmanager
def correlation_id_context(correlation_id: str):
    """
    Context manager for temporarily setting a correlation ID

    Args:
        correlation_id: The correlation ID to set for the context
    """
    token = _correlation_id_ctx.set(correlation_id)
    try:
        yield
    finally:
        _correlation_id_ctx.reset(token)