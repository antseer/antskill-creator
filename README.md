<div align="center">

# Skill Creator Rick

Move a skill through a two-stage lifecycle: Requirement Skill first, Complete Skill after real MCP/data verification.

English | [简体中文](README.zh.md)

</div>

## Two stages

### Stage 1 — Requirement Skill

Use this when the product plan is complete but real data integration is not finished.

Required outcome:
- full product plan / PRD / user flow
- frontend or output experience
- backend capability requirements
- data-source dependency list
- mock-data boundary and replacement plan
- engineering implementation docs

The skill may use mock data, but every mock item must map to the real MCP / API / database source that will replace it.

### Stage 2 — Complete Skill

Use this when the Stage 1 mock data has been replaced.

Required outcome:
- user path no longer depends on mock / stub / random demo data
- all required data dependencies are covered by MCP / API / database or explicitly marked as not requiring external data
- `MCP-COVERAGE.md` proves coverage
- README contains data sources and validation evidence
- package can be installed, run, shared, or published

> `split` is a packaging action, not a third stage.

## What this skill does

- classify a local skill as Stage 1 Requirement or Stage 2 Complete
- detect when a mixed package should be split first
- scaffold stage-specific files from maintainable templates
- add bilingual README files, metadata, icons, and agent facade
- generate engineering-facing MCP / API / data-source request docs
- validate stage-specific package readiness
- generate structured audit reports with score, missing items, and Stage 2 blockers
- publish to GitHub when asked

## Data Sources

This meta-skill does not require external market data. It operates on local skill files provided by the user.

| Data item | Real source | Method | Last verified | Failure handling |
|---|---|---|---|---|
| Skill package files | User local filesystem | Direct file read/write | 2026-04-27 | Report missing files and required fixes |
| Package standards | Local references in this skill | `references/*.md` | 2026-04-27 | Fall back to `SKILL.md` contract |
| Validation rules | Local Python scripts | `scripts/quick_validate.py`, `scripts/validate_shareable_skill.py`, `scripts/audit_skill.py` | 2026-04-27 | Print validation errors and audit reports |
| Scaffold templates | Local template files | `templates/requirement`, `templates/complete`, `templates/common` | 2026-04-27 | Fail fast if a template is missing |
| Executable checks | Local check config | `validation.checks.json` | 2026-04-27 | Fail the Stage 2 `--run-checks` gate |

## Validation Evidence

| Check | Command / method | Result | Date |
|---|---|---|---|
| Frontmatter validation | `python scripts/quick_validate.py .` | pass | 2026-04-27 |
| Stage validator syntax | `python -m py_compile scripts/*.py` | pass | 2026-04-27 |
| Stage 1 scaffold smoke test | generate temp requirement package then validate with `--stage requirement` | pass | 2026-04-27 |
| Stage 2 scaffold smoke test | generate temp complete package then validate with `--stage complete` | pass with filled sample values | 2026-04-27 |
| Executable validation gate | `python scripts/validate_shareable_skill.py . --stage complete --run-checks` | pass | 2026-04-27 |
| Structured audit report | `python scripts/audit_skill.py . --stage complete --run-checks --format json` | pass | 2026-04-27 |

## Example requests

```text
/skill-creator-rick review this skill and tell me which stage it is
/skill-creator-rick scaffold a Stage 1 Requirement Skill from this PRD + prototype
/skill-creator-rick upgrade this Stage 1 package to Stage 2 after MCP is ready
/skill-creator-rick validate this package as Stage 2 Complete
/skill-creator-rick split this large skill into independent packages
```
