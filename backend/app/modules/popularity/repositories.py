from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.popularity.models import Favorite

class FavoriteRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def add(self, user_id: int, cafe_id: int):
        existing = self.get(user_id, cafe_id)

        if existing:
            return existing

        favorite = Favorite(
            user_id=user_id,
            cafe_id=cafe_id,
        )

        self.db.add(favorite)
        self.db.commit()
        self.db.refresh(favorite)

        return favorite

    def get(self, user_id: int, cafe_id: int):
        return (
            self.db.query(Favorite)
            .filter(
                Favorite.user_id == user_id,
                Favorite.cafe_id == cafe_id,
            )
            .first()
        )

    def get_by_user_id(self, user_id: int):
        return (
            self.db.query(Favorite)
            .filter(Favorite.user_id == user_id)
            .all()
        )

    def remove(self, user_id: int, cafe_id: int):
        favorite = self.get(user_id, cafe_id)

        if favorite:
            self.db.delete(favorite)
            self.db.commit()

        return favorite