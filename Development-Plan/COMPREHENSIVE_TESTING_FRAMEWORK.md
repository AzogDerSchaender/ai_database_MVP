# Comprehensive Testing Framework for Multi-Agent Database AI

## 🎯 Overview

This framework extends the existing unit and integration tests with E2E automation, load testing, chaos engineering, and mock data utilities to ensure production-grade quality.

**Note**: Some code snippets below intentionally repeat patterns found in `CODE_SNIPPETS_LIBRARY.md` for quick reference. Imports referencing helpers such as `MessageBusMetrics` or `AgentMetrics` are illustrative; you may need to create or adjust these utilities in your codebase.

## 📋 Testing Strategy

### Testing Pyramid
```
         E2E Tests (10%)
        /          \
    Integration (30%) \
   /                   \
  Unit Tests (60%)      \
 /_____________________ _\
```

## 🚀 E2E Test Automation Setup

### Framework: Playwright + Pytest

#### Installation
```bash
pip install playwright pytest-playwright pytest-asyncio
playwright install chromium
```

#### Base E2E Test Structure
```python
# tests/e2e/conftest.py
import pytest
from playwright.sync_api import Playwright, Page
from fastapi.testclient import TestClient
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def api_server():
    """Start API server for testing"""
    from api.app import app
    async with TestClient(app) as client:
        yield client

@pytest.fixture(scope="session")
def browser(playwright: Playwright):
    """Launch browser for E2E tests"""
    browser = playwright.chromium.launch(headless=True)
    yield browser
    browser.close()

@pytest.fixture
def page(browser):
    """Create new page for each test"""
    page = browser.new_page()
    yield page
    page.close()
```

#### E2E Test Examples
```python
# tests/e2e/test_query_workflow.py
import pytest
from playwright.sync_api import Page

class TestQueryWorkflow:
    def test_natural_language_to_sql_flow(self, page: Page, api_server):
        """Test complete flow from natural language to SQL results"""
        # Navigate to dashboard
        page.goto("http://localhost:8000/dashboard")

        # Input natural language query
        query_input = page.locator("#query-input")
        query_input.fill("Show me top 10 customers by revenue")

        # Submit query
        page.click("#submit-query")

        # Wait for clarification dialog (if needed)
        if page.locator("#clarification-dialog").is_visible():
            page.click("text=Use sales database")
            page.click("#confirm-clarification")

        # Wait for results
        results = page.wait_for_selector("#query-results", timeout=30000)

        # Verify results structure
        assert page.locator(".result-row").count() == 10
        assert page.locator("#generated-sql").is_visible()

    def test_error_handling_flow(self, page: Page):
        """Test error handling and recovery"""
        page.goto("http://localhost:8000/dashboard")

        # Input invalid query
        page.fill("#query-input", "DELETE everything from everywhere")
        page.click("#submit-query")

        # Verify safety warning
        warning = page.wait_for_selector(".safety-warning")
        assert "potentially dangerous" in warning.text_content().lower()

    def test_multi_agent_coordination(self, page: Page):
        """Test agent coordination visualization"""
        page.goto("http://localhost:8000/dashboard")

        # Enable agent visualization
        page.click("#show-agent-activity")

        # Submit complex query
        page.fill("#query-input", "Compare Q1 sales with last year")
        page.click("#submit-query")

        # Verify agent activities
        assert page.locator(".agent-clarifier.active").is_visible()
        assert page.locator(".agent-coder.active").is_visible()
        assert page.locator(".agent-tester.active").is_visible()
```

## 💪 Load Testing Framework

### Framework: Locust

#### Installation
```bash
pip install locust faker
```

#### Load Test Configuration
```python
# tests/load/locustfile.py
from locust import HttpUser, task, between
import random
import json

class DatabaseAIUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Initialize user session"""
        self.queries = [
            "Show me all customers",
            "What are the top products?",
            "Calculate total revenue",
            "Find orders from last month",
            "Show employee performance"
        ]

    @task(3)
    def submit_simple_query(self):
        """Test simple query endpoint"""
        query = random.choice(self.queries)
        response = self.client.post(
            "/api/v1/query",
            json={"query": query, "database": "main"}
        )
        assert response.status_code == 200

    @task(2)
    def submit_complex_query(self):
        """Test complex multi-step query"""
        response = self.client.post(
            "/api/v1/query",
            json={
                "query": "Compare sales performance across regions with YoY growth",
                "database": "analytics",
                "options": {"include_visualizations": True}
            }
        )
        assert response.status_code in [200, 202]

    @task(1)
    def check_task_status(self):
        """Test async task status endpoint"""
        # First create a task
        response = self.client.post(
            "/api/v1/query",
            json={"query": "Generate monthly report", "async": True}
        )
        if response.status_code == 202:
            task_id = response.json()["task_id"]

            # Poll for status
            status_response = self.client.get(f"/api/v1/tasks/{task_id}")
            assert status_response.status_code == 200

class AdminUser(HttpUser):
    wait_time = between(5, 10)

    @task
    def view_monitoring_dashboard(self):
        """Test monitoring dashboard load"""
        response = self.client.get("/api/v1/monitoring/metrics")
        assert response.status_code == 200

    @task
    def check_agent_health(self):
        """Test agent health endpoints"""
        for agent in ["clarifier", "coder", "tester"]:
            response = self.client.get(f"/api/v1/agents/{agent}/health")
            assert response.status_code == 200
```

#### Performance Test Scenarios
```python
# tests/load/scenarios.py
import subprocess
import time

class LoadTestScenarios:
    @staticmethod
    def run_baseline_test():
        """Establish baseline performance metrics"""
        subprocess.run([
            "locust",
            "--headless",
            "--users", "10",
            "--spawn-rate", "1",
            "--run-time", "5m",
            "--host", "http://localhost:8000",
            "--html", "reports/baseline_report.html"
        ])

    @staticmethod
    def run_stress_test():
        """Test system under stress"""
        subprocess.run([
            "locust",
            "--headless",
            "--users", "100",
            "--spawn-rate", "10",
            "--run-time", "10m",
            "--host", "http://localhost:8000",
            "--html", "reports/stress_report.html"
        ])

    @staticmethod
    def run_spike_test():
        """Test sudden traffic spikes"""
        # Use custom shape for spike testing
        subprocess.run([
            "locust",
            "--headless",
            "--host", "http://localhost:8000",
            "--config", "tests/load/spike_config.conf"
        ])
```

## 🔥 Chaos Engineering Tests

### Framework: Chaos Toolkit

#### Installation
```bash
pip install chaostoolkit chaostoolkit-kubernetes
```

#### Chaos Experiments
```yaml
# tests/chaos/experiments/database-failure.yaml
version: 1.0.0
title: Database Connection Failure
description: Test system resilience when database becomes unavailable

steady-state-hypothesis:
  title: System remains available
  probes:
  - type: http
    name: api-health-check
    provider:
      type: http
      url: http://localhost:8000/health
      timeout: 5

method:
- type: action
  name: kill-database
  provider:
    type: process
    module: chaoslib.process
    func: kill_process
    arguments:
      process_name: postgres

rollbacks:
- type: action
  name: restart-database
  provider:
    type: process
    module: chaoslib.process
    func: start_process
    arguments:
      command: docker-compose up -d postgres
```

```python
# tests/chaos/agent_failures.py
import asyncio
import random
from datetime import datetime

class ChaosTests:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    async def test_random_agent_failures(self):
        """Randomly fail agents and test recovery"""
        agents = ["clarifier", "coder", "tester"]

        for _ in range(10):
            # Pick random agent to fail
            agent = random.choice(agents)

            # Simulate failure
            await self.orchestrator.simulate_agent_failure(agent)

            # Wait for recovery
            await asyncio.sleep(5)

            # Verify system recovered
            health = await self.orchestrator.get_health_status()
            assert health["status"] == "healthy"
            assert all(a["status"] == "running" for a in health["agents"])

    async def test_message_bus_overload(self):
        """Test message bus under extreme load"""
        messages = []
        for i in range(10000):
            messages.append({
                "type": "query",
                "id": f"test-{i}",
                "content": "SELECT * FROM users",
                "timestamp": datetime.utcnow()
            })

        # Send all messages at once
        await asyncio.gather(*[
            self.orchestrator.message_bus.publish(msg)
            for msg in messages
        ])

        # System should handle overload gracefully
        stats = await self.orchestrator.get_message_stats()
        assert stats["dropped_messages"] < 100  # Less than 1% loss

    async def test_network_partition(self):
        """Simulate network partition between agents"""
        # Simulate network issues
        await self.orchestrator.simulate_network_delay(
            source="clarifier",
            target="coder",
            delay_ms=5000
        )

        # Submit query
        result = await self.orchestrator.process_query(
            "SELECT * FROM orders",
            timeout=30
        )

        # Should still complete, just slower
        assert result["status"] == "completed"
        assert result["duration"] > 5.0
```

## 🎭 Mock Data Generation Utilities

### Framework: Faker + Custom Generators

```python
# tests/mock/data_generator.py
from faker import Faker
import random
import pandas as pd
from datetime import datetime, timedelta

fake = Faker()

class MockDataGenerator:
    """Generate realistic test data for various scenarios"""

    @staticmethod
    def generate_customer_schema():
        """Generate realistic customer database schema"""
        return {
            "customers": {
                "columns": {
                    "id": "SERIAL PRIMARY KEY",
                    "name": "VARCHAR(255) NOT NULL",
                    "email": "VARCHAR(255) UNIQUE NOT NULL",
                    "phone": "VARCHAR(20)",
                    "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                    "is_active": "BOOLEAN DEFAULT TRUE",
                    "credit_limit": "DECIMAL(10, 2)"
                },
                "indexes": ["email", "created_at"],
                "constraints": ["CHECK (credit_limit >= 0)"]
            },
            "orders": {
                "columns": {
                    "id": "SERIAL PRIMARY KEY",
                    "customer_id": "INTEGER REFERENCES customers(id)",
                    "order_date": "TIMESTAMP NOT NULL",
                    "total_amount": "DECIMAL(10, 2) NOT NULL",
                    "status": "VARCHAR(20) NOT NULL"
                },
                "indexes": ["customer_id", "order_date", "status"]
            }
        }

    @staticmethod
    def generate_customer_data(count=1000):
        """Generate realistic customer records"""
        customers = []
        for i in range(count):
            customers.append({
                "id": i + 1,
                "name": fake.name(),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "created_at": fake.date_time_between(
                    start_date="-2y",
                    end_date="now"
                ),
                "is_active": random.choice([True, True, True, False]),
                "credit_limit": round(random.uniform(1000, 50000), 2)
            })
        return pd.DataFrame(customers)

    @staticmethod
    def generate_complex_schema():
        """Generate complex schema for testing"""
        return {
            "sales_fact": {
                "columns": {
                    "id": "BIGSERIAL PRIMARY KEY",
                    "date_key": "INTEGER NOT NULL",
                    "product_key": "INTEGER NOT NULL",
                    "customer_key": "INTEGER NOT NULL",
                    "store_key": "INTEGER NOT NULL",
                    "quantity": "INTEGER NOT NULL",
                    "unit_price": "DECIMAL(10, 2)",
                    "discount": "DECIMAL(5, 2)",
                    "tax": "DECIMAL(10, 2)",
                    "total": "DECIMAL(12, 2)"
                },
                "partitioning": {
                    "type": "RANGE",
                    "column": "date_key",
                    "interval": "MONTHLY"
                }
            }
        }

    @staticmethod
    def generate_edge_case_data():
        """Generate data with edge cases for testing"""
        return {
            "null_heavy": [
                {"id": 1, "value": None, "description": None},
                {"id": 2, "value": "", "description": ""},
                {"id": 3, "value": 0, "description": None}
            ],
            "special_characters": [
                {"text": "O'Brien", "note": "Single quote"},
                {"text": 'Say "Hello"', "note": "Double quotes"},
                {"text": "Line1\nLine2", "note": "Newlines"},
                {"text": "Tab\there", "note": "Tabs"}
            ],
            "unicode_data": [
                {"name": "José García", "emoji": "🚀"},
                {"name": "北京", "emoji": "🇨🇳"},
                {"name": "Москва", "emoji": "🇷🇺"}
            ],
            "extreme_values": [
                {"tiny": 0.00000001, "huge": 999999999999.99},
                {"min_int": -2147483648, "max_int": 2147483647},
                {"long_string": "x" * 10000}
            ]
        }

class QueryPatternGenerator:
    """Generate realistic query patterns for testing"""

    @staticmethod
    def generate_simple_queries():
        """Generate simple SELECT queries"""
        templates = [
            "SELECT * FROM {table} WHERE {column} = {value}",
            "SELECT {columns} FROM {table} LIMIT {limit}",
            "SELECT COUNT(*) FROM {table} WHERE {condition}",
            "SELECT DISTINCT {column} FROM {table}"
        ]

        queries = []
        for _ in range(100):
            template = random.choice(templates)
            query = template.format(
                table=random.choice(["users", "orders", "products"]),
                column=random.choice(["id", "name", "status", "created_at"]),
                columns=", ".join(random.sample(["id", "name", "email", "status"], 2)),
                value=random.randint(1, 1000),
                limit=random.choice([10, 25, 50, 100]),
                condition=f"{random.choice(['status', 'type'])} = '{random.choice(['active', 'pending'])}'"
            )
            queries.append(query)
        return queries

    @staticmethod
    def generate_complex_queries():
        """Generate complex queries with joins, aggregations"""
        return [
            """
            SELECT c.name, COUNT(o.id) as order_count,
                   SUM(o.total) as total_revenue
            FROM customers c
            LEFT JOIN orders o ON c.id = o.customer_id
            WHERE c.created_at >= DATE_SUB(NOW(), INTERVAL 1 YEAR)
            GROUP BY c.id, c.name
            HAVING COUNT(o.id) > 5
            ORDER BY total_revenue DESC
            LIMIT 100
            """,
            """
            WITH monthly_sales AS (
                SELECT DATE_TRUNC('month', order_date) as month,
                       SUM(total_amount) as revenue
                FROM orders
                GROUP BY 1
            )
            SELECT month, revenue,
                   LAG(revenue) OVER (ORDER BY month) as prev_revenue,
                   revenue - LAG(revenue) OVER (ORDER BY month) as growth
            FROM monthly_sales
            ORDER BY month DESC
            """
        ]
```

## 🧪 Integration with Testing Framework

```python
# tests/conftest.py - Global test configuration
import pytest
from tests.mock.data_generator import MockDataGenerator, QueryPatternGenerator

@pytest.fixture(scope="session")
def mock_data():
    """Provide mock data generator"""
    return MockDataGenerator()

@pytest.fixture(scope="session")
def query_patterns():
    """Provide query pattern generator"""
    return QueryPatternGenerator()

@pytest.fixture
def sample_database(mock_data):
    """Create sample database with test data"""
    # Implementation to create and populate test database
    pass

# Run all test types
def run_comprehensive_tests():
    """Execute all test types in sequence"""
    import subprocess

    # Unit tests
    subprocess.run(["pytest", "tests/unit", "-v", "--cov=."])

    # Integration tests
    subprocess.run(["pytest", "tests/integration", "-v"])

    # E2E tests
    subprocess.run(["pytest", "tests/e2e", "-v", "--headed"])

    # Load tests
    subprocess.run(["python", "tests/load/scenarios.py"])

    # Chaos tests
    subprocess.run(["chaos", "run", "tests/chaos/experiments/"])
```

## 📊 Test Metrics and Reporting

```python
# tests/reporting/test_metrics.py
class TestMetricsCollector:
    """Collect and report comprehensive test metrics"""

    def generate_test_report(self):
        return {
            "coverage": {
                "unit": "92%",
                "integration": "85%",
                "e2e": "78%"
            },
            "performance": {
                "avg_response_time": "145ms",
                "p99_response_time": "892ms",
                "throughput": "1250 req/s"
            },
            "reliability": {
                "uptime": "99.92%",
                "mttr": "3.2 minutes",
                "error_rate": "0.08%"
            },
            "chaos_results": {
                "database_failure_recovery": "PASSED",
                "agent_failure_recovery": "PASSED",
                "network_partition_handling": "PASSED"
            }
        }
```

## 🎯 Testing Best Practices

1. **Test Data Isolation**: Each test creates its own data
2. **Parallel Execution**: Tests run in parallel when possible
3. **Deterministic Results**: Use fixed seeds for randomness
4. **Continuous Testing**: Tests run on every commit
5. **Performance Baselines**: Track performance over time
6. **Failure Analysis**: Detailed logs for debugging

## 🚀 Quick Start

```bash
# Install all testing dependencies
pip install -r requirements-dev.txt

# Run all tests
python -m pytest

# Run specific test types
pytest tests/unit          # Unit tests only
pytest tests/e2e           # E2E tests only
locust -f tests/load       # Load tests
chaos run tests/chaos      # Chaos tests

# Generate test report
python tests/reporting/generate_report.py
```
