# L2 · 待 MCP 新建聚合接口

> 期望接口形态的**完整定义**在根目录 `data-prd.md` 对应条目。本文件是索引 + 降级路径说明。

## 本 Skill 依赖的 L2 缺口

| GAP 编号 | 工具名 | 优先级 | 对应模块 | 核心产出 |
|---|---|---|---|---|
| **DATA-03** | `ant_polymarket.similar_drift_stats` | **P1** | M3(Hero 正文历史命中率)+ M4(历史命中率段落) | D57(`return_to_ma_rate_72h`) |

## DATA-03 期望接口形态(摘要)

完整定义见 `data-prd.md` DATA-03 段。关键点:

- **入参**: `category` / `drift_sigma` / `drift_direction` / `lookback_days`
- **出参关键字段**: `sample_size` / `return_to_ma_rate_{24h, 72h, 7d}` / `median_days_to_return` / `confidence_interval_72h`
- **刷新频率**: 1h 预计算,非实时
- **预计算粒度**: `category × sigma_bucket([1.5, 2.0, 2.5, 3.0]) × direction(up/down)`

## 降级路径(L3/L4 能否兜底)

| 层 | 兜底能力 | 性能代价 |
|---|---|---|
| L3 | ❌ 无法兜底 | 历史回归命中率需全量市场历史扫描,Skill 单次请求 P95 < 2s 内做不了 |
| L4 | ✅ 完全兜底 | 无性能代价 —— `hero-narrative.md` 和 `hit-rate-narrative.md` 的 Fallback 模板函数有「无 D57」分支,输出**不含具体数字**的通用表述 |
| 用户感知 | 说服力下降,不影响可用性 | Hero 正文从"72h 回归命中率 73%"退化为"历史上类似模式通常在 72h 内回归",信任层显式标注「历史命中率统计暂未接入」|

## 为什么不归 L3(PM 脚本)

按路由决策树 Q2:本接口需**扫全量已关闭市场历史数据**做预计算,跨 Skill 可复用,用量会随 Skill 数量线性增长 → 适合 MCP 侧维护一份预计算缓存,不适合每个 Skill L3 各自实现。

## 追溯

- PRD M3 §3.4 L2
- mcp-audit.md R5 D57
- data-prd.md DATA-03
