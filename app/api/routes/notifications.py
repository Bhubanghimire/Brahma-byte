from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.response import success
from app.schemas.notification import (
    NotificationCreateApiResponse,
    NotificationListApiResponse,
    NotificationCreate,
)

from app.api.dependencies import get_db
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post("", response_model=NotificationCreateApiResponse)
async def create_notification(
    payload: NotificationCreate,
    db: AsyncSession = Depends(get_db)
):
    notification = await NotificationService.create_notification(
        db=db,
        user_id=payload.user_id,
        message=payload.message
    )

    return success(
        data=notification,
        message="Data created successfully"
    )


@router.get("/{user_id}", response_model=NotificationListApiResponse)
async def get_notifications(
    user_id: str,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    notifications = await NotificationService.get_user_notifications(db, user_id, page, size)
    return success(
        data=notifications,
        message="Notifications fetched successfully"
    )
