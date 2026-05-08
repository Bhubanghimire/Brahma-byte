import logging
from collections import defaultdict

from fastapi import WebSocket

logger = logging.getLogger(__name__)

class ConnectionManager:

    def __init__(self):
        self.active_connections = defaultdict(list)

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id].append(websocket)
        logger.info("WebSocket connected: user_id=%s active=%s", user_id, len(self.active_connections[user_id]))

    def disconnect(self, user_id: str, websocket: WebSocket):
        connections = self.active_connections.get(user_id)
        if not connections:
            return

        try:
            connections.remove(websocket)
        except ValueError:
            # Idempotent cleanup: connection may already be removed.
            return
        finally:
            if not connections:
                self.active_connections.pop(user_id, None)

        logger.info("WebSocket disconnected: user_id=%s active=%s", user_id, len(self.active_connections.get(user_id, [])))

    async def send_personal_message(
        self,
        user_id: str,
        message: dict
    ):
        connections = list(self.active_connections.get(user_id, []))

        stale_connections = []

        for connection in connections:
            try:
                await connection.send_json(message)
            except Exception as exc:
                logger.warning("WebSocket send failed: user_id=%s error=%s", user_id, str(exc))
                stale_connections.append(connection)

        for stale in stale_connections:
            self.disconnect(user_id, stale)

manager = ConnectionManager()
