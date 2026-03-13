from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field



class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class ReservationResponse(BaseModel):
    id: int
    facility_id: int
    start_time: datetime
    end_time: datetime
    status: str

    class Config:
        from_attributes = True