---
name: polymarket-drift-radar
version: 0.1.0
status: semi-finished
description: |
  任意 Polymarket 事件的概率漂移追踪图 —— 在概率曲线上叠加新闻节点标注 + 异常区间标红,
  回答"这天价格为什么跳" + "现在是不是回归入场窗口"。
  面向 Polymarket 新手交易者,一次性查询(看方向就走)。

  触发示例:
  - "帮我看看 Trump 2024 这个市场最近的价格走势和对应新闻"
  - "Polymarket Fed rate cut March 2026 这单 30 天有没有异常漂移,现在值不值得入场"

layers:
  L1-A:
    - ant_polymarket.search_markets
    - ant_polymarket.price_history
    - ant_polymarket.market_meta
  L1-B:
    - DATA-01 · ant_news.by_market (P0)
    - DATA-02 · ant_polymarket.parse_market_url (P2)
  L2:
    - DATA-03 · ant_polymarket.similar_drift_stats (P1)
  L3:
    - layers/L3-compute/parse.py (可运行)
    - layers/L3-compute/extract.py (可运行)
    - layers/L3-compute/delta.py (可运行)
    - layers/L3-compute/volatility.py (可运行)
    - layers/L3-compute/bollinger.py (可运行)
    - layers/L3-compute/zscore.py (可运行)
    - layers/L3-compute/agg.py (可运行)
    - layers/L3-compute/drift.py (可运行)
    - layers/L3-compute/volume.py (可运行)
    - layers/L3-compute/format.py (可运行)
    - layers/L3-compute/news.py (壳子+TODO,依赖 DATA-01)
  L4:
    - layers/L4-llm/verdict.md
    - layers/L4-llm/hero-narrative.md
    - layers/L4-llm/drift-narrative.md
    - layers/L4-llm/hit-rate-narrative.md
  L5:
    - frontend/index.html

mcp_gap_summary:
  P0: 1
  P1: 1
  P2: 1
---

# polymarket-drift-radar

## 分层设计概述

本 Skill 按 L1→L5 分层协作,每层职责清晰、向下依赖单向:

- **L1 数据接入**:从 Polymarket MCP 取概率时序(D80)、量时序(D81);从 DATA-01(待补)取按市场的新闻(D90)
- **L3 脚本计算**:
  - 基础指标:MA-20 / 20σ / Bollinger 上下轨(`bollinger.py`)/ Z-Score(`zscore.py`)/ 7D 波动率(`volatility.py`)/ 30D 成交量(`agg.py`)
  - 异常检测:逐点越界(`drift.py::mark_anomaly`)→ 连续段合并滤噪(`segment_anomaly`,min ≥ 24h)→ 统计段数(`count_segments`)与最后峰值(`peak_of_last`)
  - 新闻侧:Top N 筛选 + 序号编号(`news.py`,**依赖 DATA-01**)
  - 格式化:日期戳 / 相对时间 / 折叠块 summary(`format.py`)
- **L2 聚合**:DATA-03 提供历史相似漂移 72h 回归命中率(D57),供 M3 Hero 正文和 M4 信任层叙述使用
- **L4 LLM 结构化**:
  - `verdict.md` → D51/D52(结论关键词 + 副标题,三值:回归入场窗口 / 观望 / 继续偏离)
  - `hero-narrative.md` → D53(Hero 正文 2-3 句,risk_level × 有无 D57 四套模板)
  - `drift-narrative.md` → D122(每段漂移一条复盘)
  - `hit-rate-narrative.md` → D123(带样本量和止损条件的命中率段)
- **L5 前端展示**:`frontend/index.html` 按 `layers/L5-presentation/component-map.md` 的映射消费上游产出,不做任何计算加工

## MCP 依赖

本 Skill 依赖 3 个已有 MCP 工具 + 3 个待后端补齐的 MCP 工具,汇总如下(完整契约见 `data-prd.md`):

| 缺口 | 层 | 优先级 | 价值 |
|---|---|---|---|
| **DATA-01 · ant_news.by_market** | L1-B | **P0** | 新闻层叠加是本 Skill 核心差异化。不落地 Skill 退化为 D155 降级态,丧失核心价值 |
| DATA-03 · ant_polymarket.similar_drift_stats | L2 | P1 | Hero 正文"72h 命中率 73%"的数据支撑。未落地 → L4 Fallback 走"不含具体数字"模板,说服力下降但可用 |
| DATA-02 · ant_polymarket.parse_market_url | L1-B | P2 | URL 解析服务化。未落地 → 前端 regex 兜底,用户无感 |

P0 不落地 Skill **无法完整运行**(但仍可降级展示)。P1 / P2 可降级。

## 后端续写入口

按以下顺序推进可最快拿到可上线版本:

1. **实现 DATA-01**(P0)→ 本 Skill 的新闻层接通,`layers/L3-compute/news.py` 的壳子可以切换到"真逻辑"(文件头 logic 段已写明待实现点)
2. **实现 DATA-03**(P1)→ D57 接入,Hero 正文和信任层的具体命中率数字自动启用(Fallback 函数已有两条路径切换)
3. **实现 DATA-02**(P2,可选)→ `layers/L3-compute/parse.py` 从 regex 兜底退位到 MCP 直解
4. **核对 L4 Fallback 与生产 LLM 策略**:4 个 prompt 的 Fallback 模板函数均已产出合法 schema,可作为生产环境的 LLM failover 直接上线
5. **补 L3 单测**:虽每个 `.py` 文件 `__main__` 已内置 mock 验证,生产前建议迁移到 `tests/` 目录并接 CI

## 追溯索引

| 文档 | 位置 | 用途 |
|---|---|---|
| PRD | `skill-prd.md` | 分层设计权威源(附录 A 字段 schema)|
| 路由审计 | `mcp-audit.md` | Dxx → L1/L2/L3/L4/L5/INPUT/STATIC 逐条决策 |
| MCP 缺口 | `data-prd.md` | 3 条 GAP 的完整接口契约 + 降级策略 |
| S4 评审 | `review-report.md` | HTML ↔ 双 PRD 对齐证据 + G4 门禁自查 |
| 组件映射 | `layers/L5-presentation/component-map.md` | 每个 UI 组件的上游数据追溯 |
