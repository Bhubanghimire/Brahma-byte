# Real-Time Notification Service

## Overview
A FastAPI-based real-time notification backend that combines REST APIs, Redis Pub/Sub, and WebSockets.

Core flow:
- Create notifications via REST.
- Persist notifications in DB.
- Publish notification events to Redis.
- Consume events in a subscriber worker.
- Push per-user messages over active WebSocket connections.

## Tech Stack
- FastAPI
- WebSockets
- Redis Pub/Sub (`redis.asyncio`)
- SQLAlchemy Async
- SQLite
- Pydantic v2
- Docker / Docker Compose

## Architecture
This service follows an event-driven architecture:

`Client → API → Service → Redis Pub/Sub → Worker → WebSocket Manager → Client`

### Architecture Diagram
```text
Client
  ↓
FastAPI API Layer
  ↓
Service Layer
  ↓
Redis Pub/Sub (event bus)
  ↓
Redis Subscriber Worker
  ↓
WebSocket Manager
  ↓
Client
```

### Layer Responsibilities
- API layer (`app/api/routes`)
- Receives HTTP/WebSocket requests and returns response contracts.

- Service layer (`app/services`)
- Executes business logic, writes DB records, and publishes notification events.

- DB layer (`app/db`)
- SQLAlchemy models, async engine, and session management.

- Schema layer (`app/schemas`)
- Pydantic request/response models and typed `ApiResponse[T]` wrapper.

- Redis + worker (`app/core/redis.py`, `app/workers/redis_subscriber.py`)
- Provides event bus and subscriber loop for delivery.

- WebSocket layer (`app/core/websocket_manager.py`)
- In-memory per-user connection registry and message push.

## System Design Explanation
- Redis Pub/Sub is used to decouple event creation from WebSocket delivery.
- API/service path creates and publishes events; delivery happens asynchronously in the subscriber worker.
- WebSocket manager remains in-memory because socket lifecycle is process-local and fast for single-instance scope.
- API no longer directly pushes to WebSockets, reducing coupling and improving extensibility.

Redis Pub/Sub model in this project:
- Publisher sends to `notifications:{user_id}`.
- Subscriber listens to `notifications:*` and forwards payload to active sockets.
- Communication is decoupled and fire-and-forget (at-most-once delivery).

## Scalability Design
- Current design uses in-memory WebSocket connections per app instance.
- Redis enables multiple API instances to publish events to a shared event bus.
- WebSocket-serving instances can scale horizontally, each consuming events and delivering to local connections.
- Limitation: Redis Pub/Sub is non-persistent, so missed messages are not replayed.

## Key Design Decisions
- Event-driven delivery over direct socket push:
- Separates request handling, event creation, and event delivery.

- Clear separation of concerns:
- API handles request/response, service creates domain events, worker delivers events.

- `user_id` as `str`:
- Consistent across API routes, Redis channels, and WebSocket connection keys.

- Generic `ApiResponse[T]` wrapper:
- Ensures predictable, strongly-typed response contracts.

- Pagination metadata (`items`, `total`, `page`, `size`, `pages`):
- Supports practical frontend paging and API usability.

## Trade-offs
- Redis Pub/Sub is low-latency and simple, but not durable.
- In-memory WebSocket manager is fast, but limits full cross-instance connection coordination.
- SQLite keeps setup simple for assessment scope, but is not ideal as a production primary DB.
- No retry/dead-letter flow exists yet for failed or missed delivery events.

## Features Implemented
- Real-time per-user WebSocket notifications
- REST API for creating notifications
- Paginated notification retrieval
- Consistent typed API response contracts
- Async SQLAlchemy DB access
- Redis Pub/Sub event publishing and subscriber delivery worker
- Dockerized local environment (API + Redis)

## API Summary
- `POST /notifications`
- `GET /notifications/{user_id}?page=1&size=10`
- `ws://localhost:8000/ws/{user_id}`

## Run
### Environment
Create `.env`:

```env
APP_NAME=Real-Time Notification Service
DATABASE_URL=sqlite+aiosqlite:///./notifications.db
DEBUG=True
HOST=0.0.0.0
PORT=8000
REDIS_URL=redis://redis:6379/0
```

For local non-Docker run, use:
- `REDIS_URL=redis://localhost:6379/0`

### Docker (recommended)
```bash
docker-compose up --build
```

### Local
1. Start Redis
```bash
redis-server
```
2. Start API
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Future Improvements
- Redis Streams for durable event messaging
- JWT authentication/authorization for WebSocket connections
- Distributed WebSocket routing across instances
- Message retry mechanism and dead-letter queue
- PostgreSQL migration from SQLite
- WebSocket rate limiting / abuse protection

## Scope Note
This implementation is intentionally lean for assessment scope while demonstrating event-driven backend design and clear service boundaries.
