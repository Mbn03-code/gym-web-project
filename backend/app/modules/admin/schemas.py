from datetime import datetime
from pydantic import BaseModel, EmailStr

# User Schemas
class AdminUserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_active: bool = True
    is_admin: bool = False
    created_at: datetime | None = None

    class Config:
        from_attributes = True

# Cafe Schemas
class AdminCafeResponse(BaseModel):
    id: int
    name: str
    location: str | None = None
    owner_id: int
    created_at: datetime | None = None

    class Config:
        from_attributes = True

# Dashboard / Stats
class AdminDashboardStatsResponse(BaseModel):
    total_users: int
    total_cafes: int
    total_orders: int
    total_reservations: int
    total_reviews: int

# Generic Message
class AdminMessageResponse(BaseModel):
    message: str