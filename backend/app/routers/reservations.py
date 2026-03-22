from __future__ import annotations

from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db
from app.security import get_current_user

router = APIRouter(prefix="/reservations", tags=["reservations"])


def _is_valid_30_min_boundary(value: datetime) -> bool:
    return value.minute in (0, 30) and value.second == 0 and value.microsecond == 0


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
    return [schemas.ReservationResponse.model_validate(r) for r in reservations]


@router.get("/{reservation_id}", response_model=schemas.ReservationResponse)
def get_reservation_by_id(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> schemas.ReservationResponse:
    reservation = (
        db.query(models.Reservation)
        .filter(models.Reservation.id == reservation_id)
        .first()
    )

    if reservation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found",
        )

    if reservation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    return schemas.ReservationResponse.model_validate(reservation)


@router.delete("/{reservation_id}", response_model=schemas.ReservationResponse, status_code=status.HTTP_200_OK)
def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> schemas.ReservationResponse:
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if reservation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")

    if reservation.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    if reservation.status != models.RESERVATION_STATUS_CANCELED:
        reservation.status = models.RESERVATION_STATUS_CANCELED
        db.commit()
        db.refresh(reservation)

    return schemas.ReservationResponse.model_validate(reservation)


@router.post("", response_model=schemas.ReservationResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(
    payload: schemas.ReservationCreateRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> schemas.ReservationResponse:
    now_utc = datetime.now(timezone.utc)

    if payload.start_time < now_utc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_time must be in the future",
        )

    if not _is_valid_30_min_boundary(payload.start_time) or not _is_valid_30_min_boundary(payload.end_time):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_time and end_time must align to 30-minute boundaries",
        )

    if payload.start_time >= payload.end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_time must be earlier than end_time",
        )

    facility = db.query(models.Facility).filter(models.Facility.id == payload.facility_id).first()
    if not facility:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Facility not found",
        )

    overlapping = (
        db.query(models.Reservation)
        .filter(models.Reservation.facility_id == payload.facility_id)
        .filter(models.Reservation.status == models.RESERVATION_STATUS_ACTIVE)
        .filter(models.Reservation.start_time < payload.end_time)
        .filter(models.Reservation.end_time > payload.start_time)
        .first()
    )
    if overlapping:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Time slot is already booked for this facility",
        )

    reservation = models.Reservation(
        user_id=current_user.id,
        facility_id=payload.facility_id,
        start_time=payload.start_time,
        end_time=payload.end_time,
        status=models.RESERVATION_STATUS_ACTIVE,
    )

    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    return schemas.ReservationResponse.model_validate(reservation)