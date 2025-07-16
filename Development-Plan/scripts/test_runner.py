#!/usr/bin/env python3
"""
Incremental testing guidance system.
Provides step-by-step testing instructions for each development phase.
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Define incremental testing steps for each phase
TESTING_GUIDANCE = {
    "phase_0": {
        "name": "Project Setup & Standards",
        "tests": [
            {
                "step": 1,
                "name": "Project Structure Validation",
                "command": "python -c \"import core, agents, database, api, config; print('✅ All packages importable')\"",
                "description": "Verify all Python packages can be imported",
                "fix_on_fail": "Check __init__.py files exist in all directories"
            },
            {
                "step": 2,
                "name": "Package Installation",
                "command": "pip install -e . --dry-run",
                "description": "Verify package can be installed",
                "fix_on_fail": "Check pyproject.toml syntax and dependencies"
            },
            {
                "step": 3,
                "name": "Code Quality Tools",
                "command": "black --check --diff .",
                "description": "Verify code formatting standards",
                "fix_on_fail": "Run: black ."
            },
            {
                "step": 4,
                "name": "Type Checking",
                "command": "mypy . --ignore-missing-imports",
                "description": "Verify type hints are correct",
                "fix_on_fail": "Add missing type hints and fix type errors"
            }
        ]
    },
    "phase_1": {
        "name": "Core Infrastructure",
        "tests": [
            {
                "step": 1,
                "name": "Message Bus Unit Tests",
                "command": "python -m pytest tests/test_message_bus.py -v",
                "description": "Test message passing infrastructure",
                "fix_on_fail": "Fix message bus implementation or tests"
            },
            {
                "step": 2,
                "name": "Agent Orchestrator Tests",
                "command": "python -m pytest tests/test_orchestrator.py -v",
                "description": "Test agent lifecycle management",
                "fix_on_fail": "Fix orchestrator implementation or tests"
            },
            {
                "step": 3,
                "name": "Base Agent Framework Tests",
                "command": "python -m pytest tests/test_base_agent.py -v",
                "description": "Test agent base class functionality",
                "fix_on_fail": "Fix base agent implementation"
            },
            {
                "step": 4,
                "name": "Sandbox Security Tests",
                "command": "python -m pytest tests/test_sandbox.py -v",
                "description": "Test database sandbox isolation",
                "fix_on_fail": "Critical: Fix sandbox security issues immediately"
            },
            {
                "step": 5,
                "name": "Database Connector Tests",
                "command": "python -m pytest tests/test_connectors.py -v",
                "description": "Test database connectivity",
                "fix_on_fail": "Fix database connector implementation"
            },
            {
                "step": 6,
                "name": "Phase 1 Integration Tests",
                "command": "python -m pytest tests/integration/test_phase1_integration.py -v",
                "description": "Test all Phase 1 components working together",
                "fix_on_fail": "Fix integration issues between components"
            }
        ]
    },
    "phase_2": {
        "name": "Core Agents",
        "tests": [
            {
                "step": 1,
                "name": "Clarifier Agent Tests",
                "command": "python -m pytest tests/test_clarifier*.py -v",
                "description": "Test clarifier agent functionality",
                "fix_on_fail": "Fix clarifier agent implementation"
            },
            {
                "step": 2,
                "name": "Coder Agent Tests",
                "command": "python -m pytest tests/test_coder*.py -v",
                "description": "Test SQL generation functionality",
                "fix_on_fail": "Fix coder agent implementation"
            },
            {
                "step": 3,
                "name": "Tester Agent Tests",
                "command": "python -m pytest tests/test_tester*.py -v",
                "description": "Test validation and testing functionality",
                "fix_on_fail": "Fix tester agent implementation"
            },
            {
                "step": 4,
                "name": "Agent Communication Tests",
                "command": "python -m pytest tests/test_protocols.py -v",
                "description": "Test inter-agent communication",
                "fix_on_fail": "Fix agent communication protocols"
            },
            {
                "step": 5,
                "name": "Agent Ecosystem Integration",
                "command": "python -m pytest tests/integration/test_agent_ecosystem.py -v",
                "description": "Test complete agent workflow",
                "fix_on_fail": "Fix agent coordination issues"
            }
        ]
    },
    "phase_3": {
        "name": "Database Intelligence",
        "tests": [
            {
                "step": 1,
                "name": "Schema Intelligence Tests",
                "command": "python -m pytest tests/test_schema_intelligence.py -v",
                "description": "Test schema analysis capabilities",
                "fix_on_fail": "Fix schema intelligence implementation"
            },
            {
                "step": 2,
                "name": "Query Optimization Tests",
                "command": "python -m pytest tests/test_optimization.py -v",
                "description": "Test query optimization engine",
                "fix_on_fail": "Fix query optimization logic"
            },
            {
                "step": 3,
                "name": "Data Quality Tests",
                "command": "python -m pytest tests/test_data_quality.py -v",
                "description": "Test data quality analysis",
                "fix_on_fail": "Fix data quality validation"
            },
            {
                "step": 4,
                "name": "Performance Monitoring Tests",
                "command": "python -m pytest tests/test_performance.py -v",
                "description": "Test performance profiling",
                "fix_on_fail": "Fix performance monitoring implementation"
            },
            {
                "step": 5,
                "name": "Intelligence System Integration",
                "command": "python -m pytest tests/integration/test_intelligence_system.py -v",
                "description": "Test complete intelligence system",
                "fix_on_fail": "Fix intelligence system integration"
            }
        ]
    },
    "phase_4": {
        "name": "REST API & Interface",
        "tests": [
            {
                "step": 1,
                "name": "API Endpoint Tests",
                "command": "python -m pytest tests/test_api.py -v",
                "description": "Test REST API endpoints",
                "fix_on_fail": "Fix API implementation"
            },
            {
                "step": 2,
                "name": "Task Management Tests",
                "command": "python -m pytest tests/test_task_management.py -v",
                "description": "Test task queue and WebSocket functionality",
                "fix_on_fail": "Fix task management implementation"
            },
            {
                "step": 3,
                "name": "Dashboard Tests",
                "command": "python -m pytest tests/test_dashboard.py -v",
                "description": "Test monitoring dashboard",
                "fix_on_fail": "Fix dashboard implementation"
            },
            {
                "step": 4,
                "name": "SDK Tests",
                "command": "python -m pytest tests/test_sdk.py -v",
                "description": "Test Python SDK functionality",
                "fix_on_fail": "Fix SDK implementation"
            }
        ]
    },
    "phase_5": {
        "name": "Quality & Deployment",
        "tests": [
            {
                "step": 1,
                "name": "Security Audit",
                "command": "python security/security_audit.py",
                "description": "Run comprehensive security scan",
                "fix_on_fail": "Fix all security vulnerabilities before proceeding"
            },
            {
                "step": 2,
                "name": "Performance Benchmarks",
                "command": "python performance/optimization_report.py",
                "description": "Validate performance requirements",
                "fix_on_fail": "Optimize performance to meet targets"
            },
            {
                "step": 3,
                "name": "Full Test Suite",
                "command": "python -m pytest tests/ --cov=. --cov-report=term-missing",
                "description": "Run complete test suite with coverage",
                "fix_on_fail": "Fix failing tests and improve coverage to >90%"
            },
            {
                "step": 4,
                "name": "Deployment Validation",
                "command": "python scripts/deploy.py --validate",
                "description": "Validate deployment configuration",
                "fix_on_fail": "Fix deployment configuration issues"
            }
        ]
    }
}

class IncrementalTester:
    def __init__(self):
        self.project_root = Path(".")
        if Path.cwd().name == "Development-Plan":
            self.project_root = Path("..")

    def run_test(self, test: Dict) -> Tuple[bool, str]:
        """Run a single test and return success status and output."""
        try:
            result = subprocess.run(
                test["command"],
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=60
            )

            success = result.returncode == 0
            output = result.stdout + result.stderr

            return success, output

        except subprocess.TimeoutExpired:
            return False, "Test timed out after 60 seconds"
        except Exception as e:
            return False, f"Test execution failed: {str(e)}"

    def run_phase_tests(self, phase: str, stop_on_failure: bool = True) -> Dict:
        """Run all tests for a specific phase."""
        if phase not in TESTING_GUIDANCE:
            return {"error": f"Unknown phase: {phase}"}

        phase_info = TESTING_GUIDANCE[phase]
        results = {
            "phase": phase,
            "name": phase_info["name"],
            "tests": [],
            "summary": {
                "total": len(phase_info["tests"]),
                "passed": 0,
                "failed": 0,
                "skipped": 0
            }
        }

        for test in phase_info["tests"]:
            print(f"\n🧪 Running Step {test['step']}: {test['name']}")
            print(f"📝 {test['description']}")
            print(f"⚡ Command: {test['command']}")

            success, output = self.run_test(test)

            test_result = {
                "step": test["step"],
                "name": test["name"],
                "success": success,
                "output": output,
                "fix_suggestion": test.get("fix_on_fail", "Check implementation")
            }

            results["tests"].append(test_result)

            if success:
                print(f"✅ PASSED")
                results["summary"]["passed"] += 1
            else:
                print(f"❌ FAILED")
                print(f"💡 Fix: {test['fix_on_fail']}")
                results["summary"]["failed"] += 1

                if stop_on_failure:
                    print(f"\n🛑 Stopping at first failure. Fix the issue and re-run.")
                    break

        # Mark remaining tests as skipped if we stopped early
        if stop_on_failure and results["summary"]["failed"] > 0:
            skipped = results["summary"]["total"] - results["summary"]["passed"] - results["summary"]["failed"]
            results["summary"]["skipped"] = skipped

        return results

    def run_incremental_test(self, start_phase: str = "phase_0") -> Dict:
        """Run incremental tests starting from a specific phase."""
        phases = ["phase_0", "phase_1", "phase_2", "phase_3", "phase_4", "phase_5"]

        if start_phase not in phases:
            return {"error": f"Invalid start phase: {start_phase}"}

        start_index = phases.index(start_phase)
        overall_results = {
            "start_phase": start_phase,
            "phases": [],
            "overall_success": True
        }

        for phase in phases[start_index:]:
            print(f"\n{'='*60}")
            print(f"🚀 Starting {TESTING_GUIDANCE[phase]['name']} Tests")
            print(f"{'='*60}")

            phase_results = self.run_phase_tests(phase)
            overall_results["phases"].append(phase_results)

            if phase_results["summary"]["failed"] > 0:
                overall_results["overall_success"] = False
                print(f"\n❌ Phase {phase} failed. Please fix issues before continuing.")
                break
            else:
                print(f"\n✅ Phase {phase} completed successfully!")

        return overall_results

    def generate_test_report(self, results: Dict) -> str:
        """Generate a detailed test report."""
        report = f"""
🧪 Incremental Testing Report
Generated: {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()}
{'='*50}

Overall Status: {'✅ SUCCESS' if results.get('overall_success', False) else '❌ FAILURE'}

"""

        for phase_result in results.get("phases", []):
            phase_name = phase_result["name"]
            summary = phase_result["summary"]

            report += f"""
📋 {phase_name}
  Total Tests: {summary['total']}
  ✅ Passed: {summary['passed']}
  ❌ Failed: {summary['failed']}
  ⏭️  Skipped: {summary['skipped']}

"""

            # Add details for failed tests
            failed_tests = [t for t in phase_result["tests"] if not t["success"]]
            if failed_tests:
                report += "  Failed Tests:\n"
                for test in failed_tests:
                    report += f"    • {test['name']}: {test['fix_suggestion']}\n"

        return report

def main():
    tester = IncrementalTester()

    if len(sys.argv) == 1:
        # Run all tests from the beginning
        print("🧪 Running incremental tests from Phase 0...")
        results = tester.run_incremental_test()
        print(tester.generate_test_report(results))

    elif len(sys.argv) == 2:
        phase = sys.argv[1]

        if phase == "help":
            print("""
Incremental Testing System

Usage:
  python test_runner.py                    # Run all tests from Phase 0
  python test_runner.py phase_1            # Run tests starting from Phase 1
  python test_runner.py phase_2 --continue # Run Phase 2 tests, continue on failure
  python test_runner.py list              # List all available phases

Available Phases:
  phase_0 - Project Setup & Standards
  phase_1 - Core Infrastructure
  phase_2 - Core Agents
  phase_3 - Database Intelligence
  phase_4 - REST API & Interface
  phase_5 - Quality & Deployment
            """)

        elif phase == "list":
            print("\n📋 Available Test Phases:")
            for phase_id, phase_info in TESTING_GUIDANCE.items():
                print(f"  {phase_id}: {phase_info['name']} ({len(phase_info['tests'])} tests)")

        elif phase.startswith("phase_"):
            print(f"🧪 Running tests for {phase}...")
            results = tester.run_phase_tests(phase)

            print(f"\n📊 Results for {results['name']}:")
            print(f"  ✅ Passed: {results['summary']['passed']}")
            print(f"  ❌ Failed: {results['summary']['failed']}")
            print(f"  ⏭️  Skipped: {results['summary']['skipped']}")

            if results['summary']['failed'] > 0:
                print(f"\n🚨 Failed Tests:")
                for test in results['tests']:
                    if not test['success']:
                        print(f"  • {test['name']}: {test['fix_suggestion']}")

        else:
            print(f"Unknown command: {phase}")
            print("Use 'python test_runner.py help' for usage information")

if __name__ == "__main__":
    main()
