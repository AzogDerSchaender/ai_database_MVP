# Context for Prompt 2.4: Agent Communication Protocols

## LLM Recommendation
**Recommended LLM**: Claude 3.5 Sonnet
**Reasoning**: Protocol design requires understanding of distributed systems communication patterns.

## Prompt Overview
**Phase**: Phase 2 - Core Agents
**Position**: Prompt 13 of 26 total
**Dependencies**: Prompts 0.1-2.3

## Original Prompt
```
I need sophisticated communication protocols for seamless agent interaction.

Design protocols optimized for Cursor's multi-agent coordination:

1. Create core/protocols.py:
   - Message format specifications
   - Protocol versioning
   - Context sharing standards
   - Error propagation rules
   - Performance monitoring

2. Create core/agent_coordination.py:
   - Coordination patterns
   - Conflict resolution
   - Resource sharing
   - Load balancing

3. Create core/context_sync.py:
   - Context synchronization
   - Version control
   - Merge strategies
   - Conflict detection

4. Create tests/test_protocols.py:
   - Protocol compliance tests
   - Context sync tests
   - Coordination tests

Success Criteria:
✅ Agents communicate seamlessly
✅ Context stays synchronized
✅ Conflicts are resolved
✅ Performance is maintained

Performance Requirements:
- Message protocol overhead: <5ms
- Context sync: <50ms
- Coordination: <100ms
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
- All core agents implemented
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
4. Proceed to Prompt 2.5

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
git checkout -b prompt-2.5-2-4-agent-communication-protocols

# Mark prompt as in-progress
python Development-Plan/scripts/progress_tracker.py start 2.5
```

### Implementation Steps
1. **Before starting**: Ensure dependencies are completed
   ```bash
   python Development-Plan/scripts/progress_tracker.py deps 2.5
   ```

2. **During implementation**: Make incremental commits
   ```bash
   git add .
   git commit -m "feat(2.5): implement core functionality"
   ```

3. **Before completion**: Validate your work
   ```bash
   python Development-Plan/scripts/validate_prompt.py 2.5
   ```

4. **On completion**: Merge and mark complete
   ```bash
   git checkout main
   git merge --no-ff prompt-2.5-2-4-agent-communication-protocols
   python Development-Plan/scripts/progress_tracker.py complete 2.5
   ```

### Commit Message Format
```
feat(2.5): [description of changes]

- Specific change 1
- Specific change 2
- Add comprehensive tests

Addresses: Agent Communication Protocols
```

For detailed git workflow guidance, see [Shared Git Workflow Context](./_shared_git_workflow_context.md)


Remember: Each component should be production-ready and well-integrated with the existing system.
