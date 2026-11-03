"""
Database connection and setup
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# TODO: If you change here then also change same in alembic.ini -> sqlalchemy.url
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/fastapi_news_processing"

# Create Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#  Create a Session Local class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Instantiate database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
