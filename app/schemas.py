from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    description: str
    price: int
    is_active: bool = True


class PostCreate(PostBase):
    pass
