# Context for Prompt 4.3: Monitoring Dashboard & Analytics

## LLM Recommendation
**Recommended LLM**: Claude 3.5 Sonnet
**Reasoning**: Dashboard development requires frontend skills and understanding of data visualization best practices.

## Prompt Overview
**Phase**: Phase 4 - REST API & Interface
**Position**: Prompt 24 of 26 total
**Dependencies**: Prompts 0.1-4.2

## Original Prompt
```
I need a comprehensive monitoring dashboard with analytics capabilities.

Create advanced monitoring with Cursor's frontend assistance:

1. Create frontend/dashboard.html:
   - Modern responsive dashboard
   - Real-time metrics display
   - Interactive charts
   - Agent status monitoring
   - Performance analytics

2. Create frontend/dashboard.js:
   - Real-time data updates
   - Interactive visualizations
   - WebSocket integration
   - Performance charts
   - Alert notifications

3. Create api/analytics.py:
   - Usage analytics
   - Performance metrics
   - User behavior tracking
   - Trend analysis
   - Report generation

4. Create tests/test_dashboard.py:
   - Dashboard functionality tests
   - Real-time update tests
   - Chart rendering tests

Success Criteria:
✅ Dashboard loads quickly
✅ Real-time updates work
✅ Charts are interactive
✅ Analytics are accurate

Performance Requirements:
- Dashboard load time: <2 seconds
- Real-time updates: <100ms latency
- Chart rendering: <500ms
```

## Project Context

### Current Project Structure
```
multi-agent-database-ai-mvp/
├── core/
│   └── [complete infrastructure]
├── agents/
│   └── [all agents implemented]
├── database/
│   └── [intelligence system]
├── api/
│   └── [API in progress]
├──
```

### Key Dependencies
```python
# Frontend/API Dependencies
uvicorn[standard]>=0.25.0
websockets>=12.0
jinja2>=3.1.2
python-multipart>=0.0.6
httpx>=0.25.2
```

### Docker Environment
The project uses Docker Compose with:
- PostgreSQL database (primary datastore)
- Redis cache (message queue and caching)
- Application container (FastAPI app)
- Nginx reverse proxy (production only)

## Current State Analysis
- Task management implemented
- Complete backend system operational
- All intelligence features working
- Ready for API layer

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
- **Complete backend system**
- **All agents operational**
- **Database intelligence active**
- **Ready for API layer**

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
4. Proceed to Prompt 4.4

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
git checkout -b prompt-4.4-4-3-monitoring-dashboard-and-analytics

# Mark prompt as in-progress
python Development-Plan/scripts/progress_tracker.py start 4.4
```

### Implementation Steps
1. **Before starting**: Ensure dependencies are completed
   ```bash
   python Development-Plan/scripts/progress_tracker.py deps 4.4
   ```

2. **During implementation**: Make incremental commits
   ```bash
   git add .
   git commit -m "feat(4.4): implement core functionality"
   ```

3. **Before completion**: Validate your work
   ```bash
   python Development-Plan/scripts/validate_prompt.py 4.4
   ```

4. **On completion**: Merge and mark complete
   ```bash
   git checkout main
   git merge --no-ff prompt-4.4-4-3-monitoring-dashboard-and-analytics
   python Development-Plan/scripts/progress_tracker.py complete 4.4
   ```

### Commit Message Format
```
feat(4.4): [description of changes]

- Specific change 1
- Specific change 2
- Add comprehensive tests

Addresses: Monitoring Dashboard & Analytics
```

For detailed git workflow guidance, see [Shared Git Workflow Context](./_shared_git_workflow_context.md)


Remember: Each component should be production-ready and well-integrated with the existing system.
