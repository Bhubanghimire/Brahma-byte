from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import Notification
from app.schemas.notification import NotificationResponse


class NotificationService:

    @staticmethod
    async def create_notification(
        db,
        user_id: str,
        message: str
    ):
        notification = Notification(
            user_id=user_id,
            message=message
        )

        db.add(notification)

        await db.commit()
        await db.refresh(notification)

        return NotificationResponse.model_validate(notification)

    @staticmethod
    async def get_user_notifications(db, user_id: str):
        result = await db.execute(
            select(Notification).where(Notification.user_id == user_id)
        )

        notifications = result.scalars().all()

        return [
            NotificationResponse.model_validate(n)
            for n in notifications
        ]