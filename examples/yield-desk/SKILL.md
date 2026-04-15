---
name: yield-desk
description: "Stablecoin yield decision desk for comparing CEX and DeFi earning products with multi-factor scoring, structured product data, and LLM recommendation output. Use when evaluating USDT/USDC/DAI/FDUSD earn opportunities, comparing Binance/OKX/Bybit/Bitget/KuCoin/Gate/HTX against Aave/Compound/Morpho/Pendle/Spark/Ethena/Curve-style DeFi yields, or handing a PM-designed yield research workflow to engineering for implementation."
---

# Yield Desk · 稳定币收益决策台

## Status

这是一个 **PM 设计完成、工程未完工的半成品 skill 包**。

适合：
- 产品经理把需求、评分逻辑、前端原型、技术待办交给工程
- 工程同事基于现有 Pipeline 继续补 API 接入、配置、前端注入、部署

不适合直接当作：
- 已生产可用的完整技能
- 已完成真实 API 联调的上线版本

## What is already strong

- 4 层 Pipeline 架构清晰：`L1 → L2 → L3 → L4`
- L2 评分层基本成型，可直接复用
- 前端高保真原型已具备产品表达力
- 安全元数据 YAML 已有可用初版
- L3 有 fallback，LLM 挂掉时不至于完全失效

## What engineering still needs to finish

优先读：`TODO-TECH.md`

高优先缺口：
- Antseer 主通道 API 契约确认
- 其余 CEX Earn API 实现（OKX/Bybit/Bitget/KuCoin/Gate/HTX）
- L3 环境变量 / API Key / 代理接入
- 前端 mock → pipeline 输出注入
- 更完整的 L1/L4 集成测试

## Package map

```text
yield-desk/
├── SKILL.md
├── README.md / README.zh.md
├── VERSION
├── requirements.txt
├── .env.example
├── TODO-TECH.md                 # 工程待办主清单
├── HANDOFF-REVIEW.md            # 当前完成度与风险说明
├── PRD-YieldDesk-v2-完整分层规范.md
├── agents/openai.yaml
├── assets/
├── pipeline/
├── frontend/
├── tests/
└── data/
```

## Execution order

```text
L1 数据获取 → L2 计算评分 → L3 LLM 决策 → L4 前端渲染
```

## Suggested handoff reading order

1. `README.md`
2. `HANDOFF-REVIEW.md`
3. `TODO-TECH.md`
4. `PRD-YieldDesk-v2-完整分层规范.md`
5. `pipeline/` 与 `frontend/yield-desk.html`

## Quick commands

```bash
pip install -r requirements.txt
python tests/test_l2_scorer.py
python pipeline/orchestrator.py
```

## Notes for engineering

- `frontend/yield-desk.html` 当前是 mock 原型，不是数据联调完成版
- `pipeline/l1_data/fetcher.py` 中 Antseer 路径已修正字段映射方式，但真实接口契约仍需确认
- 若 LLM 不可用，`fallback_decision()` 可作为降级输出
