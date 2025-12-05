# Face Recognition Attendance System

Monorepo containing:

- `backend`: FastAPI + SQLAlchemy + JWT core API with student/admin/timetable/attendance endpoints.
- `face-service`: FastAPI microservice wrapping `face_recognition` for embeddings + recognition.
- `frontend`: React + Vite + Tailwind UI (shadcn-ready) hosting Admin, Operator, and Student portals.

## Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 15+
- Optional: Docker (compose file TBD)

## Backend (FastAPI)

```bash
cd backend
poetry install
cp .env.example .env  # set SECRET_KEY & DB urls
poetry run uvicorn app.main:app --reload
```

Alembic migrations (to be filled):

```bash
poetry run alembic upgrade head
```

## Face Recognition Service

```bash
cd face-service
poetry install
poetry run uvicorn app.main:app --reload --port 9001
```

## Frontend (React + Vite + Tailwind)

```bash
cd frontend
npm install
npm run dev -- --open
```

## High-level Roadmap

1. Finish DB schema + Alembic migrations.
2. Flesh out auth (refresh tokens, role policies).
3. Implement student image uploads & face-registration workflow.
4. Build timetable + attendance endpoints.
5. Implement operator console (camera streaming + recognition loop).
6. Build admin dashboards + student portal views.
7. Add reporting/export + QA + Docker orchestration.

