from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from src.db.models import DbComment
from src.routers.schemas import CommentBase


def create_comment(db: Session, request: CommentBase) -> DbComment:
    """Creates new comment for post.

    Args:
    - db (Session): database session
    - request (CommentBase): username, test and post_id

    Returns:
    - DbComment: id, text, username, timestamp, post_id
    """
    new_comment = DbComment(
        text=request.text,
        username=request.username,
        post_id=request.post_id,
        timestamp=datetime.now(),
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def get_all_comments(db: Session, post_id: int) -> List[DbComment]:
    """Gets all comments for post.

    Args:
        db (Session): database session
        post_id (int): id of post

    Returns:
        List[DbComment]: list of information about comments
    """
    return db.query(DbComment).filter(DbComment.post_id == post_id).all()
