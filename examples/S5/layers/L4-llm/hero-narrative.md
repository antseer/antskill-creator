# hero-narrative.md · Hero 正文(D53)

## 模块与数据点
- **模块**: M3 · 解读与建议
- **产出数据点**: `D53` — Hero 正文段落(2-3 句,含数值插值锚点)

## 输入 Schema

```typescript
type Input = {
  window_days: 7 | 30                   // 由用户 pill 选择
  drift_count: number                   // D54
  last_peak: number                     // D55 · 最后一次漂移峰值 [0, 1]
  current_prob: number                  // D56 (= D70)
  similar_hit_rate_72h: number | null   // D57,来自 DATA-03,缺失时 null
  target_ma: number                     // D58 = D82[-1]
  z_score: number                       // D74
  volatility_7d: number                 // D73
  risk_level: 'low' | 'mid' | 'high'    // 来自 verdict.md 的输出
  news_summary: string | null           // 近期 Top 1 新闻的一句话概括(可选)
}
```

## 输出 Schema

```typescript
type Output = {
  narrative: string  // 2-3 句中文,含 {D54} {D55} {D56} {D57}? {D58} 的插值锚点
}
```

## Prompt 正文

```
你是一个冷静的市场观察员。根据下列材料生成 Hero 正文(2-3 句,中文,自然流畅)。

【材料】
- 分析窗口: {{window_days}} 天
- 漂移次数: {{drift_count}}
- 最近一次峰值概率: {{last_peak}} (0~1)
- 当前概率: {{current_prob}} (0~1)
- 历史 72h 回归命中率: {{similar_hit_rate_72h}} (可为 null)
- 目标回归位 MA-20: {{target_ma}}
- Z-Score: {{z_score}}σ
- 7D 波动率: {{volatility_7d}}%
- 风险等级: {{risk_level}}
- 近期新闻摘要: {{news_summary}} (可为 null)

【约束】
- 2-3 句,90~130 字
- 数字用百分比形式(0.672 → 67.2%)
- 若 similar_hit_rate_72h 为 null:不提"72 小时命中率 XX%",改为泛化表述"通常会在 72 小时内回归"
- risk_level = low 时强调"正常波动区间",不谈机会
- risk_level = high 时不说"入场",改为"观望至形态明朗"
- 不使用感叹号,不使用"!""?""~"

严格输出 JSON:
{"narrative": "..."}

Few-shot:

输入: window_days=30, drift_count=2, last_peak=0.672, current_prob=0.624,
     similar_hit_rate_72h=0.73, target_ma=0.585, z_score=1.2, volatility_7d=4.1,
     risk_level=mid, news_summary=null
输出: {"narrative": "过去 30 天该市场出现 2 次新闻驱动的显著漂移,最近一次峰值概率 67.2%。当前 62.4%,历史上类似漂移在 72 小时内有 73% 概率回归至 MA-20 附近(约 58.5%)。"}

输入: window_days=7, drift_count=0, last_peak=null, current_prob=0.54,
     similar_hit_rate_72h=null, target_ma=0.545, z_score=0.3, volatility_7d=1.8,
     risk_level=low, news_summary=null
输出: {"narrative": "过去 7 天无明显漂移,当前概率 54.0% 处于正常波动区间。"}
```

## Fallback 模板函数

```python
def fallback_hero_narrative(inp: dict) -> dict:
    """
    LLM 不可用时走固定模板。与 PRD M3 §3.6 Fallback 表一致。
    schema 与 LLM 输出一致:{"narrative": str}
    """
    risk = inp.get("risk_level", "low")
    window = inp.get("window_days", 30)
    d54 = inp.get("drift_count", 0)
    d55 = inp.get("last_peak")
    d56 = inp.get("current_prob", 0)
    d57 = inp.get("similar_hit_rate_72h")
    d58 = inp.get("target_ma", 0)

    def pct(x):
        return "—" if x is None else f"{x * 100:.1f}%"

    if risk == "low":
        return {"narrative": f"过去 {window} 天无明显漂移,当前概率 {pct(d56)} 处于正常波动区间。"}

    if risk == "high":
        return {"narrative": (
            f"过去 {window} 天出现 {d54} 次显著漂移,"
            f"当前 {pct(d56)} 仍在偏离方向扩大,建议观望至形态明朗。"
        )}

    # risk == "mid"
    if d57 is not None:
        return {"narrative": (
            f"过去 {window} 天出现 {d54} 次显著漂移,最近一次峰值概率 {pct(d55)}。"
            f"当前 {pct(d56)},历史上类似模式 72h 回归命中率 {int(d57 * 100)}%,"
            f"目标回归位 {pct(d58)} 附近。"
        )}
    return {"narrative": (
        f"过去 {window} 天出现 {d54} 次显著漂移,最近一次峰值概率 {pct(d55)}。"
        f"当前 {pct(d56)},历史上类似模式通常在 72h 内回归,目标位约在 {pct(d58)}。"
    )}


if __name__ == "__main__":
    for c in [
        {"risk_level": "mid", "window_days": 30, "drift_count": 2,
         "last_peak": 0.672, "current_prob": 0.624, "similar_hit_rate_72h": 0.73, "target_ma": 0.585},
        {"risk_level": "mid", "window_days": 30, "drift_count": 2,
         "last_peak": 0.672, "current_prob": 0.624, "similar_hit_rate_72h": None, "target_ma": 0.585},
        {"risk_level": "low", "window_days": 7, "drift_count": 0,
         "last_peak": None, "current_prob": 0.54, "similar_hit_rate_72h": None, "target_ma": 0.545},
        {"risk_level": "high", "window_days": 30, "drift_count": 3,
         "last_peak": 0.78, "current_prob": 0.76, "similar_hit_rate_72h": None, "target_ma": 0.58},
    ]:
        print(fallback_hero_narrative(c))
```
