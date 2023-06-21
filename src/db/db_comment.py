from sqlalchemy.orm import Session
from src.db.models import DbComment
from src.routers.schemas import CommentBase
from datetime import datetime


def create(db: Session, request: CommentBase):

    new_comment = DbComment(
        text=request.text,
        username=request.username,
        post_id=request.post_id,
        timestamp=datetime.now()
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def get_all(db: Session, post_id: int):
    """
    Function returs all comments for provided post_id from database.

    """
    return db.query(DbComment).filter(DbComment.post_id == post_id).all()
