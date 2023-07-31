# NewsFeed with FastApi
![](coverage.svg)

This project allows users to view and create news posts with pictures and comments.
See detailed [OpenAPI documentation of NewsFeed project](https://katyalubyankina.github.io/NewsFeed/) without starting the project.

**Features**:
- [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10.10) - framework for API
- [OAuth2](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) - for authentication with JSON Web Token
- [SQLite](https://www.sqlite.org/index.html) - for the database
- [SqlAlchemy](https://www.sqlalchemy.org/) - for ORM
- [MinIO](https://min.io/) - for S3 storage
- [Pytest](https://docs.pytest.org/en/latest/) - for tests (Reusable Pytest fixtures and new test database for each test)
- [Docker Compose](https://docs.docker.com/compose/) - for running application (containers for application and MinIO storage with volumes)
- [Uvicorn](https://www.uvicorn.org/) - for ASGI web server
- CI/CD pipeline: Github action for pytest and docker image build before pull request in master
- [Poetry](https://python-poetry.org/) - for packaging and dependency management
- [Fastapi-pagination](https://github.com/uriyyo/fastapi-pagination) - for pagination in endpoint for getting all posts
- [Python-dotenv](https://github.com/theskumar/python-dotenv) - for reading configuration variables and secret data
- [Loguru](https://loguru.readthedocs.io/en/stable/api/logger.html) - for logging errors
- [Pre-commit](https://pre-commit.com/) - black, flake8 and isort formate code before each commit
# Getting started
Run these commands to start project
```Python
docker-compose build
docker-compose up
```
The API documentation will be at http://localhost/docs.
API endpoints will be available at http://localhost/.
MinIO object storage - http://localhost:9000 - use minioadmin as login and password.

# Testing
This project comes with Pytest and a few Pytest fixtures for new user, login, post and comment. Tests are located in **/tests** directory and the fixtures are available in **tests/conftest.py**.
To run all tests use:
```Shell
pytest
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
  'http://localhost/post' \
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
  'http://localhost/comment' \
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
  'http://localhost/post/all' \
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
  'http://localhost/comment/all/1' \
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
  'http://localhost/post/delete/1' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2ODgwMjY2NDF9.0BlUSHzdzR4lOdghXxuwxijc1E1aZQYJ_lOOUFWbNwY'
```
Response:
```
"ok"
```
