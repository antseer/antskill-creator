# AntSkill Creator — Product Logic PRD

> Version: 3.1.0  
> Updated: 2026-04-15

## 1. Problem

Most “skill generators” fail in one of two ways:

1. they output code without a stable product contract;
2. they output documents without a clear mapping to implementation and delivery.

AntSkill Creator exists to turn vague skill ideas into **reviewable, handoff-ready, publishable skill packages**.

## 2. Product goal

For any new skill, produce a package where three views are simultaneously clear:

- **Product view**: what problem the skill solves, for whom, and what decision it helps make
- **Implementation view**: what must be built in data / compute / decision / render layers
- **Delivery view**: what gets published as a reusable skill package

## 3. Primary users

- PM / founder who has the product idea
- AI agent that drafts the package
- engineer who implements the production version
- reviewer who checks consistency before handoff or publishing

## 4. Core workflow

### S1 Requirements
- define user, job-to-be-done, decision output, data sources, paradigm

### S2 Prototype
- make the decision experience visible fast

### S3 Refinement
- absorb feedback until the prototype is product-correct

### S4 PRD + requirements
- write one complete PRD first
- then decompose into business / api / computation / prompt / viz / test specs

### S5 Delivery
- package metadata, README, assets, SKILL entrypoint

### S6 Review
- verify no gap between PRD, requirement docs, implementation, and delivery

## 5. Package design principles

1. **PRD first**: no serious skill without a complete product logic document
2. **Physical separation**: `docs/`, `implementation/`, `delivery/` must not mix responsibilities
3. **Requirements before polish**: product logic beats pretty demos
4. **One-glance readability**: a reviewer should identify package type in under 10 seconds
5. **Spec ↔ implementation traceability**: every visible output must map back to a requirement

## 6. Paradigm rules

- **A Implementation-first**: runtime matters most; keep PRD lean but present
- **B Spec-first**: docs are primary; implementation may only include demo/reference artifacts
- **C Dual-mode**: both must be complete

## 7. Acceptance criteria

- a reviewer can find complete product logic in one PRD
- a reviewer can distinguish requirement docs from implementation files at a glance
- the package makes paradigm A/B/C obvious from structure and contents
- delivery artifacts can be published without reverse-engineering the package
