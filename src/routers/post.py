from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from src.routers.schemas import PostDisplay, UserAuth, PostBase
from src.db.database import get_db
from src.db import db_post
from typing import List
import random
import string
import shutil
from src.auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/post',
    tags=['post']
)
# API accepts only these types of image_url_type
image_url_types = ['absolute', 'relative']


@router.post('', response_model=PostDisplay)
def create(request: PostBase, db: Session = Depends(get_db)):
    if request.image_url_type not in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Parametre image url_type can only take values 'absolute' or 'relative'"
                            )
    return db_post.create(db, request)


@router.get('/all',
            response_model=List[PostDisplay],
            summary='Retrive all posts',
            description='This app simulates fetching all news posts',
            response_description='The list of posted news'
            )
def posts(db: Session = Depends(get_db)):
    return db_post.get_all(db)


@router.post('/image',
             summary='Upload an image',
             response_description='Path to uploaded file'
             )
def upload_file(image: UploadFile = File(...),
                current_user: UserAuth = Depends(get_current_user)):
    """

    This app performs uploading file for future posts.
    Authentication is required.

    Random string of 6 characters is added to filename to prevent overwriting.

    Returns the path to file required for posting news with that image.

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
            summary='Delete the post',
            description='Authenticated user can delete post if user created it',
            response_description='"Ok" or HTTP exception'
            )
def delete(id: int, db: Session = Depends(get_db),
           current_user: UserAuth = Depends(get_current_user)
           ):
    return db_post.delete(db, id, current_user.id)
