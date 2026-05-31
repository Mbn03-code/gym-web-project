from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    Boolean,
    Time,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.base_model import BaseModelMixin
from app.core.enums import CafeStatus, ContactType


class City(Base, BaseModelMixin):
    __tablename__ = "cities"

    name = Column(String(100), nullable=False)
    province = Column(String(100), nullable=False)
    slug = Column(String(120), unique=True, nullable=False, index=True)

    cafes = relationship("Cafe", back_populates="city")


class CafeType(Base, BaseModelMixin):
    __tablename__ = "cafe_types"

    name = Column(String(100), nullable=False)
    slug = Column(String(120), unique=True, nullable=False, index=True)

    cafes = relationship("Cafe", back_populates="cafe_type")


class Amenity(Base, BaseModelMixin):
    __tablename__ = "amenities"

    name = Column(String(100), nullable=False)
    icon = Column(String(255), nullable=True)

    cafes = relationship("CafeAmenity", back_populates="amenity", cascade="all, delete-orphan")


class Cafe(Base, BaseModelMixin):
    __tablename__ = "cafes"

    owner_id = Column("owner_user_id", Integer, ForeignKey("users.id"), nullable=False, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=True, index=True)
    cafe_type_id = Column(Integer, ForeignKey("cafe_types.id"), nullable=True, index=True)

    name = Column(String(150), nullable=False, index=True)
    slug = Column(String(180), unique=True, nullable=False, index=True)

    description = Column(Text, nullable=True)
    address_text = Column(Text, nullable=False)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    price_level = Column(Integer, nullable=True)

    average_rating = Column(Float, default=0, nullable=False)
    reviews_count = Column(Integer, default=0, nullable=False)

    status = Column(Enum(CafeStatus), default=CafeStatus.PENDING, nullable=False)

    owner = relationship("User", back_populates="cafes")
    city = relationship("City", back_populates="cafes")
    cafe_type = relationship("CafeType", back_populates="cafes")

    media = relationship("CafeMedia", back_populates="cafe", cascade="all, delete-orphan")
    contacts = relationship("CafeContact", back_populates="cafe", cascade="all, delete-orphan")
    opening_hours = relationship("OpeningHour", back_populates="cafe", cascade="all, delete-orphan")
    amenities = relationship("CafeAmenity", back_populates="cafe", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="cafe")
    reviews = relationship("Review", back_populates="cafe")
    # menus = relationship("Menu", back_populates="cafe")
    reservations = relationship("Reservation", back_populates="cafe")
    # orders = relationship("Order", back_populates="cafe")


class CafeAmenity(Base):
    __tablename__ = "cafe_amenities"

    cafe_id = Column(Integer, ForeignKey("cafes.id"), primary_key=True)
    amenity_id = Column(Integer, ForeignKey("amenities.id"), primary_key=True)

    cafe = relationship("Cafe", back_populates="amenities")
    amenity = relationship("Amenity", back_populates="cafes")


class CafeContact(Base, BaseModelMixin):
    __tablename__ = "cafe_contacts"

    cafe_id = Column(Integer, ForeignKey("cafes.id"), nullable=False, index=True)

    contact_type = Column(Enum(ContactType), nullable=False)
    contact_value = Column(String(500), nullable=False)

    cafe = relationship("Cafe", back_populates="contacts")


class OpeningHour(Base, BaseModelMixin):
    __tablename__ = "opening_hours"

    cafe_id = Column(Integer, ForeignKey("cafes.id"), nullable=False, index=True)

    day_of_week = Column(Integer, nullable=False)
    opens_at = Column(Time, nullable=True)
    closes_at = Column(Time, nullable=True)
    is_closed = Column(Boolean, default=False, nullable=False)

    cafe = relationship("Cafe", back_populates="opening_hours")
