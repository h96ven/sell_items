import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.database import Base


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, dafault="...", nullable=False)
    price = Column(Integer)
    is_active = Column(Boolean, dafault=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    # "author": {
    # "id": 1,
    # "email": ""
    # }
