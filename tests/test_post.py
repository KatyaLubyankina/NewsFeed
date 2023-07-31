from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_login(login_user):
    assert login_user.status_code == 200
    access_token = login_user.json().get("access_token")
    assert access_token


def test_get_all_posts(test_db):
    response = client.get("/post/all")
    assert response.status_code == 200


def test_create_post(create_post):
    response = create_post[0]
    assert response.status_code == 200
    assert response.json().get("caption") == "Test caption"


def test_delete_post_success(create_post):
    id = 1
    access_token = create_post[1]
    response = client.get(
        f"/post/delete/{id}", headers={"Authorization": "bearer " + access_token}
    )
    assert response.status_code == 200
    assert response.json() == "ok"


def test_delete_post_token_error(create_post):
    id = 1
    access_token = ""
    response = client.get(
        f"/post/delete/{id}", headers={"Authorization": "bearer " + access_token}
    )
    assert response.status_code == 401


def test_delete_post_id_error(create_post):
    id = 2
    access_token = create_post[1]
    response = client.get(
        f"/post/delete/{id}", headers={"Authorization": "bearer " + access_token}
    )
    assert response.status_code == 404
