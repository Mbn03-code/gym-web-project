from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.base_model import BaseModelMixin
from app.core.enums import ReviewStatus

class Review(Base, BaseModelMixin):
    __tablename__ = "reviews"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    cafe_id = Column(Integer, ForeignKey("cafes.id"), nullable=False)

    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)

    status = Column(Enum(ReviewStatus), default=ReviewStatus.PENDING, nullable=False)

    user = relationship("User", back_populates="reviews")
    cafe = relationship("Cafe", back_populates="reviews")
    replies = relationship("ReviewReply", back_populates="review")


class ReviewReply(Base, BaseModelMixin):
    __tablename__ = "review_replies"

    review_id = Column(Integer, ForeignKey("reviews.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    reply_text = Column(Text, nullable=False)

    review = relationship("Review", back_populates="replies")
    user = relationship("User", back_populates="review_replies")

class ForbiddenWord(Base, BaseModelMixin):
    __tablename__ = "forbidden_words"

    word = Column(String(100), unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)