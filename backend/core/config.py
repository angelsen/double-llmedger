"""
Configuration settings for the application.

This module defines the application settings using Pydantic's BaseSettings.
Settings can be overridden using environment variables.
"""
import os
from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings that can be loaded from environment variables"""

    # Database settings
    DATABASE_URL: str = Field(
        "sqlite:///data/auth.db",
        description="Database connection string",
    )
    DATABASE_READ_ONLY: bool = True
    DATABASE_ECHO: bool = False

    # API settings
    API_V1_PREFIX: str = "/api"
    PROJECT_NAME: str = "DoubleLLMedger API"
    PROJECT_DESCRIPTION: str = "API for Double-LLMedger financial transactions ledger"
    VERSION: str = "0.1.0"

    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True

    # CORS settings
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    # Security settings
    SECRET_KEY: str = "change_this_to_a_secure_random_value"
    ALLOWED_ORIGIN: str = "http://localhost:5173"

    # Logging settings
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    # Environment settings
    ENVIRONMENT: Literal["development", "testing", "production"] = "development"

    # Configuration for Pydantic v2
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        env_nested_delimiter="__",
        extra="ignore",
    )

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Ensure the secret key is properly set"""
        if (v == "change_this_to_a_secure_random_value" and
            cls.model_config.get("ENVIRONMENT") == "production"):
            raise ValueError("Default secret key cannot be used in production")
        return v

    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.ENVIRONMENT == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.ENVIRONMENT == "production"


@lru_cache
def get_settings() -> Settings:
    """Factory function for creating cached settings instance"""
    return Settings()


# Create global settings instance for simple imports
settings = get_settings()

# Ensure data directory exists
if settings.DATABASE_URL.startswith("sqlite:///"):
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
