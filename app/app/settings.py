from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PGSettings(BaseSettings):
    HOST: str = "db"
    PORT: int | str = 5432
    USER: str = "user"
    PASSWORD: str = "password"
    NAME: str = "db"
    POOL_MINSIZE: int = 10
    POOL_MAX_OVERFLOW: int = 30
    POOL_TIMEOUT: int = 30
    POOL_RECYCLE: int = 240

    model_config = SettingsConfigDict(env_prefix="PG_")

    @computed_field
    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    API_VERSION: str = "v1"
    LOG_LEVEL: str = "info"
    REQUEST_SEMAPHORE: int = 450
    API_AUTH_KEY: str = "0000"

    PG: PGSettings = PGSettings()

    model_config = SettingsConfigDict(env_prefix="APP_")


@lru_cache
def get_settings() -> Settings:
    return Settings()
