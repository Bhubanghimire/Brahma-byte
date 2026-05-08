from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
import logging
import json

from app.core.redis import get_redis_client
from app.db.models import Notification
from app.schemas.notification import NotificationResponse

logger = logging.getLogger(__name__)


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

        try:
            db.add(notification)
            await db.commit()
            await db.refresh(notification)
        except SQLAlchemyError as exc:
            await db.rollback()
            logger.exception(
                "Failed to create notification: user_id=%s error=%s",
                user_id,
                str(exc)
            )
            raise

        payload = {
            "user_id": user_id,
            "message": message,
            "notification_id": notification.id,
            "timestamp": notification.created_at.isoformat() if notification.created_at else None
        }
        await get_redis_client().publish(
            f"notifications:{user_id}",
            json.dumps(payload)
        )

        return NotificationResponse.model_validate(notification)

    @staticmethod
    async def get_user_notifications(
            db: AsyncSession,
            user_id: str,
            page: int = 1,
            size: int = 10
    ):
        page = max(page, 1)
        size = min(max(size, 1), 100)

        base_query = select(Notification).where(
            Notification.user_id == user_id
        ).order_by(Notification.id.desc())

        total_result = await db.execute(
            select(func.count()).select_from(
                select(Notification).where(
                    Notification.user_id == user_id
                ).subquery()
            )
        )
        total = total_result.scalar()

        result = await db.execute(
            base_query.offset((page - 1) * size).limit(size)
        )

        notifications = result.scalars().all()

        return {
            "items": [
                NotificationResponse.model_validate(n)
                for n in notifications
            ],
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size if total else 0
        }
