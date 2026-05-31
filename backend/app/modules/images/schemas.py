from datetime import datetime
from pydantic import BaseModel, HttpUrl

# Base Schema
class ImageBase(BaseModel):
    url: HttpUrl

# Response Schema
class ImageResponse(ImageBase):
    id: int
    cafe_id: int
    file_name: str
    created_at: datetime

    class Config:
        from_attributes = True  # برای Pydantic v2
        # اگر از v1 استفاده می‌کنی:
        # orm_mode = True
        
# Cover Image
class ImageBase(BaseModel):
    url: HttpUrl
    is_primary: bool = False

# Cafe Images List Response (اختیاری ولی کاربردی)
class CafeImagesResponse(BaseModel):
    cafe_id: int
    images: list[ImageResponse]

    class Config:
        from_attributes = True