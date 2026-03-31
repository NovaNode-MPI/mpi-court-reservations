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
            "description": "Not authenticated",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authenticated"
                    }
                }
            },
        },
    },
)
def me(current_user: models.User = Depends(get_current_user)) -> schemas.UserResponse:
    return schemas.UserResponse.model_validate(current_user)