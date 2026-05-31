from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.base_model import BaseModelMixin

class AdminActionLog(Base, BaseModelMixin):
    __tablename__ = "admin_action_logs"

    admin_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    action = Column(String(100), nullable=False)
    target_type = Column(String(100), nullable=True)
    target_id = Column(Integer, nullable=True)

    description = Column(Text, nullable=True)

    admin_user = relationship("User")