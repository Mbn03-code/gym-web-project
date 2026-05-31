from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.base_model import BaseModelMixin
from app.core.enums import ReservationStatus

class Reservation(Base, BaseModelMixin):
    __tablename__ = "reservations"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    cafe_id = Column(Integer, ForeignKey("cafes.id"), nullable=False)

    reservation_time = Column(DateTime, nullable=False)
    people_count = Column(Integer, nullable=False)

    status = Column(Enum(ReservationStatus), default=ReservationStatus.PENDING, nullable=False)
    note = Column(Text, nullable=True)

    user = relationship("User", back_populates="reservations")
    cafe = relationship("Cafe", back_populates="reservations")