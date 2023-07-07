from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.auth import authentication
from src.db import models
from src.db.database import engine
from src.routers import comment, post, user

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)
app.include_router(authentication.router)
app.include_router(comment.router)


@app.get("/")
def root():
    return "Welcome to News Feed!"


models.Base.metadata.create_all(engine)

app.mount("/src/images", StaticFiles(directory="src/images"), name="images")
