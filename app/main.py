from fastapi import FastAPI
import asyncio

from app.db.database import engine, Base
from app.api.routes.notifications import router as notification_router
from app.api.routes.websocket import router as websocket_router
from app.core.config import settings
from app.core.redis import close_redis_client
from app.workers.redis_subscriber import run_notification_subscriber

app = FastAPI(
    title=settings.APP_NAME
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    app.state.redis_subscriber_task = asyncio.create_task(run_notification_subscriber())


@app.on_event("shutdown")
async def shutdown():
    task = getattr(app.state, "redis_subscriber_task", None)
    if task:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
    await close_redis_client()

app.include_router(notification_router)
app.include_router(websocket_router)
