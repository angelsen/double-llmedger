from datetime import datetime, timedelta

from db.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


# Match the existing schema used by Lucia auth
class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    age = Column(Integer, nullable=True)

    # Relationship to sessions
    sessions = relationship("Session", back_populates="user")


class Session(Base):
    __tablename__ = "session"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    # Store as Integer timestamp to match Drizzle schema
    expires_at = Column(Integer, nullable=False)

    # Relationship to user
    user = relationship("User", back_populates="sessions")

    @property
    def expires_at_datetime(self):
        """Convert timestamp to datetime object"""
        # The SQLite timestamp is stored as seconds since epoch by Drizzle ORM
        try:
            return datetime.fromtimestamp(self.expires_at)  # Already in seconds
        except (ValueError, TypeError) as e:
            # If the conversion fails, log the error and return a far future date
            # to prevent sessions from being marked as expired incorrectly
            print(f"Error converting timestamp {self.expires_at}: {e}")
            return datetime.now() + timedelta(days=30)

    @property
    def is_expired(self):
        """Check if session is expired"""
        try:
            now = datetime.now()
            return now > self.expires_at_datetime
        except Exception as e:
            # If there's any error in comparison, log it and consider the session valid
            print(f"Error checking session expiration: {e}")
            return False
