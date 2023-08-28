from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import config
from src.db import db_user
from src.db.database import get_db
from src.db.models import DbUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = config.get_settings().SECRET_KEY.get_secret_value()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Generates encoded JSON Web Token(JWT) for authentication.

    If expires_delta is provided, token will be available for expires_delta.
    Otherwise expires_delta = 15 minutes.

    Args:
    - data (dict): dictionary with user info ({"username": username})
    - expires_delta (Optional[timedelta]): expiration time for token

    Returns:
    - String with encoded JSON Web Token(JWT)
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> DbUser:
    """Decodes token and validates current user.

    Args:
    - token (str, optional): encoded JSON Web Token
    - db (Session, optional): database session

    Raises:
    - credentials_exception: if no username in JWT or no user
    with username from JWT in database

    Returns:
    - DbUser - id, username, email, password, avatar_url and posts
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db_user.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user
