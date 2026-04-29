# L1-A · MCP 现有可用工具清单

> 本 Skill 依赖的**已有** MCP 工具,后端直调即可,无需新建。
> 基准:`mcp-audit.md` + `mcp-capability-map/cache/manifest.json`。

## 工具清单

| Dxx | 字段 | MCP Tool | 入参 | 出参 Schema | 使用模块 |
|---|---|---|---|---|---|
| (辅) — | 市场搜索(按关键词) | `ant_polymarket.search_markets` | `q: string, limit: int (默认 10)` | `Array<{id, title, prob, vol, end_date}>` | M1 · 市场识别 |
| D80 | 概率时序 | `ant_polymarket.price_history` | `market_id: string, interval: '1h', days: 7 \| 30` | `Array<{t: ISO8601, prob: number}>` | M2 · 漂移分析 |
| D81 | 量时序 | `ant_polymarket.price_history`(同调用联产)| 同上 | `Array<{t: ISO8601, volume: number}>` | M2 · 漂移分析 |
| — | 市场元信息 | `ant_polymarket.market_meta` | `market_id: string` | `{id, title, slug, end_date, category}` | M1 / 兜底显示 |

## 调用约定

- **D80 / D81 同源**:一次 `price_history` 调用返回 `prob` + `volume` 两个字段序列,L3 分拆,**不重复调用**。
- **interval 固定 `1h`**:窗口 7D → 168 点;窗口 30D → 720 点。不支持其它间隔。
- **错误处理**:若返回空数组或 HTTP 非 2xx,走 D153+D154 错误态 UI;超时 5-15s 切 Error。

## 追溯

- PRD M2 §2.3 L1-A 表
- mcp-audit.md R4(主 CTA 执行部分)+ R5(漂移分析主链路)
