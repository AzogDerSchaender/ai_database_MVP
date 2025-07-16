# Context for Prompt 3.5: Intelligence API & Metadata Store

## LLM Recommendation
**Recommended LLM**: Claude 3.5 Sonnet
**Reasoning**: API design and metadata management require understanding of data governance and API best practices.

## Prompt Overview
**Phase**: Phase 3 - Database Intelligence
**Position**: Prompt 20 of 26 total
**Dependencies**: Prompts 0.1-3.4

## Original Prompt
```
I need a comprehensive intelligence API and metadata management system.

Use Cursor's API design assistance:

1. Create database/intelligence_api.py:
   - Unified intelligence interface
   - Query intelligence endpoints
   - Schema analysis API
   - Performance insights API

2. Create database/metadata_store.py:
   - Centralized metadata repository
   - Version control for metadata
   - Query pattern storage
   - Performance history

3. Create database/knowledge_base.py:
   - Learning from patterns
   - Best practice repository
   - Optimization recommendations
   - Historical insights

4. Create tests/test_intelligence_api.py:
   - API functionality tests
   - Metadata storage tests
   - Knowledge base tests

Success Criteria:
✅ Comprehensive intelligence access
✅ Reliable metadata storage
✅ Learning from experience
✅ Fast knowledge retrieval

Performance Requirements:
- API response time: <200ms
- Metadata queries: <50ms
- Knowledge retrieval: <100ms
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
- Performance profiling implemented
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
4. Proceed to Prompt 3.6

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
git checkout -b prompt-3.6-3-5-intelligence-api-and-metadata-store

# Mark prompt as in-progress
python Development-Plan/scripts/progress_tracker.py start 3.6
```

### Implementation Steps
1. **Before starting**: Ensure dependencies are completed
   ```bash
   python Development-Plan/scripts/progress_tracker.py deps 3.6
   ```

2. **During implementation**: Make incremental commits
   ```bash
   git add .
   git commit -m "feat(3.6): implement core functionality"
   ```

3. **Before completion**: Validate your work
   ```bash
   python Development-Plan/scripts/validate_prompt.py 3.6
   ```

4. **On completion**: Merge and mark complete
   ```bash
   git checkout main
   git merge --no-ff prompt-3.6-3-5-intelligence-api-and-metadata-store
   python Development-Plan/scripts/progress_tracker.py complete 3.6
   ```

### Commit Message Format
```
feat(3.6): [description of changes]

- Specific change 1
- Specific change 2
- Add comprehensive tests

Addresses: Intelligence API & Metadata Store
```

For detailed git workflow guidance, see [Shared Git Workflow Context](./_shared_git_workflow_context.md)


Remember: Each component should be production-ready and well-integrated with the existing system.
