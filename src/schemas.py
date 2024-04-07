from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class ContactModel(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    phone_number: str
    birthday: date
    email: EmailStr
    additional_data: str


class ResponseContact(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    phone_number: str
    birthday: date
    email: EmailStr
    additional_data: Optional[str]

    class Config:
        or_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"