from datetime import datetime, timedelta
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.reservations.models import Reservation
from app.core.enums import ReservationStatus

class ReservationRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create(self, user_id: int, **data):
        reservation = Reservation(
            user_id=user_id,
            **data,
        )

        self.db.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)

        return reservation

    def get_by_id(self, reservation_id: int):
        return (
            self.db.query(Reservation)
            .filter(
                Reservation.id == reservation_id,
                Reservation.deleted_at.is_(None),
            )
            .first()
        )

    def get_by_user_id(self, user_id: int):
        return (
            self.db.query(Reservation)
            .filter(
                Reservation.user_id == user_id,
                Reservation.deleted_at.is_(None),
            )
            .order_by(Reservation.reservation_time.desc())
            .all()
        )

    def get_by_cafe_id(self, cafe_id: int):
        return (
            self.db.query(Reservation)
            .filter(
                Reservation.cafe_id == cafe_id,
                Reservation.deleted_at.is_(None),
            )
            .order_by(Reservation.reservation_time.desc())
            .all()
        )

    def get_active_by_cafe_id(self, cafe_id: int):
        return (
            self.db.query(Reservation)
            .filter(
                Reservation.cafe_id == cafe_id,
                Reservation.deleted_at.is_(None),
                Reservation.status.in_([
                    ReservationStatus.PENDING,
                    ReservationStatus.CONFIRMED,
                ]),
            )
            .order_by(Reservation.reservation_time.asc())
            .all()
        )

    def has_duplicate_reservation(
        self,
        user_id: int,
        cafe_id: int,
        reservation_time: datetime,
        minutes_range: int = 60,
    ) -> bool:
        start_time = reservation_time - timedelta(minutes=minutes_range)
        end_time = reservation_time + timedelta(minutes=minutes_range)

        existing_reservation = (
            self.db.query(Reservation)
            .filter(
                Reservation.user_id == user_id,
                Reservation.cafe_id == cafe_id,
                Reservation.deleted_at.is_(None),
                Reservation.status.in_([
                    ReservationStatus.PENDING,
                    ReservationStatus.CONFIRMED,
                ]),
                Reservation.reservation_time.between(start_time, end_time),
            )
            .first()
        )

        return existing_reservation is not None

    def update(self, reservation, data: dict):
        for key, value in data.items():
            setattr(reservation, key, value)

        self.db.commit()
        self.db.refresh(reservation)

        return reservation

    def delete(self, reservation):
        reservation.deleted_at = datetime.utcnow()

        self.db.commit()
        return reservation