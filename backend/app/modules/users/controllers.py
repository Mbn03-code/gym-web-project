from fastapi import APIRouter, Depends
from .schemas import UserUpdate, UserResponse
from .services import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, service: UserService = Depends()):
    return service.get_user(user_id)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, payload: UserUpdate, service: UserService = Depends()):
    return service.update_user(user_id, payload)