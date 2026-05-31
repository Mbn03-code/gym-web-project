from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# ---------- Shared Base ----------
class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    phone_number: str = Field(min_length=10, max_length=15)
    email: Optional[EmailStr] = None
    
# ایجاد کاربر (برای ثبت‌نام توسط admin یا موارد خاص)
class UserCreate(UserBase):
    verification_code: Optional[str] = Field(
        None, min_length=4, max_length=6, description="Verification Code"
    )
        
# ---------- Input -----------
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=30)
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    phone_number: Optional[str] = Field(None, min_length=10, max_length=15)
    email: Optional[EmailStr] = None

    class Config:
        orm_mode = True

# ---------- Output -----------
class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True