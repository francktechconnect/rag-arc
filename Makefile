# Placeholder for Makefile

create-tests:
	mkdir -p tests
	touch tests/__init__.py
	touch tests/test_providers.py

	echo "# Unit tests for the ARC RAG project" 
# > tests/README.md


init:
	pip install -r requirements.txt

run:
	streamlit run app/main.py

docker-build:
	docker compose build --no-cache app

docker-up:
	docker compose up -d

docker-down:
	docker compose down

ingest:
	python app/ingest.py

test:
	docker compose run --rm  -e PYTHONPATH=/app app pytest -q -rs

freeze:
	docker compose run --rm app pip freeze > requirements.txt
	
smoke-test:
	python scripts/smoke_test.py
