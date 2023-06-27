from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.db import db_comment
from src.routers.schemas import CommentBase, UserAuth
from src.auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/comment',
    tags=['comment']
)


@router.get('/all/{post_id}',
            summary='Retrive all comments for the post',
            description='This app simulates fetching all comments on the post',
            response_description='The list of comments'
            )
def comments(post_id: int, db: Session = Depends(get_db)):
    """Retrives all comments for the post

    Args:
        post_id (int): post id
        db (Session): database session

    Returns:
        List of comments 
    """
    return db_comment.get_all(db, post_id)


@router.post('',
             summary='Create a comment',
             description='This app simulates posting a comment on the post',
             response_description='Timestamp, text, id, username and post id'
             )
def create(request: CommentBase, db: Session = Depends(get_db),
           current_user: UserAuth = Depends(get_current_user)):
    return db_comment.create(db, request)
