from app.core.exceptions import (
    NotFoundException,
    ForbiddenException,
    BadRequestException,
)
from app.modules.reviews.schemas import (
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse,
)
from app.modules.reviews.repositories import ReviewRepository
#from app.modules.orders.repositories import OrderRepository
from app.modules.cafes.repositories import CafeRepository

class ReviewService:
    def __init__(
        self,
        review_repository: ReviewRepository,
        #order_repository: OrderRepository,
        cafe_repository: CafeRepository,
    ):
        self.review_repository = review_repository
        #self.order_repository = order_repository
        self.cafe_repository = cafe_repository

    # Create Review
    def create_review(
        self,
        user_id: int,
        data: ReviewCreate
    ) -> ReviewResponse:

        # 1️⃣ بررسی وجود کافه
        cafe = self.cafe_repository.get_by_id(data.cafe_id)
        if not cafe:
            raise NotFoundException("Cafe not found.")

        # 2️⃣ بررسی اینکه کاربر قبلاً از این کافه سفارش داده باشد
        #has_order = self.order_repository.has_user_ordered_from_cafe(
        #   user_id=user_id,
        #   cafe_id=data.cafe_id,
        #)

        #if not has_order:
         #   raise ForbiddenException(
          #      "You can only review cafes you have ordered from."
           # )

        # 3️⃣ جلوگیری از ثبت نظر تکراری
        # 3️⃣ جلوگیری از ثبت نظر تکراری در بازه ۲۴ ساعت
        recent_review = self.review_repository.get_recent_by_user_and_cafe(
            user_id=user_id,
            cafe_id=data.cafe_id,
            hours=24,
        )

        if recent_review:
            raise BadRequestException(
                "You can submit only one review for this cafe every 24 hours."
            )

        # 4️⃣ بررسی امتیاز معتبر (در صورت نیاز)
        if data.rating < 1 or data.rating > 5:
            raise BadRequestException("Rating must be between 1 and 5.")

        review = self.review_repository.create(
            user_id=user_id,
            **data.dict()
        )

        created_review = self.review_repository.get_by_id(review.id)

        return ReviewResponse.from_orm(created_review)

    # Get Single Review
    def get_review(self, review_id: int) -> ReviewResponse:

        review = self.review_repository.get_by_id(review_id)

        if not review:
            raise NotFoundException("Review not found.")

        return ReviewResponse.from_orm(review)

    # Update Review
    def update_review(
        self,
        review_id: int,
        user_id: int,
        data: ReviewUpdate
    ) -> ReviewResponse:

        review = self.review_repository.get_by_id(review_id)

        if not review:
            raise NotFoundException("Review not found.")

        if review.user_id != user_id:
            raise ForbiddenException(
                "You are not allowed to modify this review."
            )

        update_data = data.dict(exclude_unset=True)

        if "rating" in update_data:
            if update_data["rating"] < 1 or update_data["rating"] > 5:
                raise BadRequestException("Rating must be between 1 and 5.")

        updated_review = self.review_repository.update(
            review,
            update_data
        )

        return ReviewResponse.from_orm(updated_review)

    # Delete Review
    def delete_review(
        self,
        review_id: int,
        user_id: int
    ) -> dict:

        review = self.review_repository.get_by_id(review_id)

        if not review:
            raise NotFoundException("Review not found.")

        if review.user_id != user_id:
            raise ForbiddenException(
                "You are not allowed to delete this review."
            )

        self.review_repository.delete(review)

        return {"message": "Review deleted successfully."}
