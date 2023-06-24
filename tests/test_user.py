import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.db.database import Base
from src.main import app
from src.db.database import get_db


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_api.db"

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
        }
    )
    return response


def test_create_user(test_db, create_user):
    response = create_user
    assert response.status_code == 200
    assert response.json() == {"username": "test", "email": "test@gmail.com"}


def test_login_success(test_db, create_user):
    response = client.post('/login', data={"username": "test", "password": "test"})
    assert response.status_code == 200
    access_token = response.json().get("access_token")
    assert access_token


def test_login_error(test_db, create_user):
    response = client.post('/login', data={"username": "error", "password": "error"})
    assert response.status_code == 404
    message = response.json().get("detail")
    assert message == "Invalid credentials"
