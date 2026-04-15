# {{SKILL_NAME}}

> {{一句话描述这个 Skill 做什么}}

## 快速开始

1. 阅读 `delivery/SKILL.md` 了解操作契约
2. 阅读 `docs/product/PRD.md` 了解完整产品逻辑
3. 查看 `docs/requirements/api-spec.md` 了解数据源需求

## 架构概览

```
┌──────────────────────────────────────────────────┐
│                   delivery/                      │
│   SKILL.md · README · VERSION · metadata         │
├──────────────────────────────────────────────────┤
│                implementation/                   │
│   L1 数据 → L2 计算 → L3 决策 → L4 UI            │
├──────────────────────────────────────────────────┤
│                     docs/                        │
│   PRD → business/api/compute/prompt/viz/test     │
└──────────────────────────────────────────────────┘
```

## 文件索引

### docs/

| 文件 | 用途 |
|------|------|
| `docs/product/PRD.md` | 完整产品逻辑 |
| `docs/requirements/business-spec.md` | 产品契约 |
| `docs/requirements/api-spec.md` | API 字段定义 |
| `docs/requirements/backend-computation.md` | 计算逻辑 |
| `docs/requirements/implementation-guide.md` | 前端 + AI 架构 |
| `docs/requirements/ai-prompts.md` | Prompt 规范 |
| `docs/requirements/viz-specs.md` | 可视化规范 |
| `docs/requirements/prototype-notes.md` | 原型说明 |
| `docs/requirements/TestSuite.md` | 测试清单 |
| `docs/review/SKILL-REVIEW.md` | gap 分析 |

### implementation/

| 文件 | 用途 |
|------|------|
| `implementation/frontend/{{SKILL_SLUG}}.html` | 高保真 Demo |
| `implementation/scripts/validate-ai-output.js` | 输出校验脚本 |
| `implementation/tests/` | 自动化测试 |

### delivery/

| 文件 | 用途 |
|------|------|
| `delivery/SKILL.md` | 主控文档（8 章节） |
| `delivery/README.md` | 英文概述 |
| `delivery/README.zh.md` | 中文概述 |
| `delivery/agents/openai.yaml` | 商店元数据 |
| `delivery/VERSION` | 语义版本号 |

## 技术同事待办

详见 `docs/requirements/implementation-guide.md` 与 `docs/review/SKILL-REVIEW.md`。

## 许可

专有 — Antseer.ai
