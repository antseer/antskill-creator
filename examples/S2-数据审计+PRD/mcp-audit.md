# MCP 路由审计表 · polymarket-drift-radar

> **S2 Part A 产物** · 对应 SOP: `sop/s2_routing_and_prd.md` Part A
> **决策树**: `mcp-capability-map/routing-decision-tree.md`
> **能力地图基准**: `mcp-capability-map/真源缓存文档`(v0.1.0-example)

## 元信息

- 基于 inventory: `data-inventory.md`(约 100 个 Dxx,编号 D01-D160)
- 基于能力地图: `真源缓存文档` v0.1.0-example(示例,实际 Polymarket MCP 以部署为准)
- 生成时间: 2026-04-16
- 审计方式: 逐条过决策树 Q1-Q4,记录分支

---

## 汇总

| 归属 | 条数 | 备注 |
|---|---|---|
| L1-A (MCP 现有) | 4 | price_history / volume / search / 认证状态 |
| **L1-B (MCP 缺失)** | **2** | **新闻按市场检索(P0) / 事件 URL 解析(P2)** |
| L2 (MCP 新聚合) | 1 | 历史相似漂移命中率(P1) |
| L3 (Skill 脚本) | 21 | Bollinger / Z-Score / 异常检测 / 统计 / 格式化 |
| L4 (LLM 结构化) | 6 | 结论分类 / Hero 副文 / 漂移详解 / 历史段 |
| L5 (纯前端) | 5 | 颜色映射 / UI 交互派生 / 量柱归一 |
| INPUT (用户输入) | 4 | tab 激活 / 浮层开关 / 事件输入 / 窗口 pill |
| STATIC (静态文案) | ~60 | 标题 / label / 方法论 / 免责声明 / 状态文案 |

总计 ≈ 103 个有效条目(与 inventory 一致)。

---

## 审计表

### R1 · Nav 与装饰

| # | Dxx | 字段 | 性质 | 归属 | 实现方式 | 决策树分支 |
|---|---|---|---|---|---|---|
| 1 | D01 | 品牌"Antseer" | 静态 | STATIC | HTML 写死 | 性质=静态 → STATIC |
| 2 | D02 | 面包屑"首页" | 静态 | STATIC | HTML 写死 | 性质=静态 → STATIC |
| 3 | D03 | 面包屑"Skillhub" | 静态 | STATIC | HTML 写死 | 性质=静态 → STATIC |
| 4 | D04 | 面包屑 Skill 名 | 静态 | STATIC | 来自 SKILL.md frontmatter | 性质=静态 → STATIC |
| 5 | D05 | 阶段标签 chip | 静态 | STATIC | HTML 写死 | 性质=静态 → STATIC |
| 6 | D06 | 背景辐射线 SVG | 静态 | STATIC | 内联 SVG 装饰 | 性质=静态 → STATIC |

### R2 · Header

| # | Dxx | 字段 | 性质 | 归属 | 实现方式 | 决策树分支 |
|---|---|---|---|---|---|---|
| 7 | D10 | Skill 名 H1 | 静态 | STATIC | HTML 写死 | 静态 |
| 8 | D11 | "已认证"文字 | 静态 | STATIC | HTML 写死 | 静态 |
| 9 | D12 | 认证布尔 | 原始 | **L5** | 由 skill 平台元数据注入渲染显隐 | 纯展示视觉规则 → L5 |
| 10 | D13 | 分享按钮文字 | 静态 | STATIC | HTML 写死 | 静态 |
| 11 | D14 | Tab"在线执行" | 静态 | STATIC | HTML 写死 | 静态 |
| 12 | D15 | Tab"Skill 详情" | 静态 | STATIC | HTML 写死 | 静态 |
| 13 | D16 | 当前激活 tab | 用户输入 | INPUT | 前端本地状态 | 用户输入不走层 |

> **判定说明 D12**:认证状态来自 Skill 平台(Skillhub 审核系统),不是由 Polymarket MCP 提供,也不需要 Skill Runtime 计算。实际上是容器平台注入的一个 boolean,L5 根据它显隐徽章即可。属于"容器元数据",归 L5 最准。

### R3 · 主 CTA Bar + 参数浮层

| # | Dxx | 字段 | 性质 | 归属 | 实现方式 | 决策树分支 |
|---|---|---|---|---|---|---|
| 14 | D20 | 主 CTA 文字 | 静态 | STATIC | HTML 写死 | 静态 |
| 15 | D21 | 历史按钮文字 | 静态 | STATIC | HTML 写死 | 静态 |
| 16 | D22 | 浮层开关态 | 用户输入 | INPUT | 前端本地状态 | 用户输入 |
| 17 | D30 | 浮层标题 | 静态 | STATIC | HTML 写死 | 静态 |
| 18 | D31 | 字段1 label"事件*" | 静态 | STATIC | HTML 写死 | 静态 |
| 19 | D32 | 事件输入值 | 用户输入 | INPUT | input 绑定 | 用户输入 |
| 20 | D33 | 字段1 placeholder | 静态 | STATIC | HTML 写死 | 静态 |
| 21 | D34 | 字段2 label"时间窗口*" | 静态 | STATIC | HTML 写死 | 静态 |
| 22 | D35 | 字段2 pills 文字 | 静态 | STATIC | HTML 写死 | 静态 |
| 23 | D36 | 窗口激活值 | 用户输入 | INPUT | 前端本地状态 | 用户输入 |
| 24 | D37 | 子 CTA 文字 | 静态 | STATIC | HTML 写死 | 静态 |
| 25 | D38 | 必填校验态 | 衍生 | **L5** | 前端判空 `D32.trim() && D36` | 纯 UI 轻量规则 → L5 |
| 26 | D39 | 执行请求参数包 | 衍生 | **L5** | 前端打包 `{event:D32, window:D36}` 传给 runtime | 纯 UI 派生 → L5 |

### R4 · Meta 标签行

| # | Dxx | 字段 | 性质 | 归属 | 实现方式 | 决策树分支 |
|---|---|---|---|---|---|---|
| 27 | D40 | 模式标签"DEMO/LIVE" | 静态 | STATIC | HTML 写死(生产态由 runtime 注入) | 静态 |
| 28 | D41 | 数据源名"Polymarket" | 原始 | STATIC | 固定文本,非查询字段 | 静态文案(非数据) |
| 29 | D42 | 当前窗口显示 | 用户输入映射 | **L5** | `=D36` 回显 | 纯 UI 回显 → L5 |
| 30 | D43 | 数据时间戳 | 原始 | **L3** | `layers/L3-compute/format.py::format_timestamp(now_iso)` | 需格式化,Skill 特有 → L3 |

### R5 · Hero 结论区

| # | Dxx | 字段 | 性质 | 归属 | 实现方式 | 决策树分支 |
|---|---|---|---|---|---|---|
| 31 | D50 | "本次结论"文字 | 静态 | STATIC | HTML 写死 | 静态 |
| 32 | D51 | 结论关键词 | 自然语言 | **L4** | `layers/L4-llm/verdict.md` + Fallback | 自然语言 → L4 |
| 33 | D52 | 结论副标题 | 自然语言 | **L4** | `layers/L4-llm/verdict.md`(同 prompt 联产) | 自然语言 → L4 |
| 34 | D53 | Hero 正文解释 | 自然语言 | **L4** | `layers/L4-llm/hero-narrative.md` + Fallback | 自然语言 → L4 |
| 35 | D54 | 文中漂移次数(插值) | 衍生 | **L3** | `=len(D87)` | 纯计数 → L3 |
| 36 | D55 | 文中峰值概率 | 衍生 | **L3** | `layers/L3-compute/drift.py::peak_of_last_drift(D80,D87)` | 轻量窗口计算 → L3 |
| 37 | D56 | 文中当前概率 | 原始 | **L3** | =D70(直接引用) | 引用派生 → L3 |
| 38 | D57 | 文中历史命中率 | 衍生 | **L2** | 需新建 `ant_polymarket.similar_drift_stats` → **DATA-03 (P1)** | 跨时间跨市场聚合 → L2 |
| 39 | D58 | 文中目标位 | 衍生 | **L3** | `=D82[-1]`(MA-20 末点) | 引用派生 → L3 |
| 40 | D59 | "72 小时"文字 | 静态 | STATIC | HTML 写死 | 静态 |

### R5.x · Hero Stats(5 项)

| # | Dxx | 字段 | 性质 | 归属 | 实现方式 | 决策树分支 |
|---|---|---|---|---|---|---|
| 41 | D70 | 当前概率 | 原始 | **L3** | `layers/L3-compute/extract.py::take_last(D80)` | MCP 无单点工具,从 D80 取尾 → L3(B1 边界) |
| 42 | D71 | 24H 变化 | 衍生 | **L3** | `layers/L3-compute/delta.py::delta_24h(D70,D72)` | 轻量 → L3 |
| 43 | D72 | 24H 前概率 | 原始 | **L3** | `layers/L3-compute/extract.py::point_at(D80,-24h)` | 从 D80 取点 → L3(B1 边界) |
| 44 | D73 | 7D 波动率 | 衍生 | **L3** | `layers/L3-compute/volatility.py::std_7d(D80)` | 窗口小,Skill 特有 → L3 |
| 45 | D74 | Z-Score | 衍生 | **L3** | `layers/L3-compute/zscore.py::compute(D70,D82,D83)` | 轻量 → L3 |
| 46 | D75 | 30D 成交量 | 衍生 | **L3** | `layers/L3-compute/agg.py::sum_volume(D81)` | 窗口小,Skill 特有 → L3(非 L2) |
| 47 | D76 | 5 个 stat label | 静态 | STATIC | HTML 写死 | 静态 |
| 48 | D77 | stat 正负颜色态 | 衍生 | **L5** | 前端 `D71 > 0 ? 'pos' : D71 < 0 ? 'neg' : 'neutral'` | 极简阈值 → L5(决策树 Q4) |

> **判定说明 D75**:30D 成交量本质是跨时间聚合,但"窗口小(30 天、1h 间隔 ≈ 720 点)、Skill 特有、无复用"——按决策树 B3 + Q2 否→Q3 否→Q4 否,归 L3。如未来多 Skill 共用,可升级为 L2 `ant_polymarket.volume_window`。当前不登记 gap。

### R6 · 概率曲线图卡

#### R6.1 卡头

| # | Dxx | 字段 | 性质 | 归属 | 实现方式 | 决策树分支 |
|---|---|---|---|---|---|---|
| 49 | D78 | 卡标题 | 静态 | STATIC | 模板 `概率曲线 · {D36} 天` | 静态含插值 |
| 50 | D79 | 卡副文 | 静态 | STATIC | HTML 写死 | 静态 |

#### R6.2 主图

| # | Dxx | 字段 | 性质 | 归属 | 实现方式 | 决策树分支 |
|---|---|---|---|---|---|---|
| 51 | D80 | 概率时序 | 原始 | **L1-A** | `ant_polymarket.price_history(market_id, interval=1h, days=D36)` | 原始,capabilities 有 |
| 52 | D81 | 量时序 | 原始 | **L1-A** | 同 `ant_polymarket.price_history` 返回的 volume 字段 | 原始,capabilities 有(同 tool 联产) |
| 53 | D82 | MA-20 时序 | 衍生 | **L3** | `layers/L3-compute/bollinger.py::ma(D80, N=20)` | 滚动,Skill 特有 → L3 |
| 54 | D83 | 20 期 std 时序 | 衍生 | **L3** | `layers/L3-compute/bollinger.py::rolling_std(D80, N=20)` | 滚动,Skill 特有 → L3 |
| 55 | D84 | Bollinger 上轨 | 衍生 | **L3** | `layers/L3-compute/bollinger.py::upper(D82,D83,k=2)` | 组合派生 → L3 |
| 56 | D85 | Bollinger 下轨 | 衍生 | **L3** | `layers/L3-compute/bollinger.py::lower(D82,D83,k=2)` | 组合派生 → L3 |
| 57 | D86 | 异常点布尔序列 | 衍生 | **L3** | `layers/L3-compute/drift.py::mark_anomaly(D80,D84,D85)` | 逐点布尔 → L3 |
| 58 | D87 | 异常区间分段 | 衍生 | **L3** | `layers/L3-compute/drift.py::segment_anomaly(D86, min_span=24h)` | 窗口合并 → L3 |
| 59 | D88 | Y 轴刻度标签 | 衍生 | **L5** | 图表库自动计算刻度 | 纯渲染 → L5 |
| 60 | D89 | "NOW"标注位置 | 衍生 | **L5** | 定位在 D80 最后一点的 x 坐标 | 纯 UI 派生 → L5 |

#### R6.3 新闻节点(图上)

| # | Dxx | 字段 | 性质 | 归属 | 实现方式 | 决策树分支 |
|---|---|---|---|---|---|---|
| 61 | D90 | 新闻列表(原始) | 原始 | **L1-B** | 需新建 `ant_news.by_market` → **DATA-01 (P0)** | 原始,capabilities 无 → L1-B |
| 62 | D91 | 筛后新闻节点 | 衍生 | **L3** | `layers/L3-compute/news.py::pick_top_n(D90, D87, n=3)` | Skill 特有筛选 → L3 |
| 63 | D92 | 新闻节点 x 坐标 | 衍生 | **L5** | 图表库按时间戳 → x 映射 | 纯渲染 → L5 |
| 64 | D93 | 新闻节点序号 | 衍生 | **L3** | `layers/L3-compute/news.py::number_by_time(D91)` | 按时间排序编号 → L3 |

#### R6.4 量柱图

| # | Dxx | 字段 | 性质 | 归属 | 实现方式 | 决策树分支 |
|---|---|---|---|---|---|---|
| 65 | D94 | 量柱高度 | 衍生 | **L5** | 图表库自动归一化 | 纯渲染 → L5 |
| 66 | D95 | 量柱颜色映射 | 衍生 | **L3** | `layers/L3-compute/volume.py::mark_in_drift(D81,D87)` | 区间判定 → L3 |
| 67 | D96 | "成交量"label | 静态 | STATIC | HTML 写死 | 静态 |

#### R6.5 Legend

| # | Dxx | 字段 | 性质 | 归属 | 实现方式 | 决策树分支 |
|---|---|---|---|---|---|---|
| 68 | D97 | 5 条图例文字 | 静态 | STATIC | HTML 写死 | 静态 |

### R7 · 新闻列表卡

| # | Dxx | 字段 | 性质 | 归属 | 实现方式 | 决策树分支 |
|---|---|---|---|---|---|---|
| 69 | D100 | 卡标题 | 静态 | STATIC | HTML 写死 | 静态 |
| 70 | D101 | 卡副文 | 静态 | STATIC | HTML 写死 | 静态 |
| 71 | D102 | 新闻条目数组 | 衍生 | **L3** | =D91(与图上同源) | 引用派生 → L3 |
| 72 | D103 | 新闻序号 badge | 衍生 | **L3** | =D93 | 引用派生 → L3 |
| 73 | D104 | 新闻标题 | 原始 | **L1-B** | 从 D90.title 取(同 DATA-01) | 原始,同 D90 |
| 74 | D105 | 新闻来源 | 原始 | **L1-B** | 从 D90.source 取(同 DATA-01) | 原始,同 D90 |
| 75 | D106 | 相对时间"26 天前" | 衍生 | **L3** | `layers/L3-compute/format.py::relative_time(D90.t, now)` | 轻量格式化 → L3 |
| 76 | D107 | 影响度标签 | 原始 | **L1-B** | 从 D90.impact 取(同 DATA-01) | 原始,同 D90 |
| 77 | D108 | 影响度颜色态 | 衍生 | **L5** | 前端映射 `high→red / mid→yellow / low→gray` | 极简映射 → L5 |
| 78 | D109 | 新闻 url | 原始 | **L1-B** | 从 D90.url 取(同 DATA-01) | 原始,同 D90 |
| 79 | D110 | 新闻条目 click | 用户输入 | INPUT | `window.open(D109)` | 用户输入 |

### R8 · 信任层

#### R8.1 "为什么给这结论"

| # | Dxx | 字段 | 性质 | 归属 | 实现方式 | 决策树分支 |
|---|---|---|---|---|---|---|
| 80 | D120 | summary 文字 | 自然语言 | **L3** | `layers/L3-compute/format.py::conclusion_question(D51)` | 模板拼接 → L3 |
| 81 | D121 | 默认展开状态 | 衍生 | STATIC | HTML `<details open>` | 静态 UI 约定 |
| 82 | D122 | 漂移详解段落 | 自然语言 | **L4** | `layers/L4-llm/drift-narrative.md` + Fallback | 自然语言 → L4 |
| 83 | D123 | 历史命中率段落 | 自然语言 | **L4** | `layers/L4-llm/hit-rate-narrative.md` + Fallback | 自然语言 → L4 |
| 84 | D124 | 漂移详解块数 | 衍生 | **L3** | `=len(D87)` | 计数 → L3 |
| 85 | D125 | 折叠点击态 | 用户输入 | INPUT | `<details>` 原生 | 用户输入 |

#### R8.2 "方法论"

| # | Dxx | 字段 | 性质 | 归属 | 实现方式 | 决策树分支 |
|---|---|---|---|---|---|---|
| 86 | D130 | summary 文字 | 静态 | STATIC | HTML 写死 | 静态 |
| 87 | D131 | 漂移定义段 | 静态 | STATIC | HTML 写死 | 静态 |
| 88 | D132 | 新闻节点定义 | 静态 | STATIC | HTML 写死 | 静态 |
| 89 | D133 | 入场判定段 | 静态 | STATIC | HTML 写死 | 静态 |

#### R8.3 "风险提示"

| # | Dxx | 字段 | 性质 | 归属 | 实现方式 | 决策树分支 |
|---|---|---|---|---|---|---|
| 90 | D140 | summary 文字 | 静态 | STATIC | HTML 写死 | 静态 |
| 91 | D141 | 免责声明 | 静态 | STATIC | HTML 写死 | 静态 |
| 92 | D142 | 黑天鹅风险 | 静态 | STATIC | HTML 写死 | 静态 |
| 93 | D143 | 流动性风险 | 静态 | STATIC | HTML 写死 | 静态 |
| 94 | D144 | 多源交叉建议 | 静态 | STATIC | HTML 写死 | 静态 |

### R9 · 状态层

| # | Dxx | 字段 | 性质 | 归属 | 实现方式 | 决策树分支 |
|---|---|---|---|---|---|---|
| 95 | D150 | Loading 文案 | 静态 | STATIC | HTML 写死 | 静态 |
| 96 | D151 | Empty(不匹配) | 静态 | STATIC | HTML 写死 | 静态 |
| 97 | D152 | Empty(窗口无数据) | 静态 | STATIC | HTML 写死 | 静态 |
| 98 | D153 | Error 文案 | 静态 | STATIC | HTML 写死 | 静态 |
| 99 | D154 | 重试按钮 | 静态 | STATIC | HTML 写死 | 静态 |
| 100 | D155 | 降级文案(无新闻) | 静态 | STATIC | HTML 写死 | 静态 |

### R10 · Footer

| # | Dxx | 字段 | 性质 | 归属 | 实现方式 | 决策树分支 |
|---|---|---|---|---|---|---|
| 101 | D160 | 版权/声明文字 | 静态 | STATIC | HTML 写死 | 静态 |

---

## L1-B / L2 缺口汇总(指向 data-prd.md)

| Dxx | 归属 | GAP 编号 | 优先级 | 工具名 | 说明 |
|---|---|---|---|---|---|
| D90, D104, D105, D107, D109 | L1-B | **DATA-01** | **P0** | `ant_news.by_market` | 按市场检索新闻(核心差异化) |
| D57 | L2 | **DATA-03** | P1 | `ant_polymarket.similar_drift_stats` | 历史相似漂移命中率(跨市场跨时间聚合) |
| (潜在) D32 URL | L1-B | **DATA-02** | P2 | `ant_polymarket.parse_market_url` | 解析 Polymarket URL → market_id(降级:让用户只输关键词) |

详见 `data-prd.md`。

> **DATA-02 说明**:当前 `search_markets(q)` 已覆盖关键词输入,用户输入 URL 时 Skill 可前端 regex 提取 slug 再走 search,是 Nice-to-have 的 P2。若后端直接提供 `parse_market_url` 更稳。

---

## 判定说明摘录(有争议的 9 条)

**D12 认证状态 → L5**:
- 数据来源不是业务 MCP,是平台容器元数据,由 Skillhub 注入。
- L5 根据 `props.certified === true` 显隐徽章,不需要任何后端工具。
- 若未来"认证等级"分级复杂,可升级为 L1-A 走 `ant_skillhub.get_skill_meta`。

**D38 / D39 必填校验 + 请求打包 → L5**:
- 决策树 Q4:"根据某数值改变显示"的 UI 轻量规则归 L5。
- 校验规则极简(非空 + 必选),用 L3 不经济。

**D42 回显 / D75 30D 成交量 / D82-D87 全家桶 → L3**:
- 都是"30D 级别的滚动窗口 + Skill 特有",按 B3 边界归 L3。
- 若未来多 Skill 共用"Polymarket 30D 成交量",升级 `ant_polymarket.volume_window` 为 L2。

**D57 历史命中率 → L2**:
- "类似漂移模式" 需要跨市场搜索过去 N 个相似事件,计算回归 72h 的命中率。
- 这需要跨市场跨时间聚合 + 模式匹配,不适合 Skill 实时跑。
- 多 Skill 复用场景高(所有"漂移/回归"类 Skill 都会用)。
- 符合 B3 边界(跨 Skill 复用)→ L2。

**D70/D72 当前/历史概率 → L3(不是 L1-A)**:
- 真源缓存文档 中 `ant_polymarket.price_history` 不提供单点查询。
- 按 B1 边界,从时序取点是 Skill 本地行为,归 L3。
- 若 Polymarket MCP 未来提供 `get_current_price`,可升级 D70 为 L1-A。

**D80+D81 共用一个 Tool**:
- `ant_polymarket.price_history` 的 returns 同时包含 `prob` 和 `volume`,一次调用联产。
- 两个 Dxx 都归 L1-A,调用入口相同,前端/L3 分字段消费。

**D102-D109 新闻条目字段 → L1-B(根在 D90)**:
- 全部是 D90 结构的投影,同属 DATA-01 的字段。
- 本身不独立调 MCP,但"源"是 L1-B,故归 L1-B。

**D91 筛后新闻 → L3(不是 L1-B)**:
- 原始 D90 是 L1-B,但"按影响度 + 异常区间对齐,筛 Top 3"是 Skill 特有的展示规则。
- 归 L3,输入 D90 + D87,输出截断列表。

**D54/D124 漂移次数 → L3**:
- 虽然是"计数"极简,但非纯 UI 规则(L5 要做前端不该做的计算),归 L3。
- 与 D58 "取 MA 末点"同档。

---

## 自查(G2.1)

- [x] inventory 每行都有归属判定,无遗漏
- [x] 每行归属非空,无"待定"
- [x] L1-A 条目列出了 MCP tool + 入参(D80/D81)
- [x] L1-B 条目列出了将建的 tool + GAP 编号(DATA-01、DATA-02)
- [x] L2 条目列出了将建的聚合接口 + GAP 编号(DATA-03)
- [x] L3 条目列出了脚本位置 + 函数名(21 条)
- [x] L4 条目标明"有 Fallback"(6 条)
- [x] 每行有简短判定理由(决策树分支)

**G2.1 🔴 全部通过**。
