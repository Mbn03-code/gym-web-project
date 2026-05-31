from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user_id
from app.modules.users.models import User
from app.modules.cafes.models import Cafe
from app.modules.orders.models import Order
from app.modules.reservations.models import Reservation
from app.modules.reviews.models import Review
from .schemas import (
    AdminDashboardStatsResponse,
    AdminUserResponse,
    AdminCafeResponse,
)

router = APIRouter(prefix="/admin", tags=["Admin"])

# Helper
def require_admin(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not getattr(user, "is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return user

# Dashboard Stats
@router.get("/dashboard", response_model=AdminDashboardStatsResponse)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    require_admin(db, current_user_id)

    total_users = db.query(User).count()
    total_cafes = db.query(Cafe).count()
    total_orders = db.query(Order).count()
    total_reservations = db.query(Reservation).count()
    total_reviews = db.query(Review).count()

    return AdminDashboardStatsResponse(
        total_users=total_users,
        total_cafes=total_cafes,
        total_orders=total_orders,
        total_reservations=total_reservations,
        total_reviews=total_reviews,
    )

# List Users
@router.get("/users", response_model=list[AdminUserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    require_admin(db, current_user_id)

    users = db.query(User).all()
    return users

# List Cafes
@router.get("/cafes", response_model=list[AdminCafeResponse])
def list_cafes(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    require_admin(db, current_user_id)

    cafes = db.query(Cafe).all()
    return cafes