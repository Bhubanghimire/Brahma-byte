# Real-Time Notification Service (FastAPI + WebSockets)

## Overview

This is a lightweight real-time notification system built using FastAPI,
WebSockets, and SQLite.\
It supports creating notifications via REST API and delivering them
instantly to connected WebSocket clients.

------------------------------------------------------------------------

## Features

-   WebSocket connection per user
-   Real-time notification delivery
-   Persistent storage using SQLite (default) with support for
    PostgreSQL via configuration
-   REST APIs for creating and fetching notifications
-   Standard API response format (`data`, `message`)
-   Dockerized setup

------------------------------------------------------------------------

## Tech Stack

-   FastAPI
-   SQLAlchemy (async)
-   WebSockets
-   SQLite / PostgreSQL (configurable)
-   Docker / Docker Compose
-   Pydantic v2

------------------------------------------------------------------------

## Project Structure

app/ ├── api/ ├── core/ ├── db/ ├── schemas/ ├── services/ ├── main.py

------------------------------------------------------------------------

## Setup Instructions

### 1. Clone the repository

git clone `<repo-url>`{=html} cd `<project-folder>`{=html}

### 2. Create `.env`

APP_NAME=Real-Time Notification Service
DATABASE_URL=sqlite+aiosqlite:///./notifications.db DEBUG=True
HOST=0.0.0.0 PORT=8000

### 3. Run with Docker

docker-compose up --build

------------------------------------------------------------------------

## API Endpoints

### Create Notification

POST /notifications

Request: { "user_id": 1, "message": "Hello User" }

Response: { "data": { "id": 1, "user_id": 1, "message": "Hello User",
"created_at": "2026-05-08T12:00:00" }, "message": "Data created
successfully" }

------------------------------------------------------------------------

### Get Notifications

GET /notifications/{user_id}

Response: { "data": \[\], "message": "Notifications fetched
successfully" }

------------------------------------------------------------------------

## WebSocket

### Connection

ws://localhost:8000/ws/{user_id}

Example: ws://localhost:8000/ws/1

### Behavior

-   Each user maintains a persistent WebSocket connection
-   Notifications are pushed in real-time if the user is connected
-   If user is offline, notifications are stored in database

------------------------------------------------------------------------

## Design Decisions

### 1. Service Layer Architecture

Business logic is separated from API routes for maintainability.

### 2. WebSocket Connection Manager

Maintains active user connections using an in-memory dictionary.

### 3. Standard API Response

All responses follow: { "data": {}, "message": "" }

### 4. Async Database

SQLAlchemy async engine ensures non-blocking operations.

------------------------------------------------------------------------

## Important Notes

-   WebSocket connections are stored in-memory
-   Connections reset when server restarts
-   For production scaling, Redis or a message broker should be used
-   Currently suitable for single-instance deployment

------------------------------------------------------------------------

## How to Test

### WebSocket Client

const ws = new WebSocket("ws://localhost:8000/ws/1");

ws.onmessage = (event) =\> { console.log(event.data); };

### Send Notification

curl -X POST http://localhost:8000/notifications -H "Content-Type:
application/json" -d '{"user_id":1,"message":"Hello"}'

------------------------------------------------------------------------

## Author

Bhuban Ghimire Backend Developer Assignment Submission
