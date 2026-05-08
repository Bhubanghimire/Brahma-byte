from fastapi import WebSocket
from collections import defaultdict

class ConnectionManager:

    def __init__(self):
        self.active_connections = defaultdict(list)

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id].append(websocket)

    def disconnect(self, user_id: str, websocket: WebSocket):
        if websocket in self.active_connections[user_id]:
            self.active_connections[user_id].remove(websocket)

        if not self.active_connections[user_id]:
            del self.active_connections[user_id]

    async def send_personal_message(
        self,
        user_id: str,
        message: dict
    ):
        connections = self.active_connections.get(user_id, [])

        stale_connections = []

        for connection in connections:
            try:
                await connection.send_json(message)
            except Exception:
                stale_connections.append(connection)

        for stale in stale_connections:
            self.disconnect(user_id, stale)

manager = ConnectionManager()