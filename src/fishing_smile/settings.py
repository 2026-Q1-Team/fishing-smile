from functools import cache

from pydantic import (
    BaseModel,
    Field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    user: str
    password: str
    host: str
    database: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix = 'FISHING_SMILE_',
        env_nested_delimiter = '_',
    )

    db: DatabaseSettings


@cache
def get_settings() -> Settings:
    return Settings()
