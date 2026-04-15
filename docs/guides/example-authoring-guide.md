# Example Authoring Guide

> Updated: 2026-04-15

## Goal

Help authors create new example packages that are immediately readable, reusable, and consistent with the vNext package standard.

This guide is for creating **new examples**, not migrating old ones.

## Authoring principle

An example package is not just “sample files.”

It must answer three questions fast:

1. what product is this example about?
2. what is requirement truth vs implementation truth?
3. what is the publishable package surface?

If those answers are not obvious in under 10 seconds, the example is not done.

## Choose the example type first

### A — implementation-first example

Use when the example’s value is mostly in runnable code, tests, and execution patterns.

Good fit:

- scoring engine references
- connector skeletons
- compute-layer examples

### B — spec-first example

Use when the example’s value is mostly in PRD, requirement docs, and structure.

Good fit:

- scanner / analyzer package references
- packaging examples
- requirement-heavy examples without real runtime code

### C — dual-mode example

Use when the example should teach both product logic and implementation shape.

Good fit:

- flagship end-to-end examples
- PM-to-engineering handoff examples
- reference packages used as default starting points

## Required package shape

Every example must use:

```text
example-name/
├── docs/
├── implementation/
└── delivery/
```

### Minimum contents by area

#### docs/

Must include:

- `docs/product/PRD.md`

Should include, unless intentionally minimal:

- `docs/requirements/business-spec.md`
- `docs/requirements/api-spec.md`
- `docs/requirements/backend-computation.md`
- `docs/requirements/implementation-guide.md`
- `docs/review/SKILL-REVIEW.md`

#### implementation/

Contains only runtime-facing artifacts:

- `pipeline/`
- `frontend/`
- `tests/`
- `scripts/`
- `data/`
- or `reference/` for light implementation examples

#### delivery/

Must include:

- `delivery/SKILL.md`
- `delivery/README.md`
- `delivery/VERSION`

Should include when publishable:

- `delivery/README.zh.md`
- `delivery/agents/openai.yaml`
- `delivery/assets/`
- `delivery/templates/`

## Naming rules

### PRD naming

Always use:

`docs/product/PRD.md`

Do not create:

- `full-prd-v2-final.md`
- `product-spec-complete.md`
- `yield-desk-final-final.md`

The whole point is to make the PRD location guess-free.

### Handoff and review naming

Use:

- `docs/handoff/TODO-TECH.md`
- `docs/handoff/TECH-ONBOARDING.md`
- `docs/review/HANDOFF-REVIEW.md`
- `docs/review/SKILL-REVIEW.md`

### Delivery naming

Use:

- `delivery/README.zh.md`

not:

- `README_zh.md`
- `README-cn.md`

## What good examples should demonstrate

### A good example should teach one primary thing

Bad:

- tries to demonstrate packaging, prompting, UI polish, test philosophy, and 12 connector patterns at once

Good:

- “this is the best dual-mode handoff example”
- “this is the best spec-first packaging example”
- “this is the smallest useful implementation reference”

### A good example should be honest about completeness

Use clear status language:

- “reference-only”
- “prototype-only frontend”
- “implementation incomplete”
- “handoff-ready but not production-complete”

Do not imply production readiness if the package is still mock-first or connector-incomplete.

### A good example should include a reading order

Every example README should answer:

1. what to read first
2. what the example is best for
3. what is intentionally incomplete

## Recommended author workflow

### Step 1 — choose paradigm

Decide whether the example is A, B, or C.

### Step 2 — write the PRD summary

Create `docs/product/PRD.md` before polishing implementation details.

### Step 3 — decide the teaching objective

Write one sentence:

> “This example is the canonical reference for ______.”

If you cannot write that sentence, the example is probably too vague.

### Step 4 — build only the minimum implementation needed

Do not overbuild the example just to look complete.

If the example is spec-first, a placeholder implementation surface is acceptable.

### Step 5 — write the delivery facade last

Only after docs and implementation are organized should you finalize:

- `delivery/SKILL.md`
- `delivery/README.md`
- `delivery/README.zh.md`

## Author checklist

- [ ] paradigm A / B / C is explicit
- [ ] `docs/product/PRD.md` exists
- [ ] requirement docs are under `docs/requirements/`
- [ ] review docs are under `docs/review/`
- [ ] implementation files are under `implementation/`
- [ ] publish artifacts are under `delivery/`
- [ ] README states what the example is best for
- [ ] README states what is incomplete
- [ ] paths in README / SKILL / handoff docs are real
- [ ] package looks understandable in one glance

## Anti-patterns

### Anti-pattern 1 — “perfect sample syndrome”

Do not try to make every example the biggest and most complete one.

Examples should be **purposeful**, not uniformly bloated.

### Anti-pattern 2 — hiding truth in README prose

If a business rule only exists in README text and not in `docs/`, the package is weak.

README explains; docs define.

### Anti-pattern 3 — fake dual-mode packages

Do not label an example C if one side is obviously hollow.

If docs are strong but implementation is mostly placeholder, label it B.

If runtime code is strong but docs are thin, label it A.

### Anti-pattern 4 — visual polish without package clarity

A pretty demo cannot compensate for a confusing package structure.

## Done criteria

An example is ready when:

- a new contributor can pick the right example quickly
- they know what the example is teaching
- they know which files are authoritative
- they can tell what is still incomplete
