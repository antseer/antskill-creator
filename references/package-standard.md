# Skill Creator Rick Two-Stage Package Standard

## Goal

Produce skill packages that are honest about their lifecycle stage:

1. **Stage 1 — Requirement Skill**: complete product / frontend / backend / data-source plan, current experience shown with mock data, ready for engineering implementation.
2. **Stage 2 — Complete Skill**: all user-path mock data replaced by real MCP / API / database sources, verified, ready for direct use and sharing.

`split` is a packaging action, not a lifecycle stage.

## Stage 1 — Requirement Skill

Use when the product is defined but real data integration is not finished.

Required:
- `SKILL.md`
- `README.md` with `Data Reality`
- `README.zh.md` with `数据真实性`
- `skill.meta.json` if the skill accepts user parameters (`input_schema` required)
- `REQUIREMENT-REVIEW.md`
- `TODO-TECH.md`
- `TECH-INTERFACE-REQUEST.md`
- At least one product-plan artifact: PRD, spec, prototype, frontend/backend doc, or `docs/PRODUCT-SPEC.md`

Must state:
- which data is mock / fixture / stub
- where each mock appears in the user experience
- which MCP / API / database should replace it
- what blocks Stage 2
- that mock data is for demonstration only

Must not claim:
- direct-use ready
- directly usable for real analysis
- fully integrated with real data

## Stage 2 — Complete Skill

Use when the skill can be directly installed / run / reused.

Required:
- `SKILL.md`
- `README.md` with `Data Sources` and `Validation Evidence`
- `README.zh.md` with `数据来源` and `验证证据`
- `skill.meta.json` if the skill accepts user parameters (`input_schema` required)
- `agents/openai.yaml`
- `VERSION`
- `.env.example` if env vars / auth are needed
- `MCP-COVERAGE.md`
- runnable logic / scripts / pipeline when the skill requires execution
- tests, evals, or minimal run evidence
- `validation.checks.json` when Stage 2 readiness depends on executable local checks

Must state:
- every required data item
- real source for each item
- MCP / API / database method
- last verification date
- failure / empty-state handling
- evidence that user-path mock data is gone

## Split package

Use when one original skill contains multiple independent promises.

Required per child package:
- independent `SKILL.md`
- independent README pair
- own data-source / mock reality table
- copied or recreated assets/scripts/references if needed
- no hidden dependency on a sibling skill's README or assets

Split plan format:

```markdown
| Child skill | User | Input | Output | Data dependency | Stage |
|---|---|---|---|---|---|
```

## Validation checklist

- `SKILL.md` passes frontmatter validation
- Stage is explicitly stated as Stage 1 Requirement or Stage 2 Complete
- Stage 1 has `Data Reality`, Stage 1 implementation docs, tech interface request, and product-plan artifact
- Stage 2 has `Data Sources`, `Validation Evidence`, `MCP-COVERAGE.md`, `VERSION`, and `agents/openai.yaml`
- If the skill accepts user parameters, `skill.meta.json > input_schema` exists and follows the standard
- No `.DS_Store`, `__pycache__`, or `*.pyc`
- No unresolved placeholders in Stage 2 README or coverage docs
- No Stage 2 user-path mock / stub / random data
- `--run-checks` passes when executable checks are provided
- `scripts/audit_skill.py` reports score, missing items, and Stage 2 blockers
