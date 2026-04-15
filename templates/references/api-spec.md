# {{SKILL_NAME}} — API Specification

> API 字段定义：数据源、端点、字段映射、降级策略。SoT 优先级第 3 位。

---

## 1. 数据源清单

| # | 数据源 | 端点 | 认证 | 频率上限 | 延迟 | 优先级 |
|---|--------|------|------|----------|------|--------|
| D1 | {{source}} | `{{endpoint}}` | {{API Key / None}} | {{N/min}} | {{<Xs}} | 主源 |
| D2 | {{source}} | `{{endpoint}}` | {{auth}} | {{rate}} | {{latency}} | Fallback |

### 降级链

```
D1 (主源) → 失败 → D2 (Fallback) → 失败 → 缓存 → 失败 → 错误卡
```

---

## 2. 统一内部 Schema

### RawProduct（L1 输出）

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `id` | string | ✅ | 唯一标识 `{platform}_{protocol}_{pool}` | `binance_simple_earn_usdt_flex` |
| `platform` | string | ✅ | 平台名 | `Binance` |
| `product_name` | string | ✅ | 产品名 | `USDT Flexible Savings` |
| `apy` | float | ✅ | 年化收益率（小数） | `0.052` |
| `currency` | string | ✅ | 币种 | `USDT` |
| `venue_type` | enum | ✅ | `CEX` 或 `DeFi` | `CEX` |
| `chain` | string | ❌ | 链名（DeFi 必填） | `Ethereum` |
| `tvl_usd` | float | ❌ | TVL（USD） | `1500000000` |
| `lock_days` | int | ✅ | 锁仓天数（0=活期） | `0` |
| `min_amount` | float | ❌ | 最低投入 | `100` |
| `capacity_usd` | float | ❌ | 剩余容量 | `50000000` |
| `updated_at` | datetime | ✅ | 数据更新时间 ISO8601 UTC | `2025-01-15T14:30:00Z` |

### ScoredProduct（L2 输出，继承 RawProduct 并增加）

| 字段 | 类型 | 说明 |
|------|------|------|
| `score_yield` | float 0-100 | 收益维度评分 |
| `score_safety` | float 0-100 | 安全维度评分 |
| `score_convenience` | float 0-100 | 便利维度评分 |
| `score_capacity` | float 0-100 | 容量维度评分 |
| `score_stability` | float 0-100 | 稳定维度评分 |
| `total_score` | float 0-100 | 综合评分 |
| `rank` | int | 排名（1=最优） |
| `anomalies` | list[string] | 异常标签列表 |

---

## 3. 字段映射表（每数据源→内部 Schema）

### D1: {{主数据源名}}

| 原始字段 | → 内部字段 | 转换规则 |
|----------|-----------|----------|
| `{{raw_field}}` | `apy` | `raw_value / 100`（百分比→小数） |
| `{{raw_field}}` | `tvl_usd` | 直接映射 |
| {{...}} | {{...}} | {{...}} |

### D2: {{Fallback 数据源名}}

| 原始字段 | → 内部字段 | 转换规则 |
|----------|-----------|----------|
| {{...}} | {{...}} | {{...}} |

---

## 4. L3 输入 Schema（喂给 LLM）

```json
{
  "user_context": {
    "principal_usd": 10000,
    "risk_preference": "balanced",
    "convenience_requirement": "flexible_only"
  },
  "market_stats": {
    "median_apy": 0.045,
    "mean_apy": 0.052,
    "product_count": 42
  },
  "scored_products": ["... top N ScoredProduct objects"],
  "anomaly_alerts": ["... anomaly descriptions"]
}
```

## 5. L3 输出 Schema（LLM 返回）

```json
{
  "headline": "string, ≤40 chars",
  "top1_reason": "string, 80-120 chars",
  "opportunity_cost": "string, contains dollar comparison",
  "risk_warning": "string, ≥40 chars",
  "anomaly_narratives": ["string"],
  "brief_for_card": [
    {"rank": 1, "one_liner": "string, ≤60 chars"}
  ]
}
```
