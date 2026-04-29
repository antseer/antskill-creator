# PRD · polymarket-drift-radar

> **S2 Part B 产物** · 对应 SOP: `sop/s2_routing_and_prd.md` Part B
> **结构**: 按功能模块(M1-M4)组织,每模块完整写 L1-L5 五层。
> **铁律**: 不涉及的层显式声明"本模块不涉及 L?,原因..."。
> **附录 A 是字段 Schema 唯一源**,模块内只引用 Dxx。

---

## 元信息

- Skill 名: `polymarket-drift-radar`
- 版本: 0.1.0(半成品 PM 交付)
- 范式: B 规范型
- 对应需求画布: `requirement-canvas.md`
- 对应审计: `mcp-audit.md`
- 对应 gap: `data-prd.md`
- 生成时间: 2026-04-16

---

## §0 概览

### 一句话定位

> 任意 Polymarket 事件的**概率漂移追踪图**——在概率曲线上叠加**新闻节点**标注 + **异常区间**标红,回答"这天价格为什么跳" + "现在是不是回归入场窗口"。

### 用户与场景

- **WHO**: Polymarket 新手交易者,有基本交易思维但不想学 Z-Score/Bollinger 这些术语,"看方向就行"。
- **WHEN**: 盯上某事件后,打开 → 看一次 → 关。一次性查询,非监控工具。
- **WHY 好于替代方案**:
  - Polymarket 自带图:有曲线无新闻标注、无异常检测
  - ElectionBettingOdds:只做选举品类
  - Metaculus:学术向无交易视角
  - 本 Skill 唯一同时覆盖:任意市场 + 新闻层 + 异常标红 + 均值回归建议

### 模块索引

| 模块 | 名称 | 核心价值 | 主要 Dxx |
|---|---|---|---|
| **M1** | 市场识别 | 用户输入关键词/URL,快速定位目标 Polymarket 市场 | D32/D36/D38/D39 |
| **M2** | 漂移分析 | 概率曲线 + Bollinger + 异常区间 + 新闻节点叠加 | D80/D84/D87/D90 |
| **M3** | 解读与建议 | 把 M2 数字翻译成"回归入场 / 观望 / 继续偏离"的白话结论 | D51/D53/D122 |
| **M4** | 信任层 | 方法论透明度、漂移详解、历史命中率、风险对称 | D122/D123/D131 |

### Hero 公式

> **"{结论关键词(橙高亮)}:{副标题}"** + 5 项 stats + 正文 2-3 句

由 L4 `hero-narrative.md` 产出,Fallback 按 `risk_level` 模板化。

---

## §1 模块 M1 · 市场识别

### 1.1 用户故事

用户输入 Polymarket 链接或关键词(如"Trump 2024"),并选择时间窗口(7D/30D),点击"执行 Skill"后系统识别到具体市场,准备分析。

### 1.2 成功指标

- 从输入到命中市场 < 1s(P95)
- 链接输入 100% 正确解析(通过 search 兜底)
- 关键词无匹配时清晰告知

### 1.3 L1 · 数据接入层

#### L1-A · MCP 现有可用

| Dxx | 字段 | MCP Tool | 入参 | 出参 Schema |
|---|---|---|---|---|
| (辅) — | 市场搜索 | `ant_polymarket.search_markets` | `q: string, limit: 10` | 见附录 A · `SearchResult[]` |

> 本模块不存储 search 结果到 Dxx(只用其 `market_id` 作为 M2 的入参),故不单列 Dxx。

#### L1-B · MCP 缺失待补齐

| Dxx | 字段 | GAP 编号 | 优先级 | 期望工具 |
|---|---|---|---|---|
| (辅) — | URL 直接解析 | **DATA-02** | P2 | `ant_polymarket.parse_market_url` |

**降级**:前端用 regex 提取 slug 再走 search_markets,用户无感。详见 `data-prd.md` DATA-02。

### 1.4 L2 · MCP 新建聚合接口

**本模块不涉及 L2**,原因:M1 只做单次搜索,不涉及跨时间/跨实体聚合。

### 1.5 L3 · Skill 脚本计算

| Dxx | 字段 | 脚本位置 | 输入 | 输出 | 逻辑 |
|---|---|---|---|---|---|
| (辅) — | URL → market_id | `layers/L3-compute/parse.py::url_to_market_id` | `input: string` | `market_id: string \| null` | 正则检测是否为 URL,提取 slug,走 search 兜底。若非 URL 直接作为 `q` 走 search |

### 1.6 L4 · LLM 结构化层

**本模块不涉及 L4**,原因:M1 返回结构化市场列表,无自然语言加工需求。

### 1.7 L5 · 前端展示层

| 组件 | 位置 | 消费字段 | 交互 |
|---|---|---|---|
| 主 CTA「执行 Skill」按钮 | 顶部 Bar | D20(静态) | click → 弹出参数浮层 D22=true |
| 参数浮层 Popover | CTA 下方 | D30-D37 | ESC / 外部点击关闭;子 CTA 提交触发 Skill 运行 |
| 事件输入框 | 浮层字段 1 | D32 + D33 placeholder | input 绑定 |
| 时间窗口 pills | 浮层字段 2 | D35 选项 + D36 激活值 | click 切换 |
| 校验态 | 子 CTA 按钮 | D38 | D38=false 时按钮禁用 |
| 请求参数包 | 提交时 | D39 | 触发 `runtime.execute({ event, window })` |
| Empty(不匹配) | 输出区 | D151 | 显示"未找到匹配的 Polymarket 市场,请尝试其他关键词" |

---

## §2 模块 M2 · 漂移分析

### 2.1 用户故事

市场识别后,在 3 秒内看到:过去 7D/30D 的概率曲线 + Bollinger 上下轨 + 异常区间标红 + 关键新闻节点 + 成交量柱图,一眼判断"是否处于异常漂移后的回归窗口"。

### 2.2 成功指标

- 首屏 Hero 3 秒内渲染(不等 L4 LLM)
- 统计卡数值与曲线数据严格一致(同源)
- 异常区间标红与新闻节点视觉对齐

### 2.3 L1 · 数据接入层

#### L1-A · MCP 现有可用

| Dxx | 字段 | MCP Tool | 入参 | 出参 Schema |
|---|---|---|---|---|
| D80 | 概率时序 | `ant_polymarket.price_history` | `market_id: string, interval: '1h', days: D36 ∈ {7,30}` | 见附录 A · D80 |
| D81 | 量时序 | 同上(同 tool 联产) | 同上 | 见附录 A · D81 |

> 注:D80/D81 是同一次 `price_history` 调用返回的两个字段(`prob` + `volume`),不重复调用。

#### L1-B · MCP 缺失待补齐

| Dxx | 字段 | GAP 编号 | 优先级 | 期望工具 |
|---|---|---|---|---|
| D90(根)D104/D105/D107/D109(衍生字段) | 按市场的新闻 | **DATA-01** | **P0** | `ant_news.by_market` |

详见 `data-prd.md` DATA-01。**这是本 Skill 核心差异化功能的关键缺口。**

### 2.4 L2 · MCP 新建聚合接口

**本模块不涉及 L2**,原因:本模块所有派生(MA-20 / Bollinger / Z-Score / 异常标记 / 量柱映射)都是窗口 ≤ 30D 的滚动计算,Skill 特有,归 L3 即可。

### 2.5 L3 · Skill 脚本计算

| Dxx | 字段 | 脚本位置 · 函数 | 输入 | 输出 | 逻辑 |
|---|---|---|---|---|---|
| D70 | 当前概率 | `layers/L3-compute/extract.py::take_last` | D80 | number | `D80[-1].prob` |
| D72 | 24H 前概率 | `layers/L3-compute/extract.py::point_at` | D80, `-24h` | number | 二分找 `t ≤ now - 24h` 的最近点 |
| D71 | 24H 变化 | `layers/L3-compute/delta.py::delta` | D70, D72 | number(pp) | `(D70 - D72) * 100` |
| D73 | 7D 波动率 | `layers/L3-compute/volatility.py::std_window` | D80, 7d | number | `std(prob where t ≥ now-7d) * 100` |
| D82 | MA-20 时序 | `layers/L3-compute/bollinger.py::rolling_ma` | D80, N=20 | 见附录 A · D82 | 滚动均值 |
| D83 | 20σ 时序 | `layers/L3-compute/bollinger.py::rolling_std` | D80, N=20 | 见附录 A · D83 | 滚动标准差 |
| D84 | Bollinger 上轨 | `layers/L3-compute/bollinger.py::band` | D82, D83, k=+2 | 见附录 A · D84 | `ma + 2*std` |
| D85 | Bollinger 下轨 | `layers/L3-compute/bollinger.py::band` | D82, D83, k=-2 | 见附录 A · D85 | `ma - 2*std` |
| D74 | Z-Score | `layers/L3-compute/zscore.py::compute` | D70, D82[-1], D83[-1] | number | `(D70 - ma) / std` |
| D75 | 30D 成交量 | `layers/L3-compute/agg.py::sum_volume` | D81 | number | `sum(vol)` |
| D86 | 异常点布尔 | `layers/L3-compute/drift.py::mark_anomaly` | D80, D84, D85 | bool[] | 逐点 `prob > upper \|\| prob < lower` |
| D87 | 异常区间分段 | `layers/L3-compute/drift.py::segment_anomaly` | D86, min_span=24h | 见附录 A · D87 | 连续 true 合并,滤除 < 24h 的噪音 |
| D54 | 漂移次数 | `layers/L3-compute/drift.py::count_segments` | D87 | int | `len(D87)` |
| D55 | 最近一次漂移峰值 | `layers/L3-compute/drift.py::peak_of_last` | D80, D87 | number | 最后一段区间内的 max/min |
| D58 | 目标回归位 | `layers/L3-compute/extract.py::take_last` | D82 | number | `D82[-1]` |
| D91 | 筛后新闻(Top N) | `layers/L3-compute/news.py::pick_top_n` | D90, D87, n=3 | 见附录 A · D91 | 优先对齐 D87 区间 + 按 impact 排序 |
| D93 | 新闻序号编号 | `layers/L3-compute/news.py::number_by_time` | D91 | int[] | 按 t 升序编号 1..N |
| D95 | 量柱落在异常区间 | `layers/L3-compute/volume.py::mark_in_drift` | D81, D87 | bool[] | 每个 bar 的 t 是否落在某 D87 区间 |
| D43 | 数据时间戳(格式化) | `layers/L3-compute/format.py::format_timestamp` | `now_iso` | string | `"YYYY/M/D"` |
| D106 | 新闻相对时间 | `layers/L3-compute/format.py::relative_time` | `t, now` | string | `"N 天前" / "N 小时前"` |
| D120 | 折叠块 summary | `layers/L3-compute/format.py::conclusion_question` | D51 | string | `"为什么给出'{D51}'的结论?"` |
| D102 | 右卡新闻列表 | (引用) | =D91 | — | 与图上同源 |
| D103 | 右卡新闻序号 | (引用) | =D93 | — | 与图上同序 |
| D56 | 文中当前概率 | (引用) | =D70 | — | — |
| D124 | 漂移详解块数 | (引用) | =D54 | — | — |

### 2.6 L4 · LLM 结构化层

**本模块不涉及 L4**,原因:M2 只产结构化数值和布尔。所有自然语言解读集中在 M3 / M4,避免同一信息两处生成导致不一致。

### 2.7 L5 · 前端展示层

| 组件 | 位置 | 消费字段 | 交互 |
|---|---|---|---|
| Meta 标签行 | 输出区顶部 | D40/D41/D42(=D36)/D43 | 静态展示 |
| Hero Stats 5 项卡 | Hero 区 | D70/D71/D73/D74/D75 + D76 label | hover 显示公式 tooltip |
| 统计卡正负色 | 同上 | D77 ← D71 符号 | 纯视觉映射 |
| 概率主曲线 | 图卡主区 | D80 | hover 显示当前点 t/prob |
| Bollinger 带虚线 | 图卡主区 | D82/D84/D85 | — |
| 异常区间红色覆盖 | 图卡主区 | D87 | hover 显示区间内 max/min + 持续时长 |
| 新闻节点竖线 + 编号圈 | 图卡主区 | D91/D92/D93 | click → 跳转 D109 外链 |
| NOW 当前点标注 | 图卡主区 | D70 + D89 坐标 | — |
| 量柱图 | 图卡下方 | D81 + D94(归一) | — |
| 量柱异常色 | 同上 | D95 | 纯视觉映射 |
| Legend | 图卡底部 | D97 | — |
| Y 轴刻度 | 图卡左侧 | D88 | 图表库自动生成 |
| Loading 态 | 覆盖图卡 | D150 | 5-15s 超时切 Error |
| Empty 态(窗口无数据) | 覆盖图卡 | D152 | — |
| Error 态 | 覆盖图卡 | D153 + D154 重试 | click 重试 → 重新 execute |
| 部分降级态(DATA-01 未实现) | 新闻列表卡位 | D155 | 保留概率曲线,隐藏新闻层 |

---

## §3 模块 M3 · 解读与建议

### 3.1 用户故事

看到 M2 的数字后,用户希望得到一句话白话结论("回归入场窗口"/"观望"/"继续偏离")+ Hero 正文 2-3 句把数字翻译成可操作建议 + 随手能看到风险提示。

### 3.2 成功指标

- 新手 3 秒内能复述核心结论
- 结论关键词与 stats 数字一致(无互相矛盾)
- L4 超时/失败时 Fallback 输出与正常输出同 schema

### 3.3 L1 · 数据接入层

**本模块不涉及 L1**,原因:M3 消费 M2 + (若有)DATA-03 的数据,不直接调 MCP。

### 3.4 L2 · MCP 新建聚合接口

| Dxx | 字段 | GAP 编号 | 优先级 | 期望工具 |
|---|---|---|---|---|
| (辅) similar_stats → D57 | 历史相似漂移命中率 | **DATA-03** | P1 | `ant_polymarket.similar_drift_stats` |

详见 `data-prd.md` DATA-03。降级:L4 Fallback 生成不含具体数字的版本。

### 3.5 L3 · Skill 脚本计算

**本模块不涉及 L3**,原因:M3 直接把 M2 的数值和 DATA-03 结果喂给 L4。插值数字(D54/D55/D58)虽出现在 Hero 文本中,但来自 M2 的 L3 输出。

### 3.6 L4 · LLM 结构化层

| Dxx | 字段 | prompt 位置 | 输入 Schema | 输出 Schema | Fallback |
|---|---|---|---|---|---|
| D51 | 结论关键词 | `layers/L4-llm/verdict.md` | `{D70, D74, D73, D87_len, trend_direction}` | `{verdict: '回归入场窗口' \| '观望' \| '继续偏离', risk_level: 'low'\|'mid'\|'high'}` | 按 Z 阈值硬映射:`abs(D74)<0.5→观望,D74∈(0.5,2)同向→继续偏离,D74>2 且在回落→回归入场窗口` |
| D52 | 结论副标题 | 同 `verdict.md` 联产 | 同上 | `{subtitle: string(≤30 字)}` | 按 verdict 查模板库 |
| D53 | Hero 正文(2-3 句) | `layers/L4-llm/hero-narrative.md` | `{D54, D55, D56, D57?, D58, D74, D73, news_summary?}` | `{narrative: string}` 含 `{D54},{D55},{D56},{D57},{D58}` 插值锚点 | 模板化:根据 risk_level 选 3 套固定句式模板,插值填充 |
| D57 | 历史命中率(插值用) | 来自 DATA-03 的 `return_to_ma_rate_72h` | DATA-03 out | number | 若 DATA-03 缺失,Fallback 模板走"不含具体数字"版本 |

#### Fallback 模板详细说明

**`verdict.md` Fallback 规则**:

```
if abs(D74) < 0.5:
  return {verdict:'观望', risk_level:'low', subtitle:'概率处于正常区间,无特殊操作机会'}
if D74 >= 2 and trend=='falling':  # 漂移后回落
  return {verdict:'回归入场窗口', risk_level:'mid', subtitle:'当前概率正从新闻脉冲峰值回落'}
if D74 <= -2 and trend=='rising':
  return {verdict:'回归入场窗口', risk_level:'mid', subtitle:'当前概率正从异常低点回升'}
if abs(D74) >= 2 and trend=='continuing':
  return {verdict:'继续偏离', risk_level:'high', subtitle:'价格仍在偏离均线方向扩大'}
else:
  return {verdict:'观望', risk_level:'low', subtitle:'当前无明确机会信号'}
```

**`hero-narrative.md` Fallback 模板**(risk_level 三档 × 有无 DATA-03):

- `mid + 有 D57`:`"过去 {window} 天出现 {D54} 次显著漂移,最近一次峰值概率 {D55}%。当前 {D56}%,历史上类似模式 72h 回归命中率 {D57}%,目标回归位 {D58}% 附近。"`
- `mid + 无 D57`:`"过去 {window} 天出现 {D54} 次显著漂移,最近一次峰值概率 {D55}%。当前 {D56}%,历史上类似模式通常在 72h 内回归,目标位约在 {D58}%。"`
- `low`:`"过去 {window} 天无明显漂移,当前概率 {D56}% 处于正常波动区间。"`
- `high`:`"过去 {window} 天出现 {D54} 次显著漂移,当前 {D56}% 仍在偏离方向扩大,建议观望至形态明朗。"`

### 3.7 L5 · 前端展示层

| 组件 | 位置 | 消费字段 | 交互 |
|---|---|---|---|
| Hero 结论关键词(橙高亮) | Hero 区左上 | D51 | — |
| Hero 结论副标题 | 关键词下 | D52 | — |
| Hero 正文段落 | Hero 正文区 | D53(含插值) | — |
| Hero 标签「本次结论」 | 最顶 | D50 | — |

---

## §4 模块 M4 · 信任层

### 4.1 用户故事

Hero 只给结论,但用户想"打开看看凭什么这么说"——每次漂移的叙述、方法论、历史命中率段落、风险提示。

### 4.2 成功指标

- 3 个折叠块分别覆盖"为什么/怎么算/有何风险"
- 默认只展开第一个,避免信息轰炸
- 风险提示永远存在(铁律:有推荐必有风险)

### 4.3 L1 · 数据接入层

**本模块不涉及 L1**,原因:M4 消费 M2/M3 + DATA-03 的数据,不直接调 MCP。

### 4.4 L2 · MCP 新建聚合接口

(复用 M3 的 DATA-03,不重复登记)

### 4.5 L3 · Skill 脚本计算

本模块不涉及新增 L3(D120 / D124 在 M2 已列)。

### 4.6 L4 · LLM 结构化层

| Dxx | 字段 | prompt 位置 | 输入 Schema | 输出 Schema | Fallback |
|---|---|---|---|---|---|
| D122 | 漂移详解段落 | `layers/L4-llm/drift-narrative.md` | `{drifts: D87, news: D91, prices: D80_window_slices}` | `{sections: [{drift_index, text}]}` | 模板化:对每个 D87 区间生成固定句式 `"第 {i} 次漂移(t→t):概率从 X% 跳至 Y%,{若有对应新闻 then '对应 {title} 新闻' else '无明确新闻关联'}"` |
| D123 | 历史命中率段落 | `layers/L4-llm/hit-rate-narrative.md` | `{D57, D54, D58, similar_stats 全量: DATA-03}` | `{text: string}` | Fallback 无 DATA-03 时输出:`"历史上类似模式的回归统计暂未接入,但本 Skill 的方法论基于 Bollinger 2σ,经典实战中该信号的均值回归概率通常高于 50%。"` |

### 4.7 L5 · 前端展示层

| 组件 | 位置 | 消费字段 | 交互 |
|---|---|---|---|
| 右侧新闻列表卡标题 | 顶 | D100/D101 | — |
| 新闻条目 × N | 列表 | D102(=D91) | click 条目 → D110 跳 D109 外链 |
| 新闻条目序号 badge | 每条左侧 | D103(=D93) | — |
| 新闻标题 | 每条主文 | D104 | — |
| 新闻来源 + 相对时间 | 每条副文 | D105 + D106 | — |
| 影响度 chip | 每条右侧 | D107 | — |
| chip 颜色 | 同上 | D108 ← D107 | 视觉映射 |
| 折叠块 1「为什么给这结论」 | 信任层顶 | D120 summary + D122 + D123 | click 展开/收起(默认展开) |
| 折叠块 2「方法论」 | 信任层中 | D130/D131/D132/D133 | click 展开(默认收起) |
| 折叠块 3「风险提示」 | 信任层底 | D140/D141/D142/D143/D144 | click 展开(默认收起) |
| Footer | 页底 | D160 | — |

---

## §5 铁律自查(PRD 级)

| 铁律 | 落地位置 |
|---|---|
| Hero 有结论 | D51 + D52 + D53(L4)/ Fallback 硬映射 |
| 有推荐必有风险 | M4 折叠块 3(D140-D144 永远存在) |
| 无一键下单 | 整个 PRD 无"下单"动作,CTA 只是"执行分析" |
| 半成品边界 | DATA-01 P0 明确声明,前端有降级文案 D155 |
| 新手友好 | Hero 用"回归入场窗口"而非"Z-Score +1.2σ",术语藏在 M4 折叠块 |

---

## 附录 A · 字段 Schema(唯一源)

> 所有 Dxx 的权威 Schema。模块内只引用 Dxx。

### SearchResult(M1 辅助,不存 Dxx)

```typescript
type SearchResult = {
  market_id: string;
  title: string;
  current_prob: number;      // 0-1
  volume_24h: number;
  status: 'open' | 'closed' | 'resolved';
};
```

### D32 · 事件输入

```typescript
type D32 = string;  // Polymarket URL 或关键词
```

### D36 · 时间窗口

```typescript
type D36 = '7D' | '30D';
```

### D39 · 执行请求参数

```typescript
type D39 = {
  event: string;   // =D32
  window: '7D' | '30D';  // =D36
};
```

### D70 · 当前概率

```typescript
type D70 = number;  // 0-1
```

### D71 · 24H 变化(pp)

```typescript
type D71 = number;  // 百分点(已 ×100)
```

### D73 · 7D 波动率(%)

```typescript
type D73 = number;  // 0-100
```

### D74 · Z-Score

```typescript
type D74 = number;  // σ 倍数
```

### D75 · 30D 成交量

```typescript
type D75 = number;  // USD
```

### D80 · 概率时序

```typescript
type D80 = Array<{
  t: string;      // ISO 8601
  prob: number;   // 0-1
}>;
```

### D81 · 量时序

```typescript
type D81 = Array<{
  t: string;      // ISO 8601
  volume: number; // USD,单时段
}>;
```

### D82 · MA-20 时序

```typescript
type D82 = Array<{
  t: string;
  ma: number | null;  // 前 N-1 个点返回 null
}>;
```

### D83 · 20σ 时序

```typescript
type D83 = Array<{
  t: string;
  std: number | null;
}>;
```

### D84 · Bollinger 上轨

```typescript
type D84 = Array<{
  t: string;
  upper: number | null;
}>;
```

### D85 · Bollinger 下轨

```typescript
type D85 = Array<{
  t: string;
  lower: number | null;
}>;
```

### D86 · 异常点布尔

```typescript
type D86 = boolean[];  // 长度同 D80
```

### D87 · 异常区间分段

```typescript
type D87 = Array<{
  start_t: string;     // ISO
  end_t: string;       // ISO
  direction: 'up' | 'down';
  peak_prob: number;   // 区间内极值
  duration_h: number;  // 持续小时数
}>;
```

### D90 · 新闻(原始,L1-B)

```typescript
type D90 = Array<{
  t: string;
  title: string;
  source: string;
  url: string;
  impact: 'high' | 'mid' | 'low';
  summary?: string;
  category?: string;
}>;
```

### D91 · 筛后新闻(L3,Top N)

```typescript
type D91 = D90;  // 同结构,长度 ≤ 3
```

### D51 · 结论关键词(L4 输出)

```typescript
type D51 = {
  verdict: '回归入场窗口' | '观望' | '继续偏离';
  risk_level: 'low' | 'mid' | 'high';
};
```

### D52 · 副标题(L4 输出)

```typescript
type D52 = {
  subtitle: string;  // ≤ 30 字
};
```

### D53 · Hero 正文(L4 输出)

```typescript
type D53 = {
  narrative: string;  // 2-3 句,含插值锚点
};
```

### D122 · 漂移详解(L4 输出)

```typescript
type D122 = {
  sections: Array<{
    drift_index: number;
    text: string;
  }>;
};
```

### D123 · 历史命中率段(L4 输出)

```typescript
type D123 = {
  text: string;
};
```

### DATA-01 输出(D90 的来源)

```typescript
// 见 D90
```

### DATA-03 输出(D57 的来源)

```typescript
type SimilarDriftStats = {
  sample_size: number;
  return_to_ma_rate_24h: number;
  return_to_ma_rate_72h: number;   // ← D57 取此字段
  return_to_ma_rate_7d: number;
  median_days_to_return: number;
  confidence_interval_72h: [number, number];
};
```

### 其他 Dxx(引用型 / 静态型)

- **D12 认证状态**: `boolean`,来自平台元数据
- **D38 校验态**: `boolean`,前端计算
- **D42 / D56 / D58 / D102 / D103 / D124 / D120**: 引用其他 Dxx,无独立 schema
- **STATIC 类(约 60 个)**: 纯文字,写入 HTML,不定义 schema

---

## 附录 B · 降级策略

### B.1 L4 Fallback 汇总

| L4 字段 | LLM 失败/超时时的 Fallback 产出 |
|---|---|
| D51(verdict + risk_level) | 按 Z-Score 阈值硬映射,见 §3.6 Fallback 规则 |
| D52(subtitle) | 按 verdict 查 12 条模板库 |
| D53(narrative) | 按 risk_level × (有无 D57)4 套固定模板,插值 Dxx |
| D122(drift-narrative) | 对每个 D87 段生成"第 i 次漂移(t→t):概率从 X% 跳至 Y%,{有新闻 then 对应 X 新闻 else 无明确关联}" |
| D123(hit-rate-narrative) | 无 DATA-03 时输出通用版("历史上类似模式通常在 72h 内回归") |

**所有 L4 Fallback 函数必须和 LLM 正常输出 schema 一致(含所有字段,无 null)**。

### B.2 L1-B / L2 缺失时的前端降级

| GAP | 缺失时的表现 |
|---|---|
| **DATA-01** 未实现 | 概率曲线保留,图上无新闻竖线,右侧新闻列表卡替换为 D155 降级文案"新闻源暂不可用,仅展示概率",Hero D53 走"无 news_summary"分支 |
| **DATA-03** 未实现 | Hero D53 走"无 D57"模板,信任层 D123 走无数字版本,其余一切正常 |
| **DATA-02** 未实现 | 前端 regex 兜底提取 slug,用户无感 |

### B.3 数据状态降级

| 情况 | 展示 |
|---|---|
| D80 空 | 显示 D152("所选时间窗口内该市场无数据") |
| D80 长度 < 20(无法算 Bollinger) | 曲线展示原始概率,隐藏 Bollinger 带 + 异常区间,Hero 走 "low risk + 数据不足" 文案 |
| 搜索无结果 | 显示 D151("未找到匹配的 Polymarket 市场,请尝试其他关键词") |
| price_history 超时 / 500 | 显示 D153 + D154 重试按钮 |

---

## 附录 C · 测试用例

### C.1 L3 脚本单测

| 脚本 | 单测 | 覆盖场景 |
|---|---|---|
| `bollinger.py` | `tests/test_bollinger.py` | ① 正常 720 点 30D 窗口 ② 前 19 点 ma/std 返回 null ③ 全部相同值(std=0) ④ 含 NaN 跳过 |
| `drift.py` | `tests/test_drift.py` | ① 正常上穿 2σ ② 下穿 2σ ③ 持续 < 24h 的毛刺应过滤 ④ 连续 3 段紧挨的合并 |
| `volatility.py` | `tests/test_volatility.py` | 正常 / 单点 / 全相同值 |
| `delta.py` | `tests/test_delta.py` | 正常 / 24h 前数据缺失返回 null |
| `zscore.py` | `tests/test_zscore.py` | std=0 时返回 0 |
| `news.py` | `tests/test_news.py` | D87 空时退化为"按 impact 取 top 3" |
| `format.py` | `tests/test_format.py` | 相对时间边界("刚刚"/"N 小时前"/"N 天前") |

### C.2 L4 prompt eval

| Prompt | Eval 集 | 评估维度 |
|---|---|---|
| `verdict` | 10 组典型案例(每类 3-4 组) | JSON 合法性 / verdict ∈ 枚举 / 与 Z-Score 趋势不冲突 |
| `hero-narrative` | 10 组 | 字数 ≤ 80 / 插值锚点填充正确 / 句式连贯 |
| `drift-narrative` | 10 组 | 每段 JSON 合法 / 段数与 D87 长度一致 |
| `hit-rate-narrative` | 5 组(有 D57 / 无 D57 各半) | 无数字版不编造数字 |

### C.3 端到端

- **Happy path**: 输入"Trump 2024" + 30D → 3s 内 Hero 有结论 + 曲线 + 新闻
- **降级 1**: 模拟 DATA-01 未实现 → 曲线完整,无新闻层,Hero 正文不提及新闻
- **降级 2**: 模拟 L4 LLM 超时 → Fallback 输出合法 schema
- **Empty**: 输入"afjklsdfjkl" → 显示 D151
- **无数据**: 输入正常但 price_history 返空 → 显示 D152
- **Error**: 模拟后端 500 → 显示 D153 + 重试

---

## 附录 D · Design Tokens 引用

### 色彩

- **primary**(全局共用,Antseer 绿 `#36dd0c`):
  - 主 CTA「执行 Skill」按钮
  - 「已认证」徽章
  - 激活 tab「在线执行」
  - focus ring
  - NOW 当前点
  - 正常量柱
- **accent**(本 Skill 差异化,熔岩橙 `#ee6c4d`,已登记 `visual-registry.md`):
  - Hero 结论关键词「回归入场窗口」
  - 概率曲线主线
  - 新闻节点圆圈 + 编号
- **danger** `#f44`:异常区间半透明覆盖 + 异常量柱
- **warning** `#ffb000`:Bollinger 带虚线
- **success** `#05df72`:24H 变化正值(不改)
- **Display 字体**:Libre Baskerville(本 Skill 登记,用于 Hero 和一级大字)
- **Hero 类型**:趋势折线 + 摘要

### 间距 / 圆角 / 字重

引用 `design-system/antseer-design-system.md` § 1 scale,不允许自定义。

---

## §6 G2 自查

| 项 | 状态 | 证据 |
|---|---|---|
| G2.1 inventory 每行都有归属 | ✅ | mcp-audit.md 覆盖 D01-D160 |
| G2.2 L1-B/L2 都汇总到 data gap | ✅ | DATA-01(P0) DATA-02(P2) DATA-03(P1) |
| G2.2 每条 data gap 有期望接口形态 + 降级 + 优先级 | ✅ | mcp-data-prd.md |
| G2.3 PRD 按模块 × L1-L5 五层 | ✅ | M1-M4,每模块 5 层全列 |
| G2.3 不涉及的层显式声明 | ✅ | 如 M1 L2/L4、M2 L4、M3 L1/L3、M4 L1 |
| G2.3 附录 A 字段 Schema 唯一源 | ✅ | 模块内只引 Dxx |
| G2.3 附录 B/C/D 齐 | ✅ | 降级 / 测试 / Tokens |
| G2.4 L4 Fallback 全部写明 | ✅ | 附录 B.1,覆盖 D51/D52/D53/D122/D123 |
| G2.5 L5 字段能追溯上游 | ✅ | 每个 L5 组件有消费字段 Dxx |
| G2.5 无悬空依赖/循环 | ✅ | 依赖链树形 |
| G2.6 无"塞 L3 掩盖"| ✅ | DATA-01/03 都登记在 data-prd.md,不掩盖 |
| G2.7 铁律:Hero 结论/风险对称/无一键下单 | ✅ | §5 自查 |

**G2 全部 🔴 通过**。可进 S3。
