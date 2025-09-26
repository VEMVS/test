from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal, Dict
from enum import Enum

class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Заголовок")
    content: str = Field(..., min_length=1, description="Текст")

    model_config = {"from_attributes": True}

class NoteCreate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: int

class NoteUpdate(BaseModel):
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

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Scope(str, Enum):
    read = "notes:read"
    edit = "notes:edit"

class Link(BaseModel):
    note_id: int
    scope: Scope



