from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, default="...", nullable=False)
    price = Column(Integer)
    is_active = Column(Boolean, server_default="TRUE")
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        onupdate=func.now(),
    )
    # "author": {
    # "id": 1,
    # "email": ""
    # }


class Author(Base):
    __tablename__ = "authors"
