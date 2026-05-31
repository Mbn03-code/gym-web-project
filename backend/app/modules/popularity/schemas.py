from pydantic import BaseModel
from typing import List

# Cafe Popularity Item
class CafePopularityItem(BaseModel):
    cafe_id: int
    cafe_name: str
    average_rating: float | None = None
    total_reviews: int = 0
    total_favorites: int = 0
    class Config:
        from_attributes = True

# Popularity Response
class PopularityResponse(BaseModel):
    results: List[CafePopularityItem]