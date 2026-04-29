"""
模块: M2 · 漂移分析
对应数据点: D75 (30D 成交量 · USD)
输入:
  d81: list[{t, volume}]  # 量时序(L1-A)
输出:
  total: float            # 窗口内 volume 求和(单位:USD)
逻辑:
  D81 由 price_history 同次联产,窗口由 MCP 入参 days 决定,L3 不再截断。
状态: 可运行
"""

from typing import List, Dict, Any


def sum_volume(d81: List[Dict[str, Any]]) -> float:
    if not d81:
        return 0.0
    return float(sum(p.get("volume", 0) or 0 for p in d81))


if __name__ == "__main__":
    mock = [{"t": f"2026-04-{i:02d}T00:00:00Z", "volume": 1000 * i} for i in range(1, 11)]
    print("sum:", sum_volume(mock))
    print("empty:", sum_volume([]))
