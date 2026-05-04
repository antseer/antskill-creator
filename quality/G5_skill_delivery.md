# G5 — Skill 半成品交付 · 质量门禁

## G5.1 目录结构（🔴）

- [ ] 根目录包含 `SKILL.md / VERSION / data-prd.md / skill-prd.md / skill.meta.json / review-report.md`
- [ ] `frontend/index.html` 存在
- [ ] `layers/` 五层目录存在

## G5.2 文档职责（🔴）

- [ ] `data-prd.md` 只负责研发数据提需
- [ ] `skill-prd.md` 只负责 PM / 产品开发说明
- [ ] `L1-B` / `L2` 引用 `data-prd.md`

## G5.3 Skill 元数据（🔴）

- [ ] `skill.meta.json` 与 `SKILL.md` 一致
- [ ] 若有参数，`input_schema` 已填写
- [ ] `input_schema` 满足标准
- [ ] zh / en key 一致

## G5.4 可追溯性（🔴）

- [ ] 从 L5 组件能追到上游数据点
- [ ] 唯一允许的断点是 `data-prd.md` 中已登记缺口

## G5.5 Frontend Source of Truth（🔴）

- [ ] 已执行或检查 `scripts/sync_antseer_components.sh`，记录外部缓存 commit
- [ ] 发布包未包含 `antseer-components` checkout / `.git` / `node_modules` / demo 数据
- [ ] Stage 1：`frontend/index.html` 尽量符合 `references/antseer-components-standard.md`；偏差已进入 `review-report.md` / `TODO-TECH.md` / `TECH-INTERFACE-REQUEST.md`
- [ ] Stage 2：代码风格、UI 风格、设计样式、host 嵌入、source footer、`#antseer-data` / `#antseer-data-schema` 全部符合前端 SoT
- [ ] Stage 2：用户主路径无 mock / fixture / random / synthetic 数据；内联数据也有真实来源和验证证据

## 通过条件

所有 🔴 项通过；若目标是 Stage 2 Finished Skill，Frontend SoT 任一失败都必须降级为 Stage 1 blocker，不能发布为 finished。
