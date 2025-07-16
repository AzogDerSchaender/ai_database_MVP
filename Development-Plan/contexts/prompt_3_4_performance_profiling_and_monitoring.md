# Context for Prompt 3.4: Performance Profiling & Monitoring

## LLM Recommendation
**Recommended LLM**: Claude 3.5 Sonnet
**Reasoning**: Performance profiling requires understanding of database metrics and monitoring best practices.

## Prompt Overview
**Phase**: Phase 3 - Database Intelligence
**Position**: Prompt 19 of 26 total
**Dependencies**: Prompts 0.1-3.3

## Original Prompt
```
I need advanced performance profiling and monitoring for database operations.

Implement comprehensive monitoring with Cursor's performance tools:

1. Create database/performance_profiler.py:
   - Query performance analysis
   - Resource utilization tracking
   - Bottleneck identification
   - Performance trending

2. Create database/monitoring_engine.py:
   - Real-time monitoring
   - Alert generation
   - Performance dashboards
   - Historical analysis

3. Create database/bottleneck_analyzer.py:
   - I/O bottleneck detection
   - CPU utilization analysis
   - Memory pressure monitoring
   - Lock contention analysis

4. Create tests/test_performance.py:
   - Profiling accuracy tests
   - Monitoring tests
   - Alert tests

Success Criteria:
✅ Accurate performance profiling
✅ Real-time bottleneck detection
✅ Predictive alerting
✅ Comprehensive metrics

Performance Requirements:
- Profiling overhead: <5%
- Real-time monitoring: <100ms latency
- Alert generation: <1 second
```

## Project Context

### Current Project Structure
```
multi-agent-database-ai-mvp/
├── core/
│   └── [infrastructure modules]
├── agents/
│   ├── __init__.py
│   ├── clarifier.py
│   ├── coder.py
│   ├── tester.py
│   └── [agent modules]
├── database/
│   ├── connectors/
│   ├── intelligence/
│   └── [database modules]
├──
```

### Key Dependencies
```python
# Database Intelligence Dependencies
sqlparse>=0.4.4
pygments>=2.17.2
networkx>=3.2.1
scikit-learn>=1.3.2
scipy>=1.11.4
```

### Docker Environment
The project uses Docker Compose with:
- PostgreSQL database (primary datastore)
- Redis cache (message queue and caching)
- Application container (FastAPI app)
- Nginx reverse proxy (production only)

## Current State Analysis
- Data quality engine implemented
- All agents implemented and tested
- Inter-agent communication working
- Ready for intelligence layer

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
- **agents/**: All agent implementations
- **core/**: Complete infrastructure
- **database/**: Basic connectors
- **tests/**: Test infrastructure

#### External Services
- PostgreSQL database
- Redis cache
- External APIs (OpenAI, Anthropic)
- Docker runtime
- Monitoring services (later phases)

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
4. Proceed to Prompt 3.5

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
git checkout -b prompt-3.5-3-4-performance-profiling-and-monitoring

# Mark prompt as in-progress
python Development-Plan/scripts/progress_tracker.py start 3.5
```

### Implementation Steps
1. **Before starting**: Ensure dependencies are completed
   ```bash
   python Development-Plan/scripts/progress_tracker.py deps 3.5
   ```

2. **During implementation**: Make incremental commits
   ```bash
   git add .
   git commit -m "feat(3.5): implement core functionality"
   ```

3. **Before completion**: Validate your work
   ```bash
   python Development-Plan/scripts/validate_prompt.py 3.5
   ```

4. **On completion**: Merge and mark complete
   ```bash
   git checkout main
   git merge --no-ff prompt-3.5-3-4-performance-profiling-and-monitoring
   python Development-Plan/scripts/progress_tracker.py complete 3.5
   ```

### Commit Message Format
```
feat(3.5): [description of changes]

- Specific change 1
- Specific change 2
- Add comprehensive tests

Addresses: Performance Profiling & Monitoring
```

For detailed git workflow guidance, see [Shared Git Workflow Context](./_shared_git_workflow_context.md)


Remember: Each component should be production-ready and well-integrated with the existing system.
