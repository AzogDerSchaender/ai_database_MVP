# Improved Context File Structure Example

This demonstrates the improved context file format optimized for LLM comprehension.

---

# Context for Prompt 0.1: Project Initialization & Structure

## 🎯 One-Line Summary
**Create the foundational Python project structure with proper dependencies, configuration files, and directory layout for the multi-agent database AI system.**

## 📋 Checklist Summary (7 Key Items)
- [ ] Create `pyproject.toml` with all dependencies and metadata
- [ ] Create `requirements.txt` and `requirements-dev.txt` with pinned versions
- [ ] Create comprehensive `.gitignore` for Python projects
- [ ] Set up complete directory structure (core/, agents/, database/, etc.)
- [ ] Create `__init__.py` files in all Python packages
- [ ] Verify clean installation with `pip install -e .`
- [ ] Initialize git repository with proper configuration

## 💡 Key Insight
**This is the foundation - get it right the first time! A well-structured project saves hours of refactoring later. Pay special attention to dependency versions and folder organization.**

---

## 🚀 Quick Implementation Guide

### Step 1: Create pyproject.toml
```toml
[build-system]
requires = ["setuptools>=65", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "multi-agent-database-ai"
version = "0.1.0"
description = "AI-powered multi-agent system for database interactions"
requires-python = ">=3.11"

dependencies = [
    "fastapi>=0.108.0",
    "sqlalchemy>=2.0.25",
    "uvicorn>=0.25.0",
    # Add all from dependency list below
]
```

### Step 2: Directory Structure
```bash
mkdir -p {core,agents,database,api,frontend,sdk,config,tests,scripts,docs}
touch {core,agents,database,api,config,tests}/__init__.py
```

---

## 📊 Success Metrics
- ✅ **Installation Time**: < 30 seconds
- ✅ **Import Test**: All packages importable
- ✅ **No Conflicts**: Dependencies resolve cleanly
- ✅ **Structure**: All directories created

## ⚠️ Common Mistakes to Avoid

### ❌ DON'T: Use unpinned dependencies
```txt
# Bad
fastapi
sqlalchemy

# Good
fastapi>=0.108.0,<0.109.0
sqlalchemy>=2.0.25,<2.1.0
```

### ❌ DON'T: Forget __init__.py files
```python
# Every Python package directory needs __init__.py
# Even if it's empty!
```

### ❌ DON'T: Mix development and production deps
```txt
# requirements.txt = production only
# requirements-dev.txt = testing, linting, etc.
```

---

## 🔧 Implementation Details

### LLM Recommendation
**Recommended LLM**: Claude 3.5 Sonnet
**Reasoning**: Project initialization requires understanding of modern Python project structure, dependency management, and development best practices.

### Prompt Overview
**Phase**: Phase 0 - Project Setup & Standards
**Position**: Prompt 1 of 38 total
**Dependencies**: None (this is the first prompt)

### Full Dependency List
```python
# Core Dependencies
fastapi>=0.108.0,<0.109.0
sqlalchemy>=2.0.25,<2.1.0
uvicorn>=0.25.0,<0.26.0
pydantic>=2.5.0,<2.6.0
redis>=5.0.1,<5.1.0
asyncpg>=0.29.0,<0.30.0
psycopg2-binary>=2.9.9,<3.0.0
pymysql>=1.1.0,<1.2.0
alembic>=1.13.1,<1.14.0

# Development Dependencies
pytest>=7.4.3,<8.0.0
pytest-asyncio>=0.21.1,<0.22.0
pytest-cov>=4.1.0,<5.0.0
black>=23.12.0,<24.0.0
mypy>=1.8.0,<2.0.0
flake8>=7.0.0,<8.0.0
isort>=5.13.0,<6.0.0
pre-commit>=3.6.0,<4.0.0
```

### Complete .gitignore
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.hypothesis/

# IDEs
.vscode/
.idea/
*.swp
*.swo
.cursor/

# Database
*.db
*.sqlite3
postgres-data/

# Logs
logs/
*.log

# Environment
.env
.env.local
.env.*.local

# OS
.DS_Store
Thumbs.db
```

### Directory Structure with Descriptions
```
multi-agent-database-ai-mvp/
├── core/               # Core infrastructure (message bus, orchestrator)
├── agents/             # Agent implementations (clarifier, coder, tester)
├── database/           # Database connectors and intelligence
├── api/                # REST API and WebSocket endpoints
├── frontend/           # Web dashboard and monitoring UI
├── sdk/                # Python SDK for external integration
├── config/             # Configuration and settings
├── tests/              # All test suites
├── scripts/            # Utility and deployment scripts
├── docs/               # Documentation
├── docker/             # Docker configurations
├── .github/            # GitHub Actions workflows
└── monitoring/         # Prometheus and Grafana configs
```

## 🧪 Validation Commands

```bash
# Test 1: Verify installation
pip install -e . --dry-run

# Test 2: Check imports
python -c "import core, agents, database, api, config"

# Test 3: Verify structure
find . -name "__init__.py" | wc -l  # Should be >= 6

# Test 4: Dependency check
pip check
```

## 🔗 Integration Points

### Next Steps After Completion
1. **Prompt 0.2**: Development standards and CI setup
2. **Prompt 1.1**: Message bus implementation
3. Begin implementing core infrastructure

### Files Created by This Prompt
- `pyproject.toml`
- `requirements.txt`
- `requirements-dev.txt`
- `.gitignore`
- Directory structure with `__init__.py` files

## 📈 Performance Requirements
- **Installation**: < 30 seconds on standard hardware
- **Import time**: < 2 seconds for all modules
- **Disk usage**: < 500MB including dependencies

## 🔒 Security Considerations
- Use specific version ranges to avoid breaking changes
- Include security-related packages from the start
- Set up `.gitignore` to prevent credential leaks
- Use virtual environments for isolation

## 📝 Notes for LLM

### Critical Points
1. **Version Pinning**: Always use >= and < for version ranges
2. **Python Version**: Require Python 3.11+ for latest async features
3. **File Creation**: Actually create the files, don't just show examples
4. **Validation**: Run the validation commands to ensure success

### Expected Output Structure
```
Created files:
✓ pyproject.toml
✓ requirements.txt
✓ requirements-dev.txt
✓ .gitignore
✓ core/__init__.py
✓ agents/__init__.py
✓ database/__init__.py
✓ api/__init__.py
✓ config/__init__.py
✓ tests/__init__.py

Validation results:
✓ pip install -e . (successful)
✓ Import test passed
✓ Structure verified
```

## 🎯 Definition of Done
- [ ] All files created with correct content
- [ ] Dependencies have proper version constraints
- [ ] Directory structure matches specification
- [ ] Installation completes without errors
- [ ] All validation commands pass
- [ ] Git repository initialized

---

## 🚦 Quick Decision Guide

**If you're unsure about:**
- **Dependency versions**: Use the latest stable with upper bounds
- **Directory naming**: Follow Python conventions (lowercase, underscores)
- **Configuration format**: Prefer TOML over INI for modern Python
- **Testing framework**: Stick with pytest for consistency

**Red flags to watch for:**
- Unpinned dependencies
- Missing `__init__.py` files
- Mixing concerns (e.g., tests in src/)
- Overly complex initial structure

Remember: This is the foundation - simplicity and correctness over cleverness!
