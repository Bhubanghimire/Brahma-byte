# Test Suite Guide

## Scope
This test suite validates:
- Notification REST APIs (`POST /notifications`, `GET /notifications/{user_id}`)
- Pagination response shape and metadata
- Redis publish behavior (mocked, no real Redis needed)
- WebSocket `ConnectionManager` lifecycle behavior

## Files
- `tests/conftest.py`
- `tests/test_notifications.py`
- `tests/test_websocket_manager.py`

## How Tests Are Isolated
- Uses `httpx.AsyncClient` + `ASGITransport` for async API testing.
- Overrides `get_db` dependency with an isolated async SQLite in-memory session.
- Mocks Redis publish using `AsyncMock` (no external Redis server required).
- Disables app lifespan in tests to avoid starting background subscriber worker.

## Run Tests
From project root:

```bash
pytest -q
```

Run specific files:

```bash
pytest -q tests/test_notifications.py
pytest -q tests/test_websocket_manager.py
```

## Required Test Dependencies
Your environment should include:
- `pytest`
- `pytest-asyncio`
- `httpx`
- `greenlet` (required by SQLAlchemy async internals)

If missing, install in your active environment:

```bash
pip install pytest pytest-asyncio httpx greenlet
```

## Notes
- Redis integration is intentionally mocked in tests.
- Tests do not require Docker, Redis server, or network access.
- Expected runtime is fast (typically under a few seconds in a normal local environment).
