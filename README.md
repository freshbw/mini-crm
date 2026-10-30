# Mini-CRM

[![CI](https://github.com/freshbw/mini-crm/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/freshbw/mini-crm/actions/workflows/ci.yml)
![Status](https://img.shields.io/badge/status-work_in_progress-orange)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)

CRM with a centralized messaging inbox. Read and reply to messages from different sources (Telegram and email for now) via a single interface.

> **Early stage** — scaffold and core infrastructure. Product features are a work in progress.

## Stack

- **API:** Python 3.14, FastAPI, uv
- **Database:** PostgreSQL, SQLAlchemy (async), Alembic
- **Key-value store:** Valkey (GLIDE)
- **Configuration:** pydantic-settings, TOML accounts, Docker Compose secrets
- **Logging:** structlog
- **Code quality:** Ruff, mypy, pytest, pre-commit, GitHub Actions

## Repository Structure

```text
.
├── backend/                    # FastAPI app, Alembic, tests, Dockerfile
├── config/                     # Non-secret TOML configuration
├── secrets/                    # Secret file placeholders (values are not committed)
├── docker-compose.yml
├── docker-compose.override.yml # Local ports
├── .env.example
└── README.md
```

## Prerequisites

- Python 3.14
- [uv](https://docs.astral.sh/uv/)
- Docker and Docker Compose

## Quick Start

### 1. Configuration

```bash
cp .env.example .env
```

Fill in the required files under `secrets/` (e.g. `postgres__password`, `valkey__password`). Secret values are not committed to git.

Configure `config/accounts.toml` as needed.

### 2. Start Infrastructure

```bash
docker compose up -d
```

### 3. Start Backend

```bash
cd backend
uv sync --all-groups
uv run --group api uvicorn app.app:app --reload
```

Health check: `GET /api/health`

## Development

From the repository root, install Git hooks:

```bash
pre-commit install
```

From `backend/`:

```bash
cd backend
uv sync --all-groups
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
```

## Database Migrations

From `backend/`:

```bash
cd backend
uv run alembic upgrade head
uv run alembic revision --autogenerate -m "migration description"
```

## Configuration

| Source | Purpose |
|---|---|
| `.env` / environment variables | Nested application settings (`POSTGRES__*`, `VALKEY__*`, `DEBUG`, etc.) |
| `secrets/` | Secret files (`postgres__password`, `valkey__password`, etc.); values stay local |
| `config/accounts.toml` | Non-secret account endpoints and configuration |

More configuration details will be documented as the project evolves.

## Roadmap

- [ ] Message ingestion (Telegram, email)
- [ ] Unified inbox API
- [ ] Auth
- [ ] Frontend
- [ ] Production deploy

## License

[MIT](LICENSE)
