from fastapi import APIRouter, Depends
from .schemas import OrderCreate, OrderUpdate, OrderResponse
from .services import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post("/", response_model=OrderResponse)
def create_order(payload: OrderCreate, service: OrderService = Depends()):
    return service.create(payload)

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, service: OrderService = Depends()):
    return service.get(order_id)

@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, payload: OrderUpdate, service: OrderService = Depends()):
    return service.update(order_id, payload)