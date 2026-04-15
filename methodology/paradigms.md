# Skill 范式 — 三种形态

## 为什么需要范式选择？

v2 默认产出「代码型」Skill（Pipeline + 单测），但实际业务中：
- 90% 的功能最终要落地到**产品代码库**，而不是直接运行 Skill 代码
- Skill 代码 ≠ 生产代码（缺少认证、并发、监控、CI/CD）
- 工程师需要的是**规范文档**，不是半成品代码

v3 引入显式范式选择，默认改为规范型。

---

## 三种范式

### A — 实现型（Code-First）

**产出物**：可运行的 Pipeline 代码 + 单测 + 前端 HTML

**适用场景**：
- Skill 本身就是最终产品（如分析工具、仪表板）
- 不需要嵌入更大的产品代码库
- 快速验证算法可行性

**推荐目录结构**：
```
skill-name/
├── docs/
│   └── product/PRD.md            # 可简版，但建议保留产品边界
├── implementation/
│   ├── pipeline/
│   │   ├── l1_data/
│   │   ├── l2_compute/
│   │   └── l3_decision/
│   ├── frontend/
│   │   └── skill-name.html
│   └── tests/
│       └── test_l2.py
└── delivery/
    ├── SKILL.md
    ├── README.md
    └── agents/openai.yaml
```

### B — 规范型（Spec-First）⭐ 默认

**产出物**：完整 PRD + requirements 文档包 + SKILL.md + 前端 Demo + 元数据

**适用场景**：
- 功能要嵌入产品代码库
- 需要多人协作开发
- 需要长期维护和迭代

**推荐目录结构**：
```
skill-name/
├── docs/
│   ├── product/
│   │   └── PRD.md                产品逻辑总说明
│   ├── requirements/
│   │   ├── business-spec.md
│   │   ├── api-spec.md
│   │   ├── backend-computation.md
│   │   ├── implementation-guide.md
│   │   ├── ai-prompts.md
│   │   ├── viz-specs.md
│   │   ├── prototype-notes.md
│   │   └── TestSuite.md
│   └── review/
│       └── SKILL-REVIEW.md
├── implementation/
│   └── frontend/
│       └── skill-name.html       Hi-Fi Demo（仅作参考）
└── delivery/
    ├── SKILL.md
    ├── README.md
    ├── README.zh.md
    ├── VERSION
    ├── agents/openai.yaml
    ├── assets/
    └── templates/
        ├── ai-input.json
        └── ai-output.json
```

### C — 双模（Dual-Mode）

**产出物**：A + B 合体；既有完整 PRD/requirements，也有实现代码/测试

**适用场景**：
- 需要可运行原型验证算法
- 同时需要规范文档指导生产开发
- 复杂项目（如 DualYield + Yield Desk）

---

## S1 阶段如何选择？

在需求画布的第 7 题询问：

> **Q7 范式选择**
> 这个 Skill 的目标是什么？
> - (a) Skill 本身就是最终产品，直接运行 → 选 **A 实现型**
> - (b) 需要产出规范文档，指导工程师开发 → 选 **B 规范型** ⭐默认
> - (c) 两者都要 → 选 **C 双模**

如果用户不确定，默认选 B。除非用户明确说"我要能直接运行的代码"。

---

## 范式对 S4/S5 的影响

| 步骤 | A 实现型 | B 规范型 | C 双模 |
|------|----------|----------|--------|
| S4 产出 | PRD + 实现骨架 | `docs/product/PRD.md` + requirements 文档 + SKILL.md | 两者都有 |
| S5 元数据 | 建议保留 | **必须**（delivery/README + agents/openai.yaml + VERSION + assets） | 必须 |
| S5 校验 | 单测通过 | 文档完整 + validate-ai-output 通过 | 两者 |
| S6 Review | 代码 vs PRD 对比 | PRD vs requirements 一致性 | 全面 gap |
