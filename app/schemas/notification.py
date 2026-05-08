from pydantic import BaseModel
from datetime import datetime
from typing import List

from app.schemas.base import ApiResponse

class NotificationCreate(BaseModel):
    user_id: str
    message: str

class NotificationResponse(BaseModel):
    id: int
    user_id: str
    message: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class PaginatedNotificationResponse(BaseModel):
    items: List[NotificationResponse]
    total: int
    page: int
    size: int
    pages: int


class NotificationCreateApiResponse(ApiResponse[NotificationResponse]):
    pass


class NotificationListApiResponse(ApiResponse[PaginatedNotificationResponse]):
    pass
