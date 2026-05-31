from fastapi import APIRouter, Depends, Query
from .schemas import CafeCreate, CafeUpdate, CafeResponse
from .services import CafeService

router = APIRouter(
    prefix="/cafes",
    tags=["Cafes"]
)

@router.post("/", response_model=CafeResponse)
def create_cafe(payload: CafeCreate, service: CafeService = Depends()):
    return service.create(payload)

@router.get("/search/", response_model=list[CafeResponse])
def search_cafes(
    city_id: int = Query(..., description="City id is required"),
    name: str | None = Query(None, description="Optional cafe name"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: CafeService = Depends(),
):
    return service.search(
        city_id=city_id,
        name=name,
        limit=limit,
        offset=offset,
    )

@router.get("/{cafe_id}", response_model=CafeResponse)
def get_cafe(cafe_id: int, service: CafeService = Depends()):
    return service.get(cafe_id)

@router.put("/{cafe_id}", response_model=CafeResponse)
def update_cafe(cafe_id: int, payload: CafeUpdate, service: CafeService = Depends()):
    return service.update(cafe_id, payload)

@router.delete("/{cafe_id}")
def delete_cafe(cafe_id: int, service: CafeService = Depends()):
    return service.delete(cafe_id)