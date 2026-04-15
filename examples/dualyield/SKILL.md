---
name: dualyield
description: "DualYield strategist for comparing dual investment / DCI products across CEX venues, scoring strike-duration candidates by yield and touch probability, and packaging a PM-defined dual-yield recommendation workflow for engineering handoff or further implementation. Use when users mention 双币投, dual investment, DCI, 双币理财, strike selection, or want to package / continue this dual-yield recommendation skill honestly."
compatibility: filesystem access required; Python 3 recommended for tests and pipeline validation.
---

# DualYield Strategist Skill

## Status

这是一个 **PM 规格完成、工程未完工的 handoff package**。

适合：
- 产品经理把双币投推荐逻辑、评分模型、前端原型交给工程继续做
- 工程同事复用现有 L2 / L3 / 前端原型，继续补齐 L1 接口和真实数据接线

不适合直接当作：
- 已经完成联调并可上线的 production skill
- 已经接通真实 Antseer / Binance / 其他 CEX 数据源的成品包

## What is already strong

- L2 计算评分层完整，32/32 测试通过
- PRD、技术待办、入门文档都比较完整
- 前端高保真原型已成型，信息架构清楚
- 模板式 L3 结论生成已明确，不依赖 LLM 才能工作

## What engineering still needs to finish

高优先缺口：
- Antseer DCI / 市场数据端点确认并接入
- Binance / 其他 CEX 数据获取实现
- 前端 mock → orchestrator 输出接线
- 真实缓存 / 波动率 / 环境变量收口

## File index

- `pipeline/l1_data/` — 数据获取层
- `pipeline/l2_compute/` — 计算评分层
- `pipeline/l3_decision/` — 结论生成层
- `pipeline/orchestrator.py` — Pipeline 编排
- `data/platform_meta.yaml` — 平台元数据
- `frontend/dualyield.html` — 高保真前端原型
- `tests/test_l2.py` — L2 单元测试
- `docs/PRD.md` — 产品需求文档
- `docs/TODO-TECH.md` — 技术同事待办
- `docs/TECH-ONBOARDING.md` — 技术入门指南

## Suggested reading order

1. `README.md`
2. `HANDOFF-REVIEW.md`
3. `TODO-TECH.md`
4. `docs/PRD.md`
5. `docs/TECH-ONBOARDING.md`

## Quick commands

```bash
python3 -m unittest tests.test_l2 -v
python3 - <<'PY'
import asyncio, sys
sys.path.insert(0, '.')
from pipeline.orchestrator import run_pipeline
print(asyncio.run(run_pipeline({"intent":"earn_yield","underlying":"BTC","principal":10000,"durations":[7,14],"risk":"balanced"})))
PY
```
