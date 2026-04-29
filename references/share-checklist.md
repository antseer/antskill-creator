# Share Checklist

Before calling a package share-ready, confirm the right stage.

## Stage decision

- [ ] The package solves one clear problem; otherwise create a split plan first
- [ ] Stage 1 if user-path data is still mock / fixture / stub
- [ ] Stage 2 only if all user-path mock data is replaced by verified real MCP / API / database sources
- [ ] If some data is real and some is mock, the package remains Stage 1

## Stage 1 — Semi-finished Skill

- [ ] `SKILL.md` exists and validates
- [ ] `README.md` has `Data Reality`
- [ ] `README.zh.md` has `数据真实性`
- [ ] `REQUIREMENT-REVIEW.md` exists
- [ ] `TODO-TECH.md` exists
- [ ] `TECH-INTERFACE-REQUEST.md` exists
- [ ] PRD / spec / prototype / frontend-backend-data plan exists
- [ ] Every mock data item maps to a required real MCP / API / database source
- [ ] README clearly says mock data is only for demonstration
- [ ] No false direct-use claim
- [ ] If user parameters exist, `skill.meta.json > input_schema` follows the standard

## Stage 2 — Finished Skill

- [ ] `SKILL.md` exists and validates
- [ ] `README.md` has `Data Sources` and `Validation Evidence`
- [ ] `README.zh.md` has `数据来源` and `验证证据`
- [ ] `MCP-COVERAGE.md` exists and lists all data dependencies
- [ ] Every required data dependency is covered by MCP, API, database, or an explicit no-external-data explanation
- [ ] User-path code no longer depends on mock / stub / random / hardcoded demo data
- [ ] `agents/openai.yaml` exists
- [ ] `VERSION` exists
- [ ] `.env.example` exists if env vars / auth are needed
- [ ] tests, evals, or minimal run evidence exists
- [ ] `validation.checks.json` exists and passes with `--run-checks` if readiness can be checked locally
- [ ] `scripts/audit_skill.py` shows no Stage 2 blockers before sharing as Finished
- [ ] If user parameters exist, `skill.meta.json > input_schema` follows the standard

## Hygiene

- [ ] no `.DS_Store`, `__pycache__`, or `*.pyc`
- [ ] no unresolved placeholders in Stage 2 README / coverage docs
- [ ] GitHub repo root README updated if publishing into a monorepo
