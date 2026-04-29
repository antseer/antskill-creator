# S4 — HTML ↔ 双 PRD 对齐 Review

## 阶段目标

产出：

- `review-report.md`
- `skill.meta.json`

## 输入

- `demo-v1.html`
- `skill-prd.md`
- `data-prd.md`
- `mcp-audit.md`

## 核心原则

- **双向核对**
  - HTML → PRD
  - PRD → HTML
- **v2 延期项必须在 `data-prd.md` 找得到**
- **元数据不能脑补**
- **如果 Skill 有参数，必须补齐 `input_schema`**

## Skill 元数据补全

`skill.meta.json` 只能回填已经被 review 通过的事实。

若 Skill 有用户参数，`input_schema` 必须符合：

- `references/input-schema-standard.md`

至少检查：

- `zh` / `en` 参数 key 完全一致
- `type` 只用 `input | select | multiple`
- `required` 为 boolean
- `input` 类型 `options` 必须为 `[]`

## 产出物

| 文件 | 用途 |
|---|---|
| `review-report.md` | HTML ↔ 双 PRD 对齐记录 |
| `skill.meta.json` | 发布 / 平台元数据 |

## 常见错误

- 把 L1-B / L2 缺口误判成 HTML 漏实现
- 只补 `skill-prd.md`，不补 `data-prd.md`
- 有参数但没写 `input_schema`
