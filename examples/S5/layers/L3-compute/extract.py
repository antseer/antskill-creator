"""
模块: M2 · 漂移分析
对应数据点:
  D70 (当前概率) · D72 (24H 前概率) · D58 (目标回归位 = D82[-1])
输入:
  series: list[dict]  # 时序数据,每项含 't' (ISO8601) 和一个数值字段
输出:
  见各函数 docstring
逻辑:
  - take_last: 取尾部最后一项的某字段
  - point_at: 二分查找 t ≤ cutoff 的最近点
状态: 可运行
"""

from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional


def _parse_iso(ts: str) -> datetime:
    # Python 3.11+ 可直接 fromisoformat;做一层兼容
    s = ts.replace("Z", "+00:00")
    return datetime.fromisoformat(s)


def take_last(series: List[Dict[str, Any]], key: str = "prob") -> Optional[float]:
    """
    对应 D70 (key='prob') / D58 (key='ma' on D82 band series)
    返回最后一项的 key 字段,若序列为空或末项 key 为 None → 返回 None
    """
    if not series:
        return None
    last = series[-1]
    v = last.get(key)
    return v


def point_at(series: List[Dict[str, Any]], delta: timedelta, key: str = "prob",
             now: Optional[datetime] = None) -> Optional[float]:
    """
    对应 D72(delta = -timedelta(hours=24), key='prob')
    返回 t ≤ (now + delta) 的最近一点的 key 字段。
    - now 默认取 series 末项的 t(保证在 Skill runtime 单次调用内一致)
    - 若没有任何点满足条件,返回 None
    """
    if not series:
        return None
    if now is None:
        now = _parse_iso(series[-1]["t"])
    cutoff = now + delta
    # series 按 t 升序,线性扫尾即可(小数据量 ≤ 720 点)
    result = None
    for item in series:
        t = _parse_iso(item["t"])
        if t <= cutoff:
            result = item.get(key)
        else:
            break
    return result


if __name__ == "__main__":
    # mock: 10 点,每点间隔 1h
    base = datetime(2026, 4, 16, 12, 0, 0, tzinfo=timezone.utc)
    series = [
        {"t": (base - timedelta(hours=9 - i)).isoformat(), "prob": 0.50 + i * 0.01}
        for i in range(10)
    ]
    print("D70 take_last:", take_last(series))
    print("D72 point_at(-5h):", point_at(series, timedelta(hours=-5)))
    print("point_at(-24h) (超范围):", point_at(series, timedelta(hours=-24)))
