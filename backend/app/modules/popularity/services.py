from sqlalchemy import func
from sqlalchemy.orm import Session
from app.modules.cafes.models import Cafe
from app.modules.reviews.models import Review
from app.modules.popularity.models import Favorite
from .schemas import CafePopularityItem
from app.core.exceptions import BadRequestError, NotFoundError
from app.modules.popularity.repositories import FavoriteRepository

class PopularityService:
    def __init__(self, db: Session):
        self.db = db
        self.favorite_repository = FavoriteRepository(db)

    # Top cafes by rating
    def get_top_by_rating(self, limit: int = 10):
        query = (
            self.db.query(
                Cafe.id.label("cafe_id"),
                Cafe.name.label("cafe_name"),
                func.avg(Review.rating).label("average_rating"),
                func.count(Review.id).label("total_reviews"),
            )
            .join(Review, Review.cafe_id == Cafe.id)
            .group_by(Cafe.id)
            .order_by(func.avg(Review.rating).desc())
            .limit(limit)
            .all()
        )

        results = []
        for row in query:
            results.append(
                CafePopularityItem(
                    cafe_id=row.cafe_id,
                    cafe_name=row.cafe_name,
                    average_rating=round(float(row.average_rating), 2)
                    if row.average_rating else None,
                    total_reviews=row.total_reviews,
                    total_favorites=0,                )
            )
        return results


    # Top cafes by favorites
    def get_top_by_favorites(self, limit: int = 10):
        query = (
            self.db.query(
                Cafe.id.label("cafe_id"),
                Cafe.name.label("cafe_name"),
                func.count(Favorite.cafe_id).label("total_favorites"),
            )
            .join(Favorite, Favorite.cafe_id == Cafe.id)
            .group_by(Cafe.id)
            .order_by(func.count(Favorite.cafe_id).desc())
            .limit(limit)
            .all()
        )

        results = []
        for row in query:
            results.append(
                CafePopularityItem(
                    cafe_id=row.cafe_id,
                    cafe_name=row.cafe_name,
                    average_rating=None,
                    total_reviews=0,
                    total_favorites=row.total_favorites,
                )
            )

        return results


    def add_favorite(self, user_id: int, cafe_id: int):
        cafe = (
            self.db.query(Cafe)
            .filter(
                Cafe.id == cafe_id,
                Cafe.deleted_at.is_(None),
            )
            .first()
        )

        if not cafe:
            raise NotFoundError("Cafe not found.")

        existing_favorite = self.favorite_repository.get(
            user_id=user_id,
            cafe_id=cafe_id,
        )

        if existing_favorite:
            raise BadRequestError("Cafe is already in favorites.")

        return self.favorite_repository.add(
            user_id=user_id,
            cafe_id=cafe_id,
        )

    def remove_favorite(self, user_id: int, cafe_id: int):
        favorite = self.favorite_repository.get(
            user_id=user_id,
            cafe_id=cafe_id,
        )

        if not favorite:
            raise NotFoundError("Favorite not found.")

        return self.favorite_repository.remove(
            user_id=user_id,
            cafe_id=cafe_id,
        )

    def get_user_favorites(self, user_id: int):
        return self.favorite_repository.get_by_user_id(user_id)

    def is_favorite(self, user_id: int, cafe_id: int) -> bool:
        return self.favorite_repository.get(
            user_id=user_id,
            cafe_id=cafe_id,
        ) is not None