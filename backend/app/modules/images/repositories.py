from datetime import datetime
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.images.models import CafeMedia

class ImageRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create(self, cafe_id: int, url: str, file_name: str):
        image = CafeMedia(
            cafe_id=cafe_id,
            file_url=url,
            file_name=file_name,
        )

        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)

        return image

    def get_by_id(self, image_id: int):
        return (
            self.db.query(CafeMedia)
            .filter(CafeMedia.id == image_id, CafeMedia.deleted_at.is_(None))
            .first()
        )

    def get_by_cafe_id(self, cafe_id: int):
        return (
            self.db.query(CafeMedia)
            .filter(CafeMedia.cafe_id == cafe_id, CafeMedia.deleted_at.is_(None))
            .all()
        )

    def delete(self, image):
        image.deleted_at = datetime.utcnow()

        self.db.commit()
        return image