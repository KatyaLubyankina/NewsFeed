from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_create_comment(create_comment):
    response = create_comment
    assert response.status_code == 200
    assert response.json().get("post_id") == 1
    assert response.json().get("text") == "Test comment"
    assert response.json().get("id") == 1
    assert response.json().get("username") == "test"


def test_get_all_comments_success(create_comment):
    post_id = 1
    response = client.get(f"/comment/all/{post_id}")
    assert response.status_code == 200
    assert response.json()[0].get("id") == 1
    assert response.json()[0].get("post_id") == 1
    assert response.json()[0].get("text") == "Test comment"
    assert response.json()[0].get("username") == "test"
