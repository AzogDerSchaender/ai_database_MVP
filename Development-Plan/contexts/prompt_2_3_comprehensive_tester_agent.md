# Context for Prompt 2.3: Comprehensive Tester Agent

## LLM Recommendation
**Recommended LLM**: Claude 3.5 Sonnet/3 Opus
**Reasoning**: Testing strategies require understanding of various testing methodologies and safety validation techniques.

## Prompt Overview
**Phase**: Phase 2 - Core Agents
**Position**: Prompt 12 of 26 total
**Dependencies**: Prompts 0.1-2.2

## Original Prompt
```
I need a thorough Tester Agent that validates code safety, correctness, and performance.

Use Cursor's testing framework integration:

1. Create agents/tester.py:
   - Multi-level testing strategy
   - Safety validation
   - Performance testing
   - Result verification
   - Regression detection

2. Create agents/test_executor.py:
   - Sandbox test execution
   - Parallel test running
   - Result comparison
   - Performance profiling

3. Create agents/validators.py:
   - Syntax validation
   - Semantic validation
   - Data integrity checks
   - Performance validation

4. Create tests/test_tester.py:
   - Validation logic tests
   - Test execution tests
   - Performance tests
   - Safety tests

Testing scenarios:
- Edge cases and boundary conditions
- Performance under load
- Data corruption scenarios
- Security vulnerabilities

Success Criteria:
✅ Catches 99%+ of errors
✅ Performance tests are accurate
✅ Safety validation is complete
✅ Results are reproducible

Performance Requirements:
- Test execution: <2 seconds
- Validation: <100ms
- Performance profiling: <500ms
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
- Coder agent implemented
- Core infrastructure operational
- Message bus and orchestration working
- Ready for agent implementation

## Implementation Requirements

### Core Components to Build
1. Core implementation modules
2. Supporting utilities
3. Test suites
4. Documentation
5. Integration points

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
4. Proceed to Prompt 2.4

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
git checkout -b prompt-2.4-2-3-comprehensive-tester-agent

# Mark prompt as in-progress
python Development-Plan/scripts/progress_tracker.py start 2.4
```

### Implementation Steps
1. **Before starting**: Ensure dependencies are completed
   ```bash
   python Development-Plan/scripts/progress_tracker.py deps 2.4
   ```

2. **During implementation**: Make incremental commits
   ```bash
   git add .
   git commit -m "feat(2.4): implement core functionality"
   ```

3. **Before completion**: Validate your work
   ```bash
   python Development-Plan/scripts/validate_prompt.py 2.4
   ```

4. **On completion**: Merge and mark complete
   ```bash
   git checkout main
   git merge --no-ff prompt-2.4-2-3-comprehensive-tester-agent
   python Development-Plan/scripts/progress_tracker.py complete 2.4
   ```

### Commit Message Format
```
feat(2.4): [description of changes]

- Specific change 1
- Specific change 2
- Add comprehensive tests

Addresses: Comprehensive Tester Agent
```

For detailed git workflow guidance, see [Shared Git Workflow Context](./_shared_git_workflow_context.md)


Remember: Each component should be production-ready and well-integrated with the existing system.
