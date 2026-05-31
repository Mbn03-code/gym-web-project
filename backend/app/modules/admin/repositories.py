from datetime import datetime
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.enums import (
    UserRole,
    UserStatus,
    CafeStatus,
    ReviewStatus,
)
from app.modules.users.models import User
from app.modules.cafes.models import Cafe, CafeType, City, Amenity
from app.modules.reviews.models import Review, ForbiddenWord

class AdminRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    # Dashboard / Stats
    def get_dashboard_stats(self):
        users_count = self.db.query(User).filter(User.deleted_at.is_(None)).count()
        cafes_count = self.db.query(Cafe).filter(Cafe.deleted_at.is_(None)).count()
        pending_cafes_count = (
            self.db.query(Cafe)
            .filter(
                Cafe.status == CafeStatus.PENDING,
                Cafe.deleted_at.is_(None),
            )
            .count()
        )
        pending_reviews_count = (
            self.db.query(Review)
            .filter(
                Review.status == ReviewStatus.PENDING,
                Review.deleted_at.is_(None),
            )
            .count()
        )

        return {
            "users_count": users_count,
            "cafes_count": cafes_count,
            "pending_cafes_count": pending_cafes_count,
            "pending_reviews_count": pending_reviews_count,
        }

    # Users
    def get_users(self, skip: int = 0, limit: int = 100):
        return (
            self.db.query(User)
            .filter(User.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_user_by_id(self, user_id: int):
        return (
            self.db.query(User)
            .filter(User.id == user_id, User.deleted_at.is_(None))
            .first()
        )

    def get_admins(self):
        return (
            self.db.query(User)
            .filter(
                User.role == UserRole.ADMIN,
                User.deleted_at.is_(None),
            )
            .all()
        )

    def update_user_status(self, user_id: int, status: UserStatus):
        user = self.get_user_by_id(user_id)

        if not user:
            return None

        user.status = status
        self.db.commit()
        self.db.refresh(user)

        return user

    def soft_delete_user(self, user_id: int):
        user = self.get_user_by_id(user_id)

        if not user:
            return None

        user.status = UserStatus.DELETED
        user.deleted_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(user)

        return user

    # Cafes
    def get_cafes(self, skip: int = 0, limit: int = 100):
        return (
            self.db.query(Cafe)
            .filter(Cafe.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_pending_cafes(self, skip: int = 0, limit: int = 100):
        return (
            self.db.query(Cafe)
            .filter(
                Cafe.status == CafeStatus.PENDING,
                Cafe.deleted_at.is_(None),
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_cafe_by_id(self, cafe_id: int):
        return (
            self.db.query(Cafe)
            .filter(Cafe.id == cafe_id, Cafe.deleted_at.is_(None))
            .first()
        )

    def approve_cafe(self, cafe_id: int):
        cafe = self.get_cafe_by_id(cafe_id)

        if not cafe:
            return None

        cafe.status = CafeStatus.ACTIVE

        self.db.commit()
        self.db.refresh(cafe)

        return cafe

    def reject_cafe(self, cafe_id: int):
        cafe = self.get_cafe_by_id(cafe_id)

        if not cafe:
            return None

        cafe.status = CafeStatus.REJECTED

        self.db.commit()
        self.db.refresh(cafe)

        return cafe

    def delete_cafe(self, cafe_id: int):
        cafe = self.get_cafe_by_id(cafe_id)

        if not cafe:
            return None

        cafe.status = CafeStatus.DELETED
        cafe.deleted_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(cafe)

        return cafe
    
    # Reviews
    def get_reviews(self, skip: int = 0, limit: int = 100):
        return (
            self.db.query(Review)
            .filter(Review.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_pending_reviews(self, skip: int = 0, limit: int = 100):
        return (
            self.db.query(Review)
            .filter(
                Review.status == ReviewStatus.PENDING,
                Review.deleted_at.is_(None),
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_review_by_id(self, review_id: int):
        return (
            self.db.query(Review)
            .filter(Review.id == review_id, Review.deleted_at.is_(None))
            .first()
        )

    def approve_review(self, review_id: int):
        review = self.get_review_by_id(review_id)

        if not review:
            return None

        review.status = ReviewStatus.APPROVED

        self.db.commit()
        self.db.refresh(review)

        return review

    def reject_review(self, review_id: int):
        review = self.get_review_by_id(review_id)

        if not review:
            return None

        review.status = ReviewStatus.REJECTED

        self.db.commit()
        self.db.refresh(review)

        return review

    def delete_review(self, review_id: int):
        review = self.get_review_by_id(review_id)

        if not review:
            return None

        review.status = ReviewStatus.DELETED
        review.deleted_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(review)

        return review

    # Cafe Types / Cities / Amenities
    def get_cafe_types(self):
        return self.db.query(CafeType).filter(CafeType.deleted_at.is_(None)).all()

    def get_cities(self):
        return self.db.query(City).filter(City.deleted_at.is_(None)).all()

    def get_amenities(self):
        return self.db.query(Amenity).filter(Amenity.deleted_at.is_(None)).all()

    def create_cafe_type(self, name: str, slug: str):
        cafe_type = CafeType(name=name, slug=slug)

        self.db.add(cafe_type)
        self.db.commit()
        self.db.refresh(cafe_type)

        return cafe_type

    def create_city(self, name: str, province: str, slug: str):
        city = City(name=name, province=province, slug=slug)

        self.db.add(city)
        self.db.commit()
        self.db.refresh(city)

        return city

    def create_amenity(self, name: str, icon: str | None = None):
        amenity = Amenity(name=name, icon=icon)

        self.db.add(amenity)
        self.db.commit()
        self.db.refresh(amenity)

        return amenity

    # Forbidden Words
    def get_forbidden_words(self):
        return self.db.query(ForbiddenWord).all()

    def get_active_forbidden_words(self):
        return (
            self.db.query(ForbiddenWord)
            .filter(ForbiddenWord.is_active.is_(True))
            .all()
        )

    def get_forbidden_word_by_id(self, word_id: int):
        return (
            self.db.query(ForbiddenWord)
            .filter(ForbiddenWord.id == word_id)
            .first()
        )

    def create_forbidden_word(self, word: str):
        forbidden_word = ForbiddenWord(word=word, is_active=True)

        self.db.add(forbidden_word)
        self.db.commit()
        self.db.refresh(forbidden_word)

        return forbidden_word

    def deactivate_forbidden_word(self, word_id: int):
        forbidden_word = self.get_forbidden_word_by_id(word_id)

        if not forbidden_word:
            return None

        forbidden_word.is_active = False

        self.db.commit()
        self.db.refresh(forbidden_word)

        return forbidden_word

    def activate_forbidden_word(self, word_id: int):
        forbidden_word = self.get_forbidden_word_by_id(word_id)

        if not forbidden_word:
            return None

        forbidden_word.is_active = True

        self.db.commit()
        self.db.refresh(forbidden_word)

        return forbidden_word

    def delete_forbidden_word(self, word_id: int):
        forbidden_word = self.get_forbidden_word_by_id(word_id)

        if not forbidden_word:
            return None

        self.db.delete(forbidden_word)
        self.db.commit()

        return forbidden_word