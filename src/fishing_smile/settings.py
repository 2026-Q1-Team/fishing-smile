from functools import cache

from pydantic import (
    BaseModel,
    Field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    """Matches arguments of `sqlalchemy.engine.URL.create`"""
    drivername: str = 'mysql+pymysql'
    username: str = 'fish_app'
    password: str
    host: str = None
    port: int = None
    database: str = 'fishtrack'


class CastNetSettings(BaseModel):
    sender: str
    password: str
    url: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix = 'FISHING_SMILE_',
        env_nested_delimiter = '__',
    )

    db: DatabaseSettings
    cast: CastNetSettings


@cache
def get_settings() -> Settings:
    return Settings()
