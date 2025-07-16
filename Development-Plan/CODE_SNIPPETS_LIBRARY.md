# Code Snippets Library for Multi-Agent Database AI

## 🎯 Overview

This library contains battle-tested code patterns and snippets optimized for LLM implementation. Copy and adapt these patterns to ensure consistency and avoid common mistakes.

**Disclaimer**: The patterns below may include imports (e.g., `MessageBusMetrics`, `PoolMetrics`) that are placeholders. Implement or substitute these helpers in your actual code. Duplicate examples that also appear in `COMPREHENSIVE_TESTING_FRAMEWORK.md` are provided here for convenience.

## 📚 Table of Contents

1. [Agent Patterns](#agent-patterns)
2. [Database Connection Patterns](#database-connection-patterns)
3. [Error Handling Templates](#error-handling-templates)
4. [Testing Patterns](#testing-patterns)
5. [Message Bus Patterns](#message-bus-patterns)
6. [API Endpoint Patterns](#api-endpoint-patterns)
7. [Security Patterns](#security-patterns)
8. [Performance Optimization Patterns](#performance-optimization-patterns)

---

## 🤖 Agent Patterns

### Base Agent Implementation
```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import asyncio
import logging

class BaseAgent(ABC):
    """Base class for all agents in the system"""

    def __init__(self, agent_id: str, message_bus: MessageBus):
        self.agent_id = agent_id
        self.message_bus = message_bus
        self.logger = logging.getLogger(f"agent.{agent_id}")
        self.is_running = False
        self._capabilities: Dict[str, Any] = {}
        self._metrics = AgentMetrics(agent_id)

    async def initialize(self) -> None:
        """Initialize agent resources"""
        self.logger.info(f"Initializing agent {self.agent_id}")
        await self._register_capabilities()
        await self.message_bus.subscribe(self.agent_id, self._handle_message)
        self.is_running = True

    async def shutdown(self) -> None:
        """Gracefully shutdown agent"""
        self.logger.info(f"Shutting down agent {self.agent_id}")
        self.is_running = False
        await self.message_bus.unsubscribe(self.agent_id)
        await self._cleanup()

    async def _handle_message(self, message: Message) -> None:
        """Handle incoming messages"""
        try:
            self._metrics.record_message_received()
            response = await self.process_message(message)
            if response:
                await self.message_bus.publish(response)
            self._metrics.record_message_processed()
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            await self._handle_error(e, message)

    @abstractmethod
    async def process_message(self, message: Message) -> Optional[Message]:
        """Process a single message - implement in subclass"""
        pass

    @abstractmethod
    async def _register_capabilities(self) -> None:
        """Register agent capabilities - implement in subclass"""
        pass
```

### Clarifier Agent Pattern
```python
class ClarifierAgent(BaseAgent):
    """Agent responsible for clarifying ambiguous queries"""

    def __init__(self, agent_id: str, message_bus: MessageBus,
                 schema_analyzer: SchemaAnalyzer):
        super().__init__(agent_id, message_bus)
        self.schema_analyzer = schema_analyzer
        self.context_builder = ContextBuilder()

    async def _register_capabilities(self) -> None:
        """Register clarifier capabilities"""
        self._capabilities = {
            "analyze_query": True,
            "identify_ambiguities": True,
            "generate_clarifications": True,
            "build_context": True
        }

    async def process_message(self, message: Message) -> Optional[Message]:
        """Process query clarification request"""
        if message.type != MessageType.CLARIFICATION_REQUEST:
            return None

        query = message.data.get("query")
        database = message.data.get("database")

        # Analyze query for ambiguities
        ambiguities = await self._identify_ambiguities(query, database)

        if not ambiguities:
            # No clarification needed
            return Message(
                type=MessageType.CLARIFICATION_COMPLETE,
                data={
                    "original_query": query,
                    "clarified_query": query,
                    "context": await self.context_builder.build(query, database)
                }
            )

        # Generate clarification questions
        questions = await self._generate_questions(ambiguities)

        return Message(
            type=MessageType.CLARIFICATION_NEEDED,
            data={
                "original_query": query,
                "questions": questions,
                "suggestions": await self._generate_suggestions(ambiguities)
            }
        )

    async def _identify_ambiguities(self, query: str, database: str) -> List[Ambiguity]:
        """Identify ambiguous parts of the query"""
        ambiguities = []

        # Check for ambiguous table references
        tables = await self.schema_analyzer.extract_potential_tables(query)
        for table in tables:
            matches = await self.schema_analyzer.find_similar_tables(table, database)
            if len(matches) > 1:
                ambiguities.append(Ambiguity(
                    type="table_reference",
                    value=table,
                    options=matches
                ))

        # Check for ambiguous column references
        # ... implementation ...

        return ambiguities
```

### Coder Agent Pattern
```python
class CoderAgent(BaseAgent):
    """Agent responsible for generating SQL code"""

    def __init__(self, agent_id: str, message_bus: MessageBus,
                 sql_generator: SQLGenerator):
        super().__init__(agent_id, message_bus)
        self.sql_generator = sql_generator
        self.optimizer = QueryOptimizer()

    async def process_message(self, message: Message) -> Optional[Message]:
        """Generate SQL from clarified query"""
        if message.type != MessageType.CODE_GENERATION_REQUEST:
            return None

        try:
            # Extract query details
            clarified_query = message.data.get("clarified_query")
            context = message.data.get("context")

            # Generate SQL
            sql = await self.sql_generator.generate(clarified_query, context)

            # Optimize query
            optimized_sql = await self.optimizer.optimize(sql, context)

            # Add safety checks
            safety_check = await self._perform_safety_check(optimized_sql)

            return Message(
                type=MessageType.CODE_GENERATED,
                data={
                    "sql": optimized_sql,
                    "original_sql": sql,
                    "optimization_applied": sql != optimized_sql,
                    "safety_check": safety_check,
                    "estimated_cost": await self._estimate_cost(optimized_sql)
                }
            )

        except Exception as e:
            self.logger.error(f"Code generation failed: {e}")
            return Message(
                type=MessageType.CODE_GENERATION_FAILED,
                data={"error": str(e), "query": clarified_query}
            )
```

### Tester Agent Pattern
```python
class TesterAgent(BaseAgent):
    """Agent responsible for testing and validating SQL queries"""

    def __init__(self, agent_id: str, message_bus: MessageBus,
                 sandbox: Sandbox):
        super().__init__(agent_id, message_bus)
        self.sandbox = sandbox
        self.validator = QueryValidator()

    async def process_message(self, message: Message) -> Optional[Message]:
        """Test and validate generated SQL"""
        if message.type != MessageType.TEST_REQUEST:
            return None

        sql = message.data.get("sql")
        context = message.data.get("context")

        # Validate syntax
        syntax_result = await self.validator.validate_syntax(sql)
        if not syntax_result.is_valid:
            return Message(
                type=MessageType.TEST_FAILED,
                data={
                    "test_type": "syntax",
                    "errors": syntax_result.errors
                }
            )

        # Test in sandbox
        sandbox_result = await self.sandbox.execute(sql, context)

        # Validate results
        validation_result = await self._validate_results(
            sandbox_result,
            context.get("expected_results")
        )

        return Message(
            type=MessageType.TEST_COMPLETE,
            data={
                "syntax_valid": True,
                "execution_successful": sandbox_result.success,
                "performance_metrics": sandbox_result.metrics,
                "validation_result": validation_result,
                "test_coverage": await self._calculate_coverage(sql, context)
            }
        )
```

---

## 🗄️ Database Connection Patterns

### Base Database Connector
```python
from abc import ABC, abstractmethod
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict, Any, List

class BaseDatabaseConnector(ABC):
    """Base class for all database connectors"""

    def __init__(self, connection_string: str, pool_size: int = 10):
        self.connection_string = connection_string
        self.pool_size = pool_size
        self._pool = None
        self.logger = logging.getLogger(f"db.{self.__class__.__name__}")

    async def initialize(self) -> None:
        """Initialize connection pool"""
        self.logger.info(f"Initializing connection pool with size {self.pool_size}")
        self._pool = await self._create_pool()

    async def close(self) -> None:
        """Close connection pool"""
        if self._pool:
            await self._pool.close()

    @asynccontextmanager
    async def acquire(self) -> AsyncGenerator:
        """Acquire connection from pool"""
        async with self._pool.acquire() as conn:
            yield conn

    @abstractmethod
    async def _create_pool(self):
        """Create connection pool - implement in subclass"""
        pass

    @abstractmethod
    async def execute_query(self, query: str, params: Dict[str, Any] = None) -> List[Dict]:
        """Execute query and return results"""
        pass

    async def test_connection(self) -> bool:
        """Test database connectivity"""
        try:
            async with self.acquire() as conn:
                await conn.execute("SELECT 1")
            return True
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False
```

### PostgreSQL Connector Pattern
```python
import asyncpg
from typing import List, Dict, Any

class PostgreSQLConnector(BaseDatabaseConnector):
    """PostgreSQL specific connector implementation"""

    async def _create_pool(self) -> asyncpg.Pool:
        """Create PostgreSQL connection pool"""
        return await asyncpg.create_pool(
            self.connection_string,
            min_size=2,
            max_size=self.pool_size,
            command_timeout=60,
            max_queries=50000,
            max_cacheable_statement_size=0
        )

    async def execute_query(self, query: str, params: Dict[str, Any] = None) -> List[Dict]:
        """Execute query with proper parameterization"""
        async with self.acquire() as conn:
            # Prepare statement for better performance
            stmt = await conn.prepare(query)

            # Execute with parameters
            if params:
                rows = await stmt.fetch(**params)
            else:
                rows = await stmt.fetch()

            # Convert to list of dicts
            return [dict(row) for row in rows]

    async def execute_in_transaction(self, queries: List[str]) -> None:
        """Execute multiple queries in a transaction"""
        async with self.acquire() as conn:
            async with conn.transaction():
                for query in queries:
                    await conn.execute(query)

    async def get_schema_info(self, schema: str = 'public') -> Dict[str, Any]:
        """Get detailed schema information"""
        query = """
        SELECT
            t.table_name,
            t.table_type,
            array_agg(
                json_build_object(
                    'column_name', c.column_name,
                    'data_type', c.data_type,
                    'is_nullable', c.is_nullable,
                    'column_default', c.column_default
                )
            ) as columns
        FROM information_schema.tables t
        JOIN information_schema.columns c
            ON t.table_name = c.table_name
            AND t.table_schema = c.table_schema
        WHERE t.table_schema = $1
        GROUP BY t.table_name, t.table_type
        """

        return await self.execute_query(query, {'schema': schema})
```

### Connection Pool Manager Pattern
```python
class ConnectionPoolManager:
    """Manages multiple database connection pools"""

    def __init__(self):
        self._pools: Dict[str, BaseDatabaseConnector] = {}
        self._health_checker = HealthChecker()

    async def add_connection(self, name: str, connector: BaseDatabaseConnector) -> None:
        """Add a new database connection"""
        await connector.initialize()
        self._pools[name] = connector

        # Start health monitoring
        asyncio.create_task(self._monitor_health(name, connector))

    async def get_connection(self, name: str) -> BaseDatabaseConnector:
        """Get connection by name"""
        if name not in self._pools:
            raise ValueError(f"No connection found with name: {name}")
        return self._pools[name]

    async def _monitor_health(self, name: str, connector: BaseDatabaseConnector) -> None:
        """Monitor connection health"""
        while name in self._pools:
            try:
                is_healthy = await connector.test_connection()
                await self._health_checker.update(name, is_healthy)

                if not is_healthy:
                    self.logger.warning(f"Connection {name} is unhealthy")
                    # Attempt to reconnect
                    await connector.close()
                    await connector.initialize()

            except Exception as e:
                self.logger.error(f"Health check failed for {name}: {e}")

            await asyncio.sleep(30)  # Check every 30 seconds
```

---

## ❌ Error Handling Templates

### Custom Exception Hierarchy
```python
class DatabaseAIException(Exception):
    """Base exception for all custom exceptions"""
    def __init__(self, message: str, error_code: str = None, details: Dict = None):
        super().__init__(message)
        self.error_code = error_code
        self.details = details or {}
        self.timestamp = datetime.utcnow()

class QueryException(DatabaseAIException):
    """Raised when query processing fails"""
    pass

class ValidationException(DatabaseAIException):
    """Raised when validation fails"""
    pass

class SecurityException(DatabaseAIException):
    """Raised when security check fails"""
    pass

class AgentException(DatabaseAIException):
    """Raised when agent operation fails"""
    pass

class ConnectionException(DatabaseAIException):
    """Raised when database connection fails"""
    pass
```

### Global Error Handler
```python
from fastapi import Request, status
from fastapi.responses import JSONResponse
import traceback

class GlobalErrorHandler:
    """Centralized error handling for the application"""

    def __init__(self, app):
        self.app = app
        self.logger = logging.getLogger("error_handler")
        self._register_handlers()

    def _register_handlers(self):
        """Register exception handlers"""

        @self.app.exception_handler(ValidationException)
        async def validation_exception_handler(request: Request, exc: ValidationException):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "Validation Error",
                    "message": str(exc),
                    "error_code": exc.error_code,
                    "details": exc.details,
                    "timestamp": exc.timestamp.isoformat()
                }
            )

        @self.app.exception_handler(SecurityException)
        async def security_exception_handler(request: Request, exc: SecurityException):
            # Log security exceptions with full context
            self.logger.error(
                f"Security exception: {exc}",
                extra={
                    "user_id": getattr(request.state, "user_id", None),
                    "ip_address": request.client.host,
                    "endpoint": request.url.path,
                    "details": exc.details
                }
            )

            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "error": "Security Error",
                    "message": "Access denied",  # Don't expose details
                    "error_code": "SECURITY_ERROR",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )

        @self.app.exception_handler(Exception)
        async def general_exception_handler(request: Request, exc: Exception):
            # Log full traceback
            self.logger.error(
                f"Unhandled exception: {exc}",
                exc_info=True,
                extra={
                    "endpoint": request.url.path,
                    "method": request.method,
                    "traceback": traceback.format_exc()
                }
            )

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred",
                    "error_code": "INTERNAL_ERROR",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
```

### Retry Pattern with Exponential Backoff
```python
import asyncio
from functools import wraps
from typing import TypeVar, Callable, Any

T = TypeVar('T')

def retry_with_backoff(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """Decorator for retrying operations with exponential backoff"""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            delay = initial_delay
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt == max_attempts - 1:
                        # Last attempt, re-raise
                        raise

                    # Log retry attempt
                    logger = logging.getLogger(func.__module__)
                    logger.warning(
                        f"Attempt {attempt + 1} failed for {func.__name__}: {e}. "
                        f"Retrying in {delay:.2f} seconds..."
                    )

                    # Wait before retry
                    await asyncio.sleep(delay)

                    # Calculate next delay
                    delay = min(delay * exponential_base, max_delay)

            raise last_exception

        return wrapper
    return decorator

# Usage example
@retry_with_backoff(max_attempts=3, exceptions=(ConnectionException,))
async def connect_to_database():
    """Connect to database with automatic retry"""
    # Connection logic here
    pass
```

### Circuit Breaker Pattern
```python
from enum import Enum
from datetime import datetime, timedelta
import asyncio

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    """Circuit breaker for preventing cascading failures"""

    def __init__(self,
                 failure_threshold: int = 5,
                 recovery_timeout: int = 60,
                 expected_exception: type = Exception):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception

        self._failure_count = 0
        self._last_failure_time = None
        self._state = CircuitState.CLOSED

    async def call(self, func: Callable, *args, **kwargs):
        """Execute function through circuit breaker"""
        if self._state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self._state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise

    def _should_attempt_reset(self) -> bool:
        """Check if we should try to reset the circuit"""
        return (
            self._last_failure_time and
            datetime.utcnow() - self._last_failure_time > timedelta(seconds=self.recovery_timeout)
        )

    def _on_success(self):
        """Handle successful call"""
        self._failure_count = 0
        self._state = CircuitState.CLOSED

    def _on_failure(self):
        """Handle failed call"""
        self._failure_count += 1
        self._last_failure_time = datetime.utcnow()

        if self._failure_count >= self.failure_threshold:
            self._state = CircuitState.OPEN
```

---

## 🧪 Testing Patterns

### Async Test Base Class
```python
import pytest
import asyncio
from typing import AsyncGenerator

class AsyncTestBase:
    """Base class for async tests"""

    @pytest.fixture(autouse=True)
    async def setup_teardown(self):
        """Setup and teardown for each test"""
        # Setup
        await self.async_setup()

        yield

        # Teardown
        await self.async_teardown()

    async def async_setup(self):
        """Override in subclass for custom setup"""
        pass

    async def async_teardown(self):
        """Override in subclass for custom teardown"""
        pass

    @pytest.fixture
    async def message_bus(self) -> AsyncGenerator[MessageBus, None]:
        """Provide message bus for tests"""
        bus = MessageBus()
        await bus.initialize()
        yield bus
        await bus.shutdown()
```

### Mock Agent for Testing
```python
class MockAgent(BaseAgent):
    """Mock agent for testing agent interactions"""

    def __init__(self, agent_id: str, message_bus: MessageBus):
        super().__init__(agent_id, message_bus)
        self.received_messages = []
        self.responses = {}

    async def _register_capabilities(self) -> None:
        self._capabilities = {"test": True}

    async def process_message(self, message: Message) -> Optional[Message]:
        """Store received messages and return configured response"""
        self.received_messages.append(message)

        # Return configured response if available
        response_key = f"{message.type}:{message.data.get('key', '')}"
        if response_key in self.responses:
            return self.responses[response_key]

        return None

    def configure_response(self, message_type: str, key: str, response: Message):
        """Configure response for specific message"""
        self.responses[f"{message_type}:{key}"] = response
```

### Database Test Fixtures
```python
@pytest.fixture
async def test_database():
    """Provide test database with sample data"""
    connector = PostgreSQLConnector("postgresql://test:test@localhost/test_db")
    await connector.initialize()

    # Create test schema
    async with connector.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS test_users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255) UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Insert test data
        await conn.execute("""
            INSERT INTO test_users (name, email) VALUES
            ('Test User 1', 'test1@example.com'),
            ('Test User 2', 'test2@example.com')
        """)

    yield connector

    # Cleanup
    async with connector.acquire() as conn:
        await conn.execute("DROP TABLE IF EXISTS test_users")
    await connector.close()
```

### Performance Test Pattern
```python
import time
import statistics

class PerformanceTest:
    """Base class for performance tests"""

    async def measure_performance(self,
                                 func: Callable,
                                 iterations: int = 100,
                                 warmup: int = 10) -> Dict[str, float]:
        """Measure function performance"""
        times = []

        # Warmup runs
        for _ in range(warmup):
            await func()

        # Measured runs
        for _ in range(iterations):
            start = time.perf_counter()
            await func()
            end = time.perf_counter()
            times.append(end - start)

        return {
            "min": min(times) * 1000,  # Convert to ms
            "max": max(times) * 1000,
            "mean": statistics.mean(times) * 1000,
            "median": statistics.median(times) * 1000,
            "p95": statistics.quantiles(times, n=20)[18] * 1000,
            "p99": statistics.quantiles(times, n=100)[98] * 1000
        }
```

---

## 📨 Message Bus Patterns

### Message Bus Implementation
```python
from collections import defaultdict
from typing import Dict, List, Callable, Any
import asyncio
import uuid

class MessageBus:
    """Central message bus for agent communication"""

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._message_queue: asyncio.Queue = asyncio.Queue()
        self._running = False
        self._metrics = MessageBusMetrics()

    async def initialize(self) -> None:
        """Start message processing"""
        self._running = True
        asyncio.create_task(self._process_messages())

    async def shutdown(self) -> None:
        """Stop message processing"""
        self._running = False

    async def publish(self, message: Message) -> None:
        """Publish message to bus"""
        message.id = str(uuid.uuid4())
        message.timestamp = datetime.utcnow()

        await self._message_queue.put(message)
        self._metrics.record_published()

    async def subscribe(self, topic: str, handler: Callable) -> None:
        """Subscribe to messages on topic"""
        self._subscribers[topic].append(handler)

    async def unsubscribe(self, topic: str, handler: Callable = None) -> None:
        """Unsubscribe from topic"""
        if handler:
            self._subscribers[topic].remove(handler)
        else:
            self._subscribers[topic].clear()

    async def _process_messages(self) -> None:
        """Process messages from queue"""
        while self._running:
            try:
                message = await asyncio.wait_for(
                    self._message_queue.get(),
                    timeout=1.0
                )

                # Deliver to subscribers
                handlers = self._subscribers.get(message.topic, [])

                if handlers:
                    await asyncio.gather(*[
                        self._safe_handler_call(handler, message)
                        for handler in handlers
                    ])

                self._metrics.record_delivered(len(handlers))

            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self.logger.error(f"Error processing message: {e}")

    async def _safe_handler_call(self, handler: Callable, message: Message) -> None:
        """Safely call handler with error handling"""
        try:
            await handler(message)
        except Exception as e:
            self.logger.error(f"Handler {handler.__name__} failed: {e}")
            self._metrics.record_handler_error()
```

---

## 🌐 API Endpoint Patterns

### RESTful API Pattern
```python
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel, Field

# Request/Response Models
class QueryRequest(BaseModel):
    query: str = Field(..., description="Natural language query")
    database: str = Field(..., description="Target database name")
    options: Optional[Dict[str, Any]] = Field(default={})

class QueryResponse(BaseModel):
    task_id: str
    status: str
    sql: Optional[str] = None
    results: Optional[List[Dict]] = None
    error: Optional[str] = None

# Router setup
router = APIRouter(prefix="/api/v1", tags=["queries"])

# Dependency injection
async def get_orchestrator() -> Orchestrator:
    """Dependency to get orchestrator instance"""
    return app.state.orchestrator

@router.post("/query", response_model=QueryResponse, status_code=status.HTTP_202_ACCEPTED)
async def submit_query(
    request: QueryRequest,
    orchestrator: Orchestrator = Depends(get_orchestrator)
) -> QueryResponse:
    """Submit a natural language query for processing"""
    try:
        # Validate request
        if not request.query.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Query cannot be empty"
            )

        # Submit to orchestrator
        task_id = await orchestrator.submit_query(
            query=request.query,
            database=request.database,
            options=request.options
        )

        return QueryResponse(
            task_id=task_id,
            status="processing"
        )

    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Query submission failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
```

### WebSocket Pattern
```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import Set
import json

class ConnectionManager:
    """Manage WebSocket connections"""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        """Accept new connection"""
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove connection"""
        self.active_connections.discard(websocket)

    async def broadcast(self, message: dict):
        """Broadcast message to all connections"""
        message_json = json.dumps(message)

        # Send to all connections
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_text(message_json)
            except:
                disconnected.add(connection)

        # Clean up disconnected
        self.active_connections -= disconnected

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)

    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            message = json.loads(data)

            # Handle different message types
            if message["type"] == "subscribe":
                # Subscribe to task updates
                task_id = message["task_id"]
                # ... subscription logic ...

            elif message["type"] == "ping":
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

---

## 🔒 Security Patterns

### SQL Injection Prevention
```python
class SQLSanitizer:
    """Sanitize and validate SQL queries"""

    DANGEROUS_PATTERNS = [
        r";\s*DROP\s+",
        r";\s*DELETE\s+",
        r";\s*UPDATE\s+",
        r";\s*INSERT\s+",
        r"--",
        r"/\*.*\*/",
        r"xp_cmdshell",
        r"EXEC\s*\("
    ]

    @classmethod
    def is_safe(cls, query: str) -> Tuple[bool, Optional[str]]:
        """Check if query is safe to execute"""
        query_upper = query.upper()

        # Check for dangerous patterns
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, query_upper):
                return False, f"Dangerous pattern detected: {pattern}"

        # Check for multiple statements
        if query.count(';') > 1:
            return False, "Multiple statements not allowed"

        return True, None

    @classmethod
    def parameterize_query(cls, query: str, params: Dict[str, Any]) -> Tuple[str, List]:
        """Convert query to parameterized form"""
        # Replace :param_name with $1, $2, etc.
        param_list = []
        param_counter = 1

        def replace_param(match):
            nonlocal param_counter
            param_name = match.group(1)
            if param_name in params:
                param_list.append(params[param_name])
                result = f"${param_counter}"
                param_counter += 1
                return result
            return match.group(0)

        parameterized = re.sub(r':(\w+)', replace_param, query)
        return parameterized, param_list
```

### Authentication & Authorization
```python
from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

class AuthHandler:
    """Handle authentication and authorization"""

    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.algorithm = "HS256"

    def decode_token(self, token: str) -> Dict[str, Any]:
        """Decode and validate JWT token"""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    def verify_permission(self,
                         credentials: HTTPAuthorizationCredentials,
                         required_permission: str) -> Dict[str, Any]:
        """Verify user has required permission"""
        token = credentials.credentials
        payload = self.decode_token(token)

        permissions = payload.get("permissions", [])
        if required_permission not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )

        return payload

# Usage in endpoint
@router.post("/admin/clear-cache")
async def clear_cache(
    credentials: HTTPAuthorizationCredentials = Security(security),
    auth: AuthHandler = Depends(get_auth_handler)
):
    """Admin endpoint requiring special permission"""
    user = auth.verify_permission(credentials, "admin:cache:clear")
    # ... endpoint logic ...
```

---

## ⚡ Performance Optimization Patterns

### Caching Pattern
```python
from functools import lru_cache
import hashlib
import pickle

class CacheManager:
    """Manage different caching strategies"""

    def __init__(self, redis_client):
        self.redis = redis_client
        self.local_cache = {}

    async def get_or_compute(self,
                           key: str,
                           compute_func: Callable,
                           ttl: int = 3600) -> Any:
        """Get from cache or compute and store"""
        # Try local cache first
        if key in self.local_cache:
            return self.local_cache[key]

        # Try Redis
        cached = await self.redis.get(key)
        if cached:
            value = pickle.loads(cached)
            self.local_cache[key] = value
            return value

        # Compute value
        value = await compute_func()

        # Store in both caches
        self.local_cache[key] = value
        await self.redis.setex(
            key,
            ttl,
            pickle.dumps(value)
        )

        return value

    def cache_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments"""
        key_data = {"args": args, "kwargs": kwargs}
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()
```

### Connection Pooling Pattern
```python
class OptimizedConnectionPool:
    """Optimized connection pool with monitoring"""

    def __init__(self,
                 create_conn_func: Callable,
                 min_size: int = 5,
                 max_size: int = 20):
        self.create_conn = create_conn_func
        self.min_size = min_size
        self.max_size = max_size

        self._pool: asyncio.Queue = asyncio.Queue(maxsize=max_size)
        self._size = 0
        self._metrics = PoolMetrics()

    async def initialize(self):
        """Pre-create minimum connections"""
        for _ in range(self.min_size):
            conn = await self.create_conn()
            await self._pool.put(conn)
            self._size += 1

    async def acquire(self, timeout: float = 5.0):
        """Acquire connection with timeout"""
        start = time.time()

        try:
            # Try to get existing connection
            conn = await asyncio.wait_for(
                self._pool.get(),
                timeout=0.1
            )
            self._metrics.record_hit()

        except asyncio.TimeoutError:
            # Create new connection if under limit
            if self._size < self.max_size:
                conn = await self.create_conn()
                self._size += 1
                self._metrics.record_miss()
            else:
                # Wait for connection
                conn = await asyncio.wait_for(
                    self._pool.get(),
                    timeout=timeout
                )
                self._metrics.record_wait()

        self._metrics.record_acquire_time(time.time() - start)
        return conn

    async def release(self, conn):
        """Return connection to pool"""
        try:
            await self._pool.put(conn)
        except asyncio.QueueFull:
            # Pool is full, close connection
            await conn.close()
            self._size -= 1
```

### Batch Processing Pattern
```python
class BatchProcessor:
    """Process items in batches for efficiency"""

    def __init__(self,
                 process_func: Callable,
                 batch_size: int = 100,
                 flush_interval: float = 1.0):
        self.process_func = process_func
        self.batch_size = batch_size
        self.flush_interval = flush_interval

        self._buffer = []
        self._lock = asyncio.Lock()
        self._flush_task = None

    async def add(self, item: Any) -> None:
        """Add item to batch"""
        async with self._lock:
            self._buffer.append(item)

            if len(self._buffer) >= self.batch_size:
                await self._flush()
            elif not self._flush_task:
                # Schedule flush
                self._flush_task = asyncio.create_task(
                    self._scheduled_flush()
                )

    async def _flush(self) -> None:
        """Process current batch"""
        if not self._buffer:
            return

        batch = self._buffer.copy()
        self._buffer.clear()

        # Cancel scheduled flush
        if self._flush_task:
            self._flush_task.cancel()
            self._flush_task = None

        # Process batch
        await self.process_func(batch)

    async def _scheduled_flush(self) -> None:
        """Flush after interval"""
        await asyncio.sleep(self.flush_interval)
        async with self._lock:
            await self._flush()
```

## 📚 Usage Guidelines

### When to Use Each Pattern

1. **Agent Patterns**: Use when implementing new agents or extending existing ones
2. **Database Patterns**: Use for any database interaction, especially when adding new connectors
3. **Error Handling**: Apply globally for consistent error management
4. **Testing Patterns**: Use for all new test implementations
5. **Message Bus**: Use for all inter-agent communication
6. **API Patterns**: Use when adding new endpoints
7. **Security Patterns**: Apply to all user-facing interfaces
8. **Performance Patterns**: Use when optimizing bottlenecks

### Best Practices

1. **Always use type hints** for better IDE support and LLM understanding
2. **Include docstrings** with clear descriptions
3. **Handle all exceptions** explicitly
4. **Use async/await** consistently
5. **Log important events** with appropriate levels
6. **Write tests** for all patterns you implement
7. **Monitor performance** of critical paths

### Common Pitfalls to Avoid

1. **Don't forget error handling** in async code
2. **Don't mix sync and async** operations
3. **Don't ignore connection limits** in pools
4. **Don't trust user input** - always validate
5. **Don't log sensitive data** like passwords
6. **Don't use global state** - use dependency injection

## 🚀 Quick Reference

```python
# Import commonly used patterns
from patterns.agents import BaseAgent, ClarifierAgent, CoderAgent, TesterAgent
from patterns.database import BaseDatabaseConnector, PostgreSQLConnector
from patterns.errors import retry_with_backoff, CircuitBreaker, GlobalErrorHandler
from patterns.testing import AsyncTestBase, MockAgent, PerformanceTest
from patterns.api import router, ConnectionManager
from patterns.security import SQLSanitizer, AuthHandler
from patterns.performance import CacheManager, BatchProcessor
```

This snippets library provides production-ready patterns that have been tested and optimized for the multi-agent database AI system. Each pattern includes error handling, logging, and performance considerations.
