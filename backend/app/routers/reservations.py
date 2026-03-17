from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.security import get_current_user
from app import models, schemas
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db
from app.security import get_current_user  # trebuie să existe deja

router = APIRouter(prefix="/reservations", tags=["reservations"])


@router.get("", response_model=List[schemas.ReservationResponse])
def list_my_reservations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> List[schemas.ReservationResponse]:
    reservations = (
        db.query(models.Reservation)
        .filter(models.Reservation.user_id == current_user.id)
        .order_by(models.Reservation.start_time.asc())
        .all()
    )
    # dacă nu are rezervări -> [] (200 OK), automat
    return [schemas.ReservationResponse.model_validate(r) for r in reservations]
@router.post("", response_model=schemas.ReservationResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(
    payload: schemas.ReservationCreateRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> schemas.ReservationResponse:
    # 1) validate time window
    if payload.start_time >= payload.end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_time must be earlier than end_time",
        )

    # 2) ensure facility exists
    facility = db.query(models.Facility).filter(models.Facility.id == payload.facility_id).first()
    if not facility:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Facility not found",
        )

    # 3) overlap check:
    # overlap if existing.start < new.end AND existing.end > new.start
    overlapping = (
        db.query(models.Reservation)
        .filter(models.Reservation.facility_id == payload.facility_id)
        .filter(models.Reservation.status == "active")
        .filter(models.Reservation.start_time < payload.end_time)
        .filter(models.Reservation.end_time > payload.start_time)
        .first()
    )
    if overlapping:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Time slot is already booked for this facility",
        )

    # 4) create reservation (user_id from token, NOT from client)
    reservation = models.Reservation(
        user_id=current_user.id,
        facility_id=payload.facility_id,
        start_time=payload.start_time,
        end_time=payload.end_time,
        status="active",
    )

    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    return schemas.ReservationResponse.model_validate(reservation)
