from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, func
from sqlalchemy.orm import relationship
from .db import Base

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
    reservations = relationship("Reservation", back_populates="facility")

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(50), nullable=False, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="reservations")
    facility = relationship("Facility", back_populates="reservations")

Index("ix_reservations_facility_start_end", Reservation.facility_id, Reservation.start_time, Reservation.end_time)