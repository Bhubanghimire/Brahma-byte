import json
from unittest.mock import AsyncMock

import pytest
from sqlalchemy import select

from app.db.models import Notification
from app.services import notification_service


@pytest.fixture
def mock_redis_publish(monkeypatch):
    publish_mock = AsyncMock()

    class DummyRedis:
        async def publish(self, channel: str, payload: str) -> int:
            return await publish_mock(channel, payload)

    monkeypatch.setattr(
        notification_service,
        "get_redis_client",
        lambda: DummyRedis(),
    )
    return publish_mock


@pytest.mark.asyncio
async def test_create_notification_returns_wrapper_and_writes_db(client, db_session, mock_redis_publish):
    payload = {"user_id": "user-1", "message": "hello"}

    response = await client.post("/notifications", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert "message" in body
    assert "data" in body
    assert body["data"]["user_id"] == "user-1"
    assert body["data"]["message"] == "hello"

    result = await db_session.execute(select(Notification).where(Notification.user_id == "user-1"))
    row = result.scalar_one()
    assert row.message == "hello"

    mock_redis_publish.assert_awaited_once()
    channel, raw_payload = mock_redis_publish.await_args.args
    assert channel == "notifications:user-1"
    published = json.loads(raw_payload)
    assert published["user_id"] == "user-1"
    assert published["message"] == "hello"
    assert isinstance(published["notification_id"], int)


@pytest.mark.asyncio
async def test_get_notifications_empty_paginated_shape(client):
    response = await client.get("/notifications/unknown-user?page=1&size=10")

    assert response.status_code == 200
    body = response.json()
    data = body["data"]

    assert "message" in body
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["size"] == 10
    assert data["pages"] == 0


@pytest.mark.asyncio
async def test_get_notifications_non_empty_pagination(client, mock_redis_publish):
    for i in range(3):
        resp = await client.post(
            "/notifications",
            json={"user_id": "user-42", "message": f"msg-{i}"},
        )
        assert resp.status_code == 200

    response = await client.get("/notifications/user-42?page=2&size=2")

    assert response.status_code == 200
    body = response.json()
    data = body["data"]

    assert data["total"] == 3
    assert data["page"] == 2
    assert data["size"] == 2
    assert data["pages"] == 2
    assert len(data["items"]) == 1
    assert data["items"][0]["user_id"] == "user-42"
