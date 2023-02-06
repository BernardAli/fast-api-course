from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    # rating: Optional[int] = 4


class CreatePost(PostBase):
    pass


class UpdatePost(PostBase):
    pass


class PostResponse(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    created_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True
