from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from loguru import logger

from src.auth import authentication
from src.db import models
from src.db.database import engine
from src.logging import logger_wraps
from src.routers import comment, post, user

logger.remove()
logger.add(
    "log.log",
    colorize=False,
    format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>",
    level="DEBUG",
)

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)
app.include_router(authentication.router)
app.include_router(comment.router)

add_pagination(app)


@app.get("/")
@logger_wraps()
def root():
    return "Welcome to News Feed!"


origins = ["http://localhost:9000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
