#!/usr/bin/env python3
"""Clean up context files:
1. Remove placeholders ([other directories], [...]).
2. Extract boilerplate General Resources and Common Patterns to shared file.
3. Insert stub test snippet in Testing Strategy section.
"""
import re
from pathlib import Path

CONTEXTS_DIR = Path(__file__).resolve().parent.parent / "contexts"
SHARED_FILE = CONTEXTS_DIR / "_shared_global_context.md"

GENERAL_RESOURCES_HEADING = "#### General Resources"
COMMON_PATTERNS_HEADING = "### Common Patterns to Use"

SHARED_GENERAL_RESOURCES = """#### General Resources
- [Python Documentation](https://docs.python.org/)
- [AsyncIO Documentation](https://docs.python.org/3/library/asyncio.html)
- [Testing Best Practices](https://docs.pytest.org/en/latest/goodpractices.html)
- [OWASP Security Guidelines](https://owasp.org/)
- [Python Packaging User Guide](https://packaging.python.org/)
"""

SHARED_COMMON_PATTERNS = """#### Common Patterns
##### Agent Pattern
```python
class MyAgent(BaseAgent):
    async def initialize(self) -> None:
        await super().initialize()

    async def process_message(self, message: Message) -> Response:
        # Your logic here
        return Response(data={})
```

##### API Endpoint Pattern
```python
@router.post('/endpoint', response_model=ResponseModel)
async def endpoint(request: RequestModel) -> ResponseModel:
    # Validate and process
    return ResponseModel()
```

##### Async Service Pattern
```python
class Service:
    async def process(self, data):
        # Business logic
        return data
```
"""

SHARED_CONTENT = f"# Shared Global Context\n\n{SHARED_GENERAL_RESOURCES}\n\n{SHARED_COMMON_PATTERNS}\n"

def build_shared_file():
    SHARED_FILE.write_text(SHARED_CONTENT, encoding="utf-8")
    print(f"✅ Created/updated shared context file at {SHARED_FILE}")

def clean_placeholders(text: str) -> str:
    return re.sub(r"\[(?:other directories|\.\.\.)]", "", text)

def remove_section(content: str, section_heading: str) -> str:
    pattern = rf"{re.escape(section_heading)}[\s\S]*?(?=\n### |\Z)"
    return re.sub(pattern, f"{section_heading}\nSee _shared_global_context.md\n", content, flags=re.MULTILINE)

def insert_stub_test(content: str) -> str:
    stub = """#### Example Stub Test\n```python\n# tests/unit/test_stub.py\n\n
def test_stub():\n    assert True\n```\n"""
    if "Example Stub Test" in content:
        return content  # already inserted
    # insert after Test File Naming section
    return content.replace("#### Test File Naming", "#### Test File Naming\n- Unit tests: `tests/unit/test_<module_name>.py`\n- Integration tests: `tests/integration/test_<feature>.py`\n- E2E tests: `tests/e2e/test_<workflow>.py`\n\n" + stub)


def process_file(path: Path):
    text = path.read_text(encoding="utf-8")
    original = text
    text = clean_placeholders(text)
    text = remove_section(text, GENERAL_RESOURCES_HEADING)
    text = remove_section(text, COMMON_PATTERNS_HEADING)
    text = insert_stub_test(text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"Updated {path.name}")


def main():
    build_shared_file()
    for md_file in CONTEXTS_DIR.glob("prompt_*.md"):
        process_file(md_file)
    print("\n✅ All context files cleaned and updated.")

if __name__ == "__main__":
    main()
