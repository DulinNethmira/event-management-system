from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    email: EmailStr
    # phone_number: str | None = None
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None

class UserRead(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
