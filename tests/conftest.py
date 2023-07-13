import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from config import Settings, get_settings
from src.db.database import Base, get_db
from src.main import app


def get_settings_override():
    return Settings(
        SQLALCHEMY_DATABASE_URL="sqlite:///./test_api.db",
        MINIO_HOST_NAME="play.minio.io",
        ACCESS_KEY_S3="Q3AM3UQ867SPQQA43P2F",
        SECRET_KEY_S3="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
    )


app.dependency_overrides[get_settings] = get_settings_override

SQLALCHEMY_DATABASE_URL = get_settings().SQLALCHEMY_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def create_user():
    response = client.post(
        "/user",
        json={
            "username": "test",
            "email": "test@gmail.com",
            "password": "test",
        },
    )
    return response


@pytest.fixture()
def login_user(test_db, create_user):
    response = client.post("/login", data={"username": "test", "password": "test"})
    return response


@pytest.fixture()
def create_post(login_user):
    access_token = login_user.json().get("access_token")
    response = client.post(
        "/post/",
        json={
            "image_url": "test_url",
            "image_url_type": "relative",
            "caption": "Test caption",
            "creator_id": 1,
        },
        headers={"Authorization": "bearer " + access_token},
    )
    return [response, access_token]


@pytest.fixture()
def create_comment(create_post):
    access_token = create_post[1]
    response = client.post(
        "/comment",
        json={"username": "test", "text": "Test comment", "post_id": 1},
        headers={"Authorization": "bearer " + access_token},
    )
    return response
