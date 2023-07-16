# NewsFeed with FastApi
![](coverage.svg)

This project allows users to view and create news posts with pictures and comments.
See detailed [OpenAPI documentation of NewsFeed project](https://katyalubyankina.github.io/NewsFeed/) without starting the project.

**Features**:
- [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10) - JWT authentication using [OAuth2](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [SQLite](https://www.sqlite.org/index.html) - for the database
- [SqlAlchemy](https://www.sqlalchemy.org/) - for ORM
- [Pytest](https://docs.pytest.org/en/latest/) - for tests (Reusable Pytest fixtures and new test database for each test)
- [Docker Compose](https://docs.docker.com/compose/) - for running application
- [Uvicorn](https://www.uvicorn.org/) - for ASGI web server
- CI/CD pipeline: Github action for pytest and docker image build before pull request in master
- [Poetry](https://python-poetry.org/) - for packaging and dependency management
- [Python-dotenv](https://github.com/theskumar/python-dotenv) - for reading configuration variables
- [Loguru](https://loguru.readthedocs.io/en/stable/api/logger.html) - for logging errors
and secret data
# Getting started
Run these commands to start project
```Python
docker-compose build
docker-compose up
```
The project documentation will be at http://localhost/docs.

# Testing
This project comes with Pytest and a few Pytest fixtures for new user, login, post and comment. Tests are located in **/tests** directory and the fixtures are available in **tests/conftest.py**.
To run all tests use:
```Shell
pytest
```
To calculate **Code Coverage** run:
```Shell
pytest --cov
```

# Examples:
Some examples of API endpoints.

## Create new user

Request to create new user
```
curl -X 'POST' \
  'http://localhost/user' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "test",
  "email": "test@gmail.com",
  "password": "test",
  "avatar_url": ""
}'
```
Response:
```
{
  "username": "test",
  "email": "test@gmail.com"
}
```
### Create new post
Authentication is required for this endpoint.
Request:
```
curl -X 'POST' \
  'http://localhost:8000/post' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "image_url": "test url",
  "caption": "test caption",
  "creator_id": 1
}'
```
Response:
```
{
  "id": 1,
  "image_url": "test url",
  "caption": "test caption",
  "timestamp": "2023-06-29T11:02:39.927456",
  "user": {
    "username": "test"
  },
  "comments": []
}
```
### Create new comment
Authentication is required for this endpoint.
Request:
```
curl -X 'POST' \
  'http://localhost:8000/comment' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2ODgwMjY2NDF9.0BlUSHzdzR4lOdghXxuwxijc1E1aZQYJ_lOOUFWbNwY' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "test",
  "text": "test comment",
  "post_id": 1
}'
```
Response:
```
{
  "text": "test comment",
  "username": "test",
  "post_id": 1,
  "id": 1,
  "timestamp": "2023-06-29T11:04:21.418987"
}
```
### Get all posts
Request:
```
curl -X 'GET' \
  'http://localhost:8000/post/all' \
  -H 'accept: application/json'
```
Response:
```
[
  {
    "id": 1,
    "image_url": "test url",
    "caption": "test caption",
    "timestamp": "2023-06-29T11:02:39.927456",
    "user": {
      "username": "test"
    },
    "comments": [
      {
        "text": "test comment",
        "username": "test",
        "timestamp": "2023-06-29T11:04:21.418987"
      }
    ]
  }
]
```
### Get all comment for post
Request:
```
curl -X 'GET' \
  'http://localhost:8000/comment/all/1' \
  -H 'accept: application/json'
```
Response:
```
[
  {
    "text": "test comment",
    "username": "test",
    "post_id": 1,
    "id": 1,
    "timestamp": "2023-06-29T11:04:21.418987"
  }
]
```
### Delete post
Authenticated user can delete post only if user created this post.
Request:
```
curl -X 'GET' \
  'http://localhost:8000/post/delete/1' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2ODgwMjY2NDF9.0BlUSHzdzR4lOdghXxuwxijc1E1aZQYJ_lOOUFWbNwY'
```
Response:
```
"ok"
```
