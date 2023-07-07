from functools import lru_cache

from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./news_api.db"
    SECRET_KEY: SecretStr

    class Config:
        secrets_dir = "src/secrets"


@lru_cache()
def get_settings():
    return Settings()
