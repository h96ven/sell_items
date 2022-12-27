from datetime import datetime

from pydantic import BaseModel, EmailStr


class AuthorCreate(BaseModel):
    email: EmailStr
    password: str
    created_at: datetime = datetime.now()


class AuthorOutResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    description: str
    price: int
    is_active: bool = True
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    # author: AuthorOutResponse


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    author: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str | None = None


class ReviewCreate(BaseModel):
    comment: str
    # author: int
    created_at: datetime = datetime.now()


class ReviewResponse(BaseModel):
    comment: str
    # author: int
    created_at: datetime
