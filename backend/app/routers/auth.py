from __future__ import annotations

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db
from app.security import create_access_token, hash_password, verify_password

COMMON_AUTH_ERROR_RESPONSES = {
    422: {
        "model": schemas.ErrorResponse,
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": {
                    "error_code": "validation_error",
                    "message": "Request validation failed",
                    "details": [
                        {
                            "loc": ["body", "email"],
                            "msg": "value is not a valid email address",
                            "type": "value_error",
                        }
                    ],
                }
            }
        },
    },
    500: {
        "model": schemas.ErrorResponse,
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "example": {
                    "error_code": "internal_server_error",
                    "message": "Internal server error",
                    "details": None,
                }
            }
        },
    },
}

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "User registered successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "email": "alex@example.com",
                        "created_at": "2026-03-31T12:00:00Z",
                    }
                }
            },
        },
        409: {
            "model": schemas.ErrorResponse,
            "description": "Email already registered",
            "content": {
                "application/json": {
                    "example": {
                        "error_code": "conflict",
                        "message": "Email already registered",
                        "details": None,
                    }
                }
            },
        },
        **COMMON_AUTH_ERROR_RESPONSES,
    },
)
def register(
    payload: schemas.RegisterRequest = Body(
        ...,
        examples={
            "default": {
                "summary": "Register request",
                "value": {
                    "email": "alex@example.com",
                    "password": "password123",
                },
            }
        },
    ),
    db: Session = Depends(get_db),
) -> schemas.UserResponse:
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = models.User(email=payload.email, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    return schemas.UserResponse.model_validate(user)


@router.post(
    "/login",
    response_model=schemas.TokenResponse,
    responses={
        200: {
            "description": "Login successful",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.example",
                        "token_type": "bearer",
                    }
                }
            },
        },
        401: {
            "model": schemas.ErrorResponse,
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "example": {
                        "error_code": "unauthorized",
                        "message": "Invalid credentials",
                        "details": None,
                    }
                }
            },
        },
        **COMMON_AUTH_ERROR_RESPONSES,
    },
)
def login(
    payload: schemas.LoginRequest = Body(
        ...,
        examples={
            "default": {
                "summary": "Login request",
                "value": {
                    "email": "alex@example.com",
                    "password": "password123",
                },
            }
        },
    ),
    db: Session = Depends(get_db),
) -> schemas.TokenResponse:
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_access_token(subject=str(user.id))
    return schemas.TokenResponse(access_token=token)