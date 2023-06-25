from fastapi.testclient import TestClient
from src.main import app
import pytest

client = TestClient(app)


# @pytest.fixture()
# def create_user():
#     response = client.post(
#         "/user",
#         json={
#             "username": "test",
#             "email": "test@gmail.com",
#             "password": "test",
#         }
#     )
#     return response


# def test_create_user(create_user):
#     response = create_user
#     assert response.status_code == 200
#     assert response.json() == {"username": "test", "email": "test@gmail.com"}


# # fixture perfomes login and retuns access token
# @pytest.fixture
# def login(create_user):
#     response = client.post(
#         "/login",
#         json={
#             "username": "test",
#             "password": "test",
#         }
#     )
#     access_token = response.json().get("access_token")
#     return access_token


# def test_login_success(login):
#     access_token = login
#     assert access_token


# # подумать, как его изменить!
# def test_auth_error():
#     response = client.post(
#         "/login",
#         data={"username": "", "password": ""
#         }
#         )

#     access_token = response.json().get("access_token")
#     assert not access_token
#     message = response.json().get("detail")[0].get("msg")
#     assert message == "field required"


# # убрать
# def test_auth_success():
#     response = client.post(
#         "/login",
#         data={
#             "username": "test", "password": "test"
#         }
#         )
#     access_token = response.json().get("access_token")
#     assert access_token


# def test_get_all_posts():
#     response = client.get("/post/all")
#     assert response.status_code == 200


# def test_post_article(login):
#     access_token = login
#     response = client.post(
#         "/post/",
#         json={
#             "image_url": "test_url",
#             "image_url_type": "relative",
#             "caption": "Test caption",
#             "creator_id": 1
#         },
#         headers={
#             "Authorization": "bearer " + access_token
#         }
#     )
#     assert response.status_code == 200
#     assert response.json().get("caption") == "Test caption"


# def test_post_article_error_url_type(login):
#     access_token = login
#     response = client.post(
#         "/post/",
#         json={
#             "image_url": "test_url",
#             "image_url_type": "",
#             "caption": "Test caption",
#             "creator_id": 1
#         },
#         headers={
#             "Authorization": "bearer " + access_token
#         }
#     )
#     assert response.status_code == 422
