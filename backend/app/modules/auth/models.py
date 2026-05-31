from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.base_model import BaseModelMixin
from app.core.enums import OTPPurpose


class OTPCode(Base, BaseModelMixin):
    __tablename__ = "otp_codes"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    phone = Column(String(15), nullable=False, index=True)

    code_hash = Column(String(255), nullable=False)
    purpose = Column(Enum(OTPPurpose), nullable=False)

    expires_at = Column(DateTime, nullable=False)
    consumed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="otp_codes")

