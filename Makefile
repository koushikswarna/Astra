.PHONY: install dev test lint clean run web

install:
	pip install -r requirements.txt

dev:
	pip install -r requirements-dev.txt
	pre-commit install || true

test:
	pytest tests/ -v --tb=short

test-cov:
	pytest tests/ --cov=astra --cov-report=html --cov-report=term

lint:
	ruff check astra/ tests/
	mypy astra/ --ignore-missing-imports

format:
	ruff format astra/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache .mypy_cache htmlcov .coverage build dist *.egg-info

run:
	python main.py

voice:
	python main.py --voice

web:
	streamlit run main.py -- --ui streamlit

download-models:
	python scripts/download_models.py

benchmark:
	python scripts/benchmark.py
