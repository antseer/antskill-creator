"""
模块: M2 · 漂移分析
对应数据点:
  D86 (异常点布尔) · D87 (异常区间分段)
  D54 (漂移次数 = len(D87)) · D55 (最近一次漂移峰值)
输入:
  d80: list[{t, prob}]         # 概率时序
  d84: list[{t, upper}]        # Bollinger 上轨
  d85: list[{t, lower}]        # Bollinger 下轨
  min_hours: int = 24          # 过滤噪音的最小持续时长
输出:
  D86: list[bool]               # 每点是否越界
  D87: list[{start, end, peak, direction}]
       - start/end: index
       - peak: 区间内 prob 极值
       - direction: 'up' (越上轨) | 'down' (越下轨) | 'mixed'
  D54: int
  D55: float | None(最后一段的峰值)
逻辑: 逐点越界 → 连续 true 合并为段 → 滤除 < min_hours 的段(因为间隔是 1h,hours == index span)
状态: 可运行,与 frontend/index.html 中 segmentAnomaly 一致
"""

from typing import List, Dict, Any, Optional


def mark_anomaly(d80, d84, d85):
    flags = []
    for i, p in enumerate(d80):
        upper = d84[i].get("upper") if i < len(d84) else None
        lower = d85[i].get("lower") if i < len(d85) else None
        if upper is None or lower is None:
            flags.append(False)
            continue
        flags.append(p["prob"] > upper or p["prob"] < lower)
    return flags


def segment_anomaly(d80, d86, min_hours: int = 24):
    """连续 true 合并为段,过滤 < min_hours 的噪音"""
    segs = []
    start = -1
    for i, f in enumerate(d86):
        if f and start < 0:
            start = i
        elif not f and start >= 0:
            if i - start >= min_hours:
                segs.append(_build_seg(d80, d84_or_none=None, start=start, end=i - 1))
            start = -1
    if start >= 0 and len(d86) - start >= min_hours:
        segs.append(_build_seg(d80, d84_or_none=None, start=start, end=len(d86) - 1))
    return segs


def _build_seg(d80, d84_or_none, start: int, end: int):
    window = d80[start:end + 1]
    probs = [w["prob"] for w in window]
    peak_hi = max(probs)
    peak_lo = min(probs)
    mean = sum(probs) / len(probs) if probs else 0
    # 方向判定:均值在上轨附近 → up;下轨附近 → down;两者都触 → mixed
    direction = "up" if mean > 0.5 else "down"  # 简化:概率市场 baseline 通常 0.5
    peak = peak_hi if direction == "up" else peak_lo
    return {"start": start, "end": end, "peak": peak, "direction": direction}


def count_segments(d87) -> int:
    return len(d87)


def peak_of_last(d80, d87) -> Optional[float]:
    if not d87:
        return None
    last = d87[-1]
    return last.get("peak")


if __name__ == "__main__":
    # 构造 40 点序列:前 25 点正常,26-32 点越上轨(7h < 24h,应被滤除)
    # 33-37 点回落到中位,38 点之后又突破(小于 min_hours)——本测试主要验证函数可调
    d80 = [{"t": f"2026-04-01T{i:02d}:00:00Z", "prob": 0.60 + (0.05 if 26 <= i <= 32 else 0)} for i in range(40)]
    # mock 简化 band
    d84 = [{"t": p["t"], "upper": 0.63 if i >= 19 else None} for i, p in enumerate(d80)]
    d85 = [{"t": p["t"], "lower": 0.57 if i >= 19 else None} for i, p in enumerate(d80)]
    flags = mark_anomaly(d80, d84, d85)
    print("D86 flags (7 连续 true 在 26-32):", sum(flags), "处为 true")
    segs_strict = segment_anomaly(d80, flags, min_hours=24)
    print("D87 min=24h →", len(segs_strict), "段 (应 0,短于 24h 被过滤)")
    segs_loose = segment_anomaly(d80, flags, min_hours=3)
    print("D87 min=3h  →", len(segs_loose), "段,first:", segs_loose[0] if segs_loose else None)
    print("D54:", count_segments(segs_loose))
    print("D55:", peak_of_last(d80, segs_loose))
