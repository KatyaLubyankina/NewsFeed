from fastapi import FastAPI
from src.db import models
from src.db.database import engine
from src.routers import user, post, comment
from fastapi.staticfiles import StaticFiles
from src.auth import authentication
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)
app.include_router(authentication.router)
app.include_router(comment.router)


@app.get("/")
def root():
    return "Welcome to News Feed!"


origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
    )

models.Base.metadata.create_all(engine)

app.mount('/src/images', StaticFiles(directory='src/images'), name='images')
app.mount('/src/avatars', StaticFiles(directory='src/avatars'), name='avatars')