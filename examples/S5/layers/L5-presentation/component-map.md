# L5 · 前端组件 ↔ 上游数据映射

> 每行一个组件,覆盖 `frontend/index.html` 所有带 `data-binding` 的元素 + 5 个状态块。
> 消费字段列出的 Dxx 均应在 `skill-prd.md` 附录 A / `mcp-audit.md` 出现;不得出现 inventory 之外的伪造字段。

## R1 · Nav 与 Header

| 组件 | 位置 | 消费字段 | 来源层 | 交互行为 |
|---|---|---|---|---|
| 品牌点 + Antseer 文字 | 顶 Nav 左 | D01 + D02 | STATIC | — |
| 面包屑(首页 / Skillhub / Skill 名)| Nav 中 | D03 + D04 + D05 | STATIC(D05 来自 SKILL.md frontmatter) | — |
| demo 阶段 chip | Nav 右(半成品) | D06 | STATIC(交付前清理) | — |
| H1 Skill 名 | Header 顶 | D10 | STATIC | — |
| 已认证徽章 | H1 右 | D11 + D12 | STATIC 文案 + **L5**(D12 由平台元数据注入显隐) | — |
| 分享按钮 | H1 右 | D13 | STATIC | click(当前 noop) |
| Tab 导航(在线执行 / 详情) | Header 底 | D14 + D15 + D16 | STATIC + INPUT(D16) | click 切换 active |

## R2 · 主 CTA + 参数浮层

| 组件 | 位置 | 消费字段 | 来源层 | 交互行为 |
|---|---|---|---|---|
| 「执行 Skill」主 CTA | 顶 CTA Bar 左 | D20 | STATIC | click → 切换 D22(浮层开关) |
| 「历史」次 CTA | CTA Bar 右 | D21 | STATIC | click(当前 noop) |
| 浮层标题 | 浮层 | D30 | STATIC | — |
| 事件输入框 | 浮层字段 1 | D31(label)+ D32(值)+ D33(placeholder)| STATIC + INPUT | input 绑定 D32 |
| 时间窗口 pills | 浮层字段 2 | D34(label)+ D35(选项)+ D36(激活)| STATIC + INPUT | click 切换 D36 |
| 浮层子 CTA | 浮层底部 | D37(文案)+ D38(校验)+ D39(请求包)| STATIC + L5 | click → `runtime.execute(D39)`,切 Loading |

## R3 · Meta / Hero

| 组件 | 位置 | 消费字段 | 来源层 | 交互行为 |
|---|---|---|---|---|
| Meta chip - DEMO 标识 | 输出区顶 | D40 | STATIC | — |
| Meta chip - Polymarket 源 | 输出区顶 | D41 | STATIC | — |
| Meta chip - 窗口回显 | 输出区顶 | D42(=D36)| INPUT 派生 | — |
| Meta chip - 日期戳 | 输出区顶 | D43 | **L3** (`format.py::format_timestamp`) | — |
| Hero 标签「本次结论」 | Hero 顶 | D50 | STATIC | — |
| Hero 结论关键词(橙高亮)| Hero 中 | D51 | **L4** (`verdict.md`) | — |
| Hero 副标题 | Hero 中 | D52 | **L4** (`verdict.md` 联产) | — |
| Hero 正文段落 | Hero 中 | D53(+ 插值 D54/D55/D56/D57?/D58)| **L4** (`hero-narrative.md`) | — |

## R4 · Hero Stats 5 项卡

| 组件 | 位置 | 消费字段 | 来源层 | 交互行为 |
|---|---|---|---|---|
| 当前概率卡 | Hero 底 | D70 + D76(label)| **L3** (`extract.py::take_last`) | hover 显示公式 tooltip |
| 24H 变化卡 | Hero 底 | D71 + D77(正负色) | **L3** (`delta.py`) | hover 显示公式 tooltip |
| 7D 波动率卡 | Hero 底 | D73 | **L3** (`volatility.py`) | hover 显示公式 tooltip |
| Z-Score 卡 | Hero 底 | D74 | **L3** (`zscore.py`) | hover 显示公式 tooltip |
| 30D 成交量卡 | Hero 底 | D75 | **L3** (`agg.py::sum_volume`) | hover 显示公式 tooltip |

## R5 · 图表(概率曲线 + 量柱)

| 组件 | 位置 | 消费字段 | 来源层 | 交互行为 |
|---|---|---|---|---|
| 图卡标题 + 窗口 | 图卡顶 | D78 + D79 | STATIC + INPUT 派生 | — |
| Y 轴刻度 | 图卡左 | D88 | 图表库自动(覆盖 [0.45, 0.75] 四档) | — |
| 概率主曲线 | 图卡主区 | D80 | **L1-A** (`price_history`) | **hover 显示 t / prob**(S4 新增)|
| Bollinger 带虚线 | 图卡主区 | D82 + D84 + D85 | **L3** (`bollinger.py`) | — |
| 异常区间红色覆盖 | 图卡主区 | D87 | **L3** (`drift.py::segment_anomaly`) | **hover 显示 max / min / 持续时长**(S4 新增)|
| 新闻节点竖线 + 编号圈 | 图卡主区 | D91 + D92(=t) + D93 | **L3** (`news.py`,依赖 DATA-01) | click → 跳 D109 外链;hover 显 title+来源 |
| NOW 当前点标注 | 图卡主区 | D70 + D89(=坐标派生)| L3 + **L5** 派生 | — |
| 量柱图 | 图卡下方 | D81 + D94(归一)+ D96(坐标派生)| **L1-A** + **L5**(归一 + 坐标映射) | — |
| 量柱异常色 | 量柱图 | D95 | **L3** (`volume.py::mark_in_drift`) | 纯视觉映射 |
| Legend | 图卡底 | D97 | STATIC | — |

## R6 · 新闻列表

| 组件 | 位置 | 消费字段 | 来源层 | 交互行为 |
|---|---|---|---|---|
| 新闻列表卡标题 | 右卡顶 | D100 + D101 | STATIC | — |
| 新闻条目 × N | 列表主体 | D102(=D91)| **L3** (`news.py`,DATA-01)| click → 触发 D110(click 事件派生)→ 打开 D109 外链 |
| 条目左侧序号 badge | 每条左 | D103(=D93)| **L3** (`news.py::number_by_time`) | — |
| 新闻标题 | 每条主文 | D104 | **L1-B** (DATA-01 `ant_news.by_market`)| — |
| 来源 + 相对时间 | 每条副文 | D105 + D106 | L1-B + **L3** (`format.py::relative_time`) | — |
| 影响度 chip | 每条右 | D107 | **L1-B** (DATA-01) | — |
| chip 颜色 | 同上 | D108(← D107)| **L5**(纯视觉映射) | — |

## R7 · 信任层(三个折叠块)

| 组件 | 位置 | 消费字段 | 来源层 | 交互行为 |
|---|---|---|---|---|
| 折叠块 1 summary | 信任层顶 | D120(summary)+ D122 + D123 | **L3** (`format.py::conclusion_question`) + **L4** | click 展开(默认展开) |
| 折叠块 1 - 漂移详解 | 同上 | D122 | **L4** (`drift-narrative.md`) | — |
| 折叠块 1 - 历史命中率 | 同上 | D123 | **L4** (`hit-rate-narrative.md`) | — |
| 折叠块 1 - 附属标签 | 同上 | D121 + D124 + D125 | STATIC + D54 引用 | — |
| 折叠块 2 「方法论」 | 信任层中 | D130 + D131 + D132 + D133 | STATIC | click 展开(默认收起) |
| 折叠块 3 「风险提示」 | 信任层底 | D140 + D141 + D142 + D143 + D144 | STATIC | click 展开(默认收起) |

## R8 · 状态块

| 组件 | 位置 | 消费字段 | 来源层 | 交互行为 |
|---|---|---|---|---|
| Loading 态 | 覆盖图卡 | D150 | STATIC 文案 + L5 计时 | 5-15s 超时 → 切 Error |
| Empty - 未匹配市场 | 输出区 | D151 | STATIC | click 重新输入 → 打开浮层 |
| Empty - 窗口内无数据(**S4 新增**)| 输出区 | D152 | STATIC | click 切换窗口 → 打开浮层 |
| Error 态 | 输出区 | D153 + D154(重试)| STATIC + L5 | click 重试 → 重新 execute |
| Degraded 态(DATA-01 未实现)| 新闻卡位 | D155 | STATIC | — |
| Footer | 页底 | D160 | STATIC | — |

## 端到端追溯自查(G5.8)

抽样 5 个 L5 组件沿上游追溯,确认无断点:

1. **Hero 正文** D53 → L4 `hero-narrative.md` → 消费 L3 的 D54/D55/D58 + L2 的 D57(DATA-03 降级) + L1-A 的 D70 ✅
2. **异常区间红覆盖** D87 → L3 `drift.py::segment_anomaly` → 消费 L3 的 D86 + D84/D85 → `bollinger.py` → L1-A 的 D80 ✅
3. **新闻竖线** D91 → L3 `news.py::pick_top_n` → L1-B 的 D90(DATA-01 · 登记在案) ✅
4. **24H 变化** D71 → L3 `delta.py` → L3 的 D70(`extract.py`) + D72(`extract.py::point_at`) → L1-A 的 D80 ✅
5. **30D 成交量** D75 → L3 `agg.py::sum_volume` → L1-A 的 D81 ✅

**所有断点均已登记为 L1-B / L2 缺口**(在 `data-prd.md` 有条目),无其它断点。
