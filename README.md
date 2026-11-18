# CareerPulse

A FastAPI document and chat backend with RAG, pgvector storage, and Celery workers.

## Project layout

- `src/modules/` contains the authentication, users, documents, and chat modules.
- `src/rag/` contains document ingestion, retrieval, and response generation.
- `src/worker/` contains Celery workers.
- `alembic/` contains PostgreSQL migrations.

## Local setup status

The repository provides `requirements.txt` and `.env.example`. The Compose web and worker services use `build: .` and need a Dockerfile in the root to build.
