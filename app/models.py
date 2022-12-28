from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.database import Base


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, default="...", nullable=False)
    price = Column(Integer)
    is_active = Column(Boolean, server_default="TRUE")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=func.now(),
    )
    author_id = Column(
        Integer, ForeignKey("authors.id", ondelete="CASCADE"), nullable=False
    )

    author = relationship("Author")


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
    author = Column(
        Integer, ForeignKey("authors.id", ondelete="CASCADE"), nullable=False
    )
    post = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
