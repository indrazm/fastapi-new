lint:
	uv run ruff format .
	uv run ruff check . --fix
	
dev:
	uv run uvicorn app.main:app --reload

celery:
	uv run celery -A app.celery_app worker -c 2