from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, func, Numeric
from sqlalchemy.orm import relationship
from .db import Base

RESERVATION_STATUS_ACTIVE = "active"
RESERVATION_STATUS_CANCELED = "canceled"
RESERVATION_ALLOWED_STATUSES = (
    RESERVATION_STATUS_ACTIVE,
    RESERVATION_STATUS_CANCELED,
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    reservations = relationship("Reservation", back_populates="user")


class Facility(Base):
    __tablename__ = "facilities"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False)
    location = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    image_url = Column(String(500), nullable=True)
    reservations = relationship("Reservation", back_populates="facility")
    prices = relationship(
        "FacilityPrice",
        back_populates="facility",
        cascade="all, delete-orphan"
    )

class FacilityPrice(Base):
    __tablename__ = "facility_prices"

    id = Column(Integer, primary_key=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False)
    duration = Column(String(50), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    facility = relationship("Facility", back_populates="prices")
class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(50), nullable=False, default=RESERVATION_STATUS_ACTIVE)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="reservations")
    facility = relationship("Facility", back_populates="reservations")


Index("ix_reservations_facility_start_end", Reservation.facility_id, Reservation.start_time, Reservation.end_time)