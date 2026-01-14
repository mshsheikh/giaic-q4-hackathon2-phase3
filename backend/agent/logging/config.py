"""
Structured Logging Configuration for TodoAgent
"""
import logging
import json
import sys
from datetime import datetime
from pythonjsonlogger import jsonlogger
from typing import Dict, Any, Optional


class AgentJsonFormatter(jsonlogger.JsonFormatter):
    """
    Custom JSON formatter for TodoAgent with contextual information
    """
    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]) -> None:
        super().add_fields(log_record, record, message_dict)

        # Add timestamp in ISO format
        log_record['timestamp'] = datetime.fromtimestamp(record.created).isoformat()

        # Add log level
        log_record['level'] = record.levelname

        # Add service name
        log_record['service'] = 'agent'

        # Add module and function information
        log_record['module'] = record.module
        log_record['function'] = record.funcName
        log_record['line'] = record.lineno


def setup_structured_logging(debug_mode: bool = False) -> None:
    """
    Set up structured JSON logging for the TodoAgent

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
    formatter = AgentJsonFormatter(
        '%(timestamp)s %(level)s %(service)s %(module)s %(function)s %(line)s %(message)s'
    )
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)


def log_with_context(
    correlation_id: Optional[str] = None,
    user_id: Optional[str] = None,
    conversation_id: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Create a log record with contextual information for agent

    Args:
        correlation_id: Correlation ID
        user_id: User ID associated with the operation
        conversation_id: Conversation ID associated with the operation
        **kwargs: Additional context fields

    Returns:
        Dictionary with structured log information
    """
    log_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'agent',
        'correlation_id': correlation_id,
        'user_id': user_id,
        'conversation_id': conversation_id
    }

    # Add any additional context
    log_data.update(kwargs)

    return log_data