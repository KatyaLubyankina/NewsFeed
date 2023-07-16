import random
import string
from typing import Annotated, List

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from config import Settings, get_settings
from minio import Minio
from src.auth.oauth2 import get_current_user
from src.db import db_post
from src.db.database import get_db
from src.db.models import DbPost
from src.logging import logger_wraps
from src.routers.schemas import PostBase, PostDisplay, UserAuth

router = APIRouter(prefix="/post", tags=["post"])


@router.post("", response_model=PostDisplay)
@logger_wraps()
def create_post(request: PostBase, db: Session = Depends(get_db)) -> DbPost:
    """Creates new post

    Call src.db_post.create_post function

    Args:
    - request (PostBase): json with image_url, caption and creator_id
    - db (Session): database session

    Returns:
    - DbPost: id, image_url, caption, timestamp, username and
    list of comments
    """
    return db_post.create_post(db, request)


@router.get("/all", response_model=List[PostDisplay], summary="Retrive all posts")
@logger_wraps()
def posts(db: Session = Depends(get_db)) -> List[DbPost]:
    """Retrives all posts

    Calls src.db_post.get_all_posts function

    Args:
    - db (Session): database session

    Returns:
    - List of posts in PostDisplay format
    """
    return db_post.get_all_posts(db)


@router.post("/image", summary="Upload an image")
@logger_wraps()
def upload_file(
    settings: Annotated[Settings, Depends(get_settings)],
    image: UploadFile = File(...),
    current_user: UserAuth = Depends(get_current_user),
) -> dict:
    """Uploads an image

    This app performs uploading file for future posts in minIO S3 storage.
    Authentication is required.
    Random string of 6 characters is added to filename to prevent overwriting.

    Args:
    - image (UploadFile): image from filesystem
    - current_user: result of user validation by get_current_user function

    Returns:
    - {"Bucket name": "images", "filename": filename} with modified filename
    """
    letters = string.ascii_letters
    rand_str = "".join(random.choice(letters) for i in range(6))
    new = f"_{rand_str}."
    filename = new.join(image.filename.rsplit(".", 1))
    minio_client = Minio(
        endpoint=f"{settings.MINIO_HOST_NAME}:9000",
        access_key=settings.ACCESS_KEY_S3,
        secret_key=settings.SECRET_KEY_S3.get_secret_value(),
        secure=False,
    )
    found = minio_client.bucket_exists("images")
    if not found:
        minio_client.make_bucket("images")
    minio_client.put_object(
        "images", filename, image.file, length=-1, part_size=10 * 1024 * 1024
    )
    return {"Bucket name": "images", "filename": filename}


@router.get(
    "/delete/{id}", summary="Delete post", response_description='"ok" or HTTP exception'
)
@logger_wraps()
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user),
) -> str:
    """Delete post

    Call src.db_post.delete function

    Args:
    - id (int): post id
    - db (Session): database session
    - current_user (UserAuth): result of user validation
    by get_current_user function

    Returns:
    - 'ok' if post was deleted
    """
    return db_post.delete_post(db, id, current_user.id)
