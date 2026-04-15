# {{SKILL_NAME}}

> {{One-line description of what this Skill does}}

## Quick Start

1. Read `delivery/SKILL.md` for the operating contract
2. Read `docs/product/PRD.md` for complete product logic
3. Read `docs/requirements/api-spec.md` for data source requirements

## Architecture

```
┌──────────────────────────────────────────────────┐
│                   delivery/                      │
│   SKILL.md · README · VERSION · metadata         │
├──────────────────────────────────────────────────┤
│                implementation/                   │
│   L1 Data → L2 Compute → L3 Decision → L4 UI     │
├──────────────────────────────────────────────────┤
│                     docs/                        │
│   PRD → business/api/compute/prompt/viz/test     │
└──────────────────────────────────────────────────┘
```

## File Index

### docs/

| File | Purpose |
|------|---------|
| `docs/product/PRD.md` | Complete product logic |
| `docs/requirements/business-spec.md` | Business rules and constraints |
| `docs/requirements/api-spec.md` | API endpoints, fields, schemas |
| `docs/requirements/backend-computation.md` | Scoring algorithms, formulas |
| `docs/requirements/implementation-guide.md` | Frontend + AI integration guide |
| `docs/requirements/ai-prompts.md` | LLM prompt specification |
| `docs/requirements/viz-specs.md` | Visual design specifications |
| `docs/requirements/prototype-notes.md` | Demo vs production differences |
| `docs/requirements/TestSuite.md` | Test cases and checklists |
| `docs/review/SKILL-REVIEW.md` | Gap analysis template |

### implementation/

| File | Purpose |
|------|---------|
| `implementation/frontend/{{SKILL_SLUG}}.html` | Hi-Fi demo (visual reference) |
| `implementation/scripts/validate-ai-output.js` | Output validation script |
| `implementation/tests/` | Automated tests |

### delivery/

| File | Purpose |
|------|---------|
| `delivery/SKILL.md` | Main control document (8 sections) |
| `delivery/README.md` | English overview |
| `delivery/README.zh.md` | Chinese overview |
| `delivery/agents/openai.yaml` | Store metadata |
| `delivery/VERSION` | Semantic version |

## TODO for Tech Team

See `docs/requirements/implementation-guide.md` and `docs/review/SKILL-REVIEW.md`.

## License

Proprietary — Antseer.ai
