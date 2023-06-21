from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_all_posts():
    response = client.get("/post/all")
    assert response.status_code == 200


def test_create_user():
    response = client.post("/user",
                           json={
                               "username": "test",
                               "email": "test",
                               "password": "test",
                           })
    assert response.status_code == 200


def test_auth_error():
    response = client.post("/login",
                           data={"username": "", "password": ""})

    access_token = response.json().get("access_token")
    assert not access_token
    message = response.json().get("detail")[0].get("msg")
    assert message == "field required"


def test_auth_success():
    response = client.post("/login",
                           data={"username": "test", "password": "test"})
    access_token = response.json().get("access_token")
    assert access_token


def test_post_article():
    auth = client.post("/login",
                       data={"username": "test", "password": "test"})
    access_token = auth.json().get("access_token")
    assert access_token
    response = client.post(
        "/post/",
        json={
            "image_url": "test_url",
            "image_url_type": "relative",
            "caption": "Test caption",
            "creator_id": 1
        },
        headers={
            "Authorization": "bearer " + access_token
        }
    )
    assert response.status_code == 200
    assert response.json().get("caption") == "Test caption"


def test_post_article_error_url_type():
    auth = client.post("/login",
                       data={"username": "test", "password": "test"})
    access_token = auth.json().get("access_token")
    assert access_token
    response = client.post(
        "/post/",
        json={
            "image_url": "test_url",
            "image_url_type": "",
            "caption": "Test caption",
            "creator_id": 1
        },
        headers={
            "Authorization": "bearer " + access_token
        }
    )
    assert response.status_code == 422
