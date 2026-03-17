from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db

router = APIRouter(prefix="/facilities", tags=["facilities"])


@router.get("", response_model=list[schemas.FacilityResponse])
def list_facilities(db: Session = Depends(get_db)) -> list[schemas.FacilityResponse]:
    facilities = db.query(models.Facility).order_by(models.Facility.id.asc()).all()
    return [schemas.FacilityResponse.model_validate(f) for f in facilities]


@router.get("/{facility_id}", response_model=schemas.FacilityResponse)
def get_facility_by_id(
    facility_id: int,
    db: Session = Depends(get_db),
) -> schemas.FacilityResponse:
    facility = db.query(models.Facility).filter(models.Facility.id == facility_id).first()

    if facility is None:
        raise HTTPException(status_code=404, detail="Facility not found")

    return schemas.FacilityResponse.model_validate(facility)