# apps/public_api/configs/config.py

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .database_settings import DatabaseSettings


class AppSettings(BaseSettings):
    """
    Main application settings manager.
    Reads variables from environment or a .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    app_name: str = "DMS Public API"
    environment: str = Field(default="development")
    db: DatabaseSettings = DatabaseSettings()


settings = AppSettings()
