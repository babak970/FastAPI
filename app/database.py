from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
import psycopg
import time
from psycopg.rows import dict_row
from .config import settings
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg://{settings.database_username}:"
    f"{settings.database_password}@{settings.database_hostname}:"
    f"{settings.database_port}/{settings.database_name}"
)
"postgresql+psycopg://postgres:123@localhost:5433/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()