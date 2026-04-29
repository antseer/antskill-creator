# drift-narrative.md · 漂移详解段落(D122)

## 模块与数据点
- **模块**: M4 · 信任层 · 折叠块 1「为什么给这结论」
- **产出数据点**: `D122` — 漂移详解(按 D87 每段一条)

## 输入 Schema

```typescript
type Input = {
  drifts: Array<{                    // D87
    start: number                    // index
    end: number
    peak: number                     // [0, 1]
    direction: 'up' | 'down'
    peak_time?: string               // ISO8601(由上层 L3 从 d80[start..end] 取 max/min 点 t)
    range: [string, string]          // [start_time, end_time] ISO8601
  }>
  news: Array<{                      // D91(筛后 Top N)
    t: string
    title: string
    impact: 'high' | 'mid' | 'low'
  }>
  baseline_prob: number              // 漂移起点概率(用于叙述"从 X 跳至 Y")
}
```

## 输出 Schema

```typescript
type Output = {
  sections: Array<{
    drift_index: number              // 1-based,对应 D54
    text: string                     // 一句话,约 60~100 字
  }>
}
```

## Prompt 正文

```
你是一个 Polymarket 市场的复盘叙述者。针对每一段漂移区间生成一句话复盘。

【材料】
- drifts: {{drifts}}
- 筛后新闻: {{news}}
- 基线概率: {{baseline_prob}}

【规则】
1. 为每一段 drift 生成一条 text,按时间顺序编号 1..N
2. 文本结构:"第 {i} 次漂移({range_start}→{range_end}):概率从 {from}% 跳至 {to}%,{X}"
   - X = "对应 {news.title} 新闻" 若该时段 news 非空
   - X = "无明确新闻关联" 否则
3. 时间戳保留到日+小时,UTC
4. 概率用百分比,保留 1 位小数

输出 JSON:
{"sections": [{"drift_index": 1, "text": "..."}]}

Few-shot:

输入: drifts=[{start:110, end:180, peak:0.72, direction:'up',
              peak_time:"2025-11-15T14:00:00Z",
              range:["2025-11-11T00:00:00Z", "2025-11-18T00:00:00Z"]}],
     news=[{t:"2025-11-15T14:00:00Z", title:"Supreme Court rules on ballot challenge", impact:"high"}],
     baseline_prob=0.595
输出: {"sections": [{"drift_index": 1, "text": "第 1 次漂移(2025-11-11 → 2025-11-18):概率从 59.5% 跳至 72.0%,对应「Supreme Court rules on ballot challenge」新闻。"}]}
```

## Fallback 模板函数

```python
from datetime import datetime
from typing import List, Dict, Any

def _parse_iso(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _fmt_day(ts):
    d = _parse_iso(ts)
    return f"{d.year}-{d.month:02d}-{d.day:02d}"


def _match_news(drift, news_list):
    """在 drift.range 时间窗内寻找 impact 最高的一条新闻"""
    if not news_list:
        return None
    rng_start = _parse_iso(drift["range"][0])
    rng_end = _parse_iso(drift["range"][1])
    in_window = [n for n in news_list
                 if rng_start <= _parse_iso(n["t"]) <= rng_end]
    if not in_window:
        return None
    rank = {"high": 3, "mid": 2, "low": 1}
    in_window.sort(key=lambda n: -rank.get(n.get("impact", "low"), 0))
    return in_window[0]


def fallback_drift_narrative(inp: Dict[str, Any]) -> Dict[str, Any]:
    """LLM 不可用时的模板叙述。schema 与 LLM 输出一致。"""
    drifts = inp.get("drifts", []) or []
    news = inp.get("news", []) or []
    baseline = inp.get("baseline_prob", 0.5)

    sections = []
    for i, dr in enumerate(drifts, start=1):
        rng_from = _fmt_day(dr["range"][0])
        rng_to = _fmt_day(dr["range"][1])
        from_pct = f"{baseline * 100:.1f}%"
        to_pct = f"{dr.get('peak', 0) * 100:.1f}%"
        matched = _match_news(dr, news)
        if matched:
            tail = f"对应「{matched['title']}」新闻。"
        else:
            tail = "无明确新闻关联。"
        text = f"第 {i} 次漂移({rng_from} → {rng_to}):概率从 {from_pct} 跳至 {to_pct},{tail}"
        sections.append({"drift_index": i, "text": text})
    return {"sections": sections}


if __name__ == "__main__":
    out = fallback_drift_narrative({
        "drifts": [
            {"start": 110, "end": 180, "peak": 0.72, "direction": "up",
             "range": ["2025-11-11T00:00:00Z", "2025-11-18T00:00:00Z"]},
            {"start": 610, "end": 700, "peak": 0.672, "direction": "up",
             "range": ["2026-04-05T00:00:00Z", "2026-04-13T00:00:00Z"]},
        ],
        "news": [
            {"t": "2025-11-15T14:00:00Z",
             "title": "Supreme Court rules on ballot challenge", "impact": "high"},
        ],
        "baseline_prob": 0.595,
    })
    for s in out["sections"]:
        print(s)
```
