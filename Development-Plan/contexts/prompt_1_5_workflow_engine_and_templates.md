# Context for Prompt 1.5: Workflow Engine & Templates

## LLM Recommendation
**Recommended LLM**: Claude 3.5 Sonnet
**Reasoning**: Workflow engines require understanding of state machines, DAGs, and complex execution patterns.

## Prompt Overview
**Phase**: Phase 1 - Core Infrastructure
**Position**: Prompt 7 of 26 total
**Dependencies**: Prompts 0.1-1.4

## Original Prompt
```
I need a flexible workflow engine for coordinating complex multi-agent tasks.

Use Cursor's pattern matching to ensure consistency across workflow definitions:

1. Create core/workflow.py:
   - Workflow definition DSL
   - Step execution engine
   - Conditional branching
   - Parallel execution support
   - Error recovery strategies

2. Create core/workflow_templates.py:
   - Query generation workflow
   - Data validation workflow
   - Schema analysis workflow
   - Migration workflow
   - Optimization workflow

3. Create core/progress_tracker.py:
   - Real-time progress monitoring
   - ETA calculation
   - Step-by-step logging
   - Visual progress reporting

4. Create tests/test_workflow.py:
   - Workflow execution tests
   - Error recovery tests
   - Performance tests

Success Criteria:
✅ Complex workflows execute reliably
✅ Error recovery works correctly
✅ Progress tracking is accurate
✅ Parallel execution scales

Performance Requirements:
- Workflow startup: <200ms
- Step transition: <50ms
- Progress updates: <10ms
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
- Sandbox environment ready
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
- Follow principle of least privilege
- Validate all inputs
- Secure error handling (no info leakage)
- Implement proper logging (no sensitive data)
- Use parameterized queries
- Follow OWASP best practices

#### Performance Requirements
- Operation latency: <100ms
- Memory efficiency: <100MB per component
- CPU usage: <70% under load
- Startup time: <5 seconds

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
- Test all public methods
- Mock external dependencies
- Achieve >90% code coverage
- Test error conditions
- Performance benchmarks
- Security vulnerability tests

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

### Next Steps

After completing this prompt:
1. Run all tests to ensure nothing is broken
2. Update any affected documentation
3. Commit changes with descriptive message
4. Proceed to Prompt 1.6

### Additional Resources

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


## Git Workflow for This Prompt

### Branch Strategy
```bash
# Create feature branch for this prompt
git checkout -b prompt-1.6-1-5-workflow-engine-and-templates

# Mark prompt as in-progress
python Development-Plan/scripts/progress_tracker.py start 1.6
```

### Implementation Steps
1. **Before starting**: Ensure dependencies are completed
   ```bash
   python Development-Plan/scripts/progress_tracker.py deps 1.6
   ```

2. **During implementation**: Make incremental commits
   ```bash
   git add .
   git commit -m "feat(1.6): implement core functionality"
   ```

3. **Before completion**: Validate your work
   ```bash
   python Development-Plan/scripts/validate_prompt.py 1.6
   ```

4. **On completion**: Merge and mark complete
   ```bash
   git checkout main
   git merge --no-ff prompt-1.6-1-5-workflow-engine-and-templates
   python Development-Plan/scripts/progress_tracker.py complete 1.6
   ```

### Commit Message Format
```
feat(1.6): [description of changes]

- Specific change 1
- Specific change 2
- Add comprehensive tests

Addresses: Workflow Engine & Templates
```

For detailed git workflow guidance, see [Shared Git Workflow Context](./_shared_git_workflow_context.md)


Remember: Each component should be production-ready and well-integrated with the existing system.
