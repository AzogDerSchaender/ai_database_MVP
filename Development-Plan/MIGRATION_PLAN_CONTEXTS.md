# Context Files Migration Plan

## 🎯 Goal
Migrate all existing *38* context files in `Development-Plan/contexts/` to the improved structure (see `IMPROVED_CONTEXT_STRUCTURE_EXAMPLE.md`) without interrupting ongoing development.

## 📅 Phased Approach

| Phase | Files to Migrate | Owner | Duration | Notes |
|-------|------------------|-------|----------|-------|
| 1 | `prompt_0_*.md` (2 files) | Docs team | 1 day | Foundation prompts, low dependency risk |
| 2 | `prompt_1_*.md` (6 files) | Docs team | 2 days | Core infra prompts referenced early |
| 3 | `prompt_2_*.md` (including sub-prompts 2.1a-c, 2.2a-c, 2.3a-c, 2.6a-b) **11 files** | Docs + Engineering | 3 days | Heaviest set, requires coordination |
| 4 | `prompt_3_*.md` (6 files) | Engineering | 2 days | Database intelligence layer |
| 5 | `prompt_4_*.md` (4 files) | Engineering | 1 day | API & monitoring |
| 6 | `prompt_5_*.md` (2 files) | Docs team | 1 day | Final QA & deployment |

Total target time: **10 working days**

## 🔄 Migration Checklist (per file)

1. Add *One-Line Summary*, *Checklist Summary*, *Key Insight* sections.
2. Collapse long dependency tables → reference central list in `CONTEXT_FILES_GUIDE.md`.
3. Move “LLM Recommendation”, “Prompt Overview” below Quick sections.
4. Ensure **Success Metrics**, **Security Considerations**, **Validation Commands** headings exist.
5. Replace inline code blocks with concise examples; move lengthy snippets to `CODE_SNIPPETS_LIBRARY.md` where suitable.
6. Validate markdown with `markdownlint`.
7. Commit with message `migrate(context): prompt_X_Y to new template`.

## ✅ Definition of Done
- All 38 context files follow the improved template.
- No broken internal links or code fences.
- Context size reduced by ≥15 % without information loss.
- LLM test run (generate summary for each file) passes without hallucinations.

---

> Keep migrations small & reviewable. If a prompt is actively being worked on, defer its context migration to the next phase.
