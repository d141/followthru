run:
	@docker-compose up --build

stop:
	@docker-compose down

backend_shell:
	@docker-compose exec backend /bin/sh

frontend_shell:
	@docker-compose exec frontend /bin/sh

db_shell:
	@docker-compose exec db psql -U followthru -d followthru_db

migration:
	@docker-compose exec backend uv run alembic revision --autogenerate -m "change-me"

migrate:
	@docker-compose exec backend uv run alembic upgrade head

admin_user:
	@docker-compose exec frontend curl -X POST http://backend:8000/auth/signup -H "Content-Type: application/json" -d '{"email": "admin@admin.com", "password": "admin", "name": "Admin"}'