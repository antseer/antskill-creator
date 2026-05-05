# G3 — 高保真 HTML · 质量门禁

> **对应 SOP**: `sop/s3_html_design.md`
> **执行时机**: S3 结束,进 S4 之前
> **失败处理**: 🔴 项不通过必须回 S3 修正

---

## G3.1 · 视觉差异化登记(🔴 Critical)

- [ ] 已执行 `scripts/sync_antseer_components.sh`，并记录外部缓存 commit
- [ ] 已参考 `references/antseer-components-standard.md`，且未把组件库 checkout / `.git` / `node_modules` / demo 数据复制进本 Skill
- [ ] `design-system/visual-registry.md` 已新增本 Skill 条目
- [ ] 登记发生在 HTML 编码之前(不允许画完再登记)
- [ ] 主色与所有已登记 Skill 至少 1 个维度(色相/明度/饱和度)显著不同
- [ ] Display 字体不与任何已登记 Skill 重复
- [ ] Hero 类型与所有已登记 Skill 不同

## G3.2 · 设计规范达标(🔴 Critical)

- [ ] 所有颜色引用 tokens(或 CSS 变量),无硬编码 hex
- [ ] 所有字号 / 行高引用 scale,无散落字号
- [ ] 所有间距引用 spacing scale,无魔法数字
- [ ] 所有圆角引用 radius scale
- [ ] 符合 `design-system/antseer-design-system.md` 的硬约束(深色底、特定对比度等)
- [ ] 符合 `references/antseer-components-standard.md` 的 Antseer canonical palette / source footer / host 嵌入规则

## G3.2A · Frontend SoT 合规(🔴 Critical)

- [ ] Stage 1：已尽量遵守 `antseer-components` 的组件结构、代码分层、UI token、状态和响应式规范；无法遵守项已记录为 Stage 2 blocker
- [ ] Stage 2：代码风格硬达标：adapter → domain calculator → view model → renderer 分层；renderer 不取数、不算业务口径、不造 fallback 数据
- [ ] Stage 2：UI 风格硬达标：使用 Antseer tokens / canonical palette；无临时主题色；无业务样式散落 hardcode
- [ ] Stage 2：设计样式硬达标：loading / empty / error / degraded 状态、source footer、响应式和数据来源证据齐全
- [ ] Stage 2：正式 HTML 模板包含 `#antseer-data` 与 `#antseer-data-schema`
- [ ] Stage 2：root / `.container` / `main` 不设置 `max-width`、`margin: 0 auto` 或外层 padding
- [ ] HTML 必须中文：`<html lang="zh-CN">` 已声明；所有用户可见文案、按钮、状态、placeholder、aria-label、title、alt、source footer 使用中文；英文仅限品牌名、ticker、协议/技术缩写、URL、版本号等不可翻译标识

## G3.3 · 高保真要求(🔴 Critical)

- [ ] 无占位图(placeholder gray box)
- [ ] 无 lorem ipsum 或 "xxxx" 假字
- [ ] 所有 mock 数据基于 PRD 附录 A 的 schema,贴近真实
- [ ] 无 NaN / undefined / 空数组(空态要显式走 empty 组件)

## G3.4 · 状态完整性(🔴 Critical)

- [ ] 每个主要组件至少画出 3 态中的 2 态(default / loading / empty / error 任选二)
- [ ] Hero 至少画出 3 态(default / 有数据 / error)
- [ ] 主图表至少画出 3 态(loading / 有数据 / empty)
- [ ] hover / active 交互状态可见(至少在按钮和卡片上)

## G3.5 · 响应式(🔴 Critical)

- [ ] 桌面 ≥ 1280px 完整可用
- [ ] 移动 ≤ 480px 可用(可以只保留关键信息,但不能破版)

## G3.6 · 数据契约对齐(🔴 Critical)

- [ ] HTML 里每个动态字段可追溯到 PRD 附录 A 的某个 Dxx
- [ ] 无前端自造字段(PRD 里没有的数据)
- [ ] 若 L1-B / L2 缺口对应的 UI 组件在 HTML 中出现,用 mock 数据呈现且清晰可识别(后续 S4 会记为 v2 延期)

## G3.7 · PRD 覆盖(🔴 Critical)

- [ ] PRD 每个 L5 组件在 HTML 中有实现(或明确在 HTML 注释标 v2 延期)
- [ ] Hero / 中间可视化 / 信任层金字塔结构清晰
- [ ] Hero 有结论(非仅输入表单)

## G3.8 · 技术约束(🟡 Important)

- [ ] 单个 HTML 文件(CSS + JS 内联),可独立打开
- [ ] 未使用 localStorage / sessionStorage
- [ ] 底部标注 `demo-v1 · Powered by Antseer.ai`
- [ ] 至少 1 个完整交互链路可跑通(输入 → 切换 → 重渲染)

---

## 常见 Block 点

| 症状 | 对策 |
|---|---|
| 未同步 antseer-components | 先执行 `scripts/sync_antseer_components.sh`，记录外部缓存 commit，再重跑 G3 |
| 把组件库 node_modules / demo 数据复制进 Skill | 删除 vendored 缓存，只保留真实 Skill 源码和必要规范引用 |
| Stage 2 前端缺 `#antseer-data` / schema / source footer | 补官网 JSON 模板契约和来源 footer，再重跑门禁 |
| HTML 可见文案是英文 | 改为中文，并声明 `<html lang="zh-CN">`；只保留 Antseer、BTC、MCP、API、URL、版本号等不可翻译标识 |
| root 容器承担页面宽度 / 居中 / padding | 删除 root 约束，交给 host page；只保留内部 section/card spacing |
| renderer 直接读 MCP payload 或生成 fallback | 增加 adapter / view model 层，renderer 只消费 view model |
| 画完才登记 visual-registry | 回 S3 重新确认主色/字体/Hero,修改若撞脸的地方,重跑门禁 |
| 硬编码颜色 | 全部改 CSS 变量,引 tokens |
| 只画 happy path | 每个主组件补 loading / empty,Hero + 主图表补 error |
| 前端字段 PRD 里找不到 | 要么删除,要么回 S2 补 PRD 并重跑 G2 |
| PRD 某个 L5 组件 HTML 没实现 | 补上,或在 HTML 注释和 PRD 同时标"v2 延期" |
| 移动端破版 | 补 ≤ 480px 断点样式 |

## 通过条件

所有 🔴 Critical 全部通过 → 进入 S4。
