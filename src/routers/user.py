from fastapi import APIRouter, Depends
from src.routers.schemas import UserDisplay, UserBase, UserAuth, AvatarBase
from sqlalchemy.orm.session import Session
from src.db.database import get_db
from src.db import db_user
from src.auth.oauth2 import get_current_user

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


@router.put('/avatar/{id}',
            summary='Update user avatar',
            description='This app sumilates updating user avatar')
def update_avatar(request: AvatarBase,
                  db: Session = Depends(get_db),
                  current_user: UserAuth = Depends(get_current_user)):
    return db_user.update_avatar(db, current_user.id, request)
