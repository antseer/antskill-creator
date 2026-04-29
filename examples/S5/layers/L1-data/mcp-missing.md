# L1-B · 待 MCP 新建原始工具

> 本 Skill 依赖的 L1-B 缺口,详细期望接口形态 + 降级策略见根目录 `data-prd.md`。

## 本 Skill 依赖的 L1-B 缺口

| GAP 编号 | 工具名 | 优先级 | 对应模块 | 核心字段 |
|---|---|---|---|---|
| **DATA-01** | `ant_news.by_market` | **P0** | M2(新闻节点叠加)+ M4(新闻列表)| D90 根 → D91/D104/D105/D107/D109 衍生 |
| DATA-02 | `ant_polymarket.parse_market_url` | P2 | M1(URL 快速解析)| 辅助 D32 |

## 排期建议(给后端)

1. **DATA-01 先做**:这是本 Skill 与 Polymarket 自带图表、ElectionBettingOdds 的**核心差异化**(新闻层叠加)。不做则 Skill 退化到 D155 降级态,丧失核心价值。
2. **DATA-02 可延后**:纯 regex 解析,前端已内置降级(regex 兜底 + search_markets),对用户**完全透明**。

## 降级依赖

每条 GAP 的前端表现、L3/L4 兜底、用户感知**在 `data-prd.md` 对应条目的「降级策略」段**。

- DATA-01 未实现 → D155 降级态(概率曲线保留,新闻卡替换为降级提示),Hero 用 L4 Fallback 不引用新闻的版本
- DATA-02 未实现 → 前端 regex `/event\/([^\/\?]+)/` 抽 slug 走 search_markets,无感降级

## 追溯

- PRD M1 §1.3 L1-B · M2 §2.3 L1-B
- mcp-audit.md R3.2(DATA-02)· R6.3+R7(DATA-01)
- data-prd.md DATA-01 / DATA-02
