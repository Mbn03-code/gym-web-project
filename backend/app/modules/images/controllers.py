from fastapi import APIRouter, UploadFile, File, Depends
from .services import ImageService

router = APIRouter(
    prefix="/images",
    tags=["Images"]
)

@router.post("/upload")
def upload_image(file: UploadFile = File(...), service: ImageService = Depends()):
    return service.upload(file)

@router.delete("/{image_id}")
def delete_image(image_id: int, service: ImageService = Depends()):
    return service.delete(image_id)