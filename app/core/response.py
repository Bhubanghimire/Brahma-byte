from app.schemas.base import ApiResponse

def success(data=None, message="Success"):
    return ApiResponse(
        data=data,
        message=message
    )