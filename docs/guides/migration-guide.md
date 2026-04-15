# Skill Package Migration Guide

> Updated: 2026-04-15

## Goal

Migrate an existing skill package from the legacy mixed layout into the vNext:

- `docs/` = requirement truth
- `implementation/` = runtime truth
- `delivery/` = publish truth

This guide is for packages that currently mix PRD, code, assets, and publish metadata at the same level.

## When to use this guide

Use this guide when a package has any of these smells:

- `README.md`, `SKILL.md`, `openai.yaml`, `pipeline/`, `frontend/`, `tests/`, and `PRD.md` all live at repo root
- requirement docs and implementation files are hard to distinguish at a glance
- the package paradigm (A / B / C) is not obvious from structure
- reviewers need to read multiple files just to understand what kind of package this is

## Target structure

```text
skill-name/
├── docs/
│   ├── product/PRD.md
│   ├── requirements/
│   ├── review/
│   └── handoff/             # optional
├── implementation/
│   ├── pipeline/
│   ├── frontend/
│   ├── tests/
│   ├── scripts/
│   └── data/
└── delivery/
    ├── SKILL.md
    ├── README.md
    ├── README.zh.md
    ├── VERSION
    ├── agents/openai.yaml
    ├── assets/
    └── templates/
```

## Migration decision rule

Before moving files, first classify the package:

- **A — implementation-first**: implementation is primary; docs may stay lighter
- **B — spec-first**: docs are primary; implementation can be demo/reference only
- **C — dual-mode**: both docs and implementation must be complete

If unclear, default to **B**.

## File move map

### Move requirement-facing files into `docs/`

| Old location | New location |
|---|---|
| `PRD.md` / `product-prd.md` | `docs/product/PRD.md` |
| `business-spec.md` | `docs/requirements/business-spec.md` |
| `api-spec.md` | `docs/requirements/api-spec.md` |
| `backend-computation.md` | `docs/requirements/backend-computation.md` |
| `implementation-guide.md` | `docs/requirements/implementation-guide.md` |
| `ai-prompts.md` | `docs/requirements/ai-prompts.md` |
| `viz-specs.md` | `docs/requirements/viz-specs.md` |
| `prototype-notes.md` | `docs/requirements/prototype-notes.md` |
| `TestSuite.md` | `docs/requirements/TestSuite.md` |
| `HANDOFF-REVIEW.md` / `SKILL-REVIEW.md` | `docs/review/...` |
| `TODO-TECH.md` / `TECH-ONBOARDING.md` | `docs/handoff/...` |

### Move implementation-facing files into `implementation/`

| Old location | New location |
|---|---|
| `pipeline/` | `implementation/pipeline/` |
| `frontend/` | `implementation/frontend/` |
| `tests/` | `implementation/tests/` |
| `scripts/` | `implementation/scripts/` |
| `data/` | `implementation/data/` |

### Move publish-facing files into `delivery/`

| Old location | New location |
|---|---|
| `SKILL.md` | `delivery/SKILL.md` |
| `README.md` | `delivery/README.md` |
| `README.zh.md` / `README_zh.md` | `delivery/README.zh.md` |
| `openai.yaml` / `agents/openai.yaml` | `delivery/agents/openai.yaml` |
| `VERSION` | `delivery/VERSION` |
| `assets/` | `delivery/assets/` |
| `templates/ai-input.json` | `delivery/templates/ai-input.json` |
| `templates/ai-output.json` | `delivery/templates/ai-output.json` |

## Migration steps

### Step 1 — Freeze the package type

Write down whether the package is A, B, or C before editing files.

If you migrate structure before deciding paradigm, the package will look tidy but still be logically ambiguous.

### Step 2 — Move the PRD first

Always create or move:

`docs/product/PRD.md`

This is the first anchor reviewers look for. Without it, the package still feels fragmented even after folders are cleaned up.

### Step 3 — Separate docs from implementation

Move all requirement and review artifacts into `docs/`.

Do **not** leave business logic decisions buried inside:

- `frontend/`
- `pipeline/`
- `README.md`
- `SKILL.md`

### Step 4 — Re-root all entrypoints

After moving files, update references in:

- `delivery/README.md`
- `delivery/README.zh.md`
- `delivery/SKILL.md`
- handoff docs
- review docs
- test instructions

The most common migration failure is a good folder structure with broken path references.

### Step 5 — Fix Python import and test paths

If tests or scripts previously assumed root-level modules, update import roots.

Typical fixes:

- `from pipeline...` → `from implementation.pipeline...`
- `python tests/test_x.py` → `python -m pytest implementation/tests/test_x.py`
- `python pipeline/orchestrator.py` → `python -m implementation.pipeline.orchestrator`

### Step 6 — Add minimum docs if missing

For old packages, do not block migration on perfect completeness. Add thin placeholder docs if needed:

- `docs/requirements/business-spec.md`
- `docs/requirements/api-spec.md`
- `docs/requirements/backend-computation.md`
- `docs/review/SKILL-REVIEW.md`

Migration should produce a readable package first; refinement can come after.

### Step 7 — Validate the package

Minimum checks:

- can a reviewer find `docs/product/PRD.md` in under 10 seconds?
- is it obvious what belongs to `docs/`, `implementation/`, and `delivery/`?
- do README and SKILL paths point to real files?
- do tests still import correctly?
- is publish metadata still present under `delivery/`?

## Common migration mistakes

### Mistake 1 — Moving files without changing references

Symptom: folder tree looks correct, but README and handoff docs still point to old paths.

Fix: run a full path-reference grep after migration.

### Mistake 2 — Using `delivery/` as product truth

`delivery/` is a facade, not the place where product logic is authored.

If `delivery/SKILL.md` contains rules that do not exist in `docs/`, the package is still structurally wrong.

### Mistake 3 — Keeping mixed root-level leftovers

If old root-level `SKILL.md`, `README.md`, `PRD.md`, or `HANDOFF-REVIEW.md` remain, reviewers lose confidence in which version is current.

Archive or delete them after migration.

### Mistake 4 — Over-migrating legacy reference packages

For light references, do not fake completeness.

It is acceptable for a small A/B reference to have:

- minimal `docs/product/PRD.md`
- small `implementation/reference/`
- thin `delivery/`

What matters is clarity, not pretending every reference is a production-ready full package.

## Done criteria

A migration is complete when:

1. the package type is obvious
2. the PRD is easy to find
3. requirement docs and implementation files are physically separated
4. delivery files are gathered in one publish surface
5. all high-traffic references point to the new paths
