"""
Database configuration module.

This module defines database connectivity, session management,
and provides utilities for working with the database.
"""
import logging
import os
from collections.abc import Generator

from core.config import settings
from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Configure logger
logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


# Function to determine database URL and mode
def get_database_url() -> str:
    """
    Get the database URL, respecting environment settings.

    Returns:
        The database URL with appropriate options
    """
    # Read from environment if provided, use default if not
    db_url = settings.DATABASE_URL
    read_only = settings.DATABASE_READ_ONLY

    # Handle SQLite specifically
    if db_url.startswith('sqlite:///'):
        # Extract the database path without the sqlite:/// prefix
        db_path = db_url.replace('sqlite:///', '')

        # Convert relative path to absolute if necessary
        if not os.path.isabs(db_path):
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            base_dir = os.path.dirname(parent_dir)
            db_path = os.path.abspath(os.path.join(base_dir, db_path))

        # Create directory for database file if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Create URI format URL with correct mode
        if read_only:
            logger.info(f"Using database in read-only mode: {db_path}")
            return f"sqlite:///file:{db_path}?mode=ro&uri=true"
        else:
            return f"sqlite:///file:{db_path}?uri=true"

    # Return original URL for non-SQLite databases
    return db_url


# Create engine
engine = create_engine(
    get_database_url(),
    connect_args={
        "check_same_thread": False
    } if settings.DATABASE_URL.startswith("sqlite") else {},
    echo=settings.DATABASE_ECHO,
)


# Set database connection pragmas for SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Set SQLite pragmas on connection."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")  # Enable foreign key constraints
    cursor.close()


# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)


# Dependency for getting DB session
def get_db() -> Generator[Session]:
    """
    Provide a database session.

    Yields:
        A database session

    Notes:
        This function is used as a FastAPI dependency.
        The session is automatically closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
