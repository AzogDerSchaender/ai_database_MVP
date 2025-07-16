#!/usr/bin/env python3
"""
Error recovery script that provides specific fix prompts for failed implementations.
"""

import sys
from pathlib import Path
from typing import Dict, List

# Recovery procedures for each prompt
RECOVERY_PROCEDURES = {
    "0.1": {
        "common_issues": [
            "Missing pyproject.toml configuration",
            "Incorrect directory structure",
            "Missing __init__.py files",
            "Invalid requirements.txt syntax"
        ],
        "recovery_prompts": [
            """
RECOVERY PROMPT 0.1a: Fix Project Configuration
Fix the project configuration files with these exact requirements:

1. Create pyproject.toml with this structure:
```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "multi-agent-database-ai"
version = "0.1.0"
description = "Multi-Agent Database AI System"
dependencies = [
    "fastapi>=0.108.0",
    "sqlalchemy>=2.0.25",
    "uvicorn>=0.25.0",
    "pydantic>=2.5.0"
]
```

2. Fix any missing directories and __init__.py files
3. Ensure requirements.txt has pinned versions
4. Test with: pip install -e . --dry-run
            """,
            """
RECOVERY PROMPT 0.1b: Fix Directory Structure
Ensure all required directories exist with proper __init__.py files:

```bash
mkdir -p core agents database api config tests scripts docs
touch core/__init__.py agents/__init__.py database/__init__.py
touch api/__init__.py config/__init__.py tests/__init__.py
```

Add version info to each __init__.py:
```python
\"\"\"Package description.\"\"\"
__version__ = "0.1.0"
```
            """
        ]
    },
    "0.2": {
        "common_issues": [
            "Pre-commit configuration errors",
            "CI workflow syntax issues",
            "Linting tool configuration problems"
        ],
        "recovery_prompts": [
            """
RECOVERY PROMPT 0.2a: Fix Development Tools
Fix the development tools configuration:

1. Create working .pre-commit-config.yaml:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black
        args: [--line-length=100]
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=100]
```

2. Fix pyproject.toml tool configurations
3. Test with: pre-commit run --all-files
            """
        ]
    },
    "1.1": {
        "common_issues": [
            "Message bus implementation incomplete",
            "Missing async/await patterns",
            "Message type validation errors",
            "Test setup problems"
        ],
        "recovery_prompts": [
            """
RECOVERY PROMPT 1.1a: Fix Message Bus Core
Implement the core message bus with proper async patterns:

```python
# core/message_bus.py
import asyncio
from typing import Dict, List, Callable
from core.message_types import Message

class MessageBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.queue = asyncio.Queue()

    async def publish(self, message: Message):
        await self.queue.put(message)

    async def subscribe(self, message_type: str, handler: Callable):
        if message_type not in self.subscribers:
            self.subscribers[message_type] = []
        self.subscribers[message_type].append(handler)
```

Ensure all methods are async and handle errors properly.
            """,
            """
RECOVERY PROMPT 1.1b: Fix Message Types
Create proper message type definitions:

```python
# core/message_types.py
from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime

class Message(BaseModel):
    id: str
    type: str
    payload: Any
    timestamp: datetime
    priority: int = 0

class AgentRequest(Message):
    agent_id: str
    action: str

class AgentResponse(Message):
    request_id: str
    status: str
    data: Optional[Any] = None
```
            """
        ]
    },
    "1.2": {
        "common_issues": [
            "Agent registration logic incomplete",
            "Health monitoring not working",
            "Lifecycle management errors"
        ],
        "recovery_prompts": [
            """
RECOVERY PROMPT 1.2a: Fix Agent Orchestrator
Implement proper agent lifecycle management:

```python
# core/orchestrator.py
import asyncio
from typing import Dict, Set
from core.base_agent import BaseAgent

class AgentOrchestrator:
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.running: Set[str] = set()

    async def register_agent(self, agent: BaseAgent):
        self.agents[agent.id] = agent
        await agent.initialize()

    async def start_agent(self, agent_id: str):
        if agent_id in self.agents:
            await self.agents[agent_id].start()
            self.running.add(agent_id)
```
            """
        ]
    },
    "1.3": {
        "common_issues": [
            "BaseAgent abstract class not properly defined",
            "Context sharing not working",
            "Agent capabilities system incomplete"
        ],
        "recovery_prompts": [
            """
RECOVERY PROMPT 1.3a: Fix BaseAgent Framework
Create proper BaseAgent class:

```python
# core/base_agent.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    def __init__(self, agent_id: str):
        self.id = agent_id
        self.state = "initialized"
        self.context = {}

    @abstractmethod
    async def process_message(self, message) -> Any:
        pass

    @abstractmethod
    async def initialize(self) -> None:
        pass

    async def start(self):
        self.state = "running"

    async def stop(self):
        self.state = "stopped"
```
            """
        ]
    },
    "1.4": {
        "common_issues": [
            "Sandbox isolation not working",
            "Transaction rollback failing",
            "Resource limits not enforced",
            "Security validation incomplete"
        ],
        "recovery_prompts": [
            """
RECOVERY PROMPT 1.4a: Fix Sandbox Security
Implement proper transaction isolation:

```python
# core/sandbox.py
import asyncio
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

class DatabaseSandbox:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session
        self.transaction = None

    @asynccontextmanager
    async def isolated_execution(self):
        self.transaction = await self.session.begin()
        try:
            yield self.session
        except Exception:
            await self.transaction.rollback()
            raise
        else:
            await self.transaction.rollback()  # Always rollback in sandbox
```

Critical: NEVER commit transactions in sandbox mode.
            """
        ]
    },
    "2.1": {
        "common_issues": [
            "Intent classification not working",
            "Schema analysis incomplete",
            "Context building errors"
        ],
        "recovery_prompts": [
            """
RECOVERY PROMPT 2.1a: Fix Clarifier Agent
Implement basic intent classification:

```python
# agents/clarifier.py
from core.base_agent import BaseAgent
from typing import Dict, List

class ClarifierAgent(BaseAgent):
    def __init__(self):
        super().__init__("clarifier")
        self.intent_patterns = {
            "query": ["select", "find", "get", "show"],
            "insert": ["add", "create", "insert"],
            "update": ["change", "modify", "update"],
            "delete": ["remove", "delete", "drop"]
        }

    async def classify_intent(self, user_input: str) -> str:
        user_input_lower = user_input.lower()
        for intent, keywords in self.intent_patterns.items():
            if any(keyword in user_input_lower for keyword in keywords):
                return intent
        return "unknown"
```
            """
        ]
    },
    "2.2": {
        "common_issues": [
            "SQL generation logic incomplete",
            "Multi-dialect support missing",
            "Query optimization not working"
        ],
        "recovery_prompts": [
            """
RECOVERY PROMPT 2.2a: Fix Coder Agent
Implement basic SQL generation:

```python
# agents/coder.py
from core.base_agent import BaseAgent
from typing import Dict, Any

class CoderAgent(BaseAgent):
    def __init__(self):
        super().__init__("coder")
        self.templates = {
            "select": "SELECT {columns} FROM {table} WHERE {conditions}",
            "insert": "INSERT INTO {table} ({columns}) VALUES ({values})",
            "update": "UPDATE {table} SET {assignments} WHERE {conditions}",
            "delete": "DELETE FROM {table} WHERE {conditions}"
        }

    async def generate_sql(self, intent: str, context: Dict[str, Any]) -> str:
        template = self.templates.get(intent)
        if template:
            return template.format(**context)
        raise ValueError(f"Unsupported intent: {intent}")
```
            """
        ]
    },
    "2.3": {
        "common_issues": [
            "Test execution logic incomplete",
            "Validation rules missing",
            "Performance testing not working"
        ],
        "recovery_prompts": [
            """
RECOVERY PROMPT 2.3a: Fix Tester Agent
Implement basic validation:

```python
# agents/tester.py
from core.base_agent import BaseAgent
import sqlparse
from typing import List, Dict

class TesterAgent(BaseAgent):
    def __init__(self):
        super().__init__("tester")

    async def validate_sql(self, sql: str) -> Dict[str, Any]:
        try:
            parsed = sqlparse.parse(sql)
            return {
                "valid": len(parsed) > 0,
                "issues": [],
                "warnings": []
            }
        except Exception as e:
            return {
                "valid": False,
                "issues": [str(e)],
                "warnings": []
            }
```
            """
        ]
    }
}

def get_recovery_prompt(prompt_id: str, issue_type: str = "general") -> str:
    """Get recovery prompt for a specific issue."""
    if prompt_id not in RECOVERY_PROCEDURES:
        return f"No recovery procedures defined for prompt {prompt_id}"

    procedures = RECOVERY_PROCEDURES[prompt_id]

    if not procedures["recovery_prompts"]:
        return f"No recovery prompts available for prompt {prompt_id}"

    # Return the first recovery prompt by default
    return procedures["recovery_prompts"][0]

def list_common_issues(prompt_id: str) -> List[str]:
    """List common issues for a prompt."""
    if prompt_id not in RECOVERY_PROCEDURES:
        return []

    return RECOVERY_PROCEDURES[prompt_id]["common_issues"]

def main():
    if len(sys.argv) < 2:
        print("Usage: python recover_prompt.py <prompt_id> [issue_type]")
        print("Example: python recover_prompt.py 1.1")
        sys.exit(1)

    prompt_id = sys.argv[1]
    issue_type = sys.argv[2] if len(sys.argv) > 2 else "general"

    print(f"\n🔧 Recovery Procedures for Prompt {prompt_id}")
    print("=" * 60)

    # List common issues
    issues = list_common_issues(prompt_id)
    if issues:
        print(f"\n🚨 Common Issues:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")

    # Get recovery prompt
    recovery_prompt = get_recovery_prompt(prompt_id, issue_type)
    print(f"\n💡 Recovery Prompt:")
    print(recovery_prompt)

    print(f"\n📋 Next Steps:")
    print(f"  1. Copy the recovery prompt above")
    print(f"  2. Feed it to your LLM with the context file")
    print(f"  3. After implementation, run: python scripts/validate_prompt.py {prompt_id}")
    print(f"  4. If still failing, try the next recovery prompt")

if __name__ == "__main__":
    main()
