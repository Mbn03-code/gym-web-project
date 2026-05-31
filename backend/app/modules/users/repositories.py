from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.users.models import User

class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id, User.deleted_at.is_(None)).first()

    def get_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username, User.deleted_at.is_(None)).first()

    def get_by_phone(self, phone_number: str):
        return self.db.query(User).filter(User.phone_number == phone_number, User.deleted_at.is_(None)).first()

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email, User.deleted_at.is_(None)).first()

    def update(self, user, data: dict):
        for key, value in data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user
