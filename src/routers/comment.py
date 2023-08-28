from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.auth.oauth2 import get_current_user
from src.db import db_comment
from src.db.database import get_db
from src.logging import logger_wraps
from src.routers.schemas import CommentBase, UserAuth

router = APIRouter(prefix="/comment", tags=["comment"])


@router.get("/all/{post_id}", summary="Retrieve all comments for the post")
@logger_wraps()
def comments(post_id: int, db: Session = Depends(get_db)):
    """Retrieves all comments for the post.

    Args:
    - post_id (int): post id
    - db (Session): database session

    Returns:
    - List of comments (DbComment)
    """
    return db_comment.get_all_comments(db, post_id)


@router.post("", summary="Create a comment")
@logger_wraps()
def create(
    request: CommentBase,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user)
):
    """Endpoint for new comment creation.

    Args:
    - request (CommentBase): username, text and post_id
    - db (Session, optional): database session
    - current_user (UserAuth): current DbUser

    Returns:
    - DbComment: id, text, username, timestamp, post_id
    """
    return db_comment.create_comment(db, request)
