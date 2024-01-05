from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional



class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True



class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None



class OrderSchema(BaseModel):
    stock: str
    price: float
    quantity: int
    order_type: str
    order_format: str