from fastapi import FastAPI

from app.db.database import engine, Base
from app.api.routes.notifications import router as notification_router
from app.api.routes.websocket import router as websocket_router
from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(notification_router)
app.include_router(websocket_router)