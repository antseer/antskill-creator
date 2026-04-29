# MCP 缺口清单 · polymarket-drift-radar

> **本 Skill 为半成品,以下接口需后端补齐后 Skill 方可完整运行。**
> Skill PRD: `skill-prd.md`
> 对应 skill 版本: 0.1.0
> 生成时间: 2026-04-16
> 对应审计: `mcp-audit.md`

## 汇总

- **P0 (主流程必备)**: 1 条 — DATA-01
- **P1 (可降级,影响体验)**: 1 条 — DATA-03
- **P2 (nice to have)**: 1 条 — DATA-02

**核心差异化缺口**:DATA-01 是本 Skill 区别于 Polymarket 自带图表和 ElectionBettingOdds 的核心功能("新闻层叠加"),强烈建议 P0 优先。

---

## P0 — 主流程必备

### DATA-01 · ant_news.by_market

- **层级**: L1-B(新增原始工具)
- **优先级**: P0
- **对应数据点**: D90(根)、D91、D102(衍生)、D104、D105、D107、D109(字段投影)
- **对应 PRD 模块**: M2 · 漂移分析(新闻节点叠加图)、M4 · 新闻列表
- **调用场景**: 在概率曲线上叠加关键新闻竖线 + 右侧新闻列表卡,回答用户"这天价格为什么跳",是 Skill 最核心的差异化能力

#### 期望接口形态

- **tool name**: `ant_news.by_market`
- **endpoint**: `/news/by_market`
- **入参**:

  | 参数名 | 类型 | 必填 | 说明 |
  |---|---|---|---|
  | market_id | string | ✅ | Polymarket 市场 ID(从 search_markets 获取) |
  | time_range | enum('7d','30d','90d') | ✅ | 与概率曲线窗口保持一致 |
  | min_impact | enum('low','mid','high') | ❌ | 默认 'low'(不过滤) |
  | lang | string | ❌ | 默认 'zh-CN',可选 'en-US' |
  | limit | int | ❌ | 默认 20,max 100 |

- **出参**(JSON):

  ```typescript
  Array<{
    t: string;                          // ISO 8601 时间戳
    title: string;                      // 新闻标题(lang 参数决定语言)
    source: string;                     // 来源名 "CNN" / "Reuters" / "Bloomberg" / "CoinDesk"
    url: string;                        // 原文链接
    impact: 'high' | 'mid' | 'low';    // 影响度分级(见实现建议)
    summary?: string;                   // 可选:首段摘要 ≤ 200 字
    category?: string;                  // 可选:"political" / "regulatory" / "macro"
  }>
  ```

- **刷新频率**: 15 min
- **性能预期**: P95 < 500ms,单次返回 ≤ 50 条
- **鉴权**: 复用平台现有 API token,无需额外凭证

#### 实现建议

- **底层拉取源**: NewsAPI + CryptoPanic + Twitter/X 搜索(按 market 关键词)
- **关键词映射**: 需要内置 market_id → 核心关键词的映射表(如 "2024-presidential-election" → ["Trump", "Harris", "election"])。建议从 market title 和 description 自动抽取实体 + 人工校准。
- **impact 分级逻辑**:
  - `high`:来源在白名单(NYT/Reuters/Bloomberg/CNN)且互动量 > 1000
  - `mid`:白名单来源 或 互动量 > 500
  - `low`:其余
- **缓存**: 15min 缓存,按 `(market_id, time_range, lang)` 维度
- **去重**: 同一事件多源报道按 title 相似度合并,保留 impact 最高者

#### 降级策略(必填)

若此接口**未实现**时本 Skill 表现:

- **前端表现**:
  - 概率曲线不显示新闻标注竖线(D91、D92、D93 均空)
  - 右侧"关键新闻节点"卡整体替换为降级提示卡(显示 D155 文案:"新闻源暂不可用,仅展示概率")
  - Hero 结论(D51-D53)由 L4 Fallback 生成不引用新闻的版本
- **L3/L4 兜底**:
  - L4 `drift-narrative.md` 的输入 schema 中 `news` 字段允许为空数组,Fallback 模板按空数组处理,输出"XX 期间出现 N 次显著漂移(无法关联到具体新闻)"
  - L3 `pick_top_n(news=[], drifts)` 返回空列表
- **用户感知**:
  - 在信任层"方法论"顶部显示 warning 提示
  - 页面整体仍可用,但丧失本 Skill 最核心的差异化价值

#### 追溯信息

- 发现时间: S2 阶段 MCP 路由审计(2026-04-16)
- 审计记录: `mcp-audit.md` R6.3 / R7
- 是否已向 MCP 团队同步: **待同步**

---

## P1 — 可降级但影响体验

### DATA-03 · ant_polymarket.similar_drift_stats

- **层级**: L2(新聚合接口)
- **优先级**: P1
- **对应数据点**: D57(Hero 正文中的"历史命中率")
- **对应 PRD 模块**: M3 · 解读与建议(Hero 正文插值)、M4 · 信任层(历史命中率叙述)
- **调用场景**: Hero 正文声称"历史上类似漂移模式,72h 回归命中率为 73%",此数字需要有数据支撑。若缺失,Hero 只能用 L4 Fallback 说"历史上类似模式通常会回归"而无具体数字,说服力下降。

#### 期望接口形态

- **tool name**: `ant_polymarket.similar_drift_stats`
- **endpoint**: `/polymarket/similar_drift_stats`
- **入参**:

  | 参数名 | 类型 | 必填 | 说明 |
  |---|---|---|---|
  | category | string | ✅ | 市场品类(political / sports / crypto / other) |
  | drift_sigma | number | ✅ | 本次漂移的标准差倍数(如 2.0) |
  | drift_direction | enum('up','down') | ✅ | 漂移方向 |
  | lookback_days | int | ❌ | 历史回溯天数,默认 365 |

- **出参**(JSON):

  ```typescript
  {
    sample_size: number;              // 历史匹配到的类似漂移事件数
    return_to_ma_rate_24h: number;   // 24h 内回到 MA-20 的比例 [0,1]
    return_to_ma_rate_72h: number;   // 72h 内回到 MA-20 的比例 [0,1]
    return_to_ma_rate_7d: number;    // 7d 内回到 MA-20 的比例 [0,1]
    median_days_to_return: number;   // 回归中位天数
    confidence_interval_72h: [number, number];  // 72h 命中率 95% CI
  }
  ```

- **刷新频率**: 1 h(预计算,非实时)
- **性能预期**: P95 < 300ms(全量预计算后查询)

#### 实现建议

- 后端每日扫全量已关闭市场,识别历史上所有"2σ 漂移 + 24h 后是否回归 MA-20"的样本
- 按 `(category, sigma_bucket, direction)` 三维分桶预计算命中率
- 桶粒度:category × [1.5, 2.0, 2.5, 3.0] × [up, down]
- 若样本 < 20,返回 `sample_size` 小值让前端决定是否展示

#### 降级策略(必填)

若此接口**未实现**时本 Skill 表现:

- **前端表现**:
  - Hero 正文 D53 由 L4 Fallback 生成不含具体命中率的版本("历史上类似模式多数会回归到均线附近")
  - D57 字段不出现在最终 Hero 文本中
  - 信任层 D123 历史命中率段由 Fallback 输出通用描述
- **L3/L4 兜底**:
  - L4 `hero-narrative.md` 的输入 schema 中 `similar_stats` 字段允许为 null
  - L4 Fallback:`similar_stats=null` 时走"无具体数字版"的模板文案
- **用户感知**:
  - Hero 正文可用但说服力下降
  - 信任层"方法论"中注明"历史命中率统计暂未接入"

#### 追溯信息

- 发现时间: S2 阶段 MCP 路由审计(2026-04-16)
- 审计记录: `mcp-audit.md` R5 D57
- 是否已向 MCP 团队同步: **待同步**

---

## P2 — Nice to have

### DATA-02 · ant_polymarket.parse_market_url

- **层级**: L1-B(新增原始工具)
- **优先级**: P2
- **对应数据点**: 辅助 D32(用户事件输入)
- **对应 PRD 模块**: M1 · 市场识别
- **调用场景**: 用户若直接粘贴 `polymarket.com/event/xxx` 链接,直接解析出 market_id,省去一次 search 调用

#### 期望接口形态

- **tool name**: `ant_polymarket.parse_market_url`
- **endpoint**: `/polymarket/parse_url`
- **入参**:

  | 参数名 | 类型 | 必填 | 说明 |
  |---|---|---|---|
  | url | string | ✅ | Polymarket 完整 URL |

- **出参**:

  ```typescript
  {
    market_id: string | null;   // 解析失败返回 null
    title: string | null;       // 顺带返回 title 供前端回显确认
    slug: string | null;        // URL slug
  }
  ```

- **刷新频率**: 静态(URL 解析逻辑)
- **性能预期**: P95 < 100ms

#### 实现建议

- 正则解析 URL 模式即可,无需调用外部
- 后端可把解析规则维护在一处,避免前端多个 Skill 各自实现

#### 降级策略

- **前端表现**: 前端自己做 regex 兜底(已有的 `/event\/([^\/\?]+)/` 提取 slug,再走 search_markets)
- **用户感知**: 无感(完全透明降级)

#### 追溯信息

- 发现时间: S2 阶段 MCP 路由审计(2026-04-16)
- 审计记录: `mcp-audit.md` R3.2 D32
- 是否已向 MCP 团队同步: N/A(P2,可选)

---

## 自查(G2.2)

- [x] 所有 L1-B / L2 条目都汇总到本清单
- [x] 每条 GAP 有完整期望接口形态(endpoint / tool name / 入参表 / 出参 schema / 刷新频率)
- [x] 每条 GAP 有降级策略(前端表现 + L3/L4 兜底 + 用户感知)
- [x] 每条 GAP 有优先级(P0/P1/P2)
- [x] 每条 GAP 有追溯信息
- [x] P0 仅 1 条(DATA-01),确实"无此接口 Skill 无法实现核心差异化"
- [x] P0/P1/P2 分布合理(P0=1, P1=1, P2=1,非全部 P0)

**G2.2 🔴 全部通过**。
