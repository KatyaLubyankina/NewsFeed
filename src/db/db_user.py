from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from src.db.hashing import Hash
from src.db.models import DbUser
from src.routers.schemas import UserBase


def create_user(db: Session, request: UserBase) -> DbUser:
    """Creates new user.

    This function creates a new user in database using requested info.
    Password is hashed before adding to the DB.

    Args:
    - db (Session): database session
    - request (UserBase): username, email, password are required, avatar_url is optional

    Returns:
    DbUser: id, username, email, password, posts
    """
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_username(db: Session, username: str) -> DbUser:
    """Returns DbUser with provided username.

    Args:
    - db (Session): database session
    - username (str): username

    Raises:
    - HTTPException (404): if no user with provided username in database

    Returns:
    - DbUser: id, username, email, password, posts
    """
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username {username} not found",
        )
    return user
