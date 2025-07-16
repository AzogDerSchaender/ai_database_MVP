#!/usr/bin/env python3
"""
Validation script for individual prompts.
Checks if a prompt was completed correctly and provides recovery guidance.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Prompt validation definitions
PROMPT_VALIDATIONS = {
    "0.1": {
        "files": [
            "pyproject.toml",
            "requirements.txt",
            "requirements-dev.txt",
            ".gitignore",
            "core/__init__.py",
            "agents/__init__.py",
            "database/__init__.py",
            "api/__init__.py",
            "config/__init__.py",
            "tests/__init__.py"
        ],
        "commands": [
            "pip install -e . --dry-run"
        ],
        "tests": []
    },
    "0.2": {
        "files": [
            ".pre-commit-config.yaml",
            "scripts/setup-dev.py",
            "docs/CODING_STANDARDS.md",
            ".github/workflows/ci.yml"
        ],
        "commands": [
            "black --check --diff .",
            "flake8 .",
            "mypy ."
        ],
        "tests": []
    },
    "1.1": {
        "files": [
            "core/message_bus.py",
            "core/message_types.py",
            "tests/test_message_bus.py"
        ],
        "commands": [],
        "tests": ["tests/test_message_bus.py"]
    },
    "1.2": {
        "files": [
            "core/orchestrator.py",
            "core/agent_registry.py",
            "core/health_monitor.py",
            "tests/test_orchestrator.py"
        ],
        "commands": [],
        "tests": ["tests/test_orchestrator.py"]
    },
    "1.3": {
        "files": [
            "core/base_agent.py",
            "core/agent_capabilities.py",
            "core/agent_context.py",
            "tests/test_base_agent.py"
        ],
        "commands": [],
        "tests": ["tests/test_base_agent.py"]
    },
    "1.4": {
        "files": [
            "core/sandbox.py",
            "core/db_executor.py",
            "core/safety_monitor.py",
            "tests/test_sandbox.py"
        ],
        "commands": [],
        "tests": ["tests/test_sandbox.py"]
    },
    "1.5": {
        "files": [
            "core/workflow.py",
            "core/workflow_templates.py",
            "core/progress_tracker.py",
            "tests/test_workflow.py"
        ],
        "commands": [],
        "tests": ["tests/test_workflow.py"]
    },
    "1.6": {
        "files": [
            "config/settings.py",
            "database/base_connector.py",
            "database/postgres_connector.py",
            "database/mysql_connector.py",
            "tests/test_connectors.py"
        ],
        "commands": [],
        "tests": ["tests/test_connectors.py"]
    },
    "1.7": {
        "files": [
            "tests/integration/test_phase1_integration.py",
            "scripts/validate_infrastructure.py",
            "docs/PHASE1_ARCHITECTURE.md"
        ],
        "commands": ["python scripts/validate_infrastructure.py"],
        "tests": ["tests/integration/test_phase1_integration.py"]
    },
    "2.1": {
        "files": [
            "agents/clarifier.py",
            "agents/clarifier_intelligence.py",
            "agents/schema_analyzer.py",
            "tests/test_clarifier.py"
        ],
        "commands": [],
        "tests": ["tests/test_clarifier.py"]
    },
    "2.2": {
        "files": [
            "agents/coder.py",
            "agents/sql_generator.py",
            "agents/code_optimizer.py",
            "tests/test_coder.py"
        ],
        "commands": [],
        "tests": ["tests/test_coder.py"]
    },
    "2.3": {
        "files": [
            "agents/tester.py",
            "agents/test_executor.py",
            "agents/validators.py",
            "tests/test_tester.py"
        ],
        "commands": [],
        "tests": ["tests/test_tester.py"]
    },
    "2.4": {
        "files": [
            "core/protocols.py",
            "core/agent_coordination.py",
            "core/context_sync.py",
            "tests/test_protocols.py"
        ],
        "commands": [],
        "tests": ["tests/test_protocols.py"]
    },
    "2.5": {
        "files": [
            "core/advanced_coordinator.py",
            "workflows/intelligent_workflows.py",
            "core/workflow_optimizer.py",
            "tests/test_advanced_coordination.py"
        ],
        "commands": [],
        "tests": ["tests/test_advanced_coordination.py"]
    },
    "2.6": {
        "files": [
            "tests/integration/test_agent_ecosystem.py",
            "scripts/agent_benchmarks.py",
            "docs/AGENT_ARCHITECTURE.md"
        ],
        "commands": ["python scripts/agent_benchmarks.py"],
        "tests": ["tests/integration/test_agent_ecosystem.py"]
    },
    "3.1": {
        "files": [
            "database/schema_intelligence.py",
            "database/relationship_mapper.py",
            "database/pattern_detector.py",
            "tests/test_schema_intelligence.py"
        ],
        "commands": [],
        "tests": ["tests/test_schema_intelligence.py"]
    },
    "3.2": {
        "files": [
            "database/query_optimizer.py",
            "database/execution_analyzer.py",
            "database/index_advisor.py",
            "tests/test_optimization.py"
        ],
        "commands": [],
        "tests": ["tests/test_optimization.py"]
    },
    "3.3": {
        "files": [
            "database/data_quality.py",
            "database/anomaly_detector.py",
            "database/quality_metrics.py",
            "tests/test_data_quality.py"
        ],
        "commands": [],
        "tests": ["tests/test_data_quality.py"]
    },
    "3.4": {
        "files": [
            "database/performance_profiler.py",
            "database/monitoring_engine.py",
            "database/bottleneck_analyzer.py",
            "tests/test_performance.py"
        ],
        "commands": [],
        "tests": ["tests/test_performance.py"]
    },
    "3.5": {
        "files": [
            "database/intelligence_api.py",
            "database/metadata_store.py",
            "database/knowledge_base.py",
            "tests/test_intelligence_api.py"
        ],
        "commands": [],
        "tests": ["tests/test_intelligence_api.py"]
    },
    "3.6": {
        "files": [
            "tests/integration/test_intelligence_system.py",
            "scripts/intelligence_benchmarks.py",
            "docs/INTELLIGENCE_ARCHITECTURE.md"
        ],
        "commands": ["python scripts/intelligence_benchmarks.py"],
        "tests": ["tests/integration/test_intelligence_system.py"]
    },
    "4.1": {
        "files": [
            "api/app.py",
            "api/endpoints.py",
            "api/middleware.py",
            "tests/test_api.py"
        ],
        "commands": [],
        "tests": ["tests/test_api.py"]
    },
    "4.2": {
        "files": [
            "api/task_manager.py",
            "api/websocket_handler.py",
            "api/task_scheduler.py",
            "tests/test_task_management.py"
        ],
        "commands": [],
        "tests": ["tests/test_task_management.py"]
    },
    "4.3": {
        "files": [
            "frontend/dashboard.html",
            "frontend/dashboard.js",
            "api/analytics.py",
            "tests/test_dashboard.py"
        ],
        "commands": [],
        "tests": ["tests/test_dashboard.py"]
    },
    "4.4": {
        "files": [
            "sdk/client.py",
            "sdk/models.py",
            "examples/comprehensive_examples.py",
            "docs/API_DOCUMENTATION.md"
        ],
        "commands": [],
        "tests": []
    },
    "5.1": {
        "files": [
            "security/security_audit.py",
            "performance/optimization_report.py"
        ],
        "commands": [
            "python security/security_audit.py",
            "python performance/optimization_report.py"
        ],
        "tests": []
    },
    "5.2": {
        "files": [
            "docker/Dockerfile",
            "docker/docker-compose.prod.yml",
            "scripts/deploy.py",
            "monitoring/production_monitoring.py",
            "docs/PRODUCTION_GUIDE.md"
        ],
        "commands": ["python scripts/deploy.py --validate"],
        "tests": []
    }
}

class PromptValidator:
    def __init__(self, project_root: Path = Path(".")):
        self.project_root = project_root
        self.results = {}

    def validate_files(self, files: List[str]) -> Tuple[List[str], List[str]]:
        """Check if required files exist."""
        existing = []
        missing = []

        for file_path in files:
            full_path = self.project_root / file_path
            if full_path.exists():
                existing.append(file_path)
            else:
                missing.append(file_path)

        return existing, missing

    def validate_commands(self, commands: List[str]) -> Dict[str, bool]:
        """Run validation commands."""
        results = {}

        for cmd in commands:
            try:
                result = subprocess.run(
                    cmd, shell=True, capture_output=True, text=True,
                    cwd=self.project_root, timeout=30
                )
                results[cmd] = result.returncode == 0
            except subprocess.TimeoutExpired:
                results[cmd] = False
            except Exception:
                results[cmd] = False

        return results

    def validate_tests(self, test_files: List[str]) -> Dict[str, bool]:
        """Run specified test files."""
        results = {}

        for test_file in test_files:
            test_path = self.project_root / test_file
            if not test_path.exists():
                results[test_file] = False
                continue

            try:
                result = subprocess.run(
                    ["python", "-m", "pytest", str(test_path), "-v"],
                    capture_output=True, text=True,
                    cwd=self.project_root, timeout=60
                )
                results[test_file] = result.returncode == 0
            except subprocess.TimeoutExpired:
                results[test_file] = False
            except Exception:
                results[test_file] = False

        return results

    def validate_imports(self, files: List[str]) -> Dict[str, bool]:
        """Check if Python files can be imported without errors."""
        results = {}

        for file_path in files:
            if not file_path.endswith('.py'):
                continue

            full_path = self.project_root / file_path
            if not full_path.exists():
                results[file_path] = False
                continue

            try:
                # Convert file path to module name
                module_name = file_path.replace('/', '.').replace('.py', '')
                spec = importlib.util.spec_from_file_location(module_name, full_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    results[file_path] = True
                else:
                    results[file_path] = False
            except Exception as e:
                results[file_path] = False

        return results

    def validate_prompt(self, prompt_id: str) -> Dict:
        """Validate a specific prompt completion."""
        if prompt_id not in PROMPT_VALIDATIONS:
            return {"error": f"Unknown prompt ID: {prompt_id}"}

        validation = PROMPT_VALIDATIONS[prompt_id]

        # Check files
        existing_files, missing_files = self.validate_files(validation["files"])

        # Check imports for Python files
        import_results = self.validate_imports(existing_files)

        # Run commands
        command_results = self.validate_commands(validation["commands"])

        # Run tests
        test_results = self.validate_tests(validation["tests"])

        # Calculate overall status
        files_ok = len(missing_files) == 0
        imports_ok = all(import_results.values()) if import_results else True
        commands_ok = all(command_results.values()) if command_results else True
        tests_ok = all(test_results.values()) if test_results else True

        overall_status = files_ok and imports_ok and commands_ok and tests_ok

        return {
            "prompt_id": prompt_id,
            "status": "PASS" if overall_status else "FAIL",
            "files": {
                "existing": existing_files,
                "missing": missing_files
            },
            "imports": import_results,
            "commands": command_results,
            "tests": test_results,
            "issues": self._generate_issues(missing_files, import_results, command_results, test_results)
        }

    def _generate_issues(self, missing_files, import_results, command_results, test_results) -> List[str]:
        """Generate list of issues found."""
        issues = []

        if missing_files:
            issues.append(f"Missing files: {', '.join(missing_files)}")

        failed_imports = [f for f, success in import_results.items() if not success]
        if failed_imports:
            issues.append(f"Import errors: {', '.join(failed_imports)}")

        failed_commands = [cmd for cmd, success in command_results.items() if not success]
        if failed_commands:
            issues.append(f"Failed commands: {', '.join(failed_commands)}")

        failed_tests = [test for test, success in test_results.items() if not success]
        if failed_tests:
            issues.append(f"Failed tests: {', '.join(failed_tests)}")

        return issues

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_prompt.py <prompt_id>")
        print("Example: python validate_prompt.py 1.1")
        sys.exit(1)

    prompt_id = sys.argv[1]
    validator = PromptValidator()
    result = validator.validate_prompt(prompt_id)

    print(f"\n🔍 Validation Results for Prompt {prompt_id}")
    print("=" * 50)

    status_emoji = "✅" if result["status"] == "PASS" else "❌"
    print(f"Status: {status_emoji} {result['status']}")

    if result["files"]["missing"]:
        print(f"\n❌ Missing Files ({len(result['files']['missing'])}):")
        for file in result["files"]["missing"]:
            print(f"  - {file}")

    if result["files"]["existing"]:
        print(f"\n✅ Existing Files ({len(result['files']['existing'])}):")
        for file in result["files"]["existing"]:
            print(f"  - {file}")

    if result["imports"]:
        print(f"\n🐍 Import Validation:")
        for file, success in result["imports"].items():
            status = "✅" if success else "❌"
            print(f"  {status} {file}")

    if result["commands"]:
        print(f"\n⚡ Command Validation:")
        for cmd, success in result["commands"].items():
            status = "✅" if success else "❌"
            print(f"  {status} {cmd}")

    if result["tests"]:
        print(f"\n🧪 Test Validation:")
        for test, success in result["tests"].items():
            status = "✅" if success else "❌"
            print(f"  {status} {test}")

    if result["issues"]:
        print(f"\n🚨 Issues Found:")
        for issue in result["issues"]:
            print(f"  - {issue}")

        print(f"\n💡 Recovery Suggestions:")
        print(f"  1. Run: python scripts/recover_prompt.py {prompt_id}")
        print(f"  2. Check: Development-Plan/contexts/prompt_{prompt_id.replace('.', '_')}_*.md")
        print(f"  3. Verify dependencies from previous prompts")

    sys.exit(0 if result["status"] == "PASS" else 1)

if __name__ == "__main__":
    main()
