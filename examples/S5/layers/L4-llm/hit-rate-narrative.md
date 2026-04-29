# hit-rate-narrative.md · 历史命中率段落(D123)

## 模块与数据点
- **模块**: M4 · 信任层 · 折叠块 1「为什么给这结论」(段落 2)
- **产出数据点**: `D123` — 历史命中率叙述段(含样本量、置信区间提醒、止损条件)

## 输入 Schema

```typescript
type Input = {
  // DATA-03 输出(若未落地整体为 null)
  similar_stats: {
    sample_size: number
    return_to_ma_rate_24h: number
    return_to_ma_rate_72h: number       // D57
    return_to_ma_rate_7d: number
    median_days_to_return: number
    confidence_interval_72h: [number, number]
  } | null

  drift_count: number                   // D54
  target_ma: number                     // D58
  z_score_current: number               // D74(用于给出止损条件)
}
```

## 输出 Schema

```typescript
type Output = {
  text: string                          // 1-2 句完整段落,中文
}
```

## Prompt 正文

```
你是信任层叙述者。根据历史漂移统计写一段面向交易者的说明。

【材料】
- similar_stats: {{similar_stats}}(可能为 null)
- 近期漂移次数 D54: {{drift_count}}
- 目标回归位 MA-20: {{target_ma}}
- 当前 Z-Score: {{z_score_current}}σ

【约束】
- 1-2 句,80~160 字
- 若 similar_stats 非空:
  - 必含 "历史上两段类似漂移模式,在第二次回归期入场的 72 小时命中率为 {率}%"
  - 必含 "样本 n={size}"
  - 必含 "当前 Z-Score {σ} 仍处可交易回归区间"
  - 必含止损条件:"若 24 小时内跌破 MA-20({target_ma}%),则回归失败,应止损"
- 若 similar_stats 为 null:
  - 不报具体数字
  - 提及本 Skill 方法论基于 Bollinger 2σ
  - 提及"经典实战中该信号的均值回归概率通常高于 50%"

严格输出 JSON:
{"text": "..."}

Few-shot:

输入: similar_stats={sample_size:31, return_to_ma_rate_72h:0.73, ...},
      drift_count=2, target_ma=0.585, z_score_current=1.2
输出: {"text": "历史上两段类似漂移模式,在第二次回归期入场的 72 小时命中率为 73%(样本 n=31,来自过去 12 个月同类政治市场)。当前 Z-Score +1.2σ 仍处'可交易回归'区间;若 24 小时内跌破 MA-20(58.5%),则回归失败,应止损。"}

输入: similar_stats=null, drift_count=2, target_ma=0.585, z_score_current=1.2
输出: {"text": "历史上类似模式的回归统计暂未接入,但本 Skill 的方法论基于 Bollinger 2σ,经典实战中该信号的均值回归概率通常高于 50%。"}
```

## Fallback 模板函数

```python
from typing import Dict, Any


def fallback_hit_rate_narrative(inp: Dict[str, Any]) -> Dict[str, Any]:
    """
    LLM 不可用时走固定模板。schema 与 LLM 输出一致:{"text": str}

    两种路径:
      (A) similar_stats 有值 → 用 PRD 规定的"命中率+止损条件"模板
      (B) similar_stats 为 null → 用 PRD 规定的"无接入"通用方法论文案
    """
    stats = inp.get("similar_stats")
    d58 = inp.get("target_ma", 0)
    z = inp.get("z_score_current", 0)

    if stats is not None:
        rate_72h = stats.get("return_to_ma_rate_72h")
        n = stats.get("sample_size")
        if rate_72h is None or n is None:
            stats = None  # 数据不完整 → 降级为 B 路径

    if stats is not None:
        z_sign = "+" if z >= 0 else ""
        return {"text": (
            f"历史上两段类似漂移模式,"
            f"在第二次回归期入场的 72 小时命中率为 {int(stats['return_to_ma_rate_72h'] * 100)}%"
            f"(样本 n={stats['sample_size']},来自过去 12 个月同类政治市场)。"
            f"当前 Z-Score {z_sign}{z:.1f}σ 仍处'可交易回归'区间;"
            f"若 24 小时内跌破 MA-20({d58 * 100:.1f}%),则回归失败,应止损。"
        )}

    # DATA-03 未落地
    return {"text": (
        "历史上类似模式的回归统计暂未接入,"
        "但本 Skill 的方法论基于 Bollinger 2σ,"
        "经典实战中该信号的均值回归概率通常高于 50%。"
    )}


if __name__ == "__main__":
    # A 路径:DATA-03 有值
    print(fallback_hit_rate_narrative({
        "similar_stats": {
            "sample_size": 31, "return_to_ma_rate_24h": 0.48,
            "return_to_ma_rate_72h": 0.73, "return_to_ma_rate_7d": 0.82,
            "median_days_to_return": 2.5, "confidence_interval_72h": [0.61, 0.83]
        },
        "drift_count": 2, "target_ma": 0.585, "z_score_current": 1.2,
    }))
    # B 路径:DATA-03 未落地
    print(fallback_hit_rate_narrative({
        "similar_stats": None,
        "drift_count": 2, "target_ma": 0.585, "z_score_current": 1.2,
    }))
```
