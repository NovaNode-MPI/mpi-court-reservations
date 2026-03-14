from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.db import get_db
from app.security import get_current_user
from app import models, schemas

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

    # idempotent behavior: if already canceled, return it as-is (still 200)
    if reservation.status != "canceled":
        reservation.status = "canceled"
        db.commit()
        db.refresh(reservation)

    return schemas.ReservationResponse.model_validate(reservation)