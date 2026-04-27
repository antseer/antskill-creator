---
name: antskill-creator
description: "Convert local skills through a two-stage lifecycle: Stage 1 Requirement Skill with complete product plan and mock data, then Stage 2 Complete Skill with all mock data replaced by verified real MCP/data sources."
compatibility: filesystem, python3, git
---

# AntSkill Creator

把一个本地 skill 按 **两阶段生命周期**整理、审计、补包和发布：

1. **Stage 1 — Requirement Skill（需求型）**：产品方案完整，前端 / 后端 / 数据源依赖讲清楚，用 mock 数据展示效果，交付研发接手。
2. **Stage 2 — Complete Skill（完整型）**：把 Stage 1 的 mock 全部替换为真实数据源，并验证 MCP / API 能覆盖全部数据依赖，可直接安装、运行、分享。

## Core promise

这个 skill 不做“表面包装”。每次先回答三个现实问题：

1. 当前包处在 **Stage 1 需求型**，还是 **Stage 2 完整型**？
2. 产品方案、前后端方案、数据依赖是否足够研发接手？
3. 所有 mock 是否已经被真实 MCP / API / 数据库替换，并有验证证据？

> `split` 是拆包动作，不是第三阶段。边界不清时，先 split，再分别进入 Stage 1 或 Stage 2。

## Stage model

### Stage 1 — Requirement Skill（需求型）

适用于：
- 已有完整产品方案 / PRD / 用户流程
- 已有前端方案或高保真 UI / HTML 原型 / 输出样式
- 已定义后端能力、接口、数据源依赖、字段口径
- 真实数据源尚未完全接入，当前用 mock / fixture / stub 展示效果
- 目标是交付研发继续开发

核心特征：
- 可以使用 mock 数据，但必须逐项标注
- 必须说明每个 mock 数据项未来由哪个 MCP / API / 数据库提供
- 必须有前端、后端、数据源依赖的工程实现信息
- 不能声称“可直接使用 / direct-use ready / 已完整可用”

必备交付：
- `SKILL.md`
- `README.md`：必须有 `Data Reality` 章节
- `README.zh.md`：必须有 `数据真实性` 章节
- `skill.meta.json`：如果有用户参数，必须包含标准 `input_schema`
- `REQUIREMENT-REVIEW.md`
- `TODO-TECH.md`
- `TECH-INTERFACE-REQUEST.md`：列出所有真实接口 / MCP / 数据源需求
- 产品方案：PRD / spec / 用户流 / 原型 / 前后端说明，至少一种明确文档或目录

`Data Reality` 必须回答：

```markdown
## Data Reality / 数据真实性

| 数据项 | 当前状态 | 当前用途 | 需要的真实数据源 / MCP | 是否阻塞 Stage 2 |
|---|---|---|---|---|
| 资金费率历史数据 | Mock（硬编码 fixture） | 图表展示与回测示例 | mcp://market/funding-rate 或 GET /api/funding-rate/history | 是 |
| BTC 价格 | Mock（随机生成） | 实时价格卡片 | mcp://market/ticker 或 WebSocket /ws/ticker | 是 |

**重要**：当前 skill 是 Stage 1 Requirement Skill，mock 数据仅用于展示产品效果和交互逻辑，不能作为真实分析或交易依据。真实数据源需求见 `TECH-INTERFACE-REQUEST.md`。
```

### Stage 2 — Complete Skill（完整型）

适用于：
- Stage 1 的 mock / fixture / stub 已全部替换为真实数据源
- MCP / API / 数据库已经能提供全部数据依赖
- skill 可以直接运行、调用或复用
- 有最小运行记录、数据源验证记录、MCP 覆盖矩阵或测试证据
- 目标是直接安装、分享、发布或真实使用

核心特征：
- 用户主路径不能依赖 mock / random / hardcoded 示例数据
- 所有数据项都有真实来源、调用方式、验证时间、失败处理
- MCP 覆盖全部必需数据依赖；若某项不用 MCP，必须说明替代真实来源
- 可以立即安装使用，并给出运行 / 验证证据

必备交付：
- `SKILL.md`
- `README.md`：必须有 `Data Sources` 和 `Validation Evidence` 章节
- `README.zh.md`：必须有 `数据来源` 和 `验证证据` 章节
- `skill.meta.json`：如果有用户参数，必须包含标准 `input_schema`
- `agents/openai.yaml`
- `VERSION`
- `.env.example`：如需要环境变量 / 鉴权
- `MCP-COVERAGE.md`：验证 MCP / API 是否覆盖全部数据依赖
- 可运行逻辑 / scripts / pipeline
- 测试或最小验证记录
- `validation.checks.json`：如需要可执行 Stage 2 检查

`Data Sources` 必须回答：

```markdown
## Data Sources / 数据来源

| 数据项 | 真实来源 | MCP / API / 方法 | 最后验证时间 | 失败处理 |
|---|---|---|---|---|
| 资金费率历史数据 | Binance / 内部市场数据服务 | mcp://market/funding-rate | 2026-04-27 | 返回空态并提示数据不可用 |
| BTC 实时价格 | 行情 MCP | mcp://market/ticker | 2026-04-27 | 使用最近有效值并标注延迟 |

**验证状态**：用户主路径不再依赖 mock 数据；全部必需数据项已通过 `MCP-COVERAGE.md` 验证。
```

## Standard workflow

### Step 1. Reality review

优先看：
- `SKILL.md`
- README / PRD / Stage 1 implementation docs
- frontend prototype / output UI
- backend/data interface request
- scripts / pipeline / tests
- agent config / metadata
- MCP / API 调用和验证记录

先输出一句判断：
- 这是 **Stage 1 Requirement Skill**
- 这是 **Stage 2 Complete Skill**
- 这是 **混合包，需要先 split**
- 这是 **not packageable yet**（目标或输入输出不清）

### Step 2. Classify by stage gate

按四问判断：

1. **边界**：这个包是否只解决一个清晰问题？多职责混杂 → 先 split。
2. **产品方案**：用户流程、前端展示、后端能力、数据依赖是否讲清楚？不清楚 → not packageable yet。
3. **mock 状态**：用户主路径是否仍依赖 mock / random / hardcoded 示例数据？是 → Stage 1。
4. **真实数据覆盖**：所有数据依赖是否由 MCP / API / 数据库真实提供，并有验证证据？是 → Stage 2；否则 Stage 1。

判断细化：
- 生产用户路径存在 mock / fixture / stub → Stage 1
- 测试、fixture、文档样例中存在 mock → 不自动降级，但必须标注不是用户主路径
- 部分真实、部分 mock → Stage 1，并在 `Data Reality` 逐项标注
- 不需要外部数据源的 skill → Stage 2 也可以成立，但 `Data Sources` 必须说明“仅使用用户输入 / 本地文件 / 仓库内容”，并给验证证据
- MCP 不能覆盖全部必需数据项 → 不能进入 Stage 2

### Step 3. Fill the right artifacts

如果是 Stage 1，优先补：
- `Data Reality / 数据真实性`
- `REQUIREMENT-REVIEW.md`
- `TODO-TECH.md`
- `TECH-INTERFACE-REQUEST.md`
- PRD / 前端方案 / 后端方案 / 数据依赖说明
- mock / stub 边界和替换计划

如果是 Stage 2，优先补：
- `Data Sources / 数据来源`
- `Validation Evidence / 验证证据`
- `MCP-COVERAGE.md`
- `README.md` / `README.zh.md`
- `skill.meta.json`
- `agents/openai.yaml`
- `VERSION`
- `.env.example`
- 最小运行说明和测试记录

### Step 4. Validate

至少执行：

```bash
python /Users/rick/.claude/skills/antskill-creator/scripts/quick_validate.py <skill_dir>
python /Users/rick/.claude/skills/antskill-creator/scripts/validate_shareable_skill.py <skill_dir> --stage requirement
# 或
python /Users/rick/.claude/skills/antskill-creator/scripts/validate_shareable_skill.py <skill_dir> --stage complete
# Stage 2 如果提供 validation.checks.json，执行真实检查：
python /Users/rick/.claude/skills/antskill-creator/scripts/validate_shareable_skill.py <skill_dir> --stage complete --run-checks
python /Users/rick/.claude/skills/antskill-creator/scripts/audit_skill.py <skill_dir> --stage complete --run-checks --format markdown
```

如果是 Stage 2 且有测试 / MCP 连通性检查，应写入 `validation.checks.json` 并用 `--run-checks` 执行。

### Step 5. Publish when asked

如果用户要求上传：
- 同步到目标仓库
- commit / push
- 返回链接
- 明确说明发布的是 Stage 1 Requirement Skill 还是 Stage 2 Complete Skill
- Stage 1 发布时必须醒目标注：mock 数据仅用于展示，不可直接用于真实分析或生产

## Split rule

满足任意两条，建议先 split：
- 面向两个以上明显不同用户
- 有两个以上独立触发场景
- 输出物完全不同
- 依赖完全不同的数据源 / MCP / API
- README 里出现多个互不依赖的核心 promise
- 一个包同时包含 Stage 1 需求文档和 Stage 2 可运行产品，但两者边界不清
- 用户可以只安装其中一半而不影响另一半

split 输出必须包含：

```markdown
## Split Plan

| 子 skill | 目标用户 | 输入 | 输出 | 数据依赖 | 阶段 |
|---|---|---|---|---|---|
```

## Non-negotiables

1. 先判断阶段，再包装
2. Stage 1 必须有完整产品方案：前端、后端、数据源依赖都要讲清楚
3. Stage 1 必须有 `Data Reality`，标清楚哪些是 mock、未来由哪个 MCP / API / 数据源替换
4. Stage 1 不能写成“可直接使用 / direct-use ready”
5. Stage 2 必须把用户主路径里的 mock 全部替换为真实数据源
6. Stage 2 必须有 `Data Sources`、`Validation Evidence`、`MCP-COVERAGE.md`
7. Stage 2 必须验证 MCP 是否覆盖全部必需数据依赖；不能覆盖的必须说明真实替代来源
8. 中英 README 要结构对等
9. 不能隐瞒接口 / 数据 / MCP 覆盖缺口
10. 如果 skill 有用户参数，`skill.meta.json > input_schema` 必须存在，且 zh/en key 完全一致
11. split 不是阶段

## input_schema standard

凡是带参数的 shareable skill，参数配置一律写在 `skill.meta.json > input_schema`。

格式要求见：

- `/Users/rick/.claude/skills/antskill-creator/references/input-schema-standard.md`

最低要求：
- 顶层必须有 `zh` / `en`
- 每个参数必须包含 `type` / `label` / `default` / `options` / `description` / `required`
- `input` 的 `options` 必须是 `[]`
- `select.default` 必须存在于 `options[].value`
- `multiple.default` 必须是数组，且每个值存在于 `options[].value`
- `required` 必须是 boolean

## Required output contract

最终汇报至少包含：
1. 阶段判断：Stage 1 Requirement / Stage 2 Complete / 需先拆分 / not packageable yet
2. 完成度判断
3. 补了哪些文件
4. 已具备哪些能力
5. 还缺什么，尤其是 mock → MCP / 真实数据源的缺口
6. MCP / API / 数据源覆盖是否已验证
7. 如执行 audit，附结构化分数、缺失项和 Stage 2 blockers
7. 是否已上传 / 发布
