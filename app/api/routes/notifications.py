from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.response import success
from app.schemas.base import ApiResponse
from app.schemas.notification import (
    NotificationCreate,
    NotificationResponse
)

from app.api.dependencies import get_db
from app.services.notification_service import NotificationService
from app.core.websocket_manager import manager

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post("", response_model=ApiResponse)
async def create_notification(
    payload: NotificationCreate,
    db: AsyncSession = Depends(get_db)
):
    notification = await NotificationService.create_notification(
        db=db,
        user_id=payload.user_id,
        message=payload.message
    )

    await manager.send_personal_message(
        payload.user_id,
        {
            "message": payload.message,
            "created_at": str(notification.created_at)
        }
    )

    return success(
        data=notification,
        message="Data created successfully"
    )


@router.get("/{user_id}")
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