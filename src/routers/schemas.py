from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserDisplay(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: str


class PostBase(BaseModel):
    image_url: str
    caption: str
    creator_id: int


# for PostDisplay
class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str


# for PostDisplay
class Comment(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str
    username: str
    timestamp: datetime


class PostDisplay(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_url: str
    caption: str
    timestamp: datetime
    user: User
    comments: List[Comment]


class UserAuth(BaseModel):
    id: int
    username: str
    email: str


class CommentBase(BaseModel):
    username: str
    text: str
    post_id: int
