"""
模块: M2 · 漂移分析
对应数据点: D73 (7D 波动率,%)
输入:
  d80: list[{t, prob}]   # 概率时序(来自 L1-A)
  days: int              # 窗口天数(D73 固定 7)
输出:
  vol_pct: float | None  # std(prob where t ≥ now-7d) × 100,样本 < 2 时返回 None
逻辑:
  截取窗口内样本点,计算无偏标准差并 ×100 转成百分比。
状态: 可运行
"""

import math
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional


def _parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def std_window(d80: List[Dict[str, Any]], days: int = 7) -> Optional[float]:
    if not d80:
        return None
    now = _parse_iso(d80[-1]["t"])
    cutoff = now - timedelta(days=days)
    window = [p["prob"] for p in d80 if _parse_iso(p["t"]) >= cutoff]
    n = len(window)
    if n < 2:
        return None
    mean = sum(window) / n
    var = sum((x - mean) ** 2 for x in window) / (n - 1)  # 无偏
    return round(math.sqrt(var) * 100, 2)


if __name__ == "__main__":
    base = datetime(2026, 4, 16, 12, 0, 0, tzinfo=timezone.utc)
    # 10 天,每天 1 点,后 7 天作为窗口
    series = [
        {"t": (base - timedelta(days=9 - i)).isoformat(), "prob": 0.60 + (i % 3) * 0.02}
        for i in range(10)
    ]
    print("D73 7D 波动率 (%):", std_window(series, days=7))
