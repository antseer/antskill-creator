# AntSkill Packaging Style Guide

## Goal

把 skill 包装成：
- 独立
- 诚实
- 可分享
- 可上传 GitHub
- 同事一看就知道这是 **Stage 1 需求型** 还是 **Stage 2 完整型**

## Two lifecycle stages

### 1. Stage 1 — Requirement Skill

适用于：产品需求、PRD、前端/输出体验、后端能力、数据源依赖已经完整，但真实 MCP / API / 数据库尚未全部接入，当前用 mock 数据展示效果。

必须说明：
- 当前产品方案
- 前端 / 输出体验
- 后端能力和接口需求
- 哪些数据仍是 mock / fixture / stub
- 每个 mock 未来由哪个 MCP / API / 数据库替换
- 验收标准和 Stage 2 阻塞项

### 2. Stage 2 — Complete Skill

适用于：Stage 1 的 mock 已经替换为真实数据源，MCP / API / 数据库覆盖全部用户主路径数据依赖，可以直接安装、运行、分享。

必须说明：
- 安装方式
- 依赖 / 环境变量
- 真实数据源和 MCP 覆盖矩阵
- 最后验证时间
- 失败处理 / 空态
- 最小运行或验证命令

> `split` 是拆包动作，不是第三阶段。

## Minimum file contract

### All packages
- `SKILL.md`
- `README.md`
- `README.zh.md`
- `.gitignore`

### Required for Stage 1 Requirement Skills
- `README.md` with `Data Reality`
- `README.zh.md` with `数据真实性`
- `REQUIREMENT-REVIEW.md`
- `TODO-TECH.md`
- `TECH-INTERFACE-REQUEST.md`
- PRD / spec / prototype / frontend-backend-data plan

### Required for Stage 2 Complete Skills
- `README.md` with `Data Sources` and `Validation Evidence`
- `README.zh.md` with `数据来源` and `验证证据`
- `MCP-COVERAGE.md`
- `agents/openai.yaml`
- `VERSION`
- `.env.example`（如适用）
- runnable logic / scripts / pipeline when execution is required
- tests or validation evidence
- `validation.checks.json` when validation can be executed locally

## README rules

### Always include
- what the package is for
- whether it is Stage 1 Requirement or Stage 2 Complete
- what is already strong
- what is still incomplete or verified
- reading order or quick start

### Never do
- claim unfinished integrations are complete
- hide critical missing dependencies
- write English README and leave Chinese README as a stub
- present a Stage 1 Requirement Skill as directly usable
- present a skill as Stage 2 before MCP / API / data coverage is verified

## Agent facade rules

`agents/openai.yaml` should include:
- display_name
- short_description
- icon paths when available
- brand_color
- default_prompt

## TECH-INTERFACE-REQUEST.md rules

This document is for engineering teammates. It must be concrete enough that they can start implementation without asking the PM to restate requirements.

Required sections:
- current product status
- current mock / fixture / stub inventory
- required MCP / API / database list
- request / response schema details
- refresh frequency, auth, rate-limit, error handling
- frontend integration contract
- acceptance criteria
- open questions

## MCP-COVERAGE.md rules

This document proves Stage 2 readiness.

Required sections:
- all required data dependencies
- MCP / API / database source for each dependency
- whether each dependency is required or optional
- verification method
- status
- last verified date
- known gaps; if any required gap exists, the package is not Stage 2

## Repo sync rules

If publishing into an aggregate repo:
1. copy the full packaged directory
2. update root README skill list
3. validate again in repo copy with explicit `--stage`
4. remove junk files
5. commit and push

## validation.checks.json rules

Use this file when Stage 2 readiness can be verified by local commands.

```json
{
  "checks": [
    {
      "name": "minimal run",
      "command": ["python", "scripts/run.py", "--sample"],
      "timeout_seconds": 60
    }
  ]
}
```

Rules:
- commands run from the skill root
- commands must be deterministic and safe
- credentials must come from documented environment variables
- a failing command blocks Stage 2 when `--run-checks` is used

## Audit report rules

Use `scripts/audit_skill.py` when you need a structured readiness view. It outputs:

- detected stage
- overall score
- verdict
- per-dimension scores
- missing items
- warnings
- Stage 2 blockers
- validation errors

Recommended commands:

```bash
python scripts/audit_skill.py <skill_dir> --stage auto --format markdown
python scripts/audit_skill.py <skill_dir> --stage complete --run-checks --format json
```
