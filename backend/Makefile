.PHONY: lint format typecheck
	
lint:
	uv run ruff check .

format:
	uv run ruff format 
	
typecheck:
	uv run pyright

test:
	uv run pytest --cov

migrations:
	uv run src/manage.py makemigrations

migrate:
	uv run src/manage.py migrate