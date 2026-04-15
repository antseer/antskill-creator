# Skill Package Standard

> Updated: 2026-04-15

## Objective

Make every skill package readable in three layers:

- `docs/` = requirement truth
- `implementation/` = runtime truth
- `delivery/` = publish truth

## Required top-level structure

```text
skill-name/
├── docs/
│   ├── product/PRD.md
│   ├── requirements/
│   └── review/
├── implementation/
└── delivery/
```

## Directory responsibilities

### docs/
Contains product logic, business rules, field definitions, formulas, prompt contracts, test intent, and review docs.

**Must not contain** runnable production code as source of truth.

### implementation/
Contains pipeline code, demo frontend, tests, scripts, schemas, and adapters.

**Must not contain** business arbitration that is missing from `docs/`.

### delivery/
Contains package entrypoints and publish artifacts:

- `SKILL.md`
- `README.md`
- `README.zh.md`
- `VERSION`
- `agents/openai.yaml`
- `assets/`

## Paradigm visibility rule

The package type must be obvious by contents:

- **A**: `implementation/` complete, `docs/` minimal but present
- **B**: `docs/` complete, `implementation/` only demo/reference artifacts
- **C**: both complete

## Mandatory requirement documents

- `docs/product/PRD.md`
- `docs/requirements/business-spec.md`
- `docs/requirements/api-spec.md`
- `docs/requirements/backend-computation.md`
- `docs/requirements/implementation-guide.md`
- `docs/requirements/ai-prompts.md`
- `docs/requirements/viz-specs.md`
- `docs/requirements/prototype-notes.md`
- `docs/requirements/TestSuite.md`

## Review rule

If a reviewer cannot answer these in under 10 seconds, the package fails the standard:

1. What product does this skill implement?
2. Where is the single PRD?
3. Which files are requirement docs?
4. Which files are runnable implementation?
5. What is the publishable delivery surface?

## Companion guides

- `docs/guides/migration-guide.md` — move old packages into the vNext layout
- `docs/guides/example-authoring-guide.md` — author new examples in the vNext layout
