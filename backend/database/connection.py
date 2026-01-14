"""
Database connection setup for the Todo AI Chatbot with Timeout Support
"""
from sqlmodel import create_engine, Session
from sqlalchemy import event, text
from sqlalchemy.pool import Pool, NullPool
import os
from typing import Generator
from contextlib import contextmanager
from config.timeout_config import get_timeout_config

# Get timeout configuration
timeout_config = get_timeout_config()

# Get database URL from environment, with a default for development
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/todo_chatbot_dev")

# Create the engine with timeout configuration
engine = create_engine(
    DATABASE_URL,
    echo=bool(os.getenv("DATABASE_ECHO", False)),  # Set DATABASE_ECHO to enable SQL logging
    poolclass=NullPool,  # Use NullPool for Neon serverless
    connect_args={}       # Remove statement_timeout from connect_args
)


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session for use with dependency injection or direct use.
    """
    with Session(engine) as session:
        yield session


@contextmanager
def get_session_context():
    """
    Context manager for database sessions that ensures proper cleanup with timeout support.
    """
    session = Session(engine)
    try:
        # Set statement timeout for this session
        timeout_ms = timeout_config.get_database_query_timeout() * 1000
        session.execute(text(f"SET statement_timeout = {timeout_ms};"))
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        # Reset timeout and close session
        session.execute(text("RESET statement_timeout;"))
        session.close()


def create_db_and_tables():
    """
    Create database tables. This should typically be called once at startup.
    """
    from models import Task, Conversation, Message
    from sqlmodel import SQLModel

    # Create all tables
    SQLModel.metadata.create_all(engine)


# Event listener for SQLite pragmas has been removed for Neon serverless compatibility
# The original SQLite pragma listener is no longer needed with NullPool