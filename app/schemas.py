from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Заголовок")
    content: str = Field(..., min_length=1, description="Текст")

    model_config = {"from_attributes": True}

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int

class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)

    model_config = {"from_attributes": True}

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = {"from_attributes": True}

class UserOut(BaseModel):
    id: int
    email: EmailStr

    model_config = {"from_attributes": True}
