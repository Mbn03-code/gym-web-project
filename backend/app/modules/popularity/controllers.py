from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from .services import PopularityService
from .schemas import CafePopularityItem
from app.core.security import get_current_user_id

router = APIRouter(prefix="/popularity", tags=["Popularity"])

# Top cafes by rating
@router.get("/rating", response_model=List[CafePopularityItem])
def top_by_rating(
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    service = PopularityService(db)
    return service.get_top_by_rating(limit)


# Top cafes by favorites
@router.get("/favorites", response_model=List[CafePopularityItem])
def top_by_favorites(
    limit: int = 10,
    service: PopularityService = Depends(),
):
    return service.get_top_by_favorites(limit)


@router.post("/favorites/{cafe_id}")
def add_favorite(
    cafe_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    service = PopularityService(db)
    favorite = service.add_favorite(
        user_id=user_id,
        cafe_id=cafe_id,
    )

    return {
        "message": "Cafe added to favorites.",
        "cafe_id": favorite.cafe_id,
    }


@router.delete("/favorites/{cafe_id}")
def remove_favorite(
    cafe_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    service = PopularityService(db)
    service.remove_favorite(
        user_id=user_id,
        cafe_id=cafe_id,
    )

    return {
        "message": "Cafe removed from favorites.",
        "cafe_id": cafe_id,
    }


@router.get("/favorites/me")
def get_my_favorites(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    service = PopularityService(db)
    return service.get_user_favorites(user_id)


@router.get("/favorites/{cafe_id}/status")
def check_favorite_status(
    cafe_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    service = PopularityService(db)

    return {
        "cafe_id": cafe_id,
        "is_favorite": service.is_favorite(
            user_id=user_id,
            cafe_id=cafe_id,
        ),
    }