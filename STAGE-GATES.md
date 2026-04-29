# Skill Creator Rick · Stage Gates

This document is the explicit gate system for AntSkill Creator. It combines two different meanings of “stage”:

1. **Lifecycle gates** — whether a package is Stage 1 Semi-finished or Stage 2 Finished.
2. **Pipeline gates** — whether the creator workflow may advance from S0 to S5.

`quality/G0-G5` are the detailed checklists. This file is the decision layer: **pass, stop, split, or publish**.

---

## Gate 0 — Intake / Not-packageable gate

Run before any packaging or creator workflow.

| Question | Pass condition | Fail action |
|---|---|---|
| Goal clarity | One clear user problem and one primary output | Stop and clarify |
| Input clarity | Required user input is known or discoverable | Stop and ask for missing input |
| Output clarity | Final artifact shape is clear: skill package, PRD, prototype, audit, etc. | Stop and define output |
| Ownership | It is clear what the skill owns vs backend / MCP / user | Stop and define responsibility split |

**Fail verdict:** `not packageable yet`.

Do not scaffold, package, upload, or call something Stage 1 until this gate passes.

---

## Gate 1 — Split gate

Run when the package seems broad or mixed.

Split is required if two or more are true:

- Two or more distinct user types
- Two or more unrelated trigger scenarios
- Outputs are fundamentally different
- Data dependencies are unrelated
- README contains multiple independent core promises
- The package mixes Stage 1 semi-finished docs and Stage 2 finished runnable logic without a clean boundary
- One half can be installed or used without the other

**Pass verdict:** continue as one skill.  
**Fail verdict:** produce a `Split Plan` first.

Required split output:

```markdown
## Split Plan

| 子 skill | 目标用户 | 输入 | 输出 | 数据依赖 | 阶段 |
|---|---|---|---|---|---|
```

---

## Gate 2 — Stage 1 Semi-finished Skill gate

A package can be called **Stage 1 Semi-finished Skill** only if all critical items pass.

There are two accepted Stage 1 shapes:

| Shape | Use case | Required extra structure |
|---|---|---|
| Stage 1 Lite Semi-finished Package | Product plan + prototype/data reality handoff | `README`, `REQUIREMENT-REVIEW`, `TODO-TECH`, `TECH-INTERFACE-REQUEST`, product spec/prototype |
| Stage 1 Antseer S5 Semi-finished Package | Full Antseer visualization skill handoff | Everything in Lite plus `data-inventory.md`, `mcp-audit.md`, `data-prd.md`, `skill-prd.md`, `review-report.md`, `frontend/index.html`, `layers/L1-L5` |

If any S5-specific artifact exists, the package is judged by the stricter S5 structure.

### Critical pass conditions

- `SKILL.md` exists and states Stage 1 / Semi-finished status when appropriate
- `README.md` has `Data Reality`
- `README.zh.md` has `数据真实性`
- `REQUIREMENT-REVIEW.md` exists
- `TODO-TECH.md` exists
- `TECH-INTERFACE-REQUEST.md` exists
- Product plan exists: PRD / spec / user flow / prototype / frontend plan / backend plan, at least one concrete artifact
- Frontend or output experience is specified enough for engineering to build
- Backend capability requirements are specified when backend is needed
- Every mock / static / proxy / stub data item is listed with future real MCP / API / database replacement path
- The package does **not** claim direct-use / production / complete readiness
- If the skill has user parameters, `skill.meta.json > input_schema` follows `references/input-schema-standard.md`
- No unresolved scaffold placeholders remain in user-facing package files (`TODO`, `Replace this`, `{{FILL_BEFORE_VALIDATE}}`, etc.)

### Validation command

```bash
PYTHONDONTWRITEBYTECODE=1 python /Users/rick/.claude/skills/skill-creator-rick/scripts/quick_validate.py <skill_dir>
PYTHONDONTWRITEBYTECODE=1 python /Users/rick/.claude/skills/skill-creator-rick/scripts/validate_shareable_skill.py <skill_dir> --stage requirement
PYTHONDONTWRITEBYTECODE=1 python /Users/rick/.claude/skills/skill-creator-rick/scripts/audit_skill.py <skill_dir> --stage requirement --format markdown
```

**Pass verdict:** `Stage 1 Semi-finished Skill / share-ready as semi-finished`.  
**Fail action:** repair missing artifacts or downgrade to `not packageable yet`.

---

## Gate 3 — S0-S5 creator pipeline gates

These gates apply when creating a new Antseer visualization skill from an idea.

| Pipeline step | Gate file | Advance condition | Stop condition |
|---|---|---|---|
| S0 Intent + requirement + rough demo | `quality/G0_requirement.md` | All 🔴 pass, including G0.0 intent card confirmation | Intent unclear, no intent-card confirmation, no rough demo |
| S1 Data inventory | `quality/G1_data_inventory.md` | All 🔴 pass | Missing visible fields, source judged too early, dependency chain incomplete |
| S2 MCP routing + dual PRD | `quality/G2_routing_and_prd.md` | All 🔴 pass | MCP truth not synced, rows unassigned, L1-B/L2 not in data PRD |
| S3 Hi-fi HTML | `quality/G3_html_design.md` | All 🔴 pass | Visual registry missing, PRD fields not traceable, poor states/responsive behavior |
| S4 Review | `quality/G4_review.md` | All 🔴 pass | HTML and PRD disagree, unresolved deltas, upstream changes not re-gated |
| S5 Delivery | `quality/G5_skill_delivery.md` | All 🔴 pass | Missing SKILL/PRD/meta/review/layers/frontend, untraceable gaps |

### Pipeline progression rules

1. S1 must happen before S2: list first, judge later.
2. S4 must happen before S5: align before packaging.
3. If S4 changes `data-prd.md` / `skill-prd.md`, rerun G2.
4. If S4 changes HTML, rerun G3.
5. A failed 🔴 gate gets at most 3 repair loops. After 3 failures, report blocker instead of pretending pass.
6. Passing S5 normally produces a Stage 1 Semi-finished Skill unless all real data/MCP dependencies are already verified.
7. Raw scaffolds are allowed to fail validation until all placeholders are filled; this is intentional.

---

## Gate 4 — Stage 2 Finished Skill gate

A package can be called **Stage 2 Finished Skill** only if all critical items pass.

### Critical pass conditions

- User main path does not depend on mock / static / random / hardcoded demo data
- All required data dependencies have real source coverage through MCP / API / database, or are explicitly declared as local/user-input only
- `README.md` has `Data Sources` and `Validation Evidence`
- `README.zh.md` has `数据来源` and `验证证据`
- `MCP-COVERAGE.md` exists and maps every data dependency to source, method, last verification time, and failure handling
- `agents/openai.yaml` exists
- `VERSION` exists
- `.env.example` exists when environment variables or auth are needed
- Runnable logic / scripts / pipeline exist when execution is required
- Test evidence or minimum run evidence exists
- `validation.checks.json` exists when executable checks are needed
- If `validation.checks.json` exists, `--run-checks` passes

### Validation command

```bash
PYTHONDONTWRITEBYTECODE=1 python /Users/rick/.claude/skills/skill-creator-rick/scripts/quick_validate.py <skill_dir>
PYTHONDONTWRITEBYTECODE=1 python /Users/rick/.claude/skills/skill-creator-rick/scripts/validate_shareable_skill.py <skill_dir> --stage complete --run-checks
PYTHONDONTWRITEBYTECODE=1 python /Users/rick/.claude/skills/skill-creator-rick/scripts/audit_skill.py <skill_dir> --stage complete --run-checks --format markdown
```

**Pass verdict:** `Stage 2 Finished Skill / direct-use share-ready`.  
**Fail action:** stay Stage 1 and list Stage 2 blockers.

---

## Gate 5 — Publish gate

Run before GitHub upload, zip handoff, or public/internal sharing.

| Item | Stage 1 semi-finished | Stage 2 finished |
|---|---|---|
| Stage label | Must clearly say Stage 1 Semi-finished | Must clearly say Stage 2 Finished |
| Data truth | `Data Reality` table complete | `Data Sources` + `Validation Evidence` complete |
| Mock warning | Must be prominent | No user-path mock allowed |
| Validator | `--stage requirement` passes | `--stage complete --run-checks` passes |
| Audit | No errors; blockers disclosed | No errors; no Stage 2 blockers |
| README parity | English and Chinese are structurally aligned | English and Chinese are structurally aligned |
| Upload note | Must say not for real analysis / production | Must include validation evidence summary |

**Publish rule:** never upload a Stage 1 package as if it were Stage 2.

---

## Gate 6 — Creator self-integrity gate

This gate protects `skill-creator-rick` itself from being over-pruned again.

The creator package must keep:

- `PIPELINE.md`
- `STAGE-GATES.md`
- `methodology/`
- `sop/`
- `quality/`
- `mcp-capability-map/`
- `references/`
- `scripts/`
- `templates/`
- `validation.checks.json`

Creator self-validation must also prove that raw scaffolds fail until filled, so empty templates cannot pass as share-ready Stage 1 packages.

If a lighter package is required, it may remove examples/assets, but it must not remove stage gates, methodology, SOP, quality gates, validators, or templates.
