from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# ---------- Input DTOs ----------
class SendCodeRequest(BaseModel):
    phone_number: str = Field(min_length=10, max_length=15)
    
class RegisterRequest(BaseModel):
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    username: str = Field(min_length=3, max_length=30)
    phone_number: str = Field(min_length=10, max_length=15)
    email: Optional[EmailStr] = None
    verification_code: str = Field(min_length=4, max_length=6)

class LoginRequest(BaseModel):
    phone_number: str = Field(min_length=10, max_length=15)
    verification_code: str = Field(min_length=4, max_length=6)

# ---------- Output DTOs ----------
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class AuthUserResponse(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    phone_number: str
    email: Optional[str] = None

    class Config:
        orm_mode = True

# هدف: جلوگیری از نمایش password و کنترل فرایند login/register.
# اطلاعات حساس نمایش داده نمی‌شود
# ولیدیشن ایمیل + طول پسورد
#خروجی مناسب فرانت داخل dashboard