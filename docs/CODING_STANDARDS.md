# AI Database MVP - Coding Standards

> Production-grade coding standards for consistent, maintainable, and secure code

## Table of Contents

1. [Core Principles](#core-principles)
2. [Python Code Style](#python-code-style)
3. [Naming Conventions](#naming-conventions)
4. [Documentation Standards](#documentation-standards)
5. [Error Handling Patterns](#error-handling-patterns)
6. [Security Best Practices](#security-best-practices)
7. [Testing Standards](#testing-standards)
8. [Performance Guidelines](#performance-guidelines)
9. [Cursor AI Workflow Tips](#cursor-ai-workflow-tips)
10. [Code Review Checklist](#code-review-checklist)

## Core Principles

### 1. Production Quality First
- Write code as if it's going to production tomorrow
- No shortcuts, no "temporary" hacks
- Every line of code should be maintainable

### 2. Security by Design
- Never trust user input
- Follow principle of least privilege
- Sanitize all data before processing
- Use parameterized queries always

### 3. Performance Matters
- Profile before optimizing
- Use async/await consistently
- Cache expensive operations
- Monitor resource usage

### 4. Explicit is Better than Implicit
- Clear variable names over brevity
- Type hints on all functions
- Document non-obvious behavior
- No magic numbers or strings

## Python Code Style

### General Rules

```python
# Good: Clear, explicit, typed
async def fetch_user_by_id(user_id: int) -> Optional[User]:
    """Fetch a user by their ID from the database."""
    try:
        return await db.users.get(user_id)
    except DatabaseError as e:
        logger.error(f"Failed to fetch user {user_id}: {e}")
        raise UserNotFoundError(f"User {user_id} not found") from e

# Bad: Unclear, untyped, poor error handling
def get_user(id):
    return db.users.get(id)
```

### Line Length and Formatting
- Maximum line length: 100 characters
- Use Black formatter (configured in pyproject.toml)
- Break long lines at logical points:

```python
# Good: Logical line breaks
user_permissions = await permission_service.get_user_permissions(
    user_id=user.id,
    resource_type=ResourceType.DATABASE,
    include_inherited=True,
)

# Bad: Arbitrary breaks
user_permissions = await permission_service.\
    get_user_permissions(user_id=user.id, resource_type=\
    ResourceType.DATABASE, include_inherited=True)
```

### Import Organization
- Use isort for automatic import sorting
- Group imports: standard library, third-party, local

```python
# Standard library imports
import asyncio
import json
from pathlib import Path
from typing import Dict, List, Optional

# Third-party imports
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

# Local imports
from core.database import get_session
from core.models import User
from core.utils import calculate_hash
```

## Naming Conventions

### Variables and Functions
- Use `snake_case` for variables and functions
- Be descriptive but concise
- Avoid abbreviations unless widely understood

```python
# Good
user_authentication_token = generate_token()
async def validate_database_connection(connection_string: str) -> bool:
    pass

# Bad
usr_auth_tok = gen_tok()
async def val_db_conn(cs: str) -> bool:
    pass
```

### Classes
- Use `PascalCase` for classes
- Suffix with purpose when appropriate

```python
# Good
class DatabaseConnectionManager:
    pass

class UserAuthenticationService:
    pass

class QueryOptimizationEngine:
    pass

# Bad
class DBConnMgr:
    pass

class auth_service:
    pass
```

### Constants
- Use `SCREAMING_SNAKE_CASE` for constants
- Define at module level

```python
# Good
MAX_RETRY_ATTEMPTS = 3
DEFAULT_TIMEOUT_SECONDS = 30
SUPPORTED_DATABASE_TYPES = ["postgresql", "mysql", "sqlite"]

# Bad
max_retries = 3
DefaultTimeout = 30
```

### Private Methods and Variables
- Prefix with single underscore for internal use
- Double underscore only for name mangling (rare)

```python
class QueryProcessor:
    def __init__(self):
        self._cache = {}  # Internal cache
        self._is_initialized = False
    
    def _validate_query(self, query: str) -> bool:
        """Internal method for query validation."""
        return bool(query.strip())
```

## Documentation Standards

### Module Documentation
Every Python file should start with a module docstring:

```python
"""
User authentication and authorization module.

This module provides functionality for:
- User authentication via JWT tokens
- Role-based access control (RBAC)
- Session management
- Password hashing and validation

Example:
    >>> from core.auth import authenticate_user
    >>> user = await authenticate_user(email="user@example.com", password="secure123")
    >>> print(user.id)
    12345
"""
```

### Function Documentation
Use Google-style docstrings:

```python
async def execute_query(
    query: str,
    database: str,
    parameters: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
) -> QueryResult:
    """
    Execute a SQL query against the specified database.
    
    Args:
        query: The SQL query to execute
        database: Name of the target database
        parameters: Optional query parameters for parameterized queries
        timeout: Query timeout in seconds (default: 30)
    
    Returns:
        QueryResult containing the execution results and metadata
    
    Raises:
        DatabaseConnectionError: If unable to connect to the database
        QueryExecutionError: If the query fails to execute
        TimeoutError: If the query exceeds the timeout limit
    
    Example:
        >>> result = await execute_query(
        ...     "SELECT * FROM users WHERE age > :age",
        ...     database="production",
        ...     parameters={"age": 18}
        ... )
        >>> print(f"Found {result.row_count} users")
    """
```

### Class Documentation

```python
class AgentOrchestrator:
    """
    Manages the lifecycle and coordination of AI agents.
    
    The AgentOrchestrator is responsible for:
    - Starting and stopping agents
    - Routing messages between agents
    - Managing agent state and health
    - Handling agent failures and recovery
    
    Attributes:
        agents: Dictionary of registered agents
        message_bus: Message bus for inter-agent communication
        config: Orchestrator configuration
    
    Example:
        >>> orchestrator = AgentOrchestrator(config)
        >>> await orchestrator.start()
        >>> await orchestrator.register_agent(ClarifierAgent())
    """
```

### Inline Comments
- Use sparingly, only when code isn't self-explanatory
- Explain "why", not "what"

```python
# Good: Explains why
# Use exponential backoff to avoid overwhelming the service
retry_delay = min(2 ** attempt, MAX_RETRY_DELAY)

# Bad: States the obvious
# Increment counter by 1
counter += 1
```

## Error Handling Patterns

### Custom Exceptions

```python
# Define specific exceptions for different error scenarios
class DatabaseError(Exception):
    """Base exception for database-related errors."""
    pass

class QueryExecutionError(DatabaseError):
    """Raised when a query fails to execute."""
    def __init__(self, query: str, original_error: Exception):
        self.query = query
        self.original_error = original_error
        super().__init__(f"Failed to execute query: {query[:50]}...")

class ConnectionPoolExhaustedError(DatabaseError):
    """Raised when no database connections are available."""
    pass
```

### Error Handling Best Practices

```python
async def safe_database_operation():
    """Demonstrate proper error handling."""
    connection = None
    try:
        # Acquire resources
        connection = await get_connection()
        
        # Perform operation
        result = await connection.execute(query)
        
        # Process result
        return process_result(result)
        
    except asyncpg.PostgresError as e:
        # Log specific database errors
        logger.error(f"PostgreSQL error: {e}", exc_info=True)
        raise QueryExecutionError(query, e) from e
        
    except Exception as e:
        # Log unexpected errors
        logger.critical(f"Unexpected error in database operation: {e}", exc_info=True)
        raise
        
    finally:
        # Always clean up resources
        if connection:
            await connection.close()
```

### Validation and Early Returns

```python
def validate_query_parameters(
    query: str,
    parameters: Dict[str, Any],
    max_limit: int = 1000
) -> None:
    """Validate query parameters before execution."""
    # Early validation checks
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")
    
    if "limit" in parameters and parameters["limit"] > max_limit:
        raise ValueError(f"Limit cannot exceed {max_limit}")
    
    # Check for SQL injection attempts
    if any(danger in query.lower() for danger in ["drop", "truncate", "delete"]):
        logger.warning(f"Potentially dangerous query attempted: {query}")
        raise SecurityError("Query contains restricted keywords")
```

## Security Best Practices

### Input Validation

```python
from pydantic import BaseModel, validator, SecretStr

class UserCredentials(BaseModel):
    """Secure user credentials model."""
    email: str
    password: SecretStr
    
    @validator("email")
    def validate_email(cls, v):
        """Validate email format and domain."""
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", v):
            raise ValueError("Invalid email format")
        
        # Additional domain validation
        if v.endswith("@tempmail.com"):
            raise ValueError("Temporary email addresses not allowed")
        
        return v.lower()
    
    @validator("password")
    def validate_password(cls, v):
        """Ensure password meets security requirements."""
        password = v.get_secret_value()
        
        if len(password) < 12:
            raise ValueError("Password must be at least 12 characters")
        
        if not any(c.isupper() for c in password):
            raise ValueError("Password must contain uppercase letters")
        
        if not any(c.isdigit() for c in password):
            raise ValueError("Password must contain numbers")
        
        return v
```

### SQL Injection Prevention

```python
# Always use parameterized queries
async def get_user_by_email(email: str) -> Optional[User]:
    """Safely fetch user by email."""
    # Good: Parameterized query
    query = "SELECT * FROM users WHERE email = :email"
    result = await db.fetch_one(query, {"email": email})
    
    # Bad: String concatenation (NEVER DO THIS)
    # query = f"SELECT * FROM users WHERE email = '{email}'"
    
    return User(**result) if result else None
```

### Secrets Management

```python
import os
from functools import lru_cache

@lru_cache()
def get_secret(key: str) -> str:
    """Retrieve secret from environment or secret manager."""
    # Check environment first
    secret = os.environ.get(key)
    
    if not secret:
        # Fall back to secret manager (e.g., AWS Secrets Manager)
        try:
            secret = secret_manager.get_secret(key)
        except Exception as e:
            logger.error(f"Failed to retrieve secret {key}: {e}")
            raise ConfigurationError(f"Missing required secret: {key}")
    
    return secret

# Usage
database_password = get_secret("DATABASE_PASSWORD")
api_key = get_secret("OPENAI_API_KEY")
```

## Testing Standards

### Test Structure

```python
import pytest
from unittest.mock import Mock, AsyncMock

class TestUserService:
    """Test suite for UserService."""
    
    @pytest.fixture
    async def user_service(self):
        """Create UserService instance with mocked dependencies."""
        mock_db = AsyncMock()
        mock_cache = Mock()
        return UserService(db=mock_db, cache=mock_cache)
    
    async def test_create_user_success(self, user_service):
        """Test successful user creation."""
        # Arrange
        user_data = {
            "email": "test@example.com",
            "name": "Test User",
            "password": "SecurePass123!"
        }
        
        # Act
        user = await user_service.create_user(**user_data)
        
        # Assert
        assert user.email == user_data["email"]
        assert user.name == user_data["name"]
        assert user.id is not None
        
    async def test_create_user_duplicate_email(self, user_service):
        """Test user creation with duplicate email."""
        # Arrange
        user_service.db.fetch_one.return_value = {"id": 1}  # Existing user
        
        # Act & Assert
        with pytest.raises(UserAlreadyExistsError):
            await user_service.create_user(
                email="existing@example.com",
                name="Test User",
                password="SecurePass123!"
            )
```

### Test Coverage Requirements
- Minimum 90% code coverage
- 100% coverage for critical paths
- Test all error conditions
- Include performance tests for critical operations

## Performance Guidelines

### Async Best Practices

```python
# Good: Concurrent execution
async def fetch_user_data(user_id: int) -> Dict[str, Any]:
    """Fetch user data concurrently."""
    # Execute queries concurrently
    user_task = asyncio.create_task(get_user(user_id))
    permissions_task = asyncio.create_task(get_permissions(user_id))
    preferences_task = asyncio.create_task(get_preferences(user_id))
    
    # Wait for all results
    user, permissions, preferences = await asyncio.gather(
        user_task, permissions_task, preferences_task
    )
    
    return {
        "user": user,
        "permissions": permissions,
        "preferences": preferences
    }

# Bad: Sequential execution
async def fetch_user_data_slow(user_id: int) -> Dict[str, Any]:
    user = await get_user(user_id)
    permissions = await get_permissions(user_id)
    preferences = await get_preferences(user_id)
    
    return {"user": user, "permissions": permissions, "preferences": preferences}
```

### Caching Strategy

```python
from functools import lru_cache
from typing import Optional
import asyncio

class CachedDatabaseSchema:
    """Cache database schema information."""
    
    def __init__(self, cache_ttl: int = 3600):
        self._cache: Dict[str, Any] = {}
        self._cache_ttl = cache_ttl
        self._cache_timestamps: Dict[str, float] = {}
    
    async def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """Get table schema with caching."""
        # Check cache validity
        if self._is_cache_valid(table_name):
            return self._cache[table_name]
        
        # Fetch from database
        schema = await self._fetch_schema_from_db(table_name)
        
        # Update cache
        self._cache[table_name] = schema
        self._cache_timestamps[table_name] = time.time()
        
        return schema
    
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cached data is still valid."""
        if key not in self._cache:
            return False
        
        age = time.time() - self._cache_timestamps.get(key, 0)
        return age < self._cache_ttl
```

## Cursor AI Workflow Tips

### 1. Effective Code Navigation
- Use `Cmd+P` (Mac) / `Ctrl+P` (Windows) for quick file navigation
- Use `Cmd+Shift+O` for symbol search within files
- Keep related files open in tabs for context

### 2. AI Assistant Best Practices
- Be specific in your prompts
- Provide context about the current task
- Reference specific files or functions

```markdown
# Good prompt example:
"Update the execute_query function in core/database/executor.py to add retry logic 
with exponential backoff. The function should retry up to 3 times for transient 
errors like connection timeouts."

# Bad prompt example:
"Add retry logic to database queries"
```

### 3. Code Generation Tips
- Review generated code carefully
- Always run tests after AI-generated changes
- Use AI for boilerplate, implement critical logic manually

### 4. Refactoring Workflow
1. Write tests first
2. Use AI to suggest refactoring approaches
3. Implement incrementally
4. Run tests after each change
5. Use version control to track changes

### 5. Debugging with AI
- Copy error messages completely
- Include relevant stack traces
- Mention what you've already tried
- Ask for explanation of the error, not just the fix

## Code Review Checklist

### Before Submitting PR
- [ ] All tests pass locally
- [ ] Code follows style guidelines (run `black` and `flake8`)
- [ ] Type hints added for all functions
- [ ] Documentation updated (docstrings, README if needed)
- [ ] No commented-out code
- [ ] No debug print statements
- [ ] Secrets not hardcoded
- [ ] Error handling implemented
- [ ] Logging added for important operations
- [ ] Performance impact considered

### Security Review
- [ ] Input validation implemented
- [ ] SQL injection prevention (parameterized queries)
- [ ] Authentication/authorization checks
- [ ] Sensitive data not logged
- [ ] Rate limiting considered
- [ ] CORS settings appropriate

### Testing Review
- [ ] Unit tests written
- [ ] Integration tests for API endpoints
- [ ] Edge cases covered
- [ ] Error conditions tested
- [ ] Mocks used appropriately
- [ ] Test data doesn't contain real user information

### Documentation Review
- [ ] Function docstrings complete
- [ ] Complex algorithms explained
- [ ] API endpoints documented
- [ ] Configuration options described
- [ ] Examples provided where helpful

---

## Quick Reference

### Common Patterns

```python
# Singleton pattern for shared resources
class DatabaseConnectionPool:
    _instance = None
    _lock = asyncio.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Context manager for resource handling
@asynccontextmanager
async def database_transaction():
    transaction = await db.begin()
    try:
        yield transaction
        await transaction.commit()
    except Exception:
        await transaction.rollback()
        raise

# Decorator for timing functions
def timed(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            duration = time.time() - start
            logger.info(f"{func.__name__} took {duration:.3f}s")
    return wrapper
```

### Common Imports

```python
# Standard library
import asyncio
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Common third-party
import httpx
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

# Project imports
from core.config import settings
from core.database import get_session
from core.exceptions import ApplicationError
```

Remember: These standards are living guidelines. Update them as the project evolves and new patterns emerge. 