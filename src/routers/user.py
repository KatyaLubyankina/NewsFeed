from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.orm.session import Session

from src.db import db_user
from src.db.database import get_db
from src.db.models import DbUser
from src.routers.schemas import UserBase, UserDisplay

router = APIRouter(prefix="/user", tags=["user"])


@router.post("", response_model=UserDisplay, summary="Create a user")
@logger.catch()
def create_user(request: UserBase, db: Session = Depends(get_db)) -> DbUser:
    """Creates new user.

    Calls src.db_user.create_user function.

    Args:
    - request (UserBase): username, email and password required, avatar_url is optional
    - db (Session): database session

    Returns:
    - json with username and email
    """
    return db_user.create_user(db, request)
