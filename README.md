# Real-Time Notification Service

## Overview
This project is a real-time notification backend built with FastAPI, WebSockets, SQLAlchemy, SQLite, and Docker.

It supports:
- creating notifications via REST API,
- persisting notifications in a database,
- delivering notifications instantly to connected users over WebSockets,
- fetching user notifications with pagination.

The project is designed as a clean layered backend suitable for assessment/interview review.

## Tech Stack
- FastAPI
- WebSockets
- SQLAlchemy (Async)
- SQLite (default, configurable via `DATABASE_URL`)
- Pydantic v2
- Docker / Docker Compose

## Architecture
The codebase follows a layered structure:

- API layer (`app/api/routes`)
- Handles HTTP and WebSocket endpoints.
- Accepts input, delegates work to services, returns response contracts.

- Service layer (`app/services`)
- Contains business logic for notification creation and retrieval.
- Keeps route handlers thin and maintainable.

- DB layer (`app/db`)
- Defines SQLAlchemy model(s) and async engine/session setup.

- Schema layer (`app/schemas`)
- Defines request validation and response contracts.
- Uses typed wrappers (including generic `ApiResponse[T]`) for consistency.

- WebSocket layer (`app/core/websocket_manager.py`)
- Manages active in-memory user connections.
- Sends per-user real-time messages and removes stale connections.

### Architecture Flow
`Client → FastAPI Router → Service → DB + WebSocket Manager`

## Features Implemented
- Real-time per-user WebSocket notifications
- REST API for creating notifications
- Paginated notification retrieval (`items`, `total`, `page`, `size`, `pages`)
- Consistent API response contracts (`message`, `data`)
- Async database handling with SQLAlchemy
- Dockerized local setup

## Key Design Decisions
- `user_id` as `str`
- Keeps WebSocket path/user-key handling straightforward and consistent across route/manager layers.

- In-memory WebSocket manager
- Chosen to satisfy single-instance assignment scope without adding Redis or broker complexity.

- Service layer abstraction
- Separates business logic from transport concerns (HTTP/WebSocket), improving testability and readability.

- Generic `ApiResponse[T]` wrapper
- Enforces predictable typed responses for frontend integration and API contract clarity.

- Pagination with metadata
- Returning `total`, `page`, `size`, and `pages` supports practical client-side navigation and UX.

## API Summary
### Create Notification
- `POST /notifications`
- Body:
```json
{
  "user_id": "1",
  "message": "Hello"
}
```

### Get Notifications (Paginated)
- `GET /notifications/{user_id}?page=1&size=10`

### WebSocket Connect
- `ws://localhost:8000/ws/{user_id}`

## Local Run
### 1. Environment
Create `.env`:

```env
APP_NAME=Real-Time Notification Service
DATABASE_URL=sqlite+aiosqlite:///./notifications.db
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### 2. Docker
```bash
docker-compose up --build
```

App will be available at `http://localhost:8000`.

## Future Improvements
- JWT authentication/authorization for WebSocket connections
- Redis-based distributed WebSocket scaling for multi-instance deployments
- Alembic migrations for database versioning and controlled schema evolution
- Message retry mechanism and queue-backed delivery guarantees
- WebSocket rate limiting / abuse protection

## Notes
- Current WebSocket connection state is in-memory and resets on service restart.
- The current setup is suitable for single-instance deployments and assessment scope.
