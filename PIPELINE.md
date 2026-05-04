# Skill Creator Rick · Pipeline SOP

This file restores the original AntSkill Creator workflow and explains how it fits the newer two-stage lifecycle.

For the full pass / stop / split / publish decision table, see `STAGE-GATES.md`.

## Two axes, not one

| Axis | Purpose | Question answered |
|---|---|---|
| Lifecycle stage | Packaging truth | Is this a Stage 1 Semi-finished Skill or Stage 2 Finished Skill? |
| S0-S5 pipeline | Creation workflow | How do we go from raw idea to a handoff-ready skill package? |

The S0-S5 pipeline usually produces a **Stage 1 Semi-finished Skill** first. It becomes **Stage 2 Finished** only after mock / missing L1-B / L2 dependencies are replaced by verified real MCP / API / database sources.

Two source-of-truth systems run in parallel:

- **MCP capability map** is the hard authority for data truth.
- **`antseer-components`** is the hard authority for frontend truth: code style, UI style, design style, component contracts, source footer, and host embedding.

Stage 1 should conform to both as much as possible and disclose gaps. Stage 2 must conform to both; any unresolved frontend SoT gap blocks Finished status the same way an unresolved MCP gap blocks real-data status.

## S0-S5 build pipeline

| Step | Goal | SOP | Gate | Main outputs |
|---|---|---|---|---|
| S0 | Intent anchoring + requirement crystallization + rough demo | `sop/s0_requirement.md` | `quality/G0_requirement.md` | intent-card.md, requirement canvas, demo-v0 |
| S1 | Data inventory, list first and do not judge | `sop/s1_data_inventory.md` | `quality/G1_data_inventory.md` | data-inventory.md |
| S2 | MCP truth sync, routing audit, dual PRD | `sop/s2_routing_and_prd.md` | `quality/G2_routing_and_prd.md` | mcp-audit.md, data-prd.md, skill-prd.md |
| S3 | Hi-fi HTML using Antseer design rules and `antseer-components` frontend SoT | `sop/s3_html_design.md` | `quality/G3_html_design.md` | demo-v1.html, visual registry update, component cache commit |
| S4 | HTML ↔ PRD alignment review | `sop/s4_review.md` | `quality/G4_review.md` | review-report.md |
| S5 | Skill package delivery | `sop/s5_skill_delivery.md` | `quality/G5_skill_delivery.md` | SKILL.md, README, skill.meta.json, PRDs, handoff docs |

Do not skip steps. In particular:

- S0 intent card before requirement canvas: confirm the user's intent before expanding it into factory-facing requirements.
- S1 before S2: inventory before ownership/routing judgment.
- S4 before S5: review alignment before packaging.
- If S4 changes upstream assumptions, rerun the affected S2 / S3 gates.

## Layer ownership model

Every visible data point must be assigned to one layer:

| Layer | Owner | Meaning |
|---|---|---|
| L1-A | Existing MCP | MCP already provides the raw data directly |
| L1-B | Backend | New raw MCP tool is needed |
| L2 | Backend | New aggregate MCP/API is needed |
| L3 | Skill | Skill-local deterministic computation |
| L4 | Skill | LLM structured interpretation with fallback |
| L5 | Skill | Frontend presentation |

Use `mcp-capability-map/routing-decision-tree.md` for the full routing decision tree.

## Methodology references

- `methodology/core-principles.md` — first-principles rules
- `methodology/intent-anchoring.md` — S0 intent card before the 7-question requirement canvas
- `methodology/paradigms.md` — implementation / specification / dual-mode paradigms
- `methodology/responsibility-split.md` — PM / backend / skill ownership boundary
- `methodology/semi-finished-boundary.md` — why Stage 1 is a handoff-ready semi-finished product, not a broken product
- `methodology/source-of-truth.md` — conflict-resolution order across PRD, data contract, UI, and package files

## Quality gates

Each S-step must end by running or manually applying its matching `quality/G*.md` gate.

If a red item fails:

1. fix the root cause, not the symptom;
2. rerun the gate;
3. stop after 3 failed repair loops and report the blocker.

## Relation to Stage 1 / Stage 2 validators

After S5, run the lifecycle validators:

```bash
PYTHONDONTWRITEBYTECODE=1 python /Users/rick/.claude/skills/skill-creator-rick/scripts/quick_validate.py <skill_dir>
PYTHONDONTWRITEBYTECODE=1 python /Users/rick/.claude/skills/skill-creator-rick/scripts/validate_shareable_skill.py <skill_dir> --stage requirement
PYTHONDONTWRITEBYTECODE=1 python /Users/rick/.claude/skills/skill-creator-rick/scripts/audit_skill.py <skill_dir> --stage requirement --format markdown
```

When all mock / L1-B / L2 gaps are replaced by verified real data sources, run Stage 2 validation:

```bash
PYTHONDONTWRITEBYTECODE=1 python /Users/rick/.claude/skills/skill-creator-rick/scripts/validate_shareable_skill.py <skill_dir> --stage complete --run-checks
PYTHONDONTWRITEBYTECODE=1 python /Users/rick/.claude/skills/skill-creator-rick/scripts/audit_skill.py <skill_dir> --stage complete --run-checks --format markdown
```
