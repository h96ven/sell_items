from datetime import datetime

from pydantic import BaseModel, EmailStr


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


class AuthorCreate(BaseModel):
    email: EmailStr
    password: str


class AuthorOutResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime = datetime.now()

    class Config:
        orm_mode = True
