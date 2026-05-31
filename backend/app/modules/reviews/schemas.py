from datetime import datetime
from pydantic import BaseModel, Field

# Base Schema
class ReviewBase(BaseModel):
    cafe_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: str | None = Field(default=None, max_length=1000)

# Create Schema
class ReviewCreate(ReviewBase):
    pass

# Update Schema (Partial Update)
class ReviewUpdate(BaseModel):
    rating: int | None = Field(default=None, ge=1, le=5)
    comment: str | None = Field(default=None, max_length=1000)

# Response Schema
class ReviewResponse(BaseModel):
    id: int
    user_id: int
    cafe_id: int
    rating: int
    comment: str | None
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True  # برای Pydantic v2
        # اگر v1 هست:
        # orm_mode = True