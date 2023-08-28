from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from src.auth.oauth2 import create_access_token
from src.db.database import get_db
from src.db.hashing import Hash
from src.db.models import DbUser
from src.logging import logger_wraps

router = APIRouter(tags=["authentication"])


@router.post("/login")
@logger_wraps()
def login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> dict:
    """Endpoint for login.

    Validates credentials and returns
    access_token, token_type, user_id and username if credentials are valid.

    Args:
    - request (OAuth2PasswordRequestForm): automatic form request
    - db (Session): database session

    Raises:
    - HTTPException("Invalid credentials"): if no user with this username in database
    - HTTPException("Incorrect password"): if password is wrong

    Returns:
    - Dictionary with access_token, token_type, user_id and username
    """
    user = db.query(DbUser).filter(DbUser.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )
    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password"
        )
    access_token = create_access_token(data={"username": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
    }
