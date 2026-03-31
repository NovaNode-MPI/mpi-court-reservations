from __future__ import annotations

from fastapi import APIRouter, Depends

from app import schemas, models
from app.security import get_current_user

router = APIRouter(prefix="/me", tags=["me"])


@router.get(
    "",
    response_model=schemas.UserResponse,
    responses={
        200: {
            "description": "Current authenticated user",
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
        401: {
            "model": schemas.ErrorResponse,
            "description": "Not authenticated",
            "content": {
                "application/json": {
                    "example": {
                        "error_code": "unauthorized",
                        "message": "Not authenticated",
                        "details": None,
                    }
                }
            },
        },
        422: {
            "model": schemas.ErrorResponse,
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "error_code": "validation_error",
                        "message": "Request validation failed",
                        "details": [],
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
    },
)
def me(current_user: models.User = Depends(get_current_user)) -> schemas.UserResponse:
    return schemas.UserResponse.model_validate(current_user)