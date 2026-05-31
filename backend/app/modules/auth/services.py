from typing import Optional
from app.core.exceptions import NotFoundException, BadRequestException, UnauthorizedException
from app.modules.auth.schemas import (
    SendCodeRequest,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    AuthUserResponse,
)
from app.modules.auth.repositories import AuthRepository
from app.core.security import create_access_token, create_refresh_token

class AuthService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    def send_verification_code(self, phone_number: str) -> dict:
        """
        Sends a verification code to the given phone number.
        (Sprint 2: placeholder implementation)
        """
        # TODO: generate random code and send SMS
        verification_code = "123456"

        self.auth_repository.store_verification_code(
            phone_number=phone_number,
            code=verification_code
        )

        return {
            "message": "Verification code sent successfully."
        }

    def register(self, data: RegisterRequest) -> dict:
        existing_user = self.auth_repository.get_user_by_phone(data.phone_number)
        if existing_user:
            raise BadRequestException("A user with this phone number already exists.")

        existing_username = self.auth_repository.get_user_by_username(data.username)
        if existing_username:
            raise BadRequestException("This username is already taken.")

        is_valid_code = self.auth_repository.verify_code(
            phone_number=data.phone_number,
            code=data.verification_code
        )
        if not is_valid_code:
            raise UnauthorizedException("Invalid verification code.")

        new_user = self.auth_repository.create_user(
            first_name=data.first_name,
            last_name=data.last_name,
            username=data.username,
            phone_number=data.phone_number,
            email=data.email,
        )

        access_token = create_access_token({"sub": str(new_user.id)})
        refresh_token = create_refresh_token({"sub": str(new_user.id)})

        return {
            "user": AuthUserResponse.from_orm(new_user),
            "tokens": TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer"
            )
        }

    def login(self, data: LoginRequest) -> dict:
        user = self.auth_repository.get_user_by_phone(data.phone_number)
        if not user:
            raise NotFoundException("User not found!")

        is_valid_code = self.auth_repository.verify_code(
            phone_number=data.phone_number,
            code=data.verification_code
        )
        if not is_valid_code:
            raise UnauthorizedException("Invalid verification code.")

        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})

        return {
            "user": AuthUserResponse.from_orm(user),
            "tokens": TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer"
            )
        }