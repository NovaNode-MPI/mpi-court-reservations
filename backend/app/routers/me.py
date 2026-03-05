from __future__ import annotations

from fastapi import APIRouter, Depends

from app import schemas, models
from app.security import get_current_user

router = APIRouter(prefix="/me", tags=["me"])


@router.get("", response_model=schemas.UserResponse)
def me(current_user: models.User = Depends(get_current_user)) -> schemas.UserResponse:
    return schemas.UserResponse.model_validate(current_user)