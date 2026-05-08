from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import Notification

class NotificationService:

    @staticmethod
    async def create_notification(
        db: AsyncSession,
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

        return notification

    @staticmethod
    async def get_user_notifications(
        db: AsyncSession,
        user_id: str
    ):
        query = select(Notification).where(
            Notification.user_id == user_id
        )

        result = await db.execute(query)

        return result.scalars().all()