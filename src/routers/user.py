from fastapi import APIRouter, Depends
from src.routers.schemas import UserDisplay, UserBase, UserAuth
from sqlalchemy.orm.session import Session
from src.db.database import get_db
from src.db import db_user
from src.auth.oauth2 import get_current_user
from src.db.models import DbUser

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post('',
             response_model=UserDisplay,
             summary='Create a user')
def create_user(
    request: UserBase,
    db: Session = Depends(get_db)
) -> DbUser:
    """Creates new user

    Calls src.db_user.create_user function

    Args:
    - request (UserBase): username, email and password required, avatar_url is optional
    - db (Session): database session

    Returns:
    - json with username and email
    """
    return db_user.create_user(db, request)


@router.post('/avatar/{id}',
             summary='Update user avatar'
             )
def update_avatar(avatar_url: str,
                  db: Session = Depends(get_db),
                  current_user: UserAuth = Depends(get_current_user)) -> str:
    """Updates user avatar

    Calls src.db_user.create_user function

    Args:
    - avatar_url: url of uploaded image by src.post.upload_file function
    - db (Session): database session
    - current_user (UserAuth): info about current user from database

    Returns:
    - 'ok'
    """
    return db_user.update_avatar(db, current_user.id, avatar_url)
