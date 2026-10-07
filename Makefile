.PHONY: install run test export docker-up docker-down

install:
	python -m pip install -r requirements-dev.txt

run:
	uvicorn app.main:app --reload --port 8000

test:
	pytest -q

export:
	@test -n "$(SOURCE_DB)" || (echo "Use: make export SOURCE_DB=../ceara-road-safety-data-platform/data/warehouse/ceara_road_safety.duckdb" && exit 1)
	python scripts/export_gold.py --source "$(SOURCE_DB)"

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down
