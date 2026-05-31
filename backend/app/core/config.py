from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # ---------- App ----------
    app_name: str = "Cafe Finder"
    environment: str = "development"

    # ---------- Server ----------
    host: str = "0.0.0.0"
    port: int = 8000

    # ---------- Database ----------
    database_url: str = "sqlite:///./app.db"

    # ---------- JWT / Security ----------
    jwt_secret_key: str = "CHANGE_ME"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60 * 24  # 24h
    jwt_refresh_token_expire_minutes: int = 60 * 24 * 7  # 7d

    # ---------- CORS ----------
    cors_allow_origins: list[str] = ["http://localhost:3000"]

    # ---------- Media / Static ----------
    # جایی که فایل‌ها روی دیسک ذخیره می‌شن (نسبت به روت پروژه)
    media_root: str = "media"

    # URL عمومی برای فایل‌های سرو شده از StaticFiles
    # در FastAPI معمولاً باید همون host/port باشد
    public_media_base_url: str = "http://localhost:8000"

    # مثال پسوندهای مجاز برای تصاویر
    allowed_image_extensions: list[str] = [".jpg", ".jpeg", ".png", ".webp"]

    # ---------- Limits ----------
    max_upload_size_bytes: int = 5 * 1024 * 1024  # 5MB
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache()
def get_settings() -> Settings:
    return Settings()