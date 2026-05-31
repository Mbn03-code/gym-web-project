from sqlalchemy import Column, String, DateTime, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base
from app.core.base_model import BaseModelMixin
from app.core.enums import UserRole, UserStatus

class User(Base, BaseModelMixin):
    __tablename__ = "users"

    username = Column(String(50), unique=True, nullable=False, index=True)

    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)

    phone_number = Column("phone", String(15), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)

    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE, nullable=False)

    phone_verified_at = Column(DateTime, nullable=True)

    otp_codes = relationship("OTPCode", back_populates="user", cascade="all, delete-orphan")
    owner_profile = relationship(
        "CafeOwnerProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    cafes = relationship("Cafe", back_populates="owner")
    favorites = relationship("Favorite", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    review_replies = relationship("ReviewReply", back_populates="user")
    reservations = relationship("Reservation", back_populates="user")
    verification_tokens = relationship("VerificationToken", back_populates="user", cascade="all, delete-orphan")

class CafeOwnerProfile(Base):
    __tablename__ = "cafe_owner_profiles"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    national_code = Column(String(20), unique=True, nullable=False, index=True)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="owner_profile")
