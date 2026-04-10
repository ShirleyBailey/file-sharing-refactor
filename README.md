# 📦 File Sharing MVP (Refactored)

A full-stack MVP file-sharing system built with **Python (FastAPI)** and **React**, supporting file uploads, malware scanning simulation, and alert generation.  
This project has been **refactored from a legacy codebase** with improved architecture, test coverage, and pagination support.

---

# 🚀 Features

- 📁 File upload & management
- ⚠️ Suspicious file detection (mock/heuristic-based)
- 🔔 Alerts system for detected threats
- 📄 Pagination for files and alerts
- 🧪 Unit tests for backend services
- 🧱 Clean layered architecture (Backend & Frontend)

---

# 🧠 Architecture Overview

## Backend (FastAPI)

Refactored into a clean layered structure:

app/
 ├── api/          # Route controllers
 ├── services/     # Business logic layer
 ├── repositories/ # Database access layer
 ├── models/       # ORM models
 ├── schemas/      # Pydantic DTOs
 ├── core/         # Config & utilities

### Design Principles
- Separation of concerns
- Service-repository pattern
- Stateless API design
- Testable business logic

---

## Frontend (React)

Refactored into modular structure:

src/
 ├── api/        # API clients
 ├── components/ # Reusable UI components
 ├── pages/      # Page-level components
 ├── hooks/      # Custom hooks
 ├── services/   # Business/API logic
 ├── types/      # TypeScript types

### Improvements
- Separation of UI and data logic
- Reusable hooks for API calls
- Better state management structure
- Pagination-ready UI

---

# 📄 API Overview

## Files

GET /files
- Supports pagination

Example response:
{
  "data": [],
  "total": 0,
  "skip": 0,
  "limit": 10
}

## Alerts

GET /alerts
- Supports pagination

## Upload

POST /files
- Uploads file and triggers validation pipeline

---

# ⚙️ Tech Stack

## Backend
- Python 3.10+
- FastAPI
- SQLAlchemy
- Alembic
- Pytest

## Frontend
- React
- TypeScript
- Axios
- React Query

## Infrastructure
- Docker
- Docker Compose

---

# 🧪 Running Tests

pytest

Backend tests cover:
- File upload flow
- File retrieval logic
- Alert generation logic

---

# 🐳 How to Run

docker compose -f docker-compose.dev.yml up

Then run migrations:

docker exec -it backend alembic upgrade head

---

# 🌐 Access

Frontend: http://localhost:3000/test  
Backend Docs: http://localhost:8000/docs  

---

# 🔧 Improvements Made

## Backend
- Introduced service-repository architecture
- Refactored tightly coupled logic
- Added pagination support
- Improved testability
- Fixed potential bugs in file processing pipeline

## Frontend
- Separated API layer from UI
- Introduced reusable hooks
- Improved component structure
- Prepared pagination handling

---

# 📌 Known Limitations / Future Improvements

- Replace mock malware detection with real scanning engine
- Add authentication & authorization
- Improve caching for large file lists
- Add file streaming for large uploads
- Add WebSocket for real-time alerts

---

# 🧾 Notes

This project was refactored as part of a technical assessment.  
The goal was to improve maintainability, scalability, and separation of concerns without changing core business logic.

---

# 🔥 One-line Summary

Legacy MVP refactored into a clean, testable, layered architecture with pagination and improved frontend structure.