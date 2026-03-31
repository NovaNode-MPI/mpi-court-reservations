.PHONY: up down migrate run

COMPOSE=docker compose
BACKEND_DIR=backend

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

migrate:
	cd $(BACKEND_DIR) && alembic upgrade head

run:
	cd backend && uvicorn main:app --reload --env-file .env