---
name: antskill-creator
description: "Operating system for designing, prototyping, specifying, packaging, reviewing, and publishing high-quality standalone skills. Use when the user wants to create a new skill, turn a PRD or prototype into a shareable skill package, split one skill into multiple packages, enforce spec-first / dual-mode architecture, or generate a GitHub-ready skill with methodology, examples, quality gates, and delivery facade."
compatibility: filesystem, python3, git
---

# AntSkill Creator v3.0 — Skill 工厂操作系统

> **本文件是 Claude 造 Skill 时的主控大脑。每次用户要求「做一个 XXX Skill」时，必须先读本文件，再按决策树执行。**

---

## §0 决策树 — 判断当前阶段

```
用户消息 → 判断：
├─ "做/建/创建一个 XXX Skill" → S1（需求采集）
├─ 已有需求画布，用户说"开始/出demo" → S2（快速原型）
├─ 已有 demo，用户给反馈/改意见 → S3（精修定稿）
├─ 用户说"OK/定稿/出PRD" → S4（PRD 输出）
├─ 已有 PRD，用户说"打包/出skill包" → S5（包交付）
├─ 已有包，用户说"review/检查/对照" → S6（Skill Review）
└─ 不确定 → 询问用户当前想做什么
```

**每阶段结束时自动执行 `quality/gates.md` 对应门槛，🔴 项不通过则自动修复后重检，最多 3 轮。**

---

## §1 Skill 范式 — 三种形态

在 S1 阶段必须确定范式（默认 B）：

| 范式 | 名称 | 产出物 | 适用场景 |
|------|------|--------|----------|
| **A** | 实现型 | Pipeline 代码 + 单测 + 前端 | Skill 本身就是可运行服务 |
| **B** | 规范型（默认） | 引用文档包 + SKILL.md + 前端 Demo | 指导工程师在产品代码库实现 |
| **C** | 双模 | A + B 合体 | 需要可运行原型 + 生产规范 |

> 💡 绝大多数业务场景应选 B。A 型仅在"Skill 就是最终产品"时选用。

详见 `methodology/paradigms.md`。

---

## §2 6 阶段流水线

| 阶段 | 做什么 | 读取 SOP | 产出物 |
|------|--------|----------|--------|
| **S1** | 需求采集 + 范式选择 | `sop/s1_requirements.md` | 需求画布 |
| **S2** | 快速原型（Mock 数据） | `sop/s2_prototype.md` | 简版 Demo HTML |
| **S3** | 精修定稿（用户反馈） | `sop/s3_refinement.md` | 完整 Demo HTML |
| **S4** | PRD 输出（4 层拆解） | `sop/s4_prd.md` | 引用文档包 |
| **S5** | 包交付（元数据完整） | `sop/s5_delivery.md` | zip Skill 包 |
| **S6** | Skill Review（gap 分析） | `sop/s6_review.md` | SKILL-REVIEW 差距报告 |

**不允许跳步。** S1 必须在 S2 之前完成，S4 必须在 Demo 定稿后执行。

---

## §3 4 层 Pipeline 架构

每个 Skill 内部都遵循 4 层分离：

| 层 | 职责 | 特征 | 关键约束 |
|----|------|------|----------|
| **L1 数据层** | API/MCP 获取原始数据 | 有网络 I/O，可能失败 | 必须有降级策略 + 字段映射表 |
| **L2 计算层** | 脚本做过滤/评分/排序 | 纯计算，确定性，可单测 | 每个公式写伪代码 |
| **L3 决策层** | LLM 产出人话结论 + 洞察 | 有 Prompt + Fallback | 金字塔写作 + 风险对称 |
| **L4 渲染层** | 数据灌进容器组件 | 纯展示，不做计算 | Props 明确定义 |

详见 `prompts/layer_design_guides.md`。

---

## §4 金字塔原则 — 一切从结论开始

**用户永远在问「我该怎么做」。** Skill 必须：
1. **Hero 区**：先给结论（TOP 推荐 + 一句话 why）
2. **论据区**：用可视化数据证明结论
3. **信任区**：原始数据 + 方法论 + 风险提示（可折叠）

> 任何 Skill 的首屏如果不能在 3 秒内让用户理解核心信息，就是失败的。

---

## §5 视觉差异化制度

每个新 Skill 必须在 **主色 / Display 字体 / Hero 组件类型** 三个维度上与已有 Skill 不同。

### 已注册表

| Skill | 主色 | Display 字体 | Hero 类型 |
|-------|------|-------------|-----------|
| DualYield | `#d4a04a` 古铜金 | Cormorant Garamond | 排名卡 ×3 |
| Yield Desk | `#14e8b8` 电气薄荷 | Fraunces | 大卡+统计小卡 |

### 可用色池

| 色值 | 名称 | 适合主题 |
|------|------|----------|
| `#7c6aef` | 数据紫 | 分析/研究 |
| `#ff6b6b` | 警报红 | 风控/监控 |
| `#4ecdc4` | 海洋青 | 社区/治理 |
| `#ffd93d` | 信号黄 | 交易/信号 |
| `#6bcb77` | 生长绿 | 组合/增长 |
| `#ee6c4d` | 熔岩橙 | 热度/趋势 |

---

## §6 Source of Truth 优先级

当多个文件对同一细节有冲突时，按此顺序裁决：

```
delivery/SKILL.md（Non-negotiable Rules）
  > docs/product/PRD.md
    > docs/requirements/business-spec.md
      > docs/requirements/api-spec.md
        > docs/requirements/backend-computation.md
          > docs/requirements/implementation-guide.md
            > docs/requirements/ai-prompts.md
              > docs/requirements/viz-specs.md
                > implementation/frontend/*（仅作视觉参考）
```

详见 `methodology/source-of-truth.md`。

---

## §7 文件索引

```
antskill-creator/
├── SKILL.md                          ← 你在这里
├── docs/
│   ├── product/
│   │   └── PRD.md                    产品逻辑总说明
│   └── standards/
│       └── package-standard.md       包结构标准
├── VERSION
├── methodology/
│   ├── core-principles.md            底层哲学
│   ├── paradigms.md                  三种范式定义
│   ├── source-of-truth.md            SoT 优先级机制
│   └── responsibility-split.md       三方职责 + Retry Contract
├── sop/
│   ├── s1_requirements.md            需求采集
│   ├── s2_prototype.md               快速原型
│   ├── s3_refinement.md              精修定稿
│   ├── s4_prd.md                     PRD 输出
│   ├── s5_delivery.md                包交付
│   └── s6_review.md                  Skill Review
├── prompts/
│   └── layer_design_guides.md        L1-L4 设计指引
├── quality/
│   └── gates.md                      质量门槛 + 自动评估
├── templates/
│   ├── skill-md-template.md          8 章节 SKILL.md 模板
│   ├── readme-template.md            英文 README
│   ├── readme-zh-template.md         中文 README
│   ├── openai-yaml-template.yaml     Skill 商店元数据
│   ├── skeleton.html                 前端 React 骨架
│   ├── l2_compute_template.py        L2 算法骨架
│   ├── l3_decision_template.py       L3 LLM 调用骨架
│   ├── orchestrator_template.py      Pipeline 编排骨架
│   ├── test_template.py              单测骨架
│   ├── meta_template.yaml            元数据 YAML 骨架
│   ├── references/                   PRD + requirements 模板
│   ├── sample-templates/             AI input/output JSON
│   ├── scripts/                      validate-ai-output.js
│   └── assets/                       SVG 图标占位
└── examples/
    ├── seerclaw-ref/                  v3 规范型标杆
    └── yield-desk-ref/               v2 实现型参考
```

---

## §8 铁律（Non-negotiable Rules）

1. **Hero 必须有结论** — 不允许 Hero 区只放输入表单
2. **有推荐必须有风险** — 推荐段下方必须有对应风险提示
3. **不能一键下单** — Skill 只做决策辅助，不触发交易
4. **L2 单测必须全过** — 不允许跳过或注释掉失败用例
5. **L3 必须有 Fallback** — LLM 不可用时用模板函数兜底
6. **数据必须有来源标注** — 每个数据点标注 source + 更新时间
7. **每个 Skill 视觉独立** — 主色/字体/Hero 不与已有 Skill 重复
8. **PRD 覆盖每个像素** — 前端可见的每个元素都有计算逻辑说明
9. **范式先于设计** — S1 必须确定范式，不允许 S2 再改
