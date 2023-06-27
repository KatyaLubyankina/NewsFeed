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
             summary='Create a user')
def create_user(
    request: UserBase,
    db: Session = Depends(get_db)
):
    """Creates new user

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
def update_avatar(request: AvatarBase,
                  db: Session = Depends(get_db),
                  current_user: UserAuth = Depends(get_current_user)):
    """Update user avatar

    Args:
        request (AvatarBase): 
        db (Session, optional): _description_. Defaults to Depends(get_db).
        current_user (UserAuth, optional): _description_. Defaults to Depends(get_current_user).

    Returns:
        _type_: _description_
    """
    return db_user.update_avatar(db, current_user.id, request)
