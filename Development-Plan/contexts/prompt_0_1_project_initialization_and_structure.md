# Context for Prompt 0.1: Project Initialization & Structure

## LLM Recommendation
**Recommended LLM**: Claude 3.5 Sonnet
**Reasoning**: Project initialization requires understanding of modern Python project structure, dependency management, and development best practices.

## Prompt Overview
**Phase**: Phase 0 - Project Setup & Standards
**Position**: Prompt 1 of 26 total
**Dependencies**: None (this is the first prompt)

## Original Prompt
```
I need to set up a complete Python project structure for a multi-agent database AI system, optimized for Cursor AI development.

Please create the complete project foundation:

1. Create pyproject.toml:
   - Project metadata and dependencies
   - FastAPI, SQLAlchemy, asyncio support
   - Development dependencies (pytest, black, mypy)
   - Build system configuration

2. Create requirements.txt and requirements-dev.txt:
   - Production dependencies with pinned versions
   - Development tools and testing frameworks
   - Database drivers (psycopg2, PyMySQL)

3. Create .gitignore:
   - Python-specific ignores
   - IDE and environment files
   - Database and log files
   - Cursor-specific ignores

4. Create initial directory structure:
```

## Project Context

### Current Project Structure
This is the initial prompt, so no existing structure exists yet. We are creating the foundation from scratch.

### Key Dependencies
```python
# Core Dependencies
fastapi>=0.108.0
sqlalchemy>=2.0.25
asyncio  # Built-in
uvicorn>=0.25.0
pydantic>=2.5.0
redis>=5.0.1

# Database Dependencies
asyncpg>=0.29.0
psycopg2-binary>=2.9.9
pymysql>=1.1.0
alembic>=1.13.1

# Development Dependencies
pytest>=7.4.3
pytest-asyncio>=0.21.1
pytest-cov>=4.1.0
black>=23.12.0
mypy>=1.8.0
flake8>=7.0.0
isort>=5.13.0
pre-commit>=3.6.0
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
- Starting from scratch
- Setting up project foundation
- No existing code to integrate with
- Focus on correct structure and standards

## Implementation Requirements

### Core Components to Build
1. Project configuration files (pyproject.toml)
2. Requirements files with proper versioning
3. Complete directory structure
4. Git configuration files
5. Python package initialization files

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
- None yet (this is the beginning)

#### External Services
- Git (version control)
- PyPI (package repository)

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
4. Proceed to Prompt 0.2

### Additional Resources

#### Python Packaging
- [Python Packaging User Guide](https://packaging.python.org/)
- [PEP 517](https://peps.python.org/pep-0517/)
- [PEP 518](https://peps.python.org/pep-0518/)

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
git checkout -b prompt-0.2-0-1-project-initialization-and-structure

# Mark prompt as in-progress
python Development-Plan/scripts/progress_tracker.py start 0.2
```

### Implementation Steps
1. **Before starting**: Ensure dependencies are completed
   ```bash
   python Development-Plan/scripts/progress_tracker.py deps 0.2
   ```

2. **During implementation**: Make incremental commits
   ```bash
   git add .
   git commit -m "feat(0.2): implement core functionality"
   ```

3. **Before completion**: Validate your work
   ```bash
   python Development-Plan/scripts/validate_prompt.py 0.2
   ```

4. **On completion**: Merge and mark complete
   ```bash
   git checkout main
   git merge --no-ff prompt-0.2-0-1-project-initialization-and-structure
   python Development-Plan/scripts/progress_tracker.py complete 0.2
   ```

### Commit Message Format
```
feat(0.2): [description of changes]

- Specific change 1
- Specific change 2
- Add comprehensive tests

Addresses: Project Initialization & Structure
```

For detailed git workflow guidance, see [Shared Git Workflow Context](./_shared_git_workflow_context.md)


Remember: Each component should be production-ready and well-integrated with the existing system.
