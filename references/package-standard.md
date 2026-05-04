# Skill Creator Rick Two-Stage Package Standard

## Goal

Produce skill packages that are honest about their lifecycle stage:

1. **Stage 1 — Semi-finished Skill**: complete product / frontend / backend / data-source plan, current experience shown with mock data, ready for engineering implementation.
2. **Stage 2 — Finished Skill**: all user-path mock data replaced by real MCP / API / database sources, verified, ready for direct use and sharing.

`split` is a packaging action, not a lifecycle stage.

## Stage 1 — Semi-finished Skill

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

Two valid shapes:
- **Stage 1 Lite Semi-finished Package**: the minimum contract above.
- **Stage 1 Antseer S5 Semi-finished Package**: the minimum contract above plus `data-inventory.md`, `mcp-audit.md`, `data-prd.md`, `skill-prd.md`, `review-report.md`, `frontend/index.html`, and `layers/L1-data`, `layers/L2-aggregation`, `layers/L3-compute`, `layers/L4-llm`, `layers/L5-presentation`.

If any S5-specific artifact exists, the stricter S5 structure is required.

Must state:
- which data is mock / fixture / stub
- where each mock appears in the user experience
- which MCP / API / database should replace it
- what blocks Stage 2
- that mock data is for demonstration only
- if a frontend exists, which `antseer-components` cache commit was used and which code/UI/design deviations remain

Must not claim:
- direct-use ready
- directly usable for real analysis
- fully integrated with real data
- share-ready while unresolved placeholders remain (`TODO`, `Replace this`, `{{FILL_BEFORE_VALIDATE}}`, etc.)

Frontend compliance:
- `antseer-components` is the frontend source of truth.
- Stage 1 must be best-effort compliant with `references/antseer-components-standard.md`.
- Code style should already separate data adapter / domain calculator / view model / renderer where practical.
- UI/design should use Antseer tokens, canonical palette, source footer, state model, and host-embedded layout rules where practical.
- Any deviation is allowed only as an explicit Stage 2 blocker in handoff docs.

## Stage 2 — Finished Skill

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

Frontend compliance:
- `antseer-components` hard gate must pass for every user-path frontend.
- No vendored `antseer-components` checkout / cache / `node_modules`.
- No user-path mock / fixture / random / synthetic data, including inline `#antseer-data`.
- `#antseer-data` and `#antseer-data-schema` are required for official HTML templates consumed by SkillHub / website JSON.
- Root containers must not own host width, centering, or outer padding.
- Code style, UI style, design style, responsive states, source footer, and data-source evidence must follow `references/antseer-components-standard.md`.

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
- Stage is explicitly stated as Stage 1 Semi-finished or Stage 2 Finished
- Stage 1 has `Data Reality`, Stage 1 implementation docs, tech interface request, and product-plan artifact
- Stage 2 has `Data Sources`, `Validation Evidence`, `MCP-COVERAGE.md`, `VERSION`, and `agents/openai.yaml`
- If the skill accepts user parameters, `skill.meta.json > input_schema` exists and follows the standard
- No `.DS_Store`, `__pycache__`, or `*.pyc`
- No unresolved placeholders in Stage 2 README or coverage docs
- No unresolved placeholders in Stage 1 user-facing handoff docs
- No Stage 2 user-path mock / stub / random data
- If frontend exists: Stage 1 records `antseer-components` commit and deviations; Stage 2 passes frontend SoT hard gate
- `--run-checks` passes when executable checks are provided
- `scripts/audit_skill.py` reports score, missing items, and Stage 2 blockers
