# Yield Desk

稳定币收益决策台。

> **状态：PM 规格包 / 工程交接包**
>
> 这不是一个已经联调完成、可直接上线的 skill，而是一个适合分享给技术同事继续开发的半成品包。

## 包内有什么

- 4 层 Pipeline 架构
- 完整产品技术 PRD
- 高保真前端原型
- 已基本成型的 L2 评分逻辑与单测
- 平台 / 协议安全元数据
- 工程待办清单
- 当前完成度 review

## 当前判断

### 已经比较强的部分
- `L1 → L2 → L3 → L4` 架构清晰
- L2 评分层最成熟，可直接复用
- 前端原型表达力强
- YAML 元数据已有可用初版
- 当前 L2 单测通过 `16/16`

### 明显还没做完的部分
- Antseer API 契约未锁定
- Binance 之外的大多数 CEX 仍是存根
- L3 环境变量 / API Key / 部署接线未完成
- 前端还在使用 mock 数据
- 没有完整 E2E 可靠性层

## 建议阅读顺序

1. `HANDOFF-REVIEW.md`
2. `TODO-TECH.md`
3. `PRD-YieldDesk-v2-完整分层规范.md`

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python tests/test_l2_scorer.py
python pipeline/orchestrator.py
```

## 分享目的

这个包的目标不是“展示已经做完”，而是让技术同事拿到之后能快速知道：
- 哪些已经能直接复用
- 哪些是明确待办
- 哪些风险还没消除
- 从哪里继续接着做
