"""
Application configuration settings.
"""

import os
from functools import lru_cache
from pathlib import Path


class Settings:
    """Application settings."""

    def __init__(self) -> None:
        # Application
        self.APP_NAME: str = "Context Assembly Framework"
        self.APP_VERSION: str = "0.1.0"
        self.DEBUG: bool = self._get_bool_env("DEBUG", False)

        # Database
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./caf.db")
        self.DATABASE_ECHO: bool = self._get_bool_env("DATABASE_ECHO", False)

        # Security
        self.SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")

        # File paths
        self.UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
        self.TEMPLATE_DIR: str = os.getenv("TEMPLATE_DIR", "./caf/templates")

        # Logging
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        # Ensure directories exist
        Path(self.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.TEMPLATE_DIR).mkdir(parents=True, exist_ok=True)

    def _get_bool_env(self, key: str, default: bool) -> bool:
        """Get boolean value from environment variable."""
        value = os.getenv(key, str(default)).lower()
        return value in ("true", "1", "yes", "on")


@lru_cache
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()


# For backward compatibility
settings = get_settings()
