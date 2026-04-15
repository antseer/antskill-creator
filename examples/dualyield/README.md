# DualYield

Dual-investment / DCI recommendation desk for finding high-yield, lower-touch-probability strike candidates across CEX venues.

> **Status: PM-spec / engineering handoff package**
>
> This package is intentionally **not production-complete**. It is a shareable package for engineering teammates to continue from an already-defined product spec, scoring engine, template decision layer, and high-fidelity frontend prototype.

## What it contains

- dual-yield product + technical PRD
- L1→L2→L3 pipeline skeleton
- strong L2 scoring engine with tests
- template-based L3 conclusion generation
- high-fidelity frontend prototype
- platform metadata
- engineering onboarding and TODO docs

## Current completion summary

### Strong already
- L2 compute layer is the strongest part and currently passes `32/32` tests
- PRD is detailed and implementation-oriented
- frontend prototype is already expressive enough for engineering handoff
- technical onboarding and TODO docs are present
- L3 template decision logic exists and can be used without an LLM

### Still incomplete
- Antseer and exchange connectors are mostly stubs
- frontend still uses mock data rather than real orchestrator output
- pipeline had a broken L3 orchestration hook and still needs full real-data wiring
- no production-ready cache / env / API integration yet
- package facade was missing before this packaging pass

## Read this first

1. `HANDOFF-REVIEW.md`
2. `TODO-TECH.md`
3. `docs/PRD.md`
4. `docs/TECH-ONBOARDING.md`

## Quick start

```bash
python3 -m unittest tests.test_l2 -v
```

Optional smoke test:

```bash
python3 - <<'PY'
import asyncio, sys
sys.path.insert(0, '.')
from pipeline.orchestrator import run_pipeline
print(asyncio.run(run_pipeline({"intent":"earn_yield","underlying":"BTC","principal":10000,"durations":[7,14],"risk":"balanced"})))
PY
```

## Sharing intent

This repo is meant to be shared with engineering teammates so they can:
- reuse the scoring model and probability logic
- understand the intended DualYield UX quickly
- see what is already done vs. what is still missing
- continue implementation without re-deriving the product logic from scratch
