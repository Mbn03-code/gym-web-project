from fastapi import HTTPException, status

class AppError(HTTPException):
    """
   base Errors
    """
    def __init__(
        self,
        status_code: int,
        detail: str,
        *,
        headers: dict | None = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)

# ---------- Common ----------
class NotFoundError(AppError):
    def __init__(self, detail: str = "Not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class BadRequestError(AppError):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class UnauthorizedError(AppError):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class ForbiddenError(AppError):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class ConflictError(AppError):
    def __init__(self, detail: str = "Conflict"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

# ---------- Domain-specific ----------
class OwnershipError(ForbiddenError):
    def __init__(self, detail: str = "You don't have access to this resource"):
        super().__init__(detail=detail)

class ValidationError(BadRequestError):
    def __init__(self, detail: str = "Validation error"):
        super().__init__(detail=detail)