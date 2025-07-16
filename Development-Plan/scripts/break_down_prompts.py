#!/usr/bin/env python3
"""
Break down complex prompts into smaller, more manageable sub-prompts.
"""

from pathlib import Path

# Define how to break down the most complex prompts
PROMPT_BREAKDOWNS = {
    "2.1": {
        "original_title": "Advanced Clarifier Agent",
        "sub_prompts": [
            {
                "id": "2.1a",
                "title": "Basic Clarifier Agent Core",
                "content": """
I need to implement the core Clarifier Agent with basic intent classification.

Use Cursor's AI assistance to create the foundation:

1. Create agents/clarifier.py:
   - Basic ClarifierAgent class inheriting from BaseAgent
   - Simple intent classification (query, insert, update, delete)
   - User input processing
   - Context initialization

2. Create tests/test_clarifier_core.py:
   - Test agent initialization
   - Test basic intent classification
   - Test message handling

Success Criteria:
✅ Agent initializes correctly
✅ Basic intent classification works
✅ Tests pass with >90% coverage

Performance Requirements:
- Agent startup: <200ms
- Intent classification: <100ms
                """
            },
            {
                "id": "2.1b",
                "title": "Schema Analysis & Intelligence",
                "content": """
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
                """
            },
            {
                "id": "2.1c",
                "title": "Question Generation & Context Building",
                "content": """
Complete the Clarifier Agent with intelligent question generation.

Depends on: Prompts 2.1a, 2.1b

1. Create agents/clarifier_intelligence.py:
   - Question prioritization algorithm
   - Context-aware question generation
   - Disambiguation techniques
   - Learning from user responses

2. Update agents/clarifier.py:
   - Integrate question generation
   - Add context building strategies
   - Implement conversation memory

3. Create tests/test_clarifier_intelligence.py:
   - Test question relevance
   - Test context building accuracy
   - Test conversation flow

Success Criteria:
✅ Generates relevant questions
✅ Builds complete context incrementally
✅ Learns from interactions

Performance Requirements:
- Question generation: <200ms
- Context building: <100ms
                """
            }
        ]
    },
    "2.2": {
        "original_title": "Intelligent Coder Agent",
        "sub_prompts": [
            {
                "id": "2.2a",
                "title": "Basic SQL Generation",
                "content": """
Implement the core SQL generation capabilities.

1. Create agents/coder.py:
   - Basic CoderAgent class
   - Template-based SQL generation
   - Support for basic CRUD operations
   - Error handling

2. Create agents/sql_templates.py:
   - SQL templates for different operations
   - Multi-dialect template support
   - Parameter binding support

3. Create tests/test_coder_basic.py:
   - Test basic SQL generation
   - Test template rendering
   - Test parameter binding

Success Criteria:
✅ Generates basic SQL correctly
✅ Supports PostgreSQL and MySQL
✅ Handles parameters safely

Performance Requirements:
- SQL generation: <500ms
- Template rendering: <50ms
                """
            },
            {
                "id": "2.2b",
                "title": "Advanced SQL Generation & Optimization",
                "content": """
Add advanced SQL generation and optimization capabilities.

Depends on: Prompt 2.2a

1. Create agents/sql_generator.py:
   - Complex query generation
   - Join optimization
   - Subquery handling
   - Window functions support

2. Create agents/code_optimizer.py:
   - Query optimization rules
   - Index utilization hints
   - Performance analysis
   - Query rewriting

3. Create tests/test_sql_advanced.py:
   - Test complex query generation
   - Test optimization rules
   - Test performance improvements

Success Criteria:
✅ Generates complex SQL queries
✅ Optimizes for performance
✅ Provides optimization suggestions

Performance Requirements:
- Complex query generation: <1 second
- Optimization analysis: <500ms
                """
            },
            {
                "id": "2.2c",
                "title": "Security & Documentation",
                "content": """
Complete the Coder Agent with security validation and documentation.

Depends on: Prompts 2.2a, 2.2b

1. Update agents/coder.py:
   - SQL injection prevention
   - Input validation
   - Code documentation generation
   - Security policy enforcement

2. Create agents/security_validator.py:
   - Security rule engine
   - SQL injection detection
   - Dangerous operation prevention
   - Audit logging

3. Create tests/test_coder_security.py:
   - Test SQL injection prevention
   - Test security validation
   - Test audit logging

Success Criteria:
✅ Prevents SQL injection attacks
✅ Validates all inputs
✅ Generates code documentation

Performance Requirements:
- Security validation: <200ms
- Documentation generation: <100ms
                """
            }
        ]
    },
    "2.3": {
        "original_title": "Comprehensive Tester Agent",
        "sub_prompts": [
            {
                "id": "2.3a",
                "title": "Basic Validation & Testing",
                "content": """
Implement basic SQL validation and testing capabilities.

1. Create agents/tester.py:
   - Basic TesterAgent class
   - SQL syntax validation
   - Basic semantic checks
   - Test result reporting

2. Create agents/validators.py:
   - Syntax validation rules
   - Semantic validation rules
   - Data type validation
   - Constraint validation

3. Create tests/test_tester_basic.py:
   - Test validation logic
   - Test error detection
   - Test result reporting

Success Criteria:
✅ Validates SQL syntax correctly
✅ Detects semantic errors
✅ Reports clear error messages

Performance Requirements:
- Syntax validation: <50ms
- Semantic validation: <100ms
                """
            },
            {
                "id": "2.3b",
                "title": "Sandbox Testing & Performance",
                "content": """
Add sandbox testing and performance validation.

Depends on: Prompt 2.3a

1. Create agents/test_executor.py:
   - Sandbox test execution
   - Performance profiling
   - Resource monitoring
   - Parallel test execution

2. Update agents/tester.py:
   - Integrate sandbox testing
   - Add performance validation
   - Result comparison logic

3. Create tests/test_execution.py:
   - Test sandbox isolation
   - Test performance profiling
   - Test parallel execution

Success Criteria:
✅ Executes tests safely in sandbox
✅ Profiles performance accurately
✅ Handles concurrent tests

Performance Requirements:
- Test execution: <2 seconds
- Performance profiling: <500ms
                """
            },
            {
                "id": "2.3c",
                "title": "Advanced Testing & Regression",
                "content": """
Complete the Tester Agent with advanced testing capabilities.

Depends on: Prompts 2.3a, 2.3b

1. Update agents/tester.py:
   - Regression testing
   - Edge case detection
   - Load testing capabilities
   - Test report generation

2. Create agents/regression_tester.py:
   - Regression test management
   - Test case generation
   - Result comparison
   - Trend analysis

3. Create tests/test_advanced_testing.py:
   - Test regression detection
   - Test load testing
   - Test report generation

Success Criteria:
✅ Detects regressions accurately
✅ Handles edge cases
✅ Generates comprehensive reports

Performance Requirements:
- Regression testing: <1 second
- Load testing: <5 seconds
                """
            }
        ]
    },
    "2.6": {
        "original_title": "Phase 2 Agent Integration & Validation",
        "sub_prompts": [
            {
                "id": "2.6a",
                "title": "Agent Communication Integration",
                "content": """
Test and validate inter-agent communication.

Depends on: All Phase 2 prompts (2.1-2.5)

1. Create tests/integration/test_agent_communication.py:
   - Test Clarifier → Coder workflow
   - Test Coder → Tester workflow
   - Test error propagation
   - Test message validation

2. Create scripts/test_agent_workflows.py:
   - End-to-end workflow testing
   - Performance benchmarking
   - Error recovery testing

3. Validate agent coordination:
   - Message passing works correctly
   - Context sharing is reliable
   - Error handling is consistent

Success Criteria:
✅ All agent-to-agent communication works
✅ No message loss or corruption
✅ Error recovery is automatic

Performance Requirements:
- Agent communication: <50ms
- End-to-end workflow: <5 seconds
                """
            },
            {
                "id": "2.6b",
                "title": "Performance & Optimization",
                "content": """
Optimize and benchmark the complete agent ecosystem.

Depends on: Prompt 2.6a

1. Create scripts/agent_benchmarks.py:
   - Performance benchmarking
   - Resource usage analysis
   - Scalability testing
   - Optimization recommendations

2. Optimize critical paths:
   - Agent startup time
   - Message processing speed
   - Memory usage
   - CPU utilization

3. Create docs/AGENT_ARCHITECTURE.md:
   - Agent interaction diagrams
   - Performance characteristics
   - Best practices

Success Criteria:
✅ All performance targets met
✅ System scales to 50+ agents
✅ Resource usage optimized

Performance Requirements:
- Complete workflow: <3 seconds (improved)
- Agent coordination: <50ms (improved)
                """
            }
        ]
    }
}

def create_breakdown_files():
    """Create breakdown files for complex prompts."""
    # Fix path - if we're in Development-Plan directory, contexts is at ./contexts
    if Path.cwd().name == "Development-Plan":
        contexts_dir = Path("contexts")
    else:
        contexts_dir = Path("Development-Plan/contexts")

    for original_id, breakdown in PROMPT_BREAKDOWNS.items():
        print(f"\n📋 Breaking down Prompt {original_id}: {breakdown['original_title']}")

        for sub_prompt in breakdown["sub_prompts"]:
            sub_id = sub_prompt["id"]
            title = sub_prompt["title"]

            # Create filename
            filename = f"prompt_{sub_id.replace('.', '_')}_{title.lower().replace(' ', '_').replace('&', 'and')}.md"
            filepath = contexts_dir / filename

            # Create context content
            content = f"""# Context for Prompt {sub_id}: {title}

## LLM Recommendation
**Recommended LLM**: Claude 3.5 Sonnet
**Reasoning**: This focused sub-prompt requires specific implementation expertise while maintaining integration with the larger system.

## Prompt Overview
**Phase**: Phase 2 - Core Agents (Sub-prompt)
**Position**: Sub-prompt of original Prompt {original_id}
**Dependencies**: {get_dependencies(sub_id)}

## Original Prompt
```
{sub_prompt["content"]}
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
{get_components_for_subprompt(sub_id)}

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
{get_performance_for_subprompt(sub_id)}

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
# tests/unit/test_{sub_id.replace('.', '_')}.py

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
1. Run: `python Development-Plan/scripts/validate_prompt.py {sub_id}`
2. If validation passes, proceed to next sub-prompt
3. If validation fails, run: `python Development-Plan/scripts/recover_prompt.py {sub_id}`
4. Update progress: `python Development-Plan/scripts/progress_tracker.py complete {sub_id}`

### Notes for LLM

1. **Focus**: This is a focused sub-prompt - implement only what's specified
2. **Integration**: Must work with existing BaseAgent infrastructure
3. **Testing**: Write tests as you implement
4. **Performance**: Meet the specific performance requirements
5. **Security**: Never skip security validation
6. **Async**: All agent operations must be async
7. **Error Handling**: Expect and handle all error conditions

Remember: This sub-prompt is part of a larger system. Focus on the specific requirements while ensuring compatibility with the overall architecture.
"""

            # Write the file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"  ✅ Created {filename}")

def get_dependencies(sub_id):
    """Get dependencies for a sub-prompt."""
    if sub_id.endswith('a'):
        return "All Phase 0 and Phase 1 prompts"
    elif sub_id.endswith('b'):
        return f"Prompts 0.1-2.5, {sub_id[:-1]}a"
    else:  # ends with 'c'
        return f"Prompts 0.1-2.5, {sub_id[:-1]}a, {sub_id[:-1]}b"

def get_components_for_subprompt(sub_id):
    """Get components to build for a sub-prompt."""
    if "2.1a" in sub_id:
        return """1. Basic ClarifierAgent class
2. Intent classification system
3. Core message handling
4. Basic context management
5. Unit tests"""
    elif "2.1b" in sub_id:
        return """1. Schema analysis engine
2. Relationship mapper
3. Schema caching system
4. Integration with ClarifierAgent
5. Schema analysis tests"""
    elif "2.1c" in sub_id:
        return """1. Question generation engine
2. Context building strategies
3. Conversation memory
4. Intelligence integration
5. Complete integration tests"""
    elif "2.2a" in sub_id:
        return """1. Basic CoderAgent class
2. SQL template system
3. Parameter binding
4. Error handling
5. Basic generation tests"""
    elif "2.2b" in sub_id:
        return """1. Advanced SQL generator
2. Query optimizer
3. Join optimization
4. Performance analysis
5. Optimization tests"""
    elif "2.2c" in sub_id:
        return """1. Security validator
2. Input sanitization
3. Documentation generator
4. Audit logging
5. Security tests"""
    elif "2.3a" in sub_id:
        return """1. Basic TesterAgent class
2. Validation engine
3. Error reporting
4. Result formatting
5. Validation tests"""
    elif "2.3b" in sub_id:
        return """1. Test executor
2. Performance profiler
3. Sandbox integration
4. Parallel testing
5. Execution tests"""
    elif "2.3c" in sub_id:
        return """1. Regression tester
2. Edge case detector
3. Load testing
4. Report generator
5. Advanced tests"""
    elif "2.6a" in sub_id:
        return """1. Inter-agent communication tests
2. Workflow validation
3. Error propagation tests
4. Message validation
5. Integration test suite"""
    elif "2.6b" in sub_id:
        return """1. Performance benchmarks
2. Optimization implementation
3. Architecture documentation
4. Scalability tests
5. Final validation"""
    else:
        return """1. Core implementation
2. Supporting utilities
3. Test suite
4. Documentation
5. Integration validation"""

def get_performance_for_subprompt(sub_id):
    """Get performance requirements for a sub-prompt."""
    if "2.1" in sub_id:
        return """- Intent classification: <100ms
- Schema analysis: <1 second
- Question generation: <200ms
- Context operations: <50ms"""
    elif "2.2" in sub_id:
        return """- Basic SQL generation: <500ms
- Complex query generation: <1 second
- Security validation: <200ms
- Template rendering: <50ms"""
    elif "2.3" in sub_id:
        return """- Syntax validation: <50ms
- Test execution: <2 seconds
- Performance profiling: <500ms
- Regression testing: <1 second"""
    elif "2.6" in sub_id:
        return """- Agent communication: <50ms
- End-to-end workflow: <3 seconds
- Benchmark execution: <10 seconds
- Integration tests: <30 seconds"""
    else:
        return """- Core operations: <100ms
- Integration: <500ms
- Test execution: <5 seconds"""

def main():
    """Create all breakdown files."""
    print("🔧 Breaking down complex prompts into manageable sub-prompts...")
    create_breakdown_files()
    print("\n✅ All complex prompts have been broken down into sub-prompts!")
    print("\nUsage:")
    print("1. Use sub-prompts instead of the original complex prompts")
    print("2. Complete sub-prompts in order (a, then b, then c)")
    print("3. Validate each sub-prompt before proceeding")
    print("4. Original complex prompts are preserved for reference")

if __name__ == "__main__":
    main()
