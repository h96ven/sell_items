from datetime import datetime

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    description: str
    price: int
    is_active: bool = True
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int

    class Config:
        orm_mode = True
