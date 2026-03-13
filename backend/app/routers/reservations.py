from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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