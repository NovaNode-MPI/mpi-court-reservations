from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db

router = APIRouter(prefix="/facilities", tags=["facilities"])

@router.get("", response_model=list[schemas.FacilityResponse])
def list_facilities(db: Session = Depends(get_db)) -> list[schemas.FacilityResponse]:
    facilities = db.query(models.Facility).order_by(models.Facility.id.asc()).all()
    return [schemas.FacilityResponse.model_validate(f) for f in facilities]