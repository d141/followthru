run:
	@docker-compose up --build

stop:
	@docker-compose down

backend_shell:
	@docker-compose exec backend /bin/sh

frontend_shell:
	@docker-compose exec frontend /bin/sh