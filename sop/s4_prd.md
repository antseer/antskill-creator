# S4 — PRD 输出

## 目标

将定稿的前端 Demo **逆向拆解**为：

1. **`docs/product/PRD.md`**：完整产品逻辑总说明
2. **`docs/requirements/` 下的 8 个规范文档**：覆盖每个像素的数据来源、计算逻辑和边界条件
3. **`delivery/SKILL.md`**：交付入口

目标不是“把 demo 解释一遍”，而是让产品、工程、AI、评审都能在不同层面找到自己的单一真相来源。

## 方法论

**逆向拆解法。** 从前端 Demo 的每一个可见元素出发，追溯到数据源。

```
前端可见元素
  → 这个元素显示什么数据？（viz-specs.md）
    → 这个数据怎么算出来的？（backend-computation.md）
      → 这个计算需要哪些原始数据？（api-spec.md）
        → 这些原始数据从哪获取？（api-spec.md L1 部分）
          → 如果获取失败怎么办？（implementation-guide.md）
```

## 先写 PRD，再写 requirements

### 0. docs/product/PRD.md（完整产品逻辑）

必须先产出这一份总文档，回答：

- 这个 skill 到底替用户解决什么问题
- 用户输入是什么，系统输出是什么
- 决策链路如何从 L1 → L4 串起来
- 推荐/排序/异常/降级的完整业务逻辑是什么
- 哪些属于需求约束，哪些属于实现约束

如果没有这份 PRD，后面的文档只会变成分散的零件说明，无法形成完整产品逻辑。

## 8 个 requirements 文档的产出顺序

**必须按此顺序写**（依赖关系）：

### 1. business-spec.md（产品契约）
- 核心概念定义
- 业务规则（筛选条件、排序逻辑、推荐数量）
- 边界条件（数据不足时怎么办、极端值怎么处理）
- 成功标准

### 2. api-spec.md（API 字段定义）
- L1 数据源清单（每个源的 endpoint、认证、频率、延迟）
- 原始数据 → 内部 Schema 的字段映射表
- 降级策略表

### 3. backend-computation.md（计算逻辑）
- L2 每一步的伪代码
- 评分公式 + 权重矩阵
- 异常检测规则
- 归一化方法

### 4. implementation-guide.md（前端 + AI 架构）
- L4 容器组件列表 + Props 定义
- 数据从 L2/L3 灌入容器的绑定流程
- Production-vs-Prototype 标注
- 降级 UI 规范
- Retry Contract 实现

### 5. ai-prompts.md（Prompt 规范）
- L3 System Prompt 完整文本
- 输入 JSON Schema
- 输出 JSON Schema
- 调用参数（model / temperature / max_tokens）
- Fallback 模板函数

### 6. viz-specs.md（可视化像素规范）
- 每个组件的像素尺寸、间距、字号
- 颜色编码规则（什么值对应什么颜色）
- 动画/过渡效果
- 响应式断点

### 7. prototype-notes.md（原型 parity）
- Demo 中哪些行为是 prototype-only
- Demo 中哪些视觉是参考标准
- 生产实现与 Demo 的已知差异

### 8. TestSuite.md（自测清单）
- 功能测试用例
- 边界条件测试
- 降级测试
- 视觉回归检查点

## 然后产出 delivery/SKILL.md

用 `templates/skill-md-template.md` 模板，填入 8 章节内容。

## 逆向拆解检查表

对 Demo 的每一个可见元素，回答以下 6 个问题：

| # | 问题 | 写入文档 |
|---|------|----------|
| 1 | 这个元素显示什么？ | viz-specs.md |
| 2 | 数据从哪来？ | api-spec.md |
| 3 | 怎么算出来的？ | backend-computation.md |
| 4 | 边界条件是什么？ | business-spec.md |
| 5 | AI 需要说什么？ | ai-prompts.md |
| 6 | 出错了怎么办？ | implementation-guide.md |

如果任何一个问题答不出来，说明需求不清楚 → 回 S1 追问。

## 目录落位规则

```text
docs/
├── product/PRD.md
├── requirements/
│   ├── business-spec.md
│   ├── api-spec.md
│   ├── backend-computation.md
│   ├── implementation-guide.md
│   ├── ai-prompts.md
│   ├── viz-specs.md
│   ├── prototype-notes.md
│   └── TestSuite.md
└── review/SKILL-REVIEW.md

implementation/
├── pipeline/
├── frontend/
├── tests/
└── scripts/

delivery/
├── SKILL.md
├── README.md
├── README.zh.md
├── VERSION
└── agents/openai.yaml
```

**硬规则**：

1. `docs/` 只放需求/规范/评审，不放可运行代码
2. `implementation/` 只放实现，不放业务口径裁决
3. `delivery/` 只放可发布包装层，不承载产品逻辑
4. 评审时必须能通过目录结构一眼看出“需求型”和“实现型”边界

## 质量门 → 见 quality/gates.md S4 部分
