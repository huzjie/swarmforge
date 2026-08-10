.PHONY: help install dev test lint format clean build docker-build docker-run

help:
	@echo "SwarmForge Makefile"
	@echo "  install       Install production dependencies"
	@echo "  dev           Install dev dependencies"
	@echo "  test          Run tests"
	@echo "  lint          Run linters"
	@echo "  format        Format code"
	@echo "  clean         Clean build artifacts"
	@echo "  build         Build distribution packages"
	@echo "  docker-build  Build Docker image"
	@echo "  docker-run    Run with docker-compose"
	@echo "  migrate       Run database migrations"
	@echo "  serve         Start development server"

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=swarmforge --cov-report=html

lint:
	ruff check swarmforge/ tests/
	mypy swarmforge/

format:
	black swarmforge/ tests/
	ruff check --fix swarmforge/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ .pytest_cache/ .mypy_cache/ htmlcov/

build:
	python -m build

docker-build:
	docker build -t swarmforge:latest .

docker-run:
	docker-compose up -d

migrate:
	alembic upgrade head

serve:
	uvicorn swarmforge.api.main:app --reload --host 0.0.0.0 --port 8000
