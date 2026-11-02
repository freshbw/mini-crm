.PHONY: help install lint format format-check typecheck test check up down logs migrate migration

BACKEND_DIR := backend
UV := cd $(BACKEND_DIR) && uv

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "  %-16s %s\n", $$1, $$2}'

install: ## Install backend dependencies
	$(UV) sync --all-groups

lint: ## Run Ruff lint checks
	$(UV) run ruff check .

format-check: ## Check code formatting
	$(UV) run ruff format --check .

format: ## Format code
	$(UV) run ruff format .

typecheck: ## Run Mypy
	$(UV) run mypy

test: ## Run tests
	$(UV) run pytest

check: lint format-check typecheck test ## Run all quality checks

up: ## Start infrastructure
	docker compose up -d

down: ## Stop infrastructure
	docker compose down

logs: ## Follow infrastructure logs
	docker compose logs -f

migrate: ## Apply database migrations
	$(UV) run alembic upgrade head

migration: ## Create migration (usage: make migration msg="description")
	$(UV) run alembic revision --autogenerate -m "$(msg)"
