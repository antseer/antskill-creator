# S5 — 包交付

## 目标

将 S4 产出的文档与实现打包为**可交付的 Skill 包**，并保证评审时可以一眼分清：

- `docs/`：需求与规范
- `implementation/`：实现与运行
- `delivery/`：发布与分发

## 方法论

**元数据完整 + 范式分支。** 不同范式的交付物清单不同，但目录职责不能混。

## 交付物清单

### 共同必须（所有范式）

| 文件 | 用途 | 检查项 |
|------|------|--------|
| `delivery/SKILL.md` | 主控 | 8 章节齐全 |
| `delivery/README.md` | 英文概述 | 含 Quick Start |
| `delivery/README.zh.md` | 中文概述 | 含快速开始 |
| `delivery/agents/openai.yaml` | 商店元数据 | name / description / version 齐全 |
| `delivery/VERSION` | 语义版本号 | 格式 x.y.z |
| `delivery/assets/icon-small.svg` | 小图标 | 48×48, viewBox 正确 |
| `delivery/assets/icon-card.svg` | 卡片图标 | 200×120, viewBox 正确 |

### B 规范型额外必须

| 文件 | 用途 |
|------|------|
| `docs/product/PRD.md` | 完整产品逻辑 |
| `docs/requirements/*.md` × 8 | requirements 文档 |
| `docs/review/SKILL-REVIEW.md` | gap 分析模板（空白待填） |
| `delivery/templates/ai-input.json` | AI 输入样例 |
| `delivery/templates/ai-output.json` | AI 输出样例 |
| `implementation/scripts/validate-ai-output.js` | 输出校验脚本 |
| `implementation/frontend/skill-name.html` | Hi-Fi Demo |

### A 实现型额外必须

| 文件 | 用途 |
|------|------|
| `implementation/pipeline/l1_data/` | 数据获取代码 |
| `implementation/pipeline/l2_compute/` | 计算代码 |
| `implementation/pipeline/l3_decision/` | LLM 调用代码 |
| `implementation/tests/test_l2.py` | 单测（必须全过） |
| `implementation/data/meta.yaml` | 平台/协议元数据 |
| `implementation/frontend/skill-name.html` | 前端 |
| `docs/product/PRD.md` | 完整 PRD |
| `docs/handoff/TODO-TECH.md` | 技术同事待办（按 🔴🟡🟢 分级） |
| `docs/handoff/TECH-ONBOARDING.md` | 技术入门文档 |
| `docs/review/HANDOFF-REVIEW.md` | 交付自查报告 |
| `.env.example` | 环境变量模板 |
| `.gitignore` | Git 忽略规则 |
| `requirements.txt` | Python 依赖 |

### C 双模 = A + B

## 打包步骤

1. 按范式检查文件完整性
2. 运行校验：
   - `python -m json.tool delivery/templates/ai-input.json`
   - `python -m json.tool delivery/templates/ai-output.json`
   - `node implementation/scripts/validate-ai-output.js`（用样例 JSON 跑一遍）
   - A/C 范式：`python -m pytest implementation/tests/`
3. **A/C 范式额外步骤**：创建 L3 Prompt 调优工具
   - 从 `templates/skeleton.html` 的 prompt tuner 模式起步
   - 至少 3 个测试场景
   - 含 Quality Checklist 自动评分
4. 压缩：`zip -r skill-name.zip skill-name/`
5. 输出到 `/mnt/user-data/outputs/`

## README 模板要求

- 第一段：一句话说清楚这个 Skill 做什么
- Quick Start：3 步能跑起来
- Architecture：一张 ASCII 图说明 4 层 Pipeline
- File Index：按 docs / implementation / delivery 三段列出所有文件
- TODO for Tech：按优先级列出技术同事要做的事

## 质量门 → 见 quality/gates.md S5 部分
