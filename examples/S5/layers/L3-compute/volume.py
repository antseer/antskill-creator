"""
模块: M2 · 漂移分析
对应数据点: D95 (量柱异常色标记)
输入:
  d81: list[{t, volume}]                         # 量时序(L1-A)
  d87: list[{start, end, peak, direction}]       # 异常区间分段(来自 drift.py)
输出:
  D95: list[bool]   # 每个 bar 的 t 是否落在某 D87 区间(按 index 判断,d80/d81 同源同 index)
逻辑:
  由于 d80 / d81 是 price_history 同次联产,index 对齐,直接用 d87 的 start/end 索引范围判定即可。
状态: 可运行
"""

from typing import List, Dict, Any


def mark_in_drift(d81: List[Dict[str, Any]], d87: List[Dict[str, Any]]) -> List[bool]:
    flags = [False] * len(d81)
    for seg in d87:
        start = seg.get("start", 0)
        end = seg.get("end", -1)
        for i in range(max(0, start), min(len(d81), end + 1)):
            flags[i] = True
    return flags


if __name__ == "__main__":
    d81 = [{"t": f"t{i}", "volume": 10000 + i * 100} for i in range(10)]
    d87 = [{"start": 3, "end": 5, "peak": 0.7, "direction": "up"}]
    flags = mark_in_drift(d81, d87)
    print("flags:", flags)
    print("true 个数:", sum(flags))
    assert flags == [False]*3 + [True]*3 + [False]*4
    print("✓ mark_in_drift 测试通过")
