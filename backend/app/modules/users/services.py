from app.core.exceptions import NotFoundException, BadRequestException
from app.modules.users.schemas import UserUpdate, UserResponse
from app.modules.users.repositories import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_current_user(self, user_id: int) -> UserResponse:
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise NotFoundException("User not found.")

        return UserResponse.from_orm(user)

    def update_user(self, user_id: int, data: UserUpdate) -> UserResponse:
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise NotFoundException("User not found.")

        update_data = data.dict(exclude_unset=True)

        if "username" in update_data:
            existing_user = self.user_repository.get_by_username(update_data["username"])
            if existing_user and existing_user.id != user_id:
                raise BadRequestException("This username is already taken.")

        if "phone_number" in update_data:
            existing_user = self.user_repository.get_by_phone(update_data["phone_number"])
            if existing_user and existing_user.id != user_id:
                raise BadRequestException("This phone number is already in use.")

        if "email" in update_data and update_data["email"] is not None:
            existing_user = self.user_repository.get_by_email(update_data["email"])
            if existing_user and existing_user.id != user_id:
                raise BadRequestException("This email is already in use.")

        updated_user = self.user_repository.update(user, update_data)

        return UserResponse.from_orm(updated_user)