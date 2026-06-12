# apps/public_api/configs/database_settings.py

from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    url: str = Field(default="sqlite+aiosqlite:///./test.db")
    echo: bool = Field(default=False)
