from fastapi import APIRouter, Depends
from .schemas import ReviewCreate, ReviewUpdate, ReviewResponse
from .services import ReviewService

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)

@router.post("/", response_model=ReviewResponse)
def create_review(payload: ReviewCreate, service: ReviewService = Depends()):
    return service.create(payload)

@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int, payload: ReviewUpdate, service: ReviewService = Depends()):
    return service.update(review_id, payload)

@router.delete("/{review_id}")
def delete_review(review_id: int, service: ReviewService = Depends()):
    return service.delete(review_id)