from fastapi import HTTPException, status
from routers.schemas import UserBase, AvatarBase
from sqlalchemy.orm.session import Session
from .models import DbUser
from db.hashing import Hash


def create_user(db: Session, request: UserBase):
    new_user = DbUser(  # id is generated for us by DB
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # refresh info about user (add id)
    return new_user


def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with username {username} not found')
    return user


def update_avatar(db: Session, user_id: int, request: AvatarBase):
    values_dict = {'avatar_url': request.avatar_url,
                   'avatar_url_type': request.avatar_url_type}
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    for key, value in values_dict.items():
        setattr(user, key, value)
    db.commit()
    return 'ok'
