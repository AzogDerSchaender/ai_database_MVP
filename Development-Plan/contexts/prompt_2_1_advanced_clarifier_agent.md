# Context for Prompt 2.1: Advanced Clarifier Agent

## LLM Recommendation
**Recommended LLM**: Claude 3.5 Sonnet/3 Opus
**Reasoning**: NLP and intent classification require sophisticated understanding of language processing and context building.

## Prompt Overview
**Phase**: Phase 2 - Core Agents
**Position**: Prompt 10 of 26 total
**Dependencies**: All Phase 0 and 1 prompts

## Original Prompt
```
I need an intelligent Clarifier Agent that understands user intent and builds comprehensive context.

Use Cursor's AI assistance to optimize the natural language processing:

1. Create agents/clarifier.py:
   - Intent classification system
   - Context-aware question generation
   - Schema understanding
   - User interaction management
   - Learning from previous interactions

2. Create agents/clarifier_intelligence.py:
   - NLP processing for user requests
   - Question prioritization
   - Context building strategies
   - Disambiguation techniques

3. Create agents/schema_analyzer.py:
   - Deep schema analysis
   - Relationship mapping
   - Constraint discovery
   - Performance implications

4. Create tests/test_clarifier.py:
   - Intent classification tests
   - Question generation tests
   - Context building tests
   - Schema analysis tests

Handle these scenarios:
- Ambiguous user requests
- Complex schema relationships
- Missing information
- Contradictory requirements

Success Criteria:
✅ 95%+ intent classification accuracy
✅ Relevant questions generated
✅ Complete schema understanding
✅ Context builds incrementally

Performance Requirements:
- Request analysis: <500ms
- Question generation: <200ms
- Schema analysis: <1 second
```

## Project Context

### Current Project Structure
```
multi-agent-database-ai-mvp/
├── core/
│   ├── __init__.py
│   ├── orchestrator.py
│   ├── message_bus.py
│   ├── base_agent.py
│   ├── workflow.py
│   ├── sandbox.py
│   └── [other core modules]
├── agents/
│   └── __init__.py
├── database/
│   ├── __init__.py
│   ├── base_connector.py
│   ├── postgres_connector.py
│   └── mysql_connector.py
├──
```

### Key Dependencies
```python
# AI/LLM Dependencies
openai>=1.6.1
anthropic>=0.8.1
langchain>=0.0.352
tiktoken>=0.5.2
numpy>=1.24.3
pandas>=2.0.3
```

### Docker Environment
The project uses Docker Compose with:
- PostgreSQL database (primary datastore)
- Redis cache (message queue and caching)
- Application container (FastAPI app)
- Nginx reverse proxy (production only)

## Current State Analysis
- Infrastructure validated and ready
- Core infrastructure operational
- Message bus and orchestration working
- Ready for agent implementation

## Implementation Requirements

### Core Components to Build
1. Intent classification system
2. Context building engine
3. Question generation logic
4. Schema analysis tools
5. Learning mechanism

### Technical Specifications

#### Architecture Patterns
- Follow SOLID principles strictly
- Use dependency injection for flexibility
- Implement proper separation of concerns
- Create reusable, modular components
- Use async/await patterns consistently

#### Error Handling
- Use custom exceptions for different error types
- Implement proper error propagation
- Add comprehensive error logging
- Include error recovery mechanisms
- Never expose internal errors to users

#### Security Considerations
- Validate all inter-agent messages
- Implement message signing/verification
- Prevent agent impersonation
- Resource usage limits per agent
- Secure state management
- Audit agent actions

#### Performance Requirements
- Agent startup: <500ms
- Message processing: <50ms
- State operations: <10ms
- Memory per agent: <50MB

### Integration Points

#### Existing Modules
- **core/orchestrator.py**: Agent orchestration
- **core/message_bus.py**: Message passing
- **core/base_agent.py**: Base agent class
- **core/workflow.py**: Workflow engine
- **database/connectors/**: Database connections

#### External Services
- PostgreSQL database
- Redis cache
- Docker runtime

### Testing Strategy

#### Unit Tests
- Test agent initialization and lifecycle
- Message handling tests
- State management tests
- Error recovery tests
- Performance under load
- Inter-agent communication tests
- Edge case handling

#### Integration Tests
- Test component interactions
- Verify data flow between modules
- Test failure scenarios
- Validate performance under load

#### Test File Naming
- Unit tests: `tests/unit/test_<module_name>.py`
- Integration tests: `tests/integration/test_<feature>.py`
- E2E tests: `tests/e2e/test_<workflow>.py`

#### Example Stub Test
```python
# tests/unit/test_stub.py


def test_stub():
    assert True
```

- Unit tests: `tests/unit/test_<module_name>.py`
- Integration tests: `tests/integration/test_<feature>.py`
- E2E tests: `tests/e2e/test_<workflow>.py`

### Code Quality Standards

#### Python Style
- Follow PEP 8 strictly
- Use type hints throughout
- Add comprehensive docstrings
- Maximum line length: 100 characters
- Use meaningful variable names

#### Documentation
- Document all public APIs
- Include usage examples
- Explain complex algorithms
- Add inline comments for clarity
- Keep README files updated

### Common Patterns to Use
See _shared_global_context.md

### Implementation Checklist

Before considering this prompt complete:

- [ ] All components implemented according to spec
- [ ] Unit tests written and passing (>90% coverage)
- [ ] Integration tests completed
- [ ] Documentation updated
- [ ] Code review completed
- [ ] Performance benchmarks met
- [ ] Security review passed
- [ ] Error handling comprehensive
- [ ] Logging implemented
- [ ] Configuration documented
- [ ] Agent lifecycle methods implemented
- [ ] Message handling tested
- [ ] State persistence working
- [ ] Recovery mechanisms tested

### Next Steps

After completing this prompt:
1. Run all tests to ensure nothing is broken
2. Update any affected documentation
3. Commit changes with descriptive message
4. Proceed to Prompt 2.2

### Additional Resources

#### Multi-Agent Systems
- [Multi-Agent Systems](https://en.wikipedia.org/wiki/Multi-agent_system)
- [Agent Communication Languages](https://en.wikipedia.org/wiki/Agent_Communication_Language)
- [Distributed Systems Patterns](https://martinfowler.com/articles/patterns-of-distributed-systems/)

#### General Resources
See _shared_global_context.md

### Notes for LLM

1. **Focus on Production Quality**: This is a production system, not a prototype
2. **Security First**: Always consider security implications
3. **Test Everything**: Write tests as you implement
4. **Document Thoroughly**: Future developers need to understand your code
5. **Performance Matters**: This system needs to scale
6. **Error Handling**: Expect failures and handle them gracefully
7. **Maintainability**: Write clean, readable, maintainable code


**Agent Design**: Agents should be:
- Autonomous but cooperative
- Resilient to failures
- Efficient in resource usage
- Well-documented for future agents
## Git Workflow for This Prompt

### Branch Strategy
```bash
# Create feature branch for this prompt
git checkout -b prompt-2.2-2-1-advanced-clarifier-agent

# Mark prompt as in-progress
python Development-Plan/scripts/progress_tracker.py start 2.2
```

### Implementation Steps
1. **Before starting**: Ensure dependencies are completed
   ```bash
   python Development-Plan/scripts/progress_tracker.py deps 2.2
   ```

2. **During implementation**: Make incremental commits
   ```bash
   git add .
   git commit -m "feat(2.2): implement core functionality"
   ```

3. **Before completion**: Validate your work
   ```bash
   python Development-Plan/scripts/validate_prompt.py 2.2
   ```

4. **On completion**: Merge and mark complete
   ```bash
   git checkout main
   git merge --no-ff prompt-2.2-2-1-advanced-clarifier-agent
   python Development-Plan/scripts/progress_tracker.py complete 2.2
   ```

### Commit Message Format
```
feat(2.2): [description of changes]

- Specific change 1
- Specific change 2
- Add comprehensive tests

Addresses: Advanced Clarifier Agent
```

For detailed git workflow guidance, see [Shared Git Workflow Context](./_shared_git_workflow_context.md)


Remember: Each component should be production-ready and well-integrated with the existing system.
