.PHONY: help install install-dev test lint format clean run train notebook

help:
	@echo "VQC Iris Classifier - Development Commands"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install        Install project dependencies"
	@echo "  install-dev    Install dependencies for development"
	@echo "  test           Run unit tests with coverage"
	@echo "  lint           Check code quality with flake8"
	@echo "  format         Format code with black and isort"
	@echo "  format-check   Check code formatting without changes"
	@echo "  clean          Remove build and cache files"
	@echo "  run            Run the VQC training script"
	@echo "  train          Alias for run"
	@echo "  notebook       Start Jupyter notebook server"
	@echo "  docs           Build documentation"
	@echo "  all            Run tests, lint, and format"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term

test-quick:
	pytest tests/ -v

lint:
	flake8 . --max-line-length=120 --statistics
	black . --check --line-length=120
	isort . --check-only

format:
	black . --line-length=120
	isort .

format-check:
	black . --check --line-length=120
	isort . --check-only

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info/ .eggs/
	rm -rf .pytest_cache .coverage htmlcov
	rm -rf .tox .mypy_cache

run:
	python vqc_iris.py

train: run

notebook:
	jupyter notebook notebooks/

docs:
	cd docs && make html

all: format lint test
	@echo "✅ All checks passed!"

.DEFAULT_GOAL := help
