# import os

# import pytest
from fastapi.testclient import TestClient

from config import get_settings
from src.main import app
from tests.conftest import get_settings_override

client = TestClient(app)


app.dependency_overrides[get_settings] = get_settings_override


# def test_change_settings():
#     new_settings = get_settings_override()
#     assert new_settings.MINIO_HOST_NAME == 'play.minio.io'
#     my_settings = get_settings()
#     assert my_settings.MINIO_HOST_NAME == "play.minio.io"
#     # assert my_settings.ACCESS_KEY_S3 == 'Q3AM3UQ867SPQQA43P2F'
#     # assert my_settings.SECRET_KEY_S3.get_secret_value(
#     # ) == 'zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG'


def test_login(login_user):
    assert login_user.status_code == 200
    access_token = login_user.json().get("access_token")
    assert access_token


# def test_upload_image_success(login_user):
#     access_token = login_user.json().get("access_token")
#     file_path = "tests/test.png"
#     if os.path.isfile(file_path):
#         file = {"image": open(file_path, "rb")}
#         response = client.post(
#             "/post/image",
#             files=file,
#             headers={"Authorization": "bearer " + access_token},
#         )
#         assert response.status_code == 200
#         assert response.json().get("filename")
#     else:
#         pytest.fail("File does not exists.")


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
