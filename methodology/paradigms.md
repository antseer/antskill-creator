# 三种产出范式

Skill 工厂支持三种产出范式,在 S0 的 Q7 决定。

---

## A — 实现型(Implementation-First)

**产出物**: 可直接运行的 Skill 代码 + 单测 + 前端 Demo

**适用场景**:
- Skill 本身就是最终产品(如独立分析工具、仪表板)
- 不需要嵌入更大的产品代码库
- 快速验证算法可行性

**目录结构**:
```
skill-name/
├── SKILL.md
├── VERSION
├── data-prd.md
├── skill-prd.md
├── frontend/
│   └── index.html
├── layers/
│   ├── L1-data/            真实 MCP 调用封装
│   ├── L2-aggregation/     已落地的聚合接口封装(如可能)
│   ├── L3-compute/         可运行的 Skill 脚本 + 完整单测
│   ├── L4-llm/             prompt + 真实 LLM 调用 + Fallback
│   └── L5-presentation/    组件映射
├── tests/
└── data-prd.md             (若仍有缺口)
```

**特点**: L3/L4 必须真实可跑,L1-A 连接真实 MCP,L1-B/L2 若缺口则暂时用本地 stub 代替。

---

## B — 规范型(Spec-First)⭐ v5 绝对默认

**产出物**: 分层 Skill 半成品工程(前端定稿 + PM 产出的 L3/L4 + 后端 TODO 清单)

**适用场景**:
- 功能要嵌入产品代码库(大多数情况)
- 需要后端工程师增强 MCP
- 需要多人协作开发
- 需要长期维护和迭代

**目录结构**(v5 标准):
```
skill-name/
├── SKILL.md                  分层设计说明 + MCP 依赖 + 触发描述
├── VERSION                   0.1.0(半成品初版)
├── data-prd.md               从 S2 带过来
├── skill-prd.md              从 S2 带过来
├── frontend/
│   └── index.html            S3 产出的高保真 HTML
├── layers/
│   ├── L1-data/
│   │   ├── README.md
│   │   ├── mcp-required.md   L1-A:已有 MCP 工具清单
│   │   └── mcp-missing.md    L1-B:指向 data-prd.md
│   ├── L2-aggregation/
│   │   ├── README.md
│   │   └── interfaces.md     待 MCP 新建的聚合接口
│   ├── L3-compute/
│   │   ├── README.md
│   │   └── *.py              可运行或壳子+TODO
│   ├── L4-llm/
│   │   ├── README.md
│   │   └── *.md              prompt + schema + Fallback(必)
│   └── L5-presentation/
│       ├── README.md
│       └── component-map.md  每个组件一条
├── data-prd.md               后端 TODO(P0/P1/P2 分级)
└── review-report.md          S4 对齐证据
```

**特点**: PM 交付到"后端可直接续写"的程度。L1-B/L2 要求明确接口契约,不是"后端看着办"。

---

## C — 双模(Dual-Mode)

**产出物**: A + B 合体

**适用场景**:
- 需要可运行原型验证算法
- 同时需要规范文档指导生产开发

---

## S0 阶段如何选择?

在需求画布的第 7 题询问:

> **Q7 范式选择**
> 这个 Skill 的目标是什么?
> - (a) Skill 本身就是最终产品,直接运行 → 选 **A 实现型**
> - (b) 需要产出规范文档,指导后端开发 → 选 **B 规范型** ⭐默认
> - (c) 两者都要 → 选 **C 双模**

**v5 决策提示**: 90% 以上的情况应选 B。只有用户明确说"我要能直接跑的代码"时才考虑 A 或 C。

---

## 范式对各步骤的影响

| 步骤 | A 实现型 | B 规范型 ⭐默认 | C 双模 |
|------|----------|----------|--------|
| S0 需求+Demo | 相同 | 相同 | 相同 |
| S1 数据盘点 | 相同 | 相同 | 相同 |
| S2 路由+PRD | 相同 | 相同 | 相同 |
| S3 高保真 HTML | 相同 | 相同 | 相同 |
| S4 Review | 相同 | 相同 | 相同 |
| S5 交付形态 | 可运行代码 + 前端 | **分层半成品** | 两者都有 |
| S5 L3 要求 | 必须可运行 + 单测 | 可运行 or 壳子+TODO | 必须可运行 + 单测 |
| S5 L4 要求 | 真实 LLM 调用 + Fallback | prompt 模板 + Fallback | 两者 |
| S5 L1-B/L2 | 若缺口需本地 stub | 写清接口契约交后端 | 双份声明 |
| S5 data-prd | 可能为空(已全部 stub) | 必须完整分级 | 必须完整分级 |
