from datetime import datetime, timedelta
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.enums import OTPPurpose, UserRole
from app.modules.auth.models import OTPCode
from app.modules.users.models import User
from app.core.security import get_password_hash, verify_password

class AuthRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def store_verification_code(self, phone_number: str, code: str): 
        otp = OTPCode(
            phone=phone_number,
            code_hash=get_password_hash(code),
            purpose=OTPPurpose.LOGIN,
            expires_at=datetime.utcnow() + timedelta(minutes=2),
        )
        self.db.add(otp)
        self.db.commit()
        self.db.refresh(otp)
        return otp

    def verify_code(self, phone_number: str, code: str) -> bool:
        otp = (
            self.db.query(OTPCode)
            .filter(
                OTPCode.phone == phone_number,
                OTPCode.consumed_at.is_(None),
                OTPCode.expires_at >= datetime.utcnow(),
            )
            .order_by(OTPCode.created_at.desc())
            .first()
        )
        from app.core.security import verify_password
        if not otp or not verify_password(code, otp.code_hash):
            return False

        otp.consumed_at = datetime.utcnow()
        self.db.commit()
        return True

    def get_user_by_phone(self, phone_number: str):
        return self.db.query(User).filter(User.phone_number == phone_number, User.deleted_at.is_(None)).first()

    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username, User.deleted_at.is_(None)).first()

    def create_user(self, first_name: str, last_name: str, username: str, phone_number: str, email: str | None = None):
        user = User(
            first_name=first_name, 
            last_name=last_name, 
            username=username,
            phone_number=phone_number, 
            email=email, 
            role=UserRole.CUSTOMER,
            phone_verified_at=datetime.utcnow()
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
