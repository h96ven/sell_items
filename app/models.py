from sqlalchemy import Boolean, Column, Integer, String
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
    # updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    # "author": {
    # "id": 1,
    # "email": ""
    # }
