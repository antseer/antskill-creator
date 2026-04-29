"""
模块: M2 · 漂移分析
对应数据点: D71 (24H 变化,pp = 百分点)
输入:
  d70: float | None  # 当前概率 [0, 1]
  d72: float | None  # 24H 前概率 [0, 1]
输出:
  delta_pp: float | None  # (D70 - D72) * 100,若任一输入为 None 则返回 None
逻辑:
  概率差 × 100,得到百分点(pp)。
  示例:D70=0.624 D72=0.652 → delta = -2.8pp
状态: 可运行
"""

from typing import Optional


def delta(d70: Optional[float], d72: Optional[float]) -> Optional[float]:
    if d70 is None or d72 is None:
        return None
    return round((d70 - d72) * 100, 2)


if __name__ == "__main__":
    print("0.624 vs 0.652 →", delta(0.624, 0.652), "pp")
    print("0.60 vs 0.60 →", delta(0.60, 0.60), "pp")
    print("None 输入 →", delta(None, 0.5))
