# Context for Prompt 2.1b: Schema Analysis & Intelligence

## LLM Recommendation
**Recommended LLM**: Claude 3.5 Sonnet
**Reasoning**: This focused sub-prompt requires specific implementation expertise while maintaining integration with the larger system.

## Prompt Overview
**Phase**: Phase 2 - Core Agents (Sub-prompt)
**Position**: Sub-prompt of original Prompt 2.1
**Dependencies**: Prompts 0.1-2.5, 2.1a

## Original Prompt
```

Implement schema analysis capabilities for the Clarifier Agent.

Depends on: Prompt 2.1a

1. Create agents/schema_analyzer.py:
   - Table discovery and analysis
   - Column information extraction
   - Relationship mapping
   - Index detection
   - Constraint analysis

2. Update agents/clarifier.py:
   - Integrate schema analysis
   - Add schema-aware context building
   - Implement schema caching

3. Create tests/test_schema_analyzer.py:
   - Test schema discovery
   - Test relationship detection
   - Test performance with large schemas

Success Criteria:
✅ Discovers schema relationships
✅ Handles multiple database types
✅ Caches schema information efficiently

Performance Requirements:
- Schema analysis: <1 second for 100 tables
- Relationship mapping: <500ms

```

## Project Context

### Current Project Structure
```
multi-agent-database-ai-mvp/
├── core/
│   ├── base_agent.py          # ✅ Available
│   ├── message_bus.py         # ✅ Available
│   ├── orchestrator.py        # ✅ Available
│   └── [other core modules]   # ✅ Available
├── agents/
│   └── __init__.py           # ✅ Available
├── tests/
│   └── [test infrastructure] # ✅ Available
└── [other directories]       # ✅ Available
```

### Key Dependencies
```python
# Agent Framework (already implemented)
from core.base_agent import BaseAgent
from core.message_bus import MessageBus
from core.orchestrator import AgentOrchestrator

# Testing Framework
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
```

## Implementation Requirements

### Core Components to Build
1. Schema analysis engine
2. Relationship mapper
3. Schema caching system
4. Integration with ClarifierAgent
5. Schema analysis tests

### Technical Specifications

#### Architecture Patterns
- **Inherit from BaseAgent**: Use established patterns
- **Async/Await**: All operations must be async
- **Error Handling**: Comprehensive exception handling
- **Type Hints**: Full type annotation required

#### Security Considerations
- **Input Validation**: Validate all external inputs
- **SQL Injection Prevention**: Use parameterized queries only
- **Resource Limits**: Prevent resource exhaustion
- **Audit Logging**: Log all operations

#### Performance Requirements
- Intent classification: <100ms
- Schema analysis: <1 second
- Question generation: <200ms
- Context operations: <50ms

### Integration Points

#### Existing Modules
- **core/base_agent.py**: Agent base class
- **core/message_bus.py**: Inter-agent communication
- **core/orchestrator.py**: Agent lifecycle management
- **Previous sub-prompts**: Build upon earlier implementations

#### Testing Strategy

#### Unit Tests
- Test isolated functionality
- Mock external dependencies
- Achieve >90% code coverage
- Test error conditions

#### Integration Tests
- Test with actual base infrastructure
- Verify message passing works
- Test error propagation
- Validate performance

#### Example Stub Test
```python
# tests/unit/test_2_1b.py

import pytest
from unittest.mock import AsyncMock
from agents.clarifier import ClarifierAgent  # Replace with actual module

@pytest.mark.asyncio
async def test_agent_initialization():
    agent = ClarifierAgent()
    assert agent.id == "clarifier"
    assert agent.state == "initialized"

@pytest.mark.asyncio
async def test_basic_functionality():
    agent = ClarifierAgent()
    await agent.initialize()
    # Test core functionality here
    assert True  # Replace with actual test
```

### Implementation Checklist

Before considering this sub-prompt complete:

- [ ] All specified files created
- [ ] Inherits properly from BaseAgent
- [ ] All methods are async where required
- [ ] Comprehensive error handling implemented
- [ ] Unit tests written and passing (>90% coverage)
- [ ] Integration with existing infrastructure verified
- [ ] Performance requirements met
- [ ] Security considerations addressed
- [ ] Documentation updated

### Next Steps

After completing this sub-prompt:
1. Run: `python Development-Plan/scripts/validate_prompt.py 2.1b`
2. If validation passes, proceed to next sub-prompt
3. If validation fails, run: `python Development-Plan/scripts/recover_prompt.py 2.1b`
4. Update progress: `python Development-Plan/scripts/progress_tracker.py complete 2.1b`

### Notes for LLM

1. **Focus**: This is a focused sub-prompt - implement only what's specified
2. **Integration**: Must work with existing BaseAgent infrastructure
3. **Testing**: Write tests as you implement
4. **Performance**: Meet the specific performance requirements
5. **Security**: Never skip security validation
6. **Async**: All agent operations must be async
7. **Error Handling**: Expect and handle all error conditions
## Git Workflow for This Prompt

### Branch Strategy
```bash
# Create feature branch for this prompt
git checkout -b prompt-2.1-2-1b-schema-analysis-and-intelligence

# Mark prompt as in-progress
python Development-Plan/scripts/progress_tracker.py start 2.1
```

### Implementation Steps
1. **Before starting**: Ensure dependencies are completed
   ```bash
   python Development-Plan/scripts/progress_tracker.py deps 2.1
   ```

2. **During implementation**: Make incremental commits
   ```bash
   git add .
   git commit -m "feat(2.1): implement core functionality"
   ```

3. **Before completion**: Validate your work
   ```bash
   python Development-Plan/scripts/validate_prompt.py 2.1
   ```

4. **On completion**: Merge and mark complete
   ```bash
   git checkout main
   git merge --no-ff prompt-2.1-2-1b-schema-analysis-and-intelligence
   python Development-Plan/scripts/progress_tracker.py complete 2.1
   ```

### Commit Message Format
```
feat(2.1): [description of changes]

- Specific change 1
- Specific change 2
- Add comprehensive tests

Addresses: Schema Analysis & Intelligence
```

For detailed git workflow guidance, see [Shared Git Workflow Context](./_shared_git_workflow_context.md)


Remember: This sub-prompt is part of a larger system. Focus on the specific requirements while ensuring compatibility with the overall architecture.
