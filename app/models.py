# models.py
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, func,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from starlette.authentication import BaseUser

from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    published: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id" , ondelete="CASCADE") , nullable=False)
    owner = relationship("User")
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True , nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
class Vote(Base):
    __tablename__ = "votes"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id" ,ondelete="CASCADE"),primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id" ,ondelete="CASCADE"),primary_key=True)