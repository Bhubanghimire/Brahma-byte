import asyncio
import json
import logging

from app.core.redis import get_redis_client
from app.core.websocket_manager import manager

logger = logging.getLogger(__name__)


async def run_notification_subscriber() -> None:
    while True:
        pubsub = None
        try:
            redis = get_redis_client()
            pubsub = redis.pubsub()
            await pubsub.psubscribe("notifications:*")
            logger.info("Redis subscriber started: pattern=notifications:*")

            async for event in pubsub.listen():
                if event.get("type") != "pmessage":
                    continue

                channel = event.get("channel", "")
                if not channel.startswith("notifications:"):
                    continue

                user_id = channel.split(":", 1)[1]
                raw_data = event.get("data")

                try:
                    payload = json.loads(raw_data)
                except (TypeError, json.JSONDecodeError):
                    logger.warning("Invalid Redis payload: channel=%s", channel)
                    continue

                await manager.send_personal_message(user_id, payload)

        except asyncio.CancelledError:
            logger.info("Redis subscriber cancelled")
            raise
        except Exception as exc:
            logger.exception("Redis subscriber error: %s", str(exc))
            await asyncio.sleep(2)
        finally:
            if pubsub is not None:
                await pubsub.close()
