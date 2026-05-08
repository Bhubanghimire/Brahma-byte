from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logging

from app.core.websocket_manager import manager

router = APIRouter()
logger = logging.getLogger(__name__)

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: str
):
    try:
        await manager.connect(user_id, websocket)
        while True:
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected: user_id=%s", user_id)
    except Exception as exc:
        logger.exception("WebSocket error: user_id=%s error=%s", user_id, str(exc))
    finally:
        manager.disconnect(user_id, websocket)
