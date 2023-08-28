from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(secrets_dir="src/secrets/", env_file=".env_vars")
    SQLALCHEMY_DATABASE_URL: str = "postgresql://postgres:postgres@postgres:5432/postgres"
    SECRET_KEY: SecretStr
    MINIO_HOST_NAME: str = "minio"
    ACCESS_KEY_S3: str = "minioadmin"
    SECRET_KEY_S3: SecretStr
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_USER: str = "postgres"


@lru_cache()
def get_settings():
    return Settings()
