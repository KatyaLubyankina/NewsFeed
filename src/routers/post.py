from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from src.routers.schemas import PostDisplay, UserAuth, PostBase
from src.db.database import get_db
from src.db import db_post
from typing import List
import random
import string
import shutil
from src.auth.oauth2 import get_current_user
from src.db.models import DbPost

router = APIRouter(
    prefix='/post',
    tags=['post']
)


@router.post('', response_model=PostDisplay)
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


@router.get('/all',
            response_model=List[PostDisplay],
            summary='Retrive all posts'
)
def posts(db: Session = Depends(get_db)) -> List[DbPost]:
    """Retrives all posts

    Calls src.db_post.get_all_posts function

    Args:
    - db (Session): database session

    Returns:
    - List of posts in PostDisplay format
    """
    return db_post.get_all_posts(db)


@router.post('/image',
             summary='Upload an image',
             response_description='Path to uploaded file'
             )
def upload_file(image: UploadFile = File(...),
                current_user: UserAuth = Depends(get_current_user)) -> dict:
    """Uploads an image

    This app performs uploading file for future posts.
    Authentication is required.
    Random string of 6 characters is added to filename to prevent overwriting.

    Args:
    - image (UploadFile): image from filesystem
    - current_user: result of user validation by get_current_user function

    Returns:
    - {"filename": path} with path to uploaded file
    """
    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'src/images/{filename}'

    with open(path, mode='wb+') as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'filename': path}


@router.get('/delete/{id}',
            summary='Delete post',
            response_description='"ok" or HTTP exception'
            )
def delete(id: int, db: Session = Depends(get_db),
           current_user: UserAuth = Depends(get_current_user)
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
