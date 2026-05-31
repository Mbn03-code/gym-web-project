from typing import List, Optional
from app.core.exceptions import (
    NotFoundException,
    BadRequestException,
    ForbiddenException,
)
from app.modules.cafes.schemas import (
    CafeCreate,
    CafeUpdate,
    CafeResponse,
)
from app.modules.cafes.repositories import CafeRepository

class CafeService:
    def __init__(self, cafe_repository: CafeRepository):
        self.cafe_repository = cafe_repository

    def create_cafe(self, owner_id: int, data: CafeCreate) -> CafeResponse:
        """
        Creates a new cafe owned by the given user.
        Handles location and features.
        """

        cafe_data = data.dict(exclude={"location", "features"})

        new_cafe = self.cafe_repository.create(
            owner_id=owner_id,
            **cafe_data
        )

        if data.location:
            self.cafe_repository.create_location(
                cafe_id=new_cafe.id,
                **data.location.dict()
            )

        if data.features:
            self.cafe_repository.set_features(
                cafe_id=new_cafe.id,
                features=data.features
            )

        created_cafe = self.cafe_repository.get_by_id(new_cafe.id)

        return CafeResponse.from_orm(created_cafe)

    def update_cafe(
        self,
        cafe_id: int,
        owner_id: int,
        data: CafeUpdate
    ) -> CafeResponse:
        """
        Updates a cafe (only by owner).
        Supports partial update.
        """

        cafe = self.cafe_repository.get_by_id(cafe_id)

        if not cafe:
            raise NotFoundException("Cafe not found.")

        if cafe.owner_id != owner_id:
            raise ForbiddenException(
                "You are not allowed to modify this cafe."
            )

        update_data = data.dict(
            exclude_unset=True,
            exclude={"location", "features"}
        )

        if update_data:
            self.cafe_repository.update(cafe, update_data)

        if data.location:
            self.cafe_repository.update_location(
                cafe_id=cafe_id,
                **data.location.dict(exclude_unset=True)
            )

        if data.features is not None:
            self.cafe_repository.set_features(
                cafe_id=cafe_id,
                features=data.features
            )

        updated_cafe = self.cafe_repository.get_by_id(cafe_id)

        return CafeResponse.from_orm(updated_cafe)

    def delete_cafe(self, cafe_id: int, owner_id: int) -> dict:
        """
        Deletes a cafe (only by owner).
        """

        cafe = self.cafe_repository.get_by_id(cafe_id)

        if not cafe:
            raise NotFoundException("Cafe not found.")

        if cafe.owner_id != owner_id:
            raise ForbiddenException(
                "You are not allowed to delete this cafe."
            )

        self.cafe_repository.delete(cafe)

        return {"message": "Cafe deleted successfully."}

    def get_cafe(self, cafe_id: int) -> CafeResponse:
        """
        Returns cafe details.
        """

        cafe = self.cafe_repository.get_by_id(cafe_id)

        if not cafe:
            raise NotFoundException("Cafe not found.")

        return CafeResponse.from_orm(cafe)

    def search_cafes(
        self,
        city_id: int,
        name: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[CafeResponse]:
        """
        Search active cafes by required city and optional name.
        Results are sorted by average rating.
        """

        if not city_id:
            raise BadRequestException("City is required.")

        if limit <= 0:
            raise BadRequestException("Limit must be greater than zero.")

        if limit > 100:
            raise BadRequestException("Limit cannot be greater than 100.")

        if offset < 0:
            raise BadRequestException("Offset cannot be negative.")

        cafes = self.cafe_repository.search(
            city_id=city_id,
            name=name,
            limit=limit,
            offset=offset,
        )

        return [CafeResponse.from_orm(cafe) for cafe in cafes]


    def search(
        self,
        city_id: int,
        name: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[CafeResponse]:
        return self.search_cafes(
            city_id=city_id,
            name=name,
            limit=limit,
            offset=offset,
        )