# verdict.md · 结论关键词 + 副标题(D51 + D52)

## 模块与数据点
- **模块**: M3 · 解读与建议
- **产出数据点**:
  - `D51` — 结论关键词(三值:`回归入场窗口` / `观望` / `继续偏离`)
  - `D52` — 结论副标题(≤30 字,与 D51 搭配)

## 输入 Schema

```typescript
type Input = {
  current_prob: number       // D70, [0, 1]
  z_score: number            // D74
  volatility_7d: number      // D73 · %
  drift_count: number        // D87 数组长度(近 window 内漂移次数)
  trend_direction: 'rising' | 'falling' | 'flat'  // 由 L3 基于近 6h 斜率判断
}
```

## 输出 Schema

```typescript
type Output = {
  verdict: '回归入场窗口' | '观望' | '继续偏离'  // D51
  risk_level: 'low' | 'mid' | 'high'
  subtitle: string                               // D52,≤30 字
}
```

## Prompt 正文

```
你是一个 Polymarket 市场的量化观察员。根据下列统计数据给出结论。

【当前状态】
- 当前概率: {{current_prob}} (0~1)
- Z-Score vs MA-20: {{z_score}}σ
- 7D 波动率: {{volatility_7d}}%
- 近期漂移次数: {{drift_count}}
- 短期趋势: {{trend_direction}}

【规则】
1. |Z| < 0.5          → "观望" + low
2. Z ≥ 2 且 falling   → "回归入场窗口" + mid
3. Z ≤ -2 且 rising   → "回归入场窗口" + mid
4. |Z| ≥ 2 且 同向continuing → "继续偏离" + high
5. 其他                → "观望" + low

副标题要点:
- 回归入场窗口 → 强调"从峰值/谷值回落/回升"
- 观望         → 强调"无机会信号"或"正常波动"
- 继续偏离     → 强调"方向仍在扩大"

严格输出 JSON,无前后缀:
{"verdict": "...", "risk_level": "low|mid|high", "subtitle": "..."}

Few-shot:

输入: current_prob=0.624, z_score=2.3, volatility_7d=4.1, drift_count=2, trend_direction=falling
输出: {"verdict": "回归入场窗口", "risk_level": "mid", "subtitle": "当前概率正从新闻脉冲峰值回落"}

输入: current_prob=0.52, z_score=0.3, volatility_7d=1.8, drift_count=0, trend_direction=flat
输出: {"verdict": "观望", "risk_level": "low", "subtitle": "概率处于正常区间,无特殊操作机会"}

输入: current_prob=0.78, z_score=3.1, volatility_7d=6.2, drift_count=3, trend_direction=rising
输出: {"verdict": "继续偏离", "risk_level": "high", "subtitle": "价格仍在偏离均线方向扩大"}
```

## Fallback 模板函数

```python
def fallback_verdict(inp: dict) -> dict:
    """
    LLM 不可用时走纯硬阈值映射,schema 与 LLM 输出一致。
    输入字段与上方 Input Schema 一致。
    """
    z = inp.get("z_score") or 0.0
    trend = inp.get("trend_direction", "flat")

    if abs(z) < 0.5:
        return {
            "verdict": "观望",
            "risk_level": "low",
            "subtitle": "概率处于正常区间,无特殊操作机会",
        }
    if z >= 2 and trend == "falling":
        return {
            "verdict": "回归入场窗口",
            "risk_level": "mid",
            "subtitle": "当前概率正从新闻脉冲峰值回落",
        }
    if z <= -2 and trend == "rising":
        return {
            "verdict": "回归入场窗口",
            "risk_level": "mid",
            "subtitle": "当前概率正从异常低点回升",
        }
    if abs(z) >= 2 and trend in ("rising", "falling"):
        # 同向继续(Z 正且还在上升,或 Z 负且还在下跌)
        if (z >= 2 and trend == "rising") or (z <= -2 and trend == "falling"):
            return {
                "verdict": "继续偏离",
                "risk_level": "high",
                "subtitle": "价格仍在偏离均线方向扩大",
            }
    return {
        "verdict": "观望",
        "risk_level": "low",
        "subtitle": "当前无明确机会信号",
    }


# 自测
if __name__ == "__main__":
    cases = [
        {"z_score": 2.3, "trend_direction": "falling"},
        {"z_score": 0.3, "trend_direction": "flat"},
        {"z_score": 3.1, "trend_direction": "rising"},
        {"z_score": -2.1, "trend_direction": "rising"},
    ]
    for c in cases:
        print(c, "→", fallback_verdict(c))
```
