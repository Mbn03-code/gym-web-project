from datetime import time
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

class CafeSocialLinks(BaseModel):
    website: Optional[HttpUrl] = None
    instagram: Optional[HttpUrl] = None
    telegram: Optional[HttpUrl] = None

class CafeLocation(BaseModel):
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)

class CafeOpeningHour(BaseModel):
    day_of_week: int = Field(..., ge=0, le=6, description="0=Monday, 6=Sunday")
    opens_at: Optional[time] = None
    closes_at: Optional[time] = None
    is_closed: bool = False

class CafeCreate(BaseModel):
    address: str = Field(..., min_length=5, description="Address")

    location: Optional[CafeLocation] = None

    features: Optional[List[str]] = Field(
        default=None,
        description="Cafe's Amenities"
    )

    phone_numbers: Optional[List[str]] = None

    working_hours: Optional[List[CafeOpeningHour]] = Field(
        default=None,
        description="Cafe opening hours"
    )

    online_menu_url: Optional[HttpUrl] = None

    social_links: Optional[CafeSocialLinks] = None

class CafeUpdate(BaseModel):
    address: Optional[str] = Field(None, min_length=5)

    location: Optional[CafeLocation] = None

    features: Optional[List[str]] = None
    phone_numbers: Optional[List[str]] = None
    working_hours: Optional[List[CafeOpeningHour]] = None
    online_menu_url: Optional[HttpUrl] = None
    social_links: Optional[CafeSocialLinks] = None

class CafeResponse(BaseModel):
    id: int
    owner_id: int

    address: str

    location: Optional[CafeLocation]
    features: Optional[List[str]]
    phone_numbers: Optional[List[str]]
    working_hours: Optional[List[CafeOpeningHour]]
    online_menu_url: Optional[HttpUrl]
    social_links: Optional[CafeSocialLinks]

    images: Optional[List[HttpUrl]] = None

    class Config:
        orm_mode = True