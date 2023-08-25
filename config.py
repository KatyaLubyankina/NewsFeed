from functools import lru_cache

from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "postgresql://postgres:postgres@postgres:5432/db"
    SECRET_KEY: SecretStr
    MINIO_HOST_NAME: str = "minio"
    ACCESS_KEY_S3: str = "minioadmin"
    SECRET_KEY_S3: SecretStr
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_USER: str = "postgres"

    class Config:
        env_file = ".env_vars"
        secrets_dir = "src/secrets"


@lru_cache()
def get_settings():
    return Settings()
