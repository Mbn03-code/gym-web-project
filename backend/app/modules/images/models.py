from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.base_model import BaseModelMixin
from app.core.enums import MediaType

class CafeMedia(Base, BaseModelMixin):
    __tablename__ = "cafe_media"

    cafe_id = Column(Integer, ForeignKey("cafes.id"), nullable=False)

    media_type = Column(Enum(MediaType), default=MediaType.IMAGE, nullable=False)
    file_url = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=True)
    alt_text = Column(String(255), nullable=True)

    sort_order = Column(Integer, default=0, nullable=False)
    is_cover = Column(Boolean, default=False, nullable=False)

    cafe = relationship("Cafe", back_populates="media")