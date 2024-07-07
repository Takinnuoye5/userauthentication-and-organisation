from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str
    phone: Optional[str] = Field(None, description="Phone number of the user")

class User(BaseModel):
    userId: str
    firstName: str
    lastName: str
    email: EmailStr
    phone: Optional[str] = Field(None, description="Phone number of the user")

    class Config:
        from_attributes = True  # Updated to use from_attributes instead of orm_mode

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    status: str
    message: str
    access_token: str
    token_type: str
    user: User

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class TokenData(BaseModel):
    email: Optional[str] = None

class UserResponse(BaseModel):
    status: str
    message: str
    data: User
