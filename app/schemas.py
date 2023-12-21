from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    first_name: str
    last_name: str
    age: int
    password: str
    keycloak_id: Optional[str]

class UserUpdate(UserBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None

class UserInDBBase(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Login():
    username: str
    password: str

class User(UserInDBBase):
    first_name: str
    last_name: str
    age: int

class UserInDB(UserInDBBase):
    hashed_password: str  # Only for internal use
