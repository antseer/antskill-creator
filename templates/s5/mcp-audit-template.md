# MCP 路由审计表 · {skill-name}

> **用途**: S2 产出。对 S1 数据盘点清单每一行,标注归属层(L1-A/L1-B/L2/L3/L4/L5/INPUT/STATIC)。
> **对应 SOP**: `sop/s2_routing_and_prd.md` Part A
> **进 PRD 前须过 G2.1 / G2.2 门禁**

## 元信息

- 基于 inventory: `data-inventory.md`
- 基于真源缓存: `mcp-capability-map/cache/MCP-Data-Capabilities.md`
- 远端 HEAD SHA: `{remote-head-sha}`
- 同步时间: `{synced-at}`
- 生成时间: YYYY-MM-DD

## 汇总

| 归属 | 条数 |
|---|---|
| L1-A (MCP 现有可用) | N |
| L1-B (MCP 缺失待补) → 进 data-prd | N |
| L2 (MCP 新聚合) → 进 data-prd | N |
| L3 (Skill 脚本) | N |
| L4 (LLM 结构化) | N |
| L5 (纯前端) | N |
| INPUT | N |
| STATIC | N |

---

## 审计表

| # | Dxx | 字段名 | 性质 | 归属 | 实现方式 / MCP Tool / 脚本位置 | 判定理由(决策树分支) |
|---|---|---|---|---|---|---|
| 1 | D01 | 用户输入关键词 | 用户输入 | INPUT | — | 用户输入不走层级判定 |
| 2 | D02 | 窗口档位 | 用户输入 | INPUT | — | 用户输入 |
| 3 | D03 | 匹配市场列表 | 原始值 | L1-A | `ant_polymarket.search_markets(q)` | Q1 原始值 → 真源已有 |
| 4 | D05 | Hero 结论 | 自然语言 | L4 | `layers/L4-llm/hero-verdict.md` (有 Fallback) | 自然语言直判 L4 |
| 5 | D10 | 当前概率 | 原始值 | L3 | `layers/L3-compute/extract.py::take_last(D30)` | Q1 原始但 MCP 无单点,从 D30 取尾 |
| 6 | D11 | 24h 变化 | 衍生值 | L3 | `layers/L3-compute/delta.py::delta_24h(D10,D12)` | Q2 否 → Q3 否 → 轻量计算 |
| 7 | D12 | 24h 前概率 | 原始值 | L3 | `layers/L3-compute/extract.py::point_at(D30,-24h)` | 从 D30 时序取点 |
| 8 | D13 | 7d 波动率 | 衍生值 | L3 | `layers/L3-compute/volatility.py::std_7d(D30)` | Q2 否(窗口小),轻量 |
| 9 | D30 | 概率时序 | 原始值 | L1-A | `ant_polymarket.price_history(id, 1h, 30d)` | MCP 已有 |
| 10 | D31 | Bollinger 上下轨 | 衍生值 | L3 | `layers/L3-compute/bollinger.py::compute_bands(D30)` | 滚动计算,Skill 特有 |
| 11 | D32 | 异常区间布尔 | 衍生值 | L3 | `layers/L3-compute/bollinger.py::mark_anomaly(D30,D31)` | 逐点布尔 |
| 12 | D50 | 漂移分析摘要 | 自然语言 | L4 | `layers/L4-llm/drift-summary.md` (有 Fallback) | 需主观解读 |
| 13 | D51 | 状态提示 | 自然语言 | L4 | `layers/L4-llm/state-guidance.md` (有 Fallback) | 综合判断 |
| 14 | D52 | 风险提示条目 | 自然语言 | L4 | `layers/L4-llm/risk-notes.md` (有 Fallback) | 自然语言列表 |
| 15 | D60 | 相关新闻 | 关联数据 | **L1-B** | 需新增 `ant_news.by_market` → **DATA-01 (P0)** | Q1 原始 → 真源无 |
| 16 | D70 | 月度 GMV | 衍生值 | **L2** | 需新增 `ant_market.monthly_gmv` → **DATA-02 (P1)** | Q2 是(跨时间聚合、多 Skill 复用) |
| 17 | D80 | 异常点新闻 | 原始值 | L3 | `layers/L3-compute/filter.py::news_at(D60,t)` | 对 D60 按时间筛选 |
| 18 | D81 | 视口范围 | 衍生值 | L5 | 前端缩放组件内部状态 | 纯 UI 交互派生 |
| 19 | D90 | Loading 文案 | 静态文案 | STATIC | 写死在 HTML | — |
| 20 | D91 | Empty 文案 | 静态文案 | STATIC | 写死在 HTML | — |
| 21 | D92 | Error 文案 | 静态文案 | STATIC | 写死在 HTML | — |
| 22 | D93 | Tooltip 公式 | 静态文案 | STATIC | 写死在 HTML | — |

---

## L1-B / L2 缺口汇总(指向 data-prd.md)

| Dxx | 归属 | GAP 编号 | 优先级 | 工具名 |
|---|---|---|---|---|
| D60 | L1-B | DATA-01 | P0 | `ant_news.by_market` |
| D70 | L2 | DATA-02 | P1 | `ant_market.monthly_gmv` |

详见 `data-prd.md`。

---

## 自查(G2.1)

- [ ] inventory 每行都有对应审计记录,无遗漏
- [ ] 每行归属非空,无"待定"
- [ ] L1-A 条目列出了具体 MCP tool 名 + 入参
- [ ] L1-B / L2 条目列出了将要新建的 tool 名 + 指向 DATA 编号
- [ ] L3 条目列出了脚本位置 + 函数名
- [ ] L4 条目标明"有 Fallback"
- [ ] 每行有简短判定理由(决策树分支)
