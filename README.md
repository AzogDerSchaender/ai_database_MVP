# Multi-Agent Database AI MVP

A production-ready multi-agent database AI system for intelligent query generation and execution, built with FastAPI, SQLAlchemy, and modern Python best practices.

## Features

- **Multi-Agent Architecture**: Specialized agents for query clarification, code generation, and testing
- **Database Agnostic**: Support for PostgreSQL, MySQL, and other SQL databases
- **Async First**: Built on FastAPI with full async/await support
- **Type Safe**: Comprehensive type hints and runtime validation with Pydantic
- **Production Ready**: Monitoring, logging, and error handling built-in
- **Extensible**: Plugin architecture for custom agents and workflows

## Quick Start

### Prerequisites

- Python 3.10 or higher
- PostgreSQL or MySQL (optional)
- Redis (for caching and message bus)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/multi-agent-database-ai-mvp.git
cd multi-agent-database-ai-mvp
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package in development mode:
```bash
pip install -e ".[dev]"
```

4. Copy environment configuration:
```bash
cp .env.example .env
```

5. Run the development server:
```bash
uvicorn core.api.main:app --reload
```

## Project Structure

```
multi-agent-database-ai-mvp/
├── core/               # Core application code
│   ├── agents/        # Agent implementations
│   ├── database/      # Database connectors and models
│   └── api/          # FastAPI routes and endpoints
├── frontend/          # Web UI (if applicable)
├── sdk/              # Python SDK for external integration
├── config/           # Configuration files
├── tests/            # Test suites
│   ├── unit/        # Unit tests
│   ├── integration/ # Integration tests
│   └── e2e/         # End-to-end tests
├── scripts/          # Utility scripts
└── docs/             # Documentation
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=core --cov-report=html

# Run specific test categories
pytest -m unit
pytest -m integration
pytest -m e2e
```

### Code Quality

```bash
# Format code
black .
isort .

# Type checking
mypy .

# Linting
flake8 .

# Security checks
bandit -r core/
safety check
```

### Pre-commit Hooks

```bash
pre-commit install
pre-commit run --all-files
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Configuration

Configuration is managed through environment variables and YAML files. See `config/` directory for examples.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@example.com or open an issue in the GitHub repository.
