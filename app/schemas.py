from pydantic import BaseModel

# from sqlalchemy.sql.sqltypes import TIMESTAMP


class PostBase(BaseModel):
    title: str
    description: str
    price: int
    is_active: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(BaseModel):
    id: int
    title: str
    description: str
    price: int
    # is_active: bool
    # created_at: TIMESTAMP

    class Config:
        orm_mode = True
