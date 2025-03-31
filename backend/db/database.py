import os

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get absolute path to the database
import logging
logger = logging.getLogger(__name__)

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db_path = os.path.join(base_dir, "data", "auth.db")

# Read from environment if provided, use default if not
from core.config import settings

# Convert standard SQLite URL to read-only URL with URI enabled
if settings.DATABASE_URL.startswith('sqlite:///'):
    # Extract the database path without the sqlite:/// prefix
    db_path = settings.DATABASE_URL.replace('sqlite:///', '')
    
    # Convert relative path to absolute if necessary
    if not os.path.isabs(db_path):
        db_path = os.path.abspath(os.path.join(base_dir, db_path))
    
    # Create URI format URL with read-only mode and URI enabled
    SQLALCHEMY_DATABASE_URL = f"sqlite:///file:{db_path}?mode=ro&uri=true"
    
    logger.info(f"Using database at: {db_path}")
else:
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create SQLite engine with thread checking disabled
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)


# Set database connection pragmas
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")  # Enable foreign key constraints
    cursor.close()


# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Dependency for getting DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
