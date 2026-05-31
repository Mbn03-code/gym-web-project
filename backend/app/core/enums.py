import enum

class UserRole(str, enum.Enum):
    CUSTOMER = "CUSTOMER"
    CAFE_OWNER = "CAFE_OWNER"
    ADMIN = "ADMIN"

class UserStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    DELETED = "DELETED"

class OTPPurpose(str, enum.Enum):
    REGISTER = "REGISTER"
    LOGIN = "LOGIN"

class CafeStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    REJECTED = "REJECTED"
    DELETED = "DELETED"

class MediaType(str, enum.Enum):
    LOGO = "LOGO"
    IMAGE = "IMAGE"

class ContactType(str, enum.Enum):
    PHONE = "PHONE"
    WEBSITE = "WEBSITE"
    TELEGRAM = "TELEGRAM"
    INSTAGRAM = "INSTAGRAM"
    MENU_URL = "MENU_URL"
    OTHER = "OTHER"

class ReviewStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    DELETED = "DELETED"

class ReservationStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"