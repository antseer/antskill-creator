# Yield Desk

Stablecoin yield decision desk for comparing CEX + DeFi earning products.

> **Status: PM-spec / engineering handoff package**
>
> This is intentionally **not a finished production integration**. It is a shareable package for engineering teammates to continue implementation from a strong PM-defined spec, prototype, and scoring pipeline.

## What it contains

- 4-layer pipeline architecture
- Product + technical PRD
- High-fidelity frontend prototype
- L2 scoring logic and tests
- Static platform/protocol safety metadata
- Engineering TODO list
- Handoff review summary

## Current completion summary

### Strong already
- Clear architecture (`L1 → L2 → L3 → L4`)
- L2 scoring logic is mostly implemented
- Frontend prototype communicates intended UX well
- YAML metadata is useful and concrete
- L2 tests currently pass (`16/16`)

### Still incomplete
- Antseer API contract unresolved
- Most non-Binance CEX connectors are still stubs
- L3 API key / deployment wiring unfinished
- Frontend still renders mock data
- No full E2E reliability layer yet

## Read this first

1. `HANDOFF-REVIEW.md`
2. `TODO-TECH.md`
3. `PRD-YieldDesk-v2-完整分层规范.md`

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python tests/test_l2_scorer.py
python pipeline/orchestrator.py
```

## Folder overview

```text
yield-desk/
├── SKILL.md
├── PRD-YieldDesk-v2-完整分层规范.md
├── TODO-TECH.md
├── HANDOFF-REVIEW.md
├── pipeline/
├── frontend/
├── tests/
└── data/
```

## Sharing intent

This repo is meant to be shared with engineering teammates so they can:
- reuse the scoring/data model
- understand what is already done
- see exactly what remains
- continue implementation without re-deriving the product logic
