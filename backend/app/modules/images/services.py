import os
import uuid
from typing import Optional
from fastapi import UploadFile
from app.modules.images.repositories import ImageRepository
from app.modules.cafes.repositories import CafeRepository
from app.modules.images.schemas import ImageResponse
from app.core.exceptions import (
    NotFoundException,
    ForbiddenException,
    BadRequestException,
)

MEDIA_ROOT = "media"
CAFE_IMAGE_PATH = "cafes"
BASE_URL = "http://localhost:8000"  # در production از config خوانده شود

class ImageService:
    def __init__(
        self,
        image_repository: ImageRepository,
        cafe_repository: CafeRepository,
    ):
        self.image_repository = image_repository
        self.cafe_repository = cafe_repository

    # Upload Cafe Image
    async def upload_cafe_image(
        self,
        cafe_id: int,
        user_id: int,
        file: UploadFile,
    ) -> ImageResponse:

        # 1️⃣ بررسی وجود کافه
        cafe = self.cafe_repository.get_by_id(cafe_id)
        if not cafe:
            raise NotFoundException("Cafe not found.")

        # 2️⃣ فقط مالک کافه بتواند تصویر اضافه کند
        if cafe.owner_id != user_id:
            raise ForbiddenException(
                "You are not allowed to upload images for this cafe."
            )

        # 3️⃣ بررسی نوع فایل
        if not file.content_type.startswith("image/"):
            raise BadRequestException("Only image files are allowed.")

        # 4️⃣ ساخت نام یکتا
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"

        # 5️⃣ ساخت مسیر ذخیره
        upload_dir = os.path.join(MEDIA_ROOT, CAFE_IMAGE_PATH)
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, unique_filename)

        # 6️⃣ ذخیره فایل
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # 7️⃣ ساخت URL عمومی
        image_url = f"{BASE_URL}/{MEDIA_ROOT}/{CAFE_IMAGE_PATH}/{unique_filename}"

        # 8️⃣ ذخیره در دیتابیس
        image = self.image_repository.create(
            cafe_id=cafe_id,
            url=image_url,
            file_name=unique_filename,
        )

        return ImageResponse.from_orm(image)

    # Delete Image
    def delete_image(
        self,
        image_id: int,
        user_id: int,
    ) -> dict:

        image = self.image_repository.get_by_id(image_id)
        if not image:
            raise NotFoundException("Image not found.")

        cafe = self.cafe_repository.get_by_id(image.cafe_id)
        if not cafe:
            raise NotFoundException("Cafe not found.")

        if cafe.owner_id != user_id:
            raise ForbiddenException(
                "You are not allowed to delete this image."
            )

        # حذف فایل از سیستم
        file_path = os.path.join(
            MEDIA_ROOT,
            CAFE_IMAGE_PATH,
            image.file_name,
        )

        if os.path.exists(file_path):
            os.remove(file_path)

        # حذف رکورد دیتابیس
        self.image_repository.delete(image)

        return {"message": "Image deleted successfully."}