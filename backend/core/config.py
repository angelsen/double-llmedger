import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings that can be loaded from environment variables"""

    # Database settings - point to the same database used by the frontend
    DATABASE_URL: str = "sqlite:///../data/auth.db"

    # API settings
    API_V1_PREFIX: str = "/api"

    # CORS settings
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]
    
    # Security settings
    SECRET_KEY: str = "change_this_to_a_secure_random_value"
    ALLOWED_ORIGIN: str = "http://localhost:5173"

    # Logging settings
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create global settings instance
settings = Settings()

# Ensure data directory exists
if settings.DATABASE_URL.startswith("sqlite:///"):
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
