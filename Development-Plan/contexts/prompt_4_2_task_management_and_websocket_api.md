# Context for Prompt 4.2: Task Management & WebSocket API

## LLM Recommendation
**Recommended LLM**: Claude 3.5 Sonnet
**Reasoning**: Real-time features require understanding of WebSocket protocols and async task management.

## Prompt Overview
**Phase**: Phase 4 - REST API & Interface
**Position**: Prompt 23 of 26 total
**Dependencies**: Prompts 0.1-4.1

## Original Prompt
```
I need advanced task management with real-time updates via WebSocket.

Implement real-time features with Cursor's async optimization:

1. Create api/task_manager.py:
   - Advanced task queue management
   - Priority-based scheduling
   - Resource allocation
   - Progress tracking
   - Result caching

2. Create api/websocket_handler.py:
   - Real-time progress updates
   - Live task status
   - Result streaming
   - Error notifications
   - Connection management

3. Create api/task_scheduler.py:
   - Intelligent task scheduling
   - Resource-aware allocation
   - Load balancing
   - Batch processing

4. Create tests/test_task_management.py:
   - Task lifecycle tests
   - WebSocket connection tests
   - Real-time update tests
   - Performance tests

Success Criteria:
✅ Tasks execute reliably
✅ Real-time updates work
✅ Resource allocation is optimal
✅ WebSocket connections are stable

Performance Requirements:
- Task scheduling: <50ms
- WebSocket latency: <100ms
- Concurrent connections: 500+
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
- REST API implemented
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
- Implement proper authentication (API keys/JWT)
- Rate limiting to prevent abuse
- Input validation on all endpoints
- CORS configuration
- SQL injection prevention
- XSS protection
- CSRF tokens for state-changing operations
- Secure headers (HSTS, CSP, etc.)

#### Performance Requirements
- Response time: <200ms (95th percentile)
- Concurrent requests: >1000
- WebSocket connections: >500
- Request processing: <100ms

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
- [ ] All endpoints documented
- [ ] Authentication working
- [ ] Rate limiting active
- [ ] OpenAPI schema generated
- [ ] Client SDK updated

### Next Steps

After completing this prompt:
1. Run all tests to ensure nothing is broken
2. Update any affected documentation
3. Commit changes with descriptive message
4. Proceed to Prompt 4.3

### Additional Resources

#### API Development
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [REST API Best Practices](https://restfulapi.net/)
- [API Security Checklist](https://github.com/shieldfy/API-Security-Checklist)

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
git checkout -b prompt-4.3-4-2-task-management-and-websocket-api

# Mark prompt as in-progress
python Development-Plan/scripts/progress_tracker.py start 4.3
```

### Implementation Steps
1. **Before starting**: Ensure dependencies are completed
   ```bash
   python Development-Plan/scripts/progress_tracker.py deps 4.3
   ```

2. **During implementation**: Make incremental commits
   ```bash
   git add .
   git commit -m "feat(4.3): implement core functionality"
   ```

3. **Before completion**: Validate your work
   ```bash
   python Development-Plan/scripts/validate_prompt.py 4.3
   ```

4. **On completion**: Merge and mark complete
   ```bash
   git checkout main
   git merge --no-ff prompt-4.3-4-2-task-management-and-websocket-api
   python Development-Plan/scripts/progress_tracker.py complete 4.3
   ```

### Commit Message Format
```
feat(4.3): [description of changes]

- Specific change 1
- Specific change 2
- Add comprehensive tests

Addresses: Task Management & WebSocket API
```

For detailed git workflow guidance, see [Shared Git Workflow Context](./_shared_git_workflow_context.md)


Remember: Each component should be production-ready and well-integrated with the existing system.
