from fastapi import Depends
from app.core.enums import (
    CafeStatus,
    ReviewStatus,
    UserStatus,
)
from app.core.exceptions import BadRequestError, NotFoundError
from app.modules.admin.repositories import AdminRepository

class AdminService:
    def __init__(
        self,
        admin_repository: AdminRepository = Depends(),
    ):
        self.admin_repository = admin_repository

    # Dashboard / Stats
    def get_dashboard_stats(self):
        return self.admin_repository.get_dashboard_stats()

    # Users
    def get_users(self, skip: int = 0, limit: int = 100):
        self._validate_pagination(skip, limit)
        return self.admin_repository.get_users(skip=skip, limit=limit)

    def get_user_by_id(self, user_id: int):
        user = self.admin_repository.get_user_by_id(user_id)

        if not user:
            raise NotFoundError("User not found.")

        return user

    def get_admins(self):
        return self.admin_repository.get_admins()

    def update_user_status(self, user_id: int, status: UserStatus):
        if isinstance(status, str):
            status = UserStatus(status)

        user = self.admin_repository.update_user_status(
            user_id=user_id,
            status=status,
        )

        if not user:
            raise NotFoundError("User not found.")

        return user

    def block_user(self, user_id: int):
        return self.update_user_status(
            user_id=user_id,
            status=UserStatus.BLOCKED,
        )

    def activate_user(self, user_id: int):
        return self.update_user_status(
            user_id=user_id,
            status=UserStatus.ACTIVE,
        )

    def delete_user(self, user_id: int):
        user = self.admin_repository.soft_delete_user(user_id)

        if not user:
            raise NotFoundError("User not found.")

        return user

    # Cafes
    def get_cafes(self, skip: int = 0, limit: int = 100):
        self._validate_pagination(skip, limit)
        return self.admin_repository.get_cafes(skip=skip, limit=limit)

    def get_pending_cafes(self, skip: int = 0, limit: int = 100):
        self._validate_pagination(skip, limit)
        return self.admin_repository.get_pending_cafes(skip=skip, limit=limit)

    def get_cafe_by_id(self, cafe_id: int):
        cafe = self.admin_repository.get_cafe_by_id(cafe_id)

        if not cafe:
            raise NotFoundError("Cafe not found.")

        return cafe

    def approve_cafe(self, cafe_id: int):
        cafe = self.admin_repository.approve_cafe(cafe_id)

        if not cafe:
            raise NotFoundError("Cafe not found.")

        return cafe

    def reject_cafe(self, cafe_id: int):
        cafe = self.admin_repository.reject_cafe(cafe_id)

        if not cafe:
            raise NotFoundError("Cafe not found.")

        return cafe

    def delete_cafe(self, cafe_id: int):
        cafe = self.admin_repository.delete_cafe(cafe_id)

        if not cafe:
            raise NotFoundError("Cafe not found.")

        return cafe

    # Reviews
    def get_reviews(self, skip: int = 0, limit: int = 100):
        self._validate_pagination(skip, limit)
        return self.admin_repository.get_reviews(skip=skip, limit=limit)

    def get_pending_reviews(self, skip: int = 0, limit: int = 100):
        self._validate_pagination(skip, limit)
        return self.admin_repository.get_pending_reviews(skip=skip, limit=limit)

    def get_review_by_id(self, review_id: int):
        review = self.admin_repository.get_review_by_id(review_id)

        if not review:
            raise NotFoundError("Review not found.")

        return review

    def approve_review(self, review_id: int):
        review = self.admin_repository.approve_review(review_id)

        if not review:
            raise NotFoundError("Review not found.")

        return review

    def reject_review(self, review_id: int):
        review = self.admin_repository.reject_review(review_id)

        if not review:
            raise NotFoundError("Review not found.")

        return review

    def delete_review(self, review_id: int):
        review = self.admin_repository.delete_review(review_id)

        if not review:
            raise NotFoundError("Review not found.")

        return review

    # Cafe Types / Cities / Amenities
    def get_cafe_types(self):
        return self.admin_repository.get_cafe_types()

    def get_cities(self):
        return self.admin_repository.get_cities()

    def get_amenities(self):
        return self.admin_repository.get_amenities()

    def create_cafe_type(self, name: str, slug: str):
        if not name or not slug:
            raise BadRequestError("Name and slug are required.")

        return self.admin_repository.create_cafe_type(
            name=name,
            slug=slug,
        )

    def create_city(self, name: str, province: str, slug: str):
        if not name or not province or not slug:
            raise BadRequestError("Name, province and slug are required.")

        return self.admin_repository.create_city(
            name=name,
            province=province,
            slug=slug,
        )

    def create_amenity(self, name: str, icon: str | None = None):
        if not name:
            raise BadRequestError("Name is required.")

        return self.admin_repository.create_amenity(
            name=name,
            icon=icon,
        )

    # Forbidden Words
    def get_forbidden_words(self):
        return self.admin_repository.get_forbidden_words()

    def get_active_forbidden_words(self):
        return self.admin_repository.get_active_forbidden_words()

    def create_forbidden_word(self, word: str):
        if not word or not word.strip():
            raise BadRequestError("Forbidden word is required.")

        return self.admin_repository.create_forbidden_word(word.strip())

    def activate_forbidden_word(self, word_id: int):
        forbidden_word = self.admin_repository.activate_forbidden_word(word_id)

        if not forbidden_word:
            raise NotFoundError("Forbidden word not found.")

        return forbidden_word

    def deactivate_forbidden_word(self, word_id: int):
        forbidden_word = self.admin_repository.deactivate_forbidden_word(word_id)

        if not forbidden_word:
            raise NotFoundError("Forbidden word not found.")

        return forbidden_word

    def delete_forbidden_word(self, word_id: int):
        forbidden_word = self.admin_repository.delete_forbidden_word(word_id)

        if not forbidden_word:
            raise NotFoundError("Forbidden word not found.")

        return forbidden_word

    # Helpers
    def _validate_pagination(self, skip: int, limit: int):
        if skip < 0:
            raise BadRequestError("Skip cannot be negative.")

        if limit <= 0:
            raise BadRequestError("Limit must be greater than zero.")

        if limit > 100:
            raise BadRequestError("Limit cannot be greater than 100.")