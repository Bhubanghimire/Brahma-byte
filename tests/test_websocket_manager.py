import pytest

from app.core.websocket_manager import ConnectionManager


class DummyWebSocket:
    def __init__(self):
        self.accepted = False
        self.sent_text = []

    async def accept(self):
        self.accepted = True

    async def send_text(self, message: str):
        self.sent_text.append(message)

    async def send_json(self, message: dict):
        self.sent_text.append(message)


@pytest.mark.asyncio
async def test_connect_adds_connection_to_user_map():
    manager = ConnectionManager()
    ws = DummyWebSocket()

    await manager.connect("user-a", ws)

    assert ws.accepted is True
    assert "user-a" in manager.active_connections
    assert ws in manager.active_connections["user-a"]


@pytest.mark.asyncio
async def test_disconnect_removes_connection_safely():
    manager = ConnectionManager()
    ws = DummyWebSocket()
    await manager.connect("user-a", ws)

    manager.disconnect("user-a", ws)

    assert "user-a" not in manager.active_connections


@pytest.mark.asyncio
async def test_disconnect_is_idempotent():
    manager = ConnectionManager()
    ws = DummyWebSocket()
    await manager.connect("user-a", ws)

    manager.disconnect("user-a", ws)
    manager.disconnect("user-a", ws)

    assert "user-a" not in manager.active_connections


@pytest.mark.asyncio
async def test_send_personal_message_handles_empty_connections():
    manager = ConnectionManager()

    await manager.send_personal_message("missing-user", {"message": "hello"})

    assert "missing-user" not in manager.active_connections
