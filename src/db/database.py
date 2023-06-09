from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import config

SQLALCHEMY_DATABASE_URL = config.get_settings().SQLALCHEMY_DATABASE_URL
# SQLALCHEMY_DATABASE_URL: str = 'sqlite:///sqlite/news_api.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    """Generates database session

    Session allows caller to user it for operations with database.
    After operations session closes.

    Yields:
    - database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
