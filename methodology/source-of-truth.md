# Source of Truth（SoT）领域裁决机制

## 为什么不能只用一条线性优先级

Antseer skill 产物同时覆盖产品体验、数据接口、字段 schema、前端实现和交付审计。不同文件对不同领域拥有不同权威性。

错误做法是一条线性优先级，例如“skill-prd.md 永远高于 data-prd.md”。这会导致一个危险情况：如果 `skill-prd.md` 把某个 L2 数据错写成 L3，而 `data-prd.md` 正确记录了 L2 后端缺口，线性裁决会抹掉真实后端提需。

所以 v5.2 起采用**领域裁决**。

---

## 领域级 Source of Truth

| 领域 | 第一事实源 | 第二事实源 | 裁决规则 |
|---|---|---|---|
| 用户问题 / 产品目标 | `requirement-canvas.md` | `skill-prd.md` 概览 | 需求变了，回 S0；不能只改 UI |
| 字段 schema / Dxx 编号 | `skill-prd.md` 附录 A，或独立 `data-contract.md` | `data-inventory.md` | Dxx 只能增量变更，删除要标废弃 |
| L1-A / L1-B / L2 / L3 / L4 / L5 归属 | `mcp-audit.md` | `routing-decision-tree.md` | 归属冲突时回 S2 重判 |
| L1-B / L2 数据接口缺口 | `data-prd.md` | `TECH-INTERFACE-REQUEST.md` | 后端接口以 data-prd 为准 |
| 产品模块 / 用户体验 / 信息架构 | `skill-prd.md` | `review-report.md` | 体验以 skill-prd 为准 |
| L3 计算逻辑 | `skill-prd.md` 附录 A + `layers/L3-compute/` | `mcp-audit.md` | 脚本不得自造 Dxx 外字段 |
| L4 prompt / fallback | `layers/L4-llm/` | `skill-prd.md` | prompt 必须有同 schema fallback |
| L5 前端呈现 | `frontend/index.html` + `layers/L5-presentation/component-map.md` | `skill-prd.md` | HTML 是呈现，不得推翻数据/产品契约 |
| HTML ↔ PRD 差异 | `review-report.md` | S4 gate | review 只记录裁决，不是新需求源 |
| Stage 1 / Stage 2 包装真实性 | `STAGE-GATES.md` + validator scripts | `README.md` / `README.zh.md` | validator 不通过不得发布 |

---

## 文件级生成链路

```text
requirement-canvas.md
       ↓
demo-v0.html
       ↓
data-inventory.md
       ↓
mcp-audit.md
       ↓
├── data-prd.md      # L1-B / L2 后端提需权威源
└── skill-prd.md     # 产品模块、字段 schema、L3/L4/L5 权威源
       ↓
frontend/index.html + layers/
       ↓
review-report.md
       ↓
SKILL.md / README / package validators
```

---

## 冲突处理 SOP

### 1. data-prd.md vs skill-prd.md

先判断冲突领域：

- 如果是**后端接口、MCP 缺口、刷新频率、鉴权、缓存、验收口径**：以 `data-prd.md` 为准。
- 如果是**用户体验、模块文案、页面布局、交互路径**：以 `skill-prd.md` 为准。
- 如果是**字段 schema / Dxx 类型**：以 `skill-prd.md` 附录 A 或 `data-contract.md` 为准；必要时回 S2 重判。

### 2. HTML vs PRD

HTML 不能创造新业务字段。发现 HTML 有 PRD 未定义字段：

1. 若字段合理：回 S2/S3 补 Dxx、归属、接口/计算逻辑。
2. 若字段不合理：删 HTML 字段。
3. 在 `review-report.md` 记录裁决。

### 3. L1-B / L2 被写成 L3

默认视为严重违规。只有同时满足以下条件，才允许 L3 临时降级实现：

- 所需 L1 原始数据已经真实覆盖；
- L3 只是临时性能降级或局部计算；
- `data-prd.md` 仍把该能力登记为 L2 缺口；
- UI / README 明确标注该能力未达到 Stage 2 成品口径。

否则就是“把后端缺口塞进 L3 掩盖”，G2 不通过。

### 4. review-report.md 的地位

`review-report.md` 是裁决记录，不是新需求来源。它只能说：

- 改 HTML
- 改 PRD
- 回 S2 重判
- v2 延期并指向 `data-prd.md`

不能凭空新增需求。

---

## 实操铁律

1. 先按领域找事实源，不按单一文件排名偷懒。
2. L1-B / L2 缺口永远不能被 `skill-prd.md` 或 HTML 抹掉。
3. 字段 schema 必须可追溯到 Dxx。
4. 前端只是消费契约，不是定义契约。
5. 改了高优先级事实源，必须重跑受影响的 Gate。
