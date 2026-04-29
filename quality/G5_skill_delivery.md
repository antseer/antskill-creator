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
