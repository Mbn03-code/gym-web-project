from datetime import datetime
from typing import Any

from fastapi import Depends

from app.core.enums import ReservationStatus
from app.core.exceptions import BadRequestError, NotFoundError
from app.modules.cafes.repositories import CafeRepository
from app.modules.reservations.repositories import ReservationRepository


class ReservationService:
    def __init__(
        self,
        reservation_repository: ReservationRepository = Depends(),
        cafe_repository: CafeRepository = Depends(),
    ):
        self.reservation_repository = reservation_repository
        self.cafe_repository = cafe_repository

    def _to_dict(self, data: Any, exclude_unset: bool = True) -> dict:
        if isinstance(data, dict):
            return data

        if hasattr(data, "model_dump"):
            return data.model_dump(exclude_unset=exclude_unset)

        if hasattr(data, "dict"):
            return data.dict(exclude_unset=exclude_unset)

        return dict(data)

    def create_reservation(self, user_id: int, data: Any):
        reservation_data = self._to_dict(data)

        cafe_id = reservation_data.get("cafe_id")
        if not cafe_id:
            raise BadRequestError("Cafe id is required.")

        cafe = self.cafe_repository.get_by_id(cafe_id)
        if not cafe:
            raise NotFoundError("Cafe not found.")

        reservation_time = reservation_data.get("reservation_time")
        if not reservation_time:
            raise BadRequestError("Reservation time is required.")

        if isinstance(reservation_time, str):
            reservation_time = datetime.fromisoformat(reservation_time)
            reservation_data["reservation_time"] = reservation_time

        if reservation_time <= datetime.utcnow():
            raise BadRequestError("Reservation time must be in the future.")

        people_count = reservation_data.get("people_count")
        if not people_count or people_count <= 0:
            raise BadRequestError("People count must be greater than zero.")

        has_duplicate_reservation = self.reservation_repository.has_duplicate_reservation(
            user_id=user_id,
            cafe_id=cafe_id,
            reservation_time=reservation_time,
        )

        if has_duplicate_reservation:
            raise BadRequestError(
                "You already have an active reservation for this cafe near this time."
            )

        reservation_data["status"] = ReservationStatus.PENDING

        return self.reservation_repository.create(
            user_id=user_id,
            **reservation_data
        )

    def get_reservation_by_id(self, reservation_id: int):
        reservation = self.reservation_repository.get_by_id(reservation_id)

        if not reservation:
            raise NotFoundError("Reservation not found.")

        return reservation

    def get_user_reservations(self, user_id: int):
        return self.reservation_repository.get_by_user_id(user_id)

    def update_reservation(self, reservation_id: int, data: Any):
        reservation = self.get_reservation_by_id(reservation_id)
        update_data = self._to_dict(data)

        if reservation.status in [
            ReservationStatus.CANCELLED,
            ReservationStatus.COMPLETED,
        ]:
            raise BadRequestError("This reservation can no longer be updated.")

        if "reservation_time" in update_data:
            reservation_time = update_data["reservation_time"]

            if isinstance(reservation_time, str):
                reservation_time = datetime.fromisoformat(reservation_time)
                update_data["reservation_time"] = reservation_time

            if reservation_time <= datetime.utcnow():
                raise BadRequestError("Reservation time must be in the future.")

        if "people_count" in update_data:
            people_count = update_data["people_count"]

            if people_count <= 0:
                raise BadRequestError("People count must be greater than zero.")

        update_data.pop("status", None)

        return self.reservation_repository.update(
            reservation,
            update_data
        )

    def update_reservation_status(
        self,
        reservation_id: int,
        status: ReservationStatus,
    ):
        reservation = self.get_reservation_by_id(reservation_id)

        if isinstance(status, str):
            status = ReservationStatus(status)

        return self.reservation_repository.update(
            reservation,
            {"status": status}
        )

    def cancel_reservation(self, reservation_id: int):
        reservation = self.get_reservation_by_id(reservation_id)

        if reservation.status == ReservationStatus.COMPLETED:
            raise BadRequestError("Completed reservation cannot be cancelled.")

        if reservation.status == ReservationStatus.CANCELLED:
            raise BadRequestError("Reservation is already cancelled.")

        return self.reservation_repository.update(
            reservation,
            {"status": ReservationStatus.CANCELLED}
        )

    # Temporary wrappers for current controller naming
    def get(self, reservation_id: int):
        return self.get_reservation_by_id(reservation_id)

    def update(self, reservation_id: int, data: Any):
        return self.update_reservation(reservation_id, data)