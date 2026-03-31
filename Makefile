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
	cd $(BACKEND_DIR) && uvicorn main:app --reload