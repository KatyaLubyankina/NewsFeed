from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


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
