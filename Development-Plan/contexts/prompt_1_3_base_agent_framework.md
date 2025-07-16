# Context for Prompt 1.3: Base Agent Framework

## LLM Recommendation
**Recommended LLM**: Claude 3.5 Sonnet
**Reasoning**: Creating extensible framework requires strong OOP design patterns and architecture knowledge.

## Prompt Overview
**Phase**: Phase 1 - Core Infrastructure
**Position**: Prompt 5 of 26 total
**Dependencies**: Prompts 0.1, 0.2, 1.1, 1.2

## Original Prompt
```
I need a comprehensive base agent framework that all agents will inherit from.

Create the foundation with Cursor's multi-file editing:

1. Create core/base_agent.py:
   - Abstract BaseAgent class
   - Message handling interface
   - State management
   - Error handling and recovery
   - Performance metrics collection

2. Create core/agent_capabilities.py:
   - Capability definition system
   - Skill registration
   - Resource requirements
   - Dependency management

3. Create core/agent_context.py:
   - Context sharing interface
   - State persistence
   - Context versioning
   - Conflict resolution

4. Create tests/test_base_agent.py:
   - Agent behavior tests
   - Context sharing tests
   - Error handling tests

Success Criteria:
✅ All agents inherit consistently
✅ Context sharing works seamlessly
✅ Error recovery is automatic
✅ Performance metrics are collected

Performance Requirements:
- Message processing: <50ms
- Context operations: <10ms
- State persistence: <100ms
```

## Project Context

### Current Project Structure
```
multi-agent-database-ai-mvp/
├── core/
├── agents/
├── database/
├── api/
├── frontend/
├── sdk/
├── config/
├── tests/
├── scripts/
└── docs/
```

### Key Dependencies
```python
# Already installed from Phase 0
# Additional dependencies for infrastructure:
aioredis>=2.0.1
celery>=5.3.4
kombu>=5.3.4
prometheus-client>=0.19.0
structlog>=23.2.0
```

### Docker Environment
```yaml
# docker-compose.yml (to be created in later prompts)
services:
  postgres:
    image: postgres:16-alpine
  redis:
    image: redis:7-alpine
  app:
    build: .
```

## Current State Analysis
- Orchestrator implemented
- Project structure in place
- Development standards established
- Ready for core infrastructure

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
- **config/settings.py**: Configuration management
- **Project structure**: Directory layout
- **Development tools**: Linting, formatting

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
4. Proceed to Prompt 1.4

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
git checkout -b prompt-1.4-1-3-base-agent-framework

# Mark prompt as in-progress
python Development-Plan/scripts/progress_tracker.py start 1.4
```

### Implementation Steps
1. **Before starting**: Ensure dependencies are completed
   ```bash
   python Development-Plan/scripts/progress_tracker.py deps 1.4
   ```

2. **During implementation**: Make incremental commits
   ```bash
   git add .
   git commit -m "feat(1.4): implement core functionality"
   ```

3. **Before completion**: Validate your work
   ```bash
   python Development-Plan/scripts/validate_prompt.py 1.4
   ```

4. **On completion**: Merge and mark complete
   ```bash
   git checkout main
   git merge --no-ff prompt-1.4-1-3-base-agent-framework
   python Development-Plan/scripts/progress_tracker.py complete 1.4
   ```

### Commit Message Format
```
feat(1.4): [description of changes]

- Specific change 1
- Specific change 2
- Add comprehensive tests

Addresses: Base Agent Framework
```

For detailed git workflow guidance, see [Shared Git Workflow Context](./_shared_git_workflow_context.md)


Remember: Each component should be production-ready and well-integrated with the existing system.
