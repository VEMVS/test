from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Заголовок")
    content: str = Field(..., min_length=1, description="Текст")

    model_config = {"from_attributes": True}

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    pass 

class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserLogin(UserBase):
    pass

