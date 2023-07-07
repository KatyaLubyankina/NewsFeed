import datetime
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from src.db.models import DbPost
from src.routers.schemas import PostBase


def create_post(db: Session, request: PostBase) -> DbPost:
    """Creates new post

    Information about post adds to DbPost table and
    database generates id and timestamp for each post.

    Args:
    - db (Session): database session
    - request (PostBase): image_url, caption and creator_id

    Returns:
    - DbPost: id, image_url, caption, timestamp, user_id
    """
    new_post = DbPost(
        image_url=request.image_url,
        caption=request.caption,
        timestamp=datetime.datetime.now(),
        user_id=request.creator_id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_all_posts(db: Session) -> List[DbPost]:
    """Gets all posts

    Args:
    - db (Session): database session

    Returns:
    - Information about all posts from DbPost table
    """
    return db.query(DbPost).all()


def delete_post(db: Session, id: int, user_id: int) -> str:
    """Delete post

    Authenticated user can delete post if user created it.

    Args:
    - db (Session): database session
    - id (int): post id
    - user_id (int): user id

    Raises:
    - HTTPException(404): if no post with with id in database
    - HTTPException(403): if user did not created this post

    Returns:
        "ok"
    """
    post = db.query(DbPost).filter(DbPost.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

    if post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only post creator can delete post",
        )

    db.delete(post)
    db.commit()
    return "ok"
