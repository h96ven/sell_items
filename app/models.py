from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
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
        server_default=func.now(),
        onupdate=func.now(),
    )
    author = Column(
        Integer, ForeignKey("authors.id", ondelete="CASCADE"), nullable=False
    )


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, nullable=False)
    comment = Column(String, nullable=False)
    # author
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
