from datetime import datetime, timedelta
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.enums import ReviewStatus
from app.modules.reviews.models import Review

class ReviewRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create(self, user_id: int, **data):
        review = Review(
            user_id=user_id,
            status=ReviewStatus.PENDING,
            **data,
        )

        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)

        return review

    def get_by_id(self, review_id: int):
        return (
            self.db.query(Review)
            .filter(Review.id == review_id, Review.deleted_at.is_(None))
            .first()
        )

    def get_recent_by_user_and_cafe(
        self,
        user_id: int,
        cafe_id: int,
        hours: int = 24,
    ):
        since_time = datetime.utcnow() - timedelta(hours=hours)

        return (
            self.db.query(Review)
            .filter(
                Review.user_id == user_id,
                Review.cafe_id == cafe_id,
                Review.deleted_at.is_(None),
                Review.created_at >= since_time,
            )
            .first()
        )

    def update(self, review, data: dict):
        for key, value in data.items():
            setattr(review, key, value)

        self.db.commit()
        self.db.refresh(review)

        return review

    def delete(self, review):
        review.status = ReviewStatus.DELETED
        review.deleted_at = datetime.utcnow()

        self.db.commit()
        return review