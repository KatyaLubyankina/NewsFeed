from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from routers.schemas import PostDisplay, UserAuth
from db.database import get_db
from db import db_post
from typing import List
import random
import string
import shutil
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/post',
    tags=['post']
)
# we accept only these types of image_url_type
image_url_types = ['absolute', 'relative']


@router.get('/all', response_model=List[PostDisplay])
def posts(db: Session = Depends(get_db)):
    return db_post.get_all(db)


@router.post('/image')
def upload_file(image: UploadFile = File(...),
                current_user: UserAuth = Depends(get_current_user)):
    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'

    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'filename': path}


@router.get('/delete/{id}')
def delete(id: int, db: Session = Depends(get_db),
           current_user: UserAuth = Depends(get_current_user)):
    return db_post.delete(db, id, current_user.id)
