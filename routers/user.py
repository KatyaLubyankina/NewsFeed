from fastapi import APIRouter, Depends, UploadFile, File
from .schemas import UserDisplay, UserBase, UserAuth, AvatarBase
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_user
import string
import random
import shutil
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post('',
             response_model=UserDisplay,
             summary='Create a user',
             description='This app simulates creating a new user')
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


@router.post('/avatar',
             summary='Upload an avatar',
             response_description='Returns the path to the uploaded avatar'
             )
def upload_avatar(image: UploadFile = File(...),
                  current_user: UserAuth = Depends(get_current_user)):
    """

    This app performs uploading avatar for user.
    Authentication is required.

    Random string of 6 characters is added to filename to prevent overwriting.

    Returns the path to file required for updating user avatar.

    """
    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'avatars/{filename}'

    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'filename': path}


@router.post('/avatar/{id}',
             summary='Update user avatar',
             description='This app sumilates updating user avatar')
def update_avatar(request: AvatarBase,
                  db: Session = Depends(get_db),
                  current_user: UserAuth = Depends(get_current_user)):
    return db_user.update_avatar(db, current_user.id, request)
