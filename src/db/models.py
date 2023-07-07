from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from src.db.database import Base


class DbUser(Base):
    """Table for users"""

    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    avatar_url = Column(String)
    posts = relationship("DbPost", back_populates="user")


class DbPost(Base):
    """Table for posts"""

    __tablename__ = "post"
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    caption = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("DbUser", back_populates="posts")
    comments = relationship("DbComment", back_populates="post")


class DbComment(Base):
    """Table for comments"""

    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    username = Column(String)
    timestamp = Column(DateTime)
    post_id = Column(Integer, ForeignKey("post.id"))
    post = relationship("DbPost", back_populates="comments")
