from pydantic import EmailStr
from sqlmodel import SQLModel
from typing import Optional

class UserBase(SQLModel):
    email: EmailStr
    username: str
    is_active: bool = True
    is_superuser: bool = False

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

class UserInDB(UserRead):
    hashed_password: str 