<div align="center">

# AntSkill Creator

把 skill 按两阶段生命周期推进：先做需求型，接入真实 MCP / 数据源后再变成完整型。

[English](README.md) | 简体中文

</div>

## 两个阶段

### Stage 1 — 需求型 Skill

适用于产品方案已经完整，但真实数据集成尚未完成的情况。

必须交付：
- 完整产品方案 / PRD / 用户流程
- 前端或输出体验
- 后端能力需求
- 数据源依赖清单
- mock 数据边界和替换计划
- 工程实现文档

可以使用 mock 数据，但每个 mock 数据项都必须说明未来由哪个真实 MCP / API / 数据库替换。

### Stage 2 — 完整型 Skill

适用于 Stage 1 的 mock 数据已经被替换之后。

必须交付：
- 用户主路径不再依赖 mock / stub / random 演示数据
- 全部必需数据依赖由 MCP / API / 数据库覆盖，或者明确说明不需要外部数据
- `MCP-COVERAGE.md` 证明覆盖情况
- README 包含数据来源和验证证据
- package 可以安装、运行、分享或发布

> `split` 是拆包动作，不是第三阶段。

## 这个 skill 做什么

- 判断本地 skill 是 Stage 1 需求型还是 Stage 2 完整型
- 识别混合包是否需要先 split
- 基于可维护模板生成阶段专属文件
- 补双语 README、元数据、图标和 agent 门面
- 生成给工程同学看的 MCP / API / 数据源提需文档
- 按阶段校验 package 是否达标
- 生成带分数、缺失项和 Stage 2 blockers 的结构化审计报告
- 用户要求时发布到 GitHub

## 数据来源

这个元 skill 不需要外部行情数据。它处理的是用户本地提供的 skill 文件。

| 数据项 | 真实来源 | 方法 | 最后验证时间 | 失败处理 |
|---|---|---|---|---|
| Skill 包文件 | 用户本地文件系统 | 直接读写文件 | 2026-04-27 | 报告缺失文件和修复项 |
| 打包标准 | 本 skill 内置引用文档 | `references/*.md` | 2026-04-27 | 回退到 `SKILL.md` 契约 |
| 校验规则 | 本地 Python 脚本 | `scripts/quick_validate.py`, `scripts/validate_shareable_skill.py`, `scripts/audit_skill.py` | 2026-04-27 | 输出校验错误和审计报告 |
| 脚手架模板 | 本地模板文件 | `templates/requirement`, `templates/complete`, `templates/common` | 2026-04-27 | 模板缺失时快速失败 |
| 可执行检查 | 本地检查配置 | `validation.checks.json` | 2026-04-27 | 使 Stage 2 `--run-checks` 闸门失败 |

## 验证证据

| 检查项 | 命令 / 方法 | 结果 | 日期 |
|---|---|---|---|
| Frontmatter 校验 | `python scripts/quick_validate.py .` | pass | 2026-04-27 |
| 阶段校验脚本语法 | `python -m py_compile scripts/*.py` | pass | 2026-04-27 |
| Stage 1 脚手架冒烟测试 | 生成临时需求型包，并用 `--stage requirement` 校验 | pass | 2026-04-27 |
| Stage 2 脚手架冒烟测试 | 生成临时完整型包，并用 `--stage complete` 校验 | 填充示例值后 pass | 2026-04-27 |
| 可执行校验闸门 | `python scripts/validate_shareable_skill.py . --stage complete --run-checks` | pass | 2026-04-27 |
| 结构化审计报告 | `python scripts/audit_skill.py . --stage complete --run-checks --format json` | pass | 2026-04-27 |

## 示例请求

```text
/antskill-creator review 这个 skill，判断它处在哪个阶段
/antskill-creator 根据这个 PRD + 原型生成 Stage 1 需求型 Skill
/antskill-creator MCP ready 后，把这个 Stage 1 包升级到 Stage 2
/antskill-creator 按 Stage 2 Complete 校验这个包
/antskill-creator 把这个大 skill 拆成多个独立包
```
