#!/usr/bin/env python3
"""
Progress tracking system for the Development Plan.
Tracks completion status, test results, and overall project health.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from validate_prompt import PromptValidator

PROGRESS_FILE = Path("Development-Plan/.progress.json")

# Define the complete prompt structure
ALL_PROMPTS = [
    {"id": "0.1", "title": "Project Initialization & Structure", "phase": "Phase 0"},
    {"id": "0.2", "title": "Development Standards & CI Setup", "phase": "Phase 0"},
    {"id": "1.1", "title": "Message Bus & Communication Core", "phase": "Phase 1"},
    {"id": "1.2", "title": "Agent Orchestrator & Lifecycle", "phase": "Phase 1"},
    {"id": "1.3", "title": "Base Agent Framework", "phase": "Phase 1"},
    {"id": "1.4", "title": "Sandbox Environment & Safety", "phase": "Phase 1"},
    {"id": "1.5", "title": "Workflow Engine & Templates", "phase": "Phase 1"},
    {"id": "1.6", "title": "Configuration & Database Connectors", "phase": "Phase 1"},
    {"id": "1.7", "title": "Phase 1 Integration & Validation", "phase": "Phase 1"},
    {"id": "2.1", "title": "Advanced Clarifier Agent", "phase": "Phase 2"},
    {"id": "2.2", "title": "Intelligent Coder Agent", "phase": "Phase 2"},
    {"id": "2.3", "title": "Comprehensive Tester Agent", "phase": "Phase 2"},
    {"id": "2.4", "title": "Agent Communication Protocols", "phase": "Phase 2"},
    {"id": "2.5", "title": "Advanced Agent Orchestration", "phase": "Phase 2"},
    {"id": "2.6", "title": "Phase 2 Agent Integration & Validation", "phase": "Phase 2"},
    {"id": "3.1", "title": "Advanced Schema Intelligence", "phase": "Phase 3"},
    {"id": "3.2", "title": "Query Optimization Engine", "phase": "Phase 3"},
    {"id": "3.3", "title": "Data Quality & Validation Engine", "phase": "Phase 3"},
    {"id": "3.4", "title": "Performance Profiling & Monitoring", "phase": "Phase 3"},
    {"id": "3.5", "title": "Intelligence API & Metadata Store", "phase": "Phase 3"},
    {"id": "3.6", "title": "Phase 3 Intelligence Integration & Validation", "phase": "Phase 3"},
    {"id": "4.1", "title": "Production-Ready REST API", "phase": "Phase 4"},
    {"id": "4.2", "title": "Task Management & WebSocket API", "phase": "Phase 4"},
    {"id": "4.3", "title": "Monitoring Dashboard & Analytics", "phase": "Phase 4"},
    {"id": "4.4", "title": "Python SDK & Documentation", "phase": "Phase 4"},
    {"id": "5.1", "title": "Comprehensive Security & Performance Review", "phase": "Phase 5"},
    {"id": "5.2", "title": "Production Deployment & Operations", "phase": "Phase 5"}
]

class ProgressTracker:
    def __init__(self, progress_file: Path = PROGRESS_FILE):
        self.progress_file = progress_file
        self.data = self._load_progress()
        self.validator = PromptValidator()

    def _load_progress(self) -> Dict:
        """Load progress data from file."""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass

        # Initialize empty progress data
        return {
            "project_started": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "prompts": {},
            "phases": {},
            "statistics": {
                "total_prompts": len(ALL_PROMPTS),
                "completed": 0,
                "failed": 0,
                "in_progress": 0,
                "not_started": len(ALL_PROMPTS)
            }
        }

    def _save_progress(self):
        """Save progress data to file."""
        self.data["last_updated"] = datetime.now().isoformat()
        self.progress_file.parent.mkdir(exist_ok=True)

        with open(self.progress_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def update_prompt_status(self, prompt_id: str, status: str, validation_result: Optional[Dict] = None):
        """Update the status of a specific prompt."""
        if prompt_id not in [p["id"] for p in ALL_PROMPTS]:
            raise ValueError(f"Unknown prompt ID: {prompt_id}")

        # Find prompt info
        prompt_info = next(p for p in ALL_PROMPTS if p["id"] == prompt_id)

        # Update prompt data
        self.data["prompts"][prompt_id] = {
            "title": prompt_info["title"],
            "phase": prompt_info["phase"],
            "status": status,
            "last_updated": datetime.now().isoformat(),
            "validation_result": validation_result,
            "attempts": self.data["prompts"].get(prompt_id, {}).get("attempts", 0) + 1
        }

        # Update phase data
        phase = prompt_info["phase"]
        if phase not in self.data["phases"]:
            self.data["phases"][phase] = {
                "prompts": [],
                "completed": 0,
                "total": 0,
                "status": "not_started"
            }

        phase_prompts = [p["id"] for p in ALL_PROMPTS if p["phase"] == phase]
        self.data["phases"][phase]["prompts"] = phase_prompts
        self.data["phases"][phase]["total"] = len(phase_prompts)

        completed_in_phase = len([
            pid for pid in phase_prompts
            if self.data["prompts"].get(pid, {}).get("status") == "completed"
        ])
        self.data["phases"][phase]["completed"] = completed_in_phase

        if completed_in_phase == len(phase_prompts):
            self.data["phases"][phase]["status"] = "completed"
        elif completed_in_phase > 0:
            self.data["phases"][phase]["status"] = "in_progress"
        else:
            self.data["phases"][phase]["status"] = "not_started"

        # Update overall statistics
        self._update_statistics()

        # Save to file
        self._save_progress()

    def _update_statistics(self):
        """Update overall project statistics."""
        completed = len([p for p in self.data["prompts"].values() if p["status"] == "completed"])
        failed = len([p for p in self.data["prompts"].values() if p["status"] == "failed"])
        in_progress = len([p for p in self.data["prompts"].values() if p["status"] == "in_progress"])
        not_started = len(ALL_PROMPTS) - completed - failed - in_progress

        self.data["statistics"] = {
            "total_prompts": len(ALL_PROMPTS),
            "completed": completed,
            "failed": failed,
            "in_progress": in_progress,
            "not_started": not_started
        }

    def validate_and_update_prompt(self, prompt_id: str) -> Dict:
        """Validate a prompt and update its status."""
        validation_result = self.validator.validate_prompt(prompt_id)

        if validation_result.get("status") == "PASS":
            self.update_prompt_status(prompt_id, "completed", validation_result)
        else:
            self.update_prompt_status(prompt_id, "failed", validation_result)

        return validation_result

    def get_next_prompt(self) -> Optional[str]:
        """Get the next prompt that should be worked on."""
        for prompt in ALL_PROMPTS:
            prompt_status = self.data["prompts"].get(prompt["id"], {}).get("status", "not_started")
            if prompt_status in ["not_started", "failed"]:
                return prompt["id"]
        return None

    def get_phase_status(self, phase: str) -> Dict:
        """Get the status of a specific phase."""
        return self.data["phases"].get(phase, {})

    def get_project_summary(self) -> Dict:
        """Get a summary of the entire project progress."""
        stats = self.data["statistics"]
        completion_percentage = (stats["completed"] / stats["total_prompts"]) * 100

        return {
            "completion_percentage": completion_percentage,
            "statistics": stats,
            "phases": {phase: data["status"] for phase, data in self.data["phases"].items()},
            "next_prompt": self.get_next_prompt(),
            "project_started": self.data["project_started"],
            "last_updated": self.data["last_updated"]
        }

    def generate_report(self) -> str:
        """Generate a detailed progress report."""
        summary = self.get_project_summary()

        report = f"""
🚀 Multi-Agent Database AI - Development Progress Report
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
==========================================

📊 OVERALL PROGRESS: {summary['completion_percentage']:.1f}%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 STATISTICS:
  ✅ Completed: {summary['statistics']['completed']}/{summary['statistics']['total_prompts']}
  ❌ Failed: {summary['statistics']['failed']}
  🔄 In Progress: {summary['statistics']['in_progress']}
  ⏳ Not Started: {summary['statistics']['not_started']}

📋 PHASE STATUS:
"""

        # Add phase details
        for phase_name, phase_status in summary['phases'].items():
            phase_data = self.data["phases"].get(phase_name, {})
            completed = phase_data.get("completed", 0)
            total = phase_data.get("total", 0)
            percentage = (completed / total * 100) if total > 0 else 0

            status_emoji = {
                "completed": "✅",
                "in_progress": "🔄",
                "not_started": "⏳"
            }.get(phase_status, "❓")

            report += f"  {status_emoji} {phase_name}: {completed}/{total} ({percentage:.0f}%)\n"

        # Add next steps
        if summary['next_prompt']:
            next_prompt_info = next(p for p in ALL_PROMPTS if p["id"] == summary['next_prompt'])
            report += f"""
🎯 NEXT STEP:
  Prompt {summary['next_prompt']}: {next_prompt_info['title']}
  Phase: {next_prompt_info['phase']}

  To start: Use context file Development-Plan/contexts/prompt_{summary['next_prompt'].replace('.', '_')}_*.md

"""
        else:
            report += "\n🎉 ALL PROMPTS COMPLETED! 🎉\n"

        # Add recent activity
        recent_prompts = sorted(
            [(pid, data) for pid, data in self.data["prompts"].items()],
            key=lambda x: x[1].get("last_updated", ""),
            reverse=True
        )[:5]

        if recent_prompts:
            report += "📝 RECENT ACTIVITY:\n"
            for prompt_id, prompt_data in recent_prompts:
                status_emoji = {
                    "completed": "✅",
                    "failed": "❌",
                    "in_progress": "🔄"
                }.get(prompt_data["status"], "❓")

                report += f"  {status_emoji} {prompt_id}: {prompt_data['title']} ({prompt_data['status']})\n"

        return report

def main():
    tracker = ProgressTracker()

    if len(sys.argv) == 1:
        # Show progress report
        print(tracker.generate_report())

    elif len(sys.argv) == 2:
        command = sys.argv[1]

        if command == "next":
            next_prompt = tracker.get_next_prompt()
            if next_prompt:
                prompt_info = next(p for p in ALL_PROMPTS if p["id"] == next_prompt)
                print(f"Next prompt: {next_prompt} - {prompt_info['title']}")
                print(f"Context file: Development-Plan/contexts/prompt_{next_prompt.replace('.', '_')}_*.md")
            else:
                print("🎉 All prompts completed!")

        elif command == "validate-all":
            print("🔍 Validating all prompts...")
            for prompt in ALL_PROMPTS:
                result = tracker.validate_and_update_prompt(prompt["id"])
                status_emoji = "✅" if result["status"] == "PASS" else "❌"
                print(f"  {status_emoji} {prompt['id']}: {result['status']}")

            print("\n" + tracker.generate_report())

        else:
            print(f"Unknown command: {command}")
            print("Usage: python progress_tracker.py [next|validate-all]")

    elif len(sys.argv) == 3:
        command, prompt_id = sys.argv[1], sys.argv[2]

        if command == "validate":
            result = tracker.validate_and_update_prompt(prompt_id)
            status_emoji = "✅" if result["status"] == "PASS" else "❌"
            print(f"{status_emoji} Prompt {prompt_id}: {result['status']}")

            if result["status"] == "FAIL" and result.get("issues"):
                print("\n🚨 Issues found:")
                for issue in result["issues"]:
                    print(f"  - {issue}")
                print(f"\n💡 To fix: python scripts/recover_prompt.py {prompt_id}")

        elif command == "start":
            tracker.update_prompt_status(prompt_id, "in_progress")
            print(f"🔄 Started prompt {prompt_id}")

        elif command == "complete":
            tracker.update_prompt_status(prompt_id, "completed")
            print(f"✅ Marked prompt {prompt_id} as completed")

        else:
            print(f"Unknown command: {command}")
            print("Usage: python progress_tracker.py [validate|start|complete] <prompt_id>")

if __name__ == "__main__":
    main()
