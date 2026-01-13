"""
Base Service Class with Timeout Support
"""
from abc import ABC
from contextlib import contextmanager
from typing import Any, Dict, Optional, Generator
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.connection import get_session_context
from config.timeout_config import get_timeout_config


class BaseService(ABC):
    """
    Base service class that provides common functionality with timeout support
    """

    def __init__(self):
        self.timeout_config = get_timeout_config()

    @contextmanager
    def get_session_with_timeout(self) -> Generator[Session, None, None]:
        """
        Context manager to get a database session with timeout settings

        Yields:
            Database session with timeout applied
        """
        with get_session_context() as session:
            # Apply query timeout at session level
            timeout_seconds = self.timeout_config.get_database_query_timeout()

            # Set statement timeout for PostgreSQL
            session.execute(text(f"SET SESSION statement_timeout = {timeout_seconds * 1000};"))  # milliseconds

            try:
                yield session
            finally:
                # Reset the timeout setting
                session.execute(text("RESET statement_timeout;"))

    def execute_with_timeout(self, session: Session, query: Any, params: Optional[Dict] = None) -> Any:
        """
        Execute a query with timeout applied

        Args:
            session: Database session
            query: SQL query to execute
            params: Query parameters (optional)

        Returns:
            Query result
        """
        timeout_seconds = self.timeout_config.get_database_query_timeout()

        # Set the timeout for this specific query
        session.execute(text(f"SET LOCAL statement_timeout = {timeout_seconds * 1000};"))  # milliseconds

        if params:
            result = session.execute(query, params)
        else:
            result = session.execute(query)

        return result

    def execute_scalar_with_timeout(self, session: Session, query: Any, params: Optional[Dict] = None) -> Any:
        """
        Execute a scalar query with timeout applied

        Args:
            session: Database session
            query: SQL query to execute
            params: Query parameters (optional)

        Returns:
            Scalar query result
        """
        result = self.execute_with_timeout(session, query, params)
        return result.scalar()