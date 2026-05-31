from fastapi import APIRouter, Depends
from .schemas import LoginRequest, RegisterRequest
from .services import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register")
def register_user(payload: RegisterRequest, service: AuthService = Depends()):
    return service.register(payload)

@router.post("/login")
def login_user(payload: LoginRequest, service: AuthService = Depends()):
    return service.login(payload)