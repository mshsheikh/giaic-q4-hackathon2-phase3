"""
Structured Logging Configuration for Backend
"""
import logging
import json
import sys
from datetime import datetime
from pythonjsonlogger import jsonlogger
from typing import Dict, Any, Optional
from ..middleware.correlation_id_middleware import get_correlation_id
from fastapi import Request


class StructuredJsonFormatter(jsonlogger.JsonFormatter):
    """
    Custom JSON formatter that adds correlation ID and other contextual information
    """
    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]) -> None:
        super().add_fields(log_record, record, message_dict)

        # Add timestamp in ISO format
        log_record['timestamp'] = datetime.fromtimestamp(record.created).isoformat()

        # Add log level
        log_record['level'] = record.levelname

        # Add service name
        log_record['service'] = 'backend'

        # Add module and function information
        log_record['module'] = record.module
        log_record['function'] = record.funcName
        log_record['line'] = record.lineno


def setup_structured_logging(debug_mode: bool = False) -> None:
    """
    Set up structured JSON logging for the backend application

    Args:
        debug_mode: Whether to enable debug level logging
    """
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)

    # Clear existing handlers
    logger.handlers.clear()

    # Create handler
    handler = logging.StreamHandler(sys.stdout)

    # Create formatter
    formatter = StructuredJsonFormatter(
        '%(timestamp)s %(level)s %(service)s %(module)s %(function)s %(line)s %(message)s'
    )
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)


def log_with_context(
    request: Optional[Request] = None,
    correlation_id: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Create a log record with contextual information

    Args:
        request: FastAPI request object (optional)
        correlation_id: Correlation ID (optional)
        **kwargs: Additional context fields

    Returns:
        Dictionary with structured log information
    """
    log_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'backend',
        'correlation_id': correlation_id or (request.state.correlation_id if request and hasattr(request.state, 'correlation_id') else None)
    }

    # Add any additional context
    log_data.update(kwargs)

    return log_data