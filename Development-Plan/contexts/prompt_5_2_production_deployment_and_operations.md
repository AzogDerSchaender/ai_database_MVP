# Context for Prompt 5.2: Production Deployment & Operations

## LLM Recommendation
**Recommended LLM**: Claude 3.5 Sonnet
**Reasoning**: Production deployment requires DevOps expertise and understanding of deployment best practices.

## Prompt Overview
**Phase**: Phase 5 - Quality & Deployment
**Position**: Prompt 27 of 26 total
**Dependencies**: All prompts 0.1-5.1

## Original Prompt
```
I need complete production deployment setup with monitoring and operations.

Create production-ready deployment with Cursor's DevOps assistance:

1. Create docker/Dockerfile:
   - Multi-stage production build
   - Security hardening
   - Minimal attack surface
   - Performance optimization

2. Create docker/docker-compose.prod.yml:
   - Production service definitions
   - Database clustering
   - Load balancing
   - Health checks
   - Logging configuration

3. Create scripts/deploy.py:
   - Automated deployment
   - Database migrations
   - Service validation
   - Rollback capability

4. Create monitoring/production_monitoring.py:
   - Application monitoring
   - Infrastructure monitoring
   - Log aggregation
   - Alert management

5. Create docs/PRODUCTION_GUIDE.md:
   - Deployment instructions
   - Configuration guide
   - Monitoring setup
   - Troubleshooting procedures
   - Maintenance guidelines

Success Criteria:
✅ One-command deployment
✅ Zero-downtime updates
✅ Comprehensive monitoring
✅ Automated recovery

Performance Requirements:
- Deployment time: <5 minutes
- Service startup: <30 seconds
- Health check response: <1 second
- Log processing: <10ms per entry
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
- System reviewed and optimized
- Full system implemented
- All features working
- Ready for production hardening

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
4. Proceed to Prompt None (final prompt)

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



Remember: Each component should be production-ready and well-integrated with the existing system.
