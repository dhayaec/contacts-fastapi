# Contacts API

Production-grade FastAPI contacts API with JWT authentication and SQLite database.

## Features
- Async SQLite with SQLAlchemy
- JWT access & refresh tokens
- Pydantic v2 validation
- Dependency injection for auth
- CORS middleware
- Health check endpoint

## Endpoints

### Auth (`/api/v1/auth`)
- `POST /register` — Create user
- `POST /login` — Login (email + password)
- `POST /refresh` — Refresh token

### Contacts (`/api/v1/contacts`)
- `GET /` — List contacts
- `POST /` — Create contact
- `GET /{id}` — Get contact
- `PATCH /{id}` — Update contact
- `DELETE /{id}` — Delete contact

All contact endpoints require `Authorization: Bearer <token>`.

## Run
```bash
pip install -e .
uvicorn main:app --reload
```
