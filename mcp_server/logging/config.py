"""
Structured Logging Configuration for MCP Server
"""
import logging
import json
import sys
from datetime import datetime
from pythonjsonlogger import jsonlogger
from typing import Dict, Any, Optional


class MCPServerJsonFormatter(jsonlogger.JsonFormatter):
    """
    Custom JSON formatter for MCP Server with contextual information
    """
    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]) -> None:
        super().add_fields(log_record, record, message_dict)

        # Add timestamp in ISO format
        log_record['timestamp'] = datetime.fromtimestamp(record.created).isoformat()

        # Add log level
        log_record['level'] = record.levelname

        # Add service name
        log_record['service'] = 'mcp_server'

        # Add module and function information
        log_record['module'] = record.module
        log_record['function'] = record.funcName
        log_record['line'] = record.lineno


def setup_structured_logging(debug_mode: bool = False) -> None:
    """
    Set up structured JSON logging for the MCP server

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
    formatter = MCPServerJsonFormatter(
        '%(timestamp)s %(level)s %(service)s %(module)s %(function)s %(line)s %(message)s'
    )
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)


def log_with_context(
    correlation_id: Optional[str] = None,
    tool_name: Optional[str] = None,
    user_id: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Create a log record with contextual information for MCP server

    Args:
        correlation_id: Correlation ID
        tool_name: Name of the tool being executed
        user_id: User ID associated with the operation
        **kwargs: Additional context fields

    Returns:
        Dictionary with structured log information
    """
    log_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'mcp_server',
        'correlation_id': correlation_id,
        'tool_name': tool_name,
        'user_id': user_id
    }

    # Add any additional context
    log_data.update(kwargs)

    return log_data