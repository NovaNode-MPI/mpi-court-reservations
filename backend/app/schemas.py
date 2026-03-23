from __future__ import annotations

from datetime import datetime
from typing import Optional

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


class ReservationCreateRequest(BaseModel):
    facility_id: int = Field(gt=0)
    start_time: datetime
    end_time: datetime


class ReservationUpdateRequest(BaseModel):
    start_time: datetime
    end_time: datetime


class ReservationResponse(BaseModel):
    id: int
    user_id: int
    facility_id: int
    start_time: datetime
    end_time: datetime
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class FacilityResponse(BaseModel):
    id: int
    name: str
    type: str
    location: Optional[str] = None

    class Config:
        from_attributes = True