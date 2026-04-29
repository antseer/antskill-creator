# S5 — Skill 半成品交付

## 阶段目标

交付一个可让后端和产品继续推进的 Skill 半成品目录。

## 根目录结构

```text
{skill-name}/
├── SKILL.md
├── VERSION
├── data-prd.md
├── skill-prd.md
├── skill.meta.json
├── review-report.md
├── frontend/
│   └── index.html
└── layers/
    ├── L1-data/
    ├── L2-aggregation/
    ├── L3-compute/
    ├── L4-llm/
    └── L5-presentation/
```

## 各文件职责

- `data-prd.md`：给研发提 MCP 数据需求
- `skill-prd.md`：给 PM / 产品自己开发 Skill
- `skill.meta.json`：平台元数据
- `skill.meta.json.input_schema`：若有参数，必须符合标准

## 强约束

- `L1-B` / `L2` 缺口必须指向 `data-prd.md`
- `L4` 必须有 fallback
- `L5` 只能消费上游字段，不自己做业务计算
- 有参数的 Skill，必须交付合法的 `input_schema`

## 后端续写入口

1. 先按 `data-prd.md` 补 P0
2. 再补 P1 / P2
3. 按 `skill-prd.md` 对齐页面和模块
4. 最后接平台元数据与真实运行时
