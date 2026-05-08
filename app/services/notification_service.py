from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

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
    async def get_user_notifications(
            db,
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
            "data": [
                NotificationResponse.model_validate(n)
                for n in notifications
            ],
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size if total else 0
        }