# Yield Desk — v2 实现型参考

> 这是用 AntSkill Creator v2 流水线产出的实现型 Skill（A 范式）。

## 包含内容

- `l2_compute.py` — 完整的 L2 评分算法（可运行）
  - 7 步 Pipeline: filter → enrich → derive → normalize → score → rank → anomaly_detect
  - 5 维评分: yield / safety / convenience / capacity / stability
  - 权重矩阵（7 种偏好组合）
  - 异常检测（YIELD_OUTLIER / APY_DECLINING / HIGH_REWARD_DEPENDENCY / CAPACITY_LOW）

- `l3_decision.py` — L3 LLM 调用（含 Fallback）
  - Claude Sonnet 4 调用
  - 金字塔原则 System Prompt
  - 模板 Fallback 函数

- `l3_prompt.md` — 完整的 Decision Prompt 文本

- `platform_meta.yaml` — 8 家 CEX + 11 个 DeFi 协议的安全元数据

- `test_l2_scorer.py` — 16 个单测（全过）

## 与 v3 标准的差距

按 v3 AntSkill Creator 标准，此包缺少以下文件：

| 文件 | 状态 |
|------|------|
| SKILL.md (8 章节) | ❌ 缺失 |
| README.md | ❌ 缺失 |
| openai.yaml | ❌ 缺失 |
| VERSION | ❌ 缺失 |
| assets/ | ❌ 缺失 |
| references/ (9 个) | ❌ 缺失 |
| SKILL-REVIEW.md | ❌ 缺失 |

如需升级到 v3，参考 `../seerclaw-ref/` 的结构补充。
