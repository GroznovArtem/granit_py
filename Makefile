up:
	docker compose -f docker-compose.yaml up -d

down:
	docker compose -f docker-compose.yaml down && docker network prune --force

test:
	pytest

format:
	black .
	ruff check . --fix

lint:
	lint .
	black --check .

types:
	mypy .