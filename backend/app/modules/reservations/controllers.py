from fastapi import APIRouter, Depends
from .schemas import ReservationCreate, ReservationUpdate, ReservationResponse
from .services import ReservationService

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)

@router.post("/", response_model=ReservationResponse)
def create_reservation(payload: ReservationCreate, service: ReservationService = Depends()):
    return service.create(payload)

@router.get("/{reservation_id}", response_model=ReservationResponse)
def get_reservation(reservation_id: int, service: ReservationService = Depends()):
    return service.get(reservation_id)

@router.put("/{reservation_id}", response_model=ReservationResponse)
def update_reservation(reservation_id: int, payload: ReservationUpdate, service: ReservationService = Depends()):
    return service.update(reservation_id, payload)