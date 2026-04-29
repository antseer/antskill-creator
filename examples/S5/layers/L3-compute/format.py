"""
模块: M2 · 漂移分析 / M4 · 信任层(格式化辅助)
对应数据点:
  D43  (数据时间戳,格式化)   · "YYYY/M/D"
  D106 (新闻相对时间)         · "N 天前" / "N 小时前" / "刚刚"
  D120 (折叠块 summary)       · "为什么给出'{D51}'的结论?"
输入:
  format_timestamp(now_iso: str)           # ISO8601 时间字符串 → D43
  relative_time(t: str, now: str | None)   # ISO8601 → D106
  conclusion_question(d51_verdict: str)    # D51 值 → D120
输出:
  均为 str。细节见各函数 docstring。
逻辑:
  纯字符串/日期格式化,无外部依赖,无副作用。
  - format_timestamp: YYYY/M/D(去零填充)
  - relative_time: 按 delta 阶梯映射("刚刚" / "N 分钟前" / "N 小时前" / "N 天前" / "1 周前")
  - conclusion_question: f-string 插值 D51
状态: 可运行(纯格式化,无外部依赖)
"""

from datetime import datetime, timezone
from typing import Optional


def _parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def format_timestamp(now_iso: str) -> str:
    """
    D43 · 数据时间戳(显示到 Meta 标签行)
    输入: ISO8601 字符串(UTC)
    输出: "YYYY/M/D"(无前导零,与 demo 中 "2026/4/16" 一致)
    """
    dt = _parse_iso(now_iso)
    return f"{dt.year}/{dt.month}/{dt.day}"


def relative_time(t_iso: str, now_iso: Optional[str] = None) -> str:
    """
    D106 · 新闻相对时间(中文)
    - < 1h       → "刚刚"
    - < 24h      → "N 小时前"
    - < 7d       → "N 天前"
    - >= 7d      → "N 周前"
    """
    t = _parse_iso(t_iso)
    now = _parse_iso(now_iso) if now_iso else datetime.now(timezone.utc)
    delta_sec = int((now - t).total_seconds())
    if delta_sec < 0:
        return "刚刚"
    minutes = delta_sec // 60
    if minutes < 60:
        return "刚刚" if minutes < 1 else f"{minutes} 分钟前"
    hours = minutes // 60
    if hours < 24:
        return f"{hours} 小时前"
    days = hours // 24
    if days < 7:
        return f"{days} 天前"
    weeks = days // 7
    return f"{weeks} 周前"


def conclusion_question(d51: str) -> str:
    """
    D120 · 折叠块 summary
    输入: D51 结论关键词(如 "回归入场窗口")
    输出: "为什么给出'{D51}'的结论?"
    """
    return f"为什么给出'{d51}'的结论?"


if __name__ == "__main__":
    print("D43:", format_timestamp("2026-04-16T12:00:00Z"))
    print("D106(-30m):", relative_time("2026-04-16T11:30:00Z", "2026-04-16T12:00:00Z"))
    print("D106(-5h): ", relative_time("2026-04-16T07:00:00Z", "2026-04-16T12:00:00Z"))
    print("D106(-3d): ", relative_time("2026-04-13T12:00:00Z", "2026-04-16T12:00:00Z"))
    print("D106(-10d):", relative_time("2026-04-06T12:00:00Z", "2026-04-16T12:00:00Z"))
    print("D120:", conclusion_question("回归入场窗口"))
