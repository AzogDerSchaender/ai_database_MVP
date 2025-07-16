# AI Database MVP

A multi-agent database AI system for intelligent query generation and execution.

## Overview

AI Database MVP is a production-ready system that uses multiple specialized AI agents to understand natural language queries, generate optimized SQL, and execute them safely across various database systems.

## Key Features

- **Multi-Agent Architecture**: Specialized agents for different tasks (clarification, SQL generation, testing, optimization)
- **Database Agnostic**: Supports PostgreSQL, MySQL, SQLite, and more
- **Security First**: Built-in SQL injection prevention and access control
- **Performance Optimized**: Query optimization and caching
- **Production Ready**: Comprehensive testing, monitoring, and documentation

## Quick Start

```bash
# Install the package
pip install ai-database-mvp

# Set up your environment
export OPENAI_API_KEY="your-api-key"
export DATABASE_URL="postgresql://user:pass@localhost/db"

# Run a query
from ai_database_mvp import QueryEngine

engine = QueryEngine()
result = await engine.execute("Show me all users who signed up last month")
```

## Documentation Structure

- **[Getting Started](getting-started/installation.md)**: Installation and setup guides
- **[Architecture](architecture/overview.md)**: System design and components
- **[API Reference](api/rest.md)**: Complete API documentation
- **[Development](CODING_STANDARDS.md)**: Contributing and development guides
- **[Deployment](deployment/docker.md)**: Production deployment guides
- **[Examples](examples/basic.md)**: Usage examples and tutorials

## License

This project is licensed under the MIT License. 