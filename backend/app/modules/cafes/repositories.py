from datetime import datetime
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.enums import ContactType, CafeStatus
from app.modules.cafes.models import Cafe, CafeContact, Amenity, CafeAmenity, OpeningHour

class CafeRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create(self, owner_id: int, **data):
        contacts_data = self._extract_contacts_data(data)
        working_hours = data.pop("working_hours", None)

        address = data.pop("address", None)
        if address is not None:
            data["address_text"] = address

        # فعلاً چون CafeCreate دوستت name و slug ندارد، مقدار موقت می‌گذاریم
        timestamp = int(datetime.utcnow().timestamp())
        data.setdefault("name", f"Cafe {owner_id}")
        data.setdefault("slug", f"cafe-{owner_id}-{timestamp}")

        allowed_fields = {
            "city_id",
            "cafe_type_id",
            "name",
            "slug",
            "description",
            "address_text",
            "latitude",
            "longitude",
            "price_level",
            "status",
        }

        cafe_data = {
            key: value
            for key, value in data.items()
            if key in allowed_fields and value is not None
        }

        cafe = Cafe(
            owner_id=owner_id,
            status=CafeStatus.PENDING,
            **cafe_data,
        )

        self.db.add(cafe)
        self.db.commit()
        self.db.refresh(cafe)

        self._save_contacts(cafe.id, **contacts_data)
        self._save_opening_hours(cafe.id, working_hours)

        return cafe

    def get_by_id(self, cafe_id: int):
        return self.db.query(Cafe).filter(Cafe.id == cafe_id, Cafe.deleted_at.is_(None)).first()

    def search(self, city_id: int, name: str | None = None, limit: int = 20, offset: int = 0):
        query = self.db.query(Cafe).filter(
            Cafe.city_id == city_id,
            Cafe.status == CafeStatus.ACTIVE,
            Cafe.deleted_at.is_(None)
        )
        if name:
            query = query.filter(Cafe.name.ilike(f"%{name}%"))
        return query.order_by(Cafe.average_rating.desc(), Cafe.reviews_count.desc()).offset(offset).limit(limit).all()

    def update(self, cafe, data: dict):
        contacts_data = self._extract_contacts_data(data)
        working_hours = data.pop("working_hours", None)

        address = data.pop("address", None)
        if address is not None:
            data["address_text"] = address

        allowed_fields = {
            "city_id",
            "cafe_type_id",
            "name",
            "slug",
            "description",
            "address_text",
            "latitude",
            "longitude",
            "price_level",
            "status",
        }

        for key, value in data.items():
            if key in allowed_fields:
                setattr(cafe, key, value)

        self.db.commit()
        self.db.refresh(cafe)

        self._save_contacts(cafe.id, replace=True, **contacts_data)

        if working_hours is not None:
            self._save_opening_hours(cafe.id, working_hours, replace=True)

        return cafe

    def delete(self, cafe: Cafe):
        cafe.status = CafeStatus.DELETED
        cafe.deleted_at = datetime.utcnow()
        self.db.commit()
        return cafe

    def create_location(self, cafe_id: int, **location_data):
        cafe = self.get_by_id(cafe_id)

        if not cafe:
            return None

        cafe.latitude = location_data.get("latitude")
        cafe.longitude = location_data.get("longitude")

        self.db.commit()
        self.db.refresh(cafe)

        return cafe

    def update_location(self, cafe_id: int, **location_data):
        cafe = self.get_by_id(cafe_id)

        if not cafe:
            return None

        if "latitude" in location_data:
            cafe.latitude = location_data["latitude"]

        if "longitude" in location_data:
            cafe.longitude = location_data["longitude"]

        self.db.commit()
        self.db.refresh(cafe)

        return cafe

    def set_features(self, cafe_id: int, features: list[str]):
        self.db.query(CafeAmenity).filter(CafeAmenity.cafe_id == cafe_id).delete()
        for feature_name in features:
            amenity = self.db.query(Amenity).filter(Amenity.name == feature_name).first()
            if not amenity:
                amenity = Amenity(name=feature_name)
                self.db.add(amenity)
                self.db.flush()
            self.db.add(CafeAmenity(cafe_id=cafe_id, amenity_id=amenity.id))
        self.db.commit()


    def _extract_contacts_data(self, data: dict) -> dict:
        return {
            "phone_numbers": data.pop("phone_numbers", None),
            "online_menu_url": data.pop("online_menu_url", None),
            "social_links": data.pop("social_links", None),
        }

    def _save_contacts(
        self,
        cafe_id: int,
        phone_numbers=None,
        online_menu_url=None,
        social_links=None,
        replace: bool = False,
    ):
        contact_types_to_replace = []

        if phone_numbers is not None:
            contact_types_to_replace.append(ContactType.PHONE)

        if online_menu_url is not None:
            contact_types_to_replace.append(ContactType.MENU_URL)

        if social_links is not None:
            contact_types_to_replace.extend([
                ContactType.WEBSITE,
                ContactType.INSTAGRAM,
                ContactType.TELEGRAM,
            ])

        if replace and contact_types_to_replace:
            self.db.query(CafeContact).filter(
                CafeContact.cafe_id == cafe_id,
                CafeContact.contact_type.in_(contact_types_to_replace),
            ).delete()

        if phone_numbers:
            for phone in phone_numbers:
                self.db.add(CafeContact(
                    cafe_id=cafe_id,
                    contact_type=ContactType.PHONE,
                    contact_value=str(phone),
                ))

        if online_menu_url:
            self.db.add(CafeContact(
                cafe_id=cafe_id,
                contact_type=ContactType.MENU_URL,
                contact_value=str(online_menu_url),
            ))

        if social_links:
            if hasattr(social_links, "dict"):
                social_links = social_links.dict(exclude_none=True)

            contact_type_map = {
                "website": ContactType.WEBSITE,
                "instagram": ContactType.INSTAGRAM,
                "telegram": ContactType.TELEGRAM,
            }

            for key, value in social_links.items():
                if value:
                    self.db.add(CafeContact(
                        cafe_id=cafe_id,
                        contact_type=contact_type_map[key],
                        contact_value=str(value),
                    ))

        self.db.commit()

    def _save_opening_hours(
        self,
        cafe_id: int,
        working_hours=None,
        replace: bool = False,
    ):
        if working_hours is None:
            return

        if replace:
            self.db.query(OpeningHour).filter(
                OpeningHour.cafe_id == cafe_id
            ).delete()

        for item in working_hours:
            if hasattr(item, "model_dump"):
                hour_data = item.model_dump(exclude_unset=True)
            elif hasattr(item, "dict"):
                hour_data = item.dict(exclude_unset=True)
            else:
                hour_data = dict(item)

            self.db.add(OpeningHour(
                cafe_id=cafe_id,
                day_of_week=hour_data.get("day_of_week"),
                opens_at=hour_data.get("opens_at"),
                closes_at=hour_data.get("closes_at"),
                is_closed=hour_data.get("is_closed", False),
            ))

        self.db.commit()