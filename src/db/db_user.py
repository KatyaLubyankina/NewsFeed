from fastapi import HTTPException, status
from src.routers.schemas import UserBase
from sqlalchemy.orm.session import Session
from src.db.models import DbUser
from src.db.hashing import Hash


def create_user(db: Session, request: UserBase) -> DbUser:
    """Creates new user

    This function creates a new user in database using requested info.
    Passoword is hashed before adding to the DB.

    Args:
    - db (Session): database session
    - request (UserBase): username, email, password are required, avatar_url is optional

    Returns:
    DbUser: id, username, email, password, posts
    """
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_username(db: Session, username: str) -> DbUser:
    """Returns DbUser with provided username

    Args:
    - db (Session): database sesion
    - username (str): username

    Raises:
    - HTTPException (404): if no user with provided username in database

    Returns:
    - DbUser: id, username, email, password, posts
    """
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with username {username} not found')
    return user


def update_avatar(db: Session, user_id: int, avatar_url: str):
    """
    Function updates avatar for authorized user.
    Avatar must be previously uploaded via GET /post/image

    """
    values_dict = {'avatar_url': avatar_url}
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    for key, value in values_dict.items():
        setattr(user, key, value)
    db.commit()
    return 'ok'
