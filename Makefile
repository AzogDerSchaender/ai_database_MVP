# AI Database MVP - Development Makefile
# Production-grade development workflow automation

.PHONY: help
help: ## Show this help message
	@echo "AI Database MVP - Development Commands"
	@echo "======================================"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: setup
setup: ## Complete development environment setup
	@echo "🚀 Setting up development environment..."
	@python scripts/setup-dev.py

.PHONY: install
install: ## Install all dependencies
	@echo "📦 Installing dependencies..."
	@pip install --upgrade pip
	@pip install -e ".[dev]"
	@pre-commit install

.PHONY: format
format: ## Format code with Black and isort
	@echo "🎨 Formatting code..."
	@isort .
	@black .

.PHONY: lint
lint: ## Run all linting tools
	@echo "🔍 Running linters..."
	@black --check .
	@isort --check-only .
	@flake8 .
	@mypy .

.PHONY: test
test: ## Run all tests with coverage
	@echo "🧪 Running tests..."
	@pytest tests/ -v --cov=core --cov-report=term-missing --cov-report=html

.PHONY: test-unit
test-unit: ## Run unit tests only
	@echo "🧪 Running unit tests..."
	@pytest tests/unit -v --cov=core --cov-report=term-missing

.PHONY: test-integration
test-integration: ## Run integration tests only
	@echo "🧪 Running integration tests..."
	@pytest tests/integration -v

.PHONY: test-e2e
test-e2e: ## Run end-to-end tests only
	@echo "🧪 Running E2E tests..."
	@pytest tests/e2e -v

.PHONY: security
security: ## Run security checks
	@echo "🔒 Running security checks..."
	@bandit -r core/ -f json -o bandit-report.json || true
	@safety check --json --output safety-report.json || true
	@echo "✅ Security reports generated"

.PHONY: clean
clean: ## Clean up temporary files and caches
	@echo "🧹 Cleaning up..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.pyd" -delete
	@find . -type f -name ".coverage" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✨ Cleaned!"

.PHONY: docs
docs: ## Build documentation
	@echo "📚 Building documentation..."
	@mkdocs build

.PHONY: docs-serve
docs-serve: ## Serve documentation locally
	@echo "📚 Serving documentation at http://localhost:8000..."
	@mkdocs serve

.PHONY: docker-up
docker-up: ## Start Docker services
	@echo "🐳 Starting Docker services..."
	@docker-compose -f docker/docker-compose.test.yml up -d
	@echo "✅ Services started"

.PHONY: docker-down
docker-down: ## Stop Docker services
	@echo "🐳 Stopping Docker services..."
	@docker-compose -f docker/docker-compose.test.yml down
	@echo "✅ Services stopped"

.PHONY: docker-logs
docker-logs: ## Show Docker service logs
	@docker-compose -f docker/docker-compose.test.yml logs -f

.PHONY: run
run: ## Run the application
	@echo "🚀 Starting application..."
	@python -m uvicorn core.api.main:app --reload --host 0.0.0.0 --port 8000

.PHONY: shell
shell: ## Start IPython shell with project context
	@echo "🐚 Starting IPython shell..."
	@ipython -i -c "import asyncio; from core import *; print('AI Database MVP shell ready!')"

.PHONY: db-upgrade
db-upgrade: ## Apply database migrations
	@echo "📊 Applying database migrations..."
	@alembic upgrade head

.PHONY: db-downgrade
db-downgrade: ## Rollback last database migration
	@echo "📊 Rolling back database migration..."
	@alembic downgrade -1

.PHONY: db-reset
db-reset: ## Reset database to initial state
	@echo "📊 Resetting database..."
	@alembic downgrade base
	@alembic upgrade head

.PHONY: benchmark
benchmark: ## Run performance benchmarks
	@echo "⚡ Running benchmarks..."
	@pytest tests/benchmarks -v --benchmark-only

.PHONY: profile
profile: ## Profile the application
	@echo "📊 Profiling application..."
	@python -m cProfile -o profile.stats scripts/profile_app.py
	@python -m pstats profile.stats

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks on all files
	@echo "🎯 Running pre-commit hooks..."
	@pre-commit run --all-files

.PHONY: update-deps
update-deps: ## Update all dependencies
	@echo "📦 Updating dependencies..."
	@pip install --upgrade pip
	@pip install --upgrade -e ".[dev]"
	@pre-commit autoupdate

.PHONY: check-all
check-all: lint test security ## Run all checks (lint, test, security)
	@echo "✅ All checks passed!"

.PHONY: release
release: check-all ## Prepare for release (run all checks)
	@echo "🎉 Ready for release!"

# Development shortcuts
.PHONY: f
f: format ## Shortcut for format

.PHONY: l
l: lint ## Shortcut for lint

.PHONY: t
t: test ## Shortcut for test

.PHONY: r
r: run ## Shortcut for run

# Docker compose shortcuts
.PHONY: up
up: docker-up ## Shortcut for docker-up

.PHONY: down
down: docker-down ## Shortcut for docker-down

.PHONY: logs
logs: docker-logs ## Shortcut for docker-logs 