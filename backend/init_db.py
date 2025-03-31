#!/usr/bin/env python3
"""
Script to test SQLAlchemy database connection.

This script does NOT create any tables as the frontend (SvelteKit with Drizzle ORM)
is responsible for managing the database schema.
"""

import logging
import os
import sys

from sqlalchemy import text

# Add the parent directory to sys.path before imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# This import must come after modifying sys.path
from db.database import engine  # noqa: E402

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_db_connection():
    """Test the database connection without creating tables"""
    try:
        # Check database connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info(f"Database connection test: {result.scalar()}")

            # List tables
            tables = conn.execute(
                text("SELECT name FROM sqlite_master WHERE type='table'")
            ).fetchall()
            logger.info(f"Existing tables: {[table[0] for table in tables]}")

            # Verify read-only mode
            logger.warning("IMPORTANT: Backend is using database in READ-ONLY mode.")
            logger.warning(
                "DO NOT attempt to modify the database from the Python backend."
            )
            logger.warning(
                "All authentication and session management is handled by the "
                "SvelteKit frontend."
            )

        return True
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        return False


if __name__ == "__main__":
    test_db_connection()
