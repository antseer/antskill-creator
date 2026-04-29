"""
模块: M2 · 漂移分析
对应数据点: D74 (Z-Score)
输入:
  d70: float          # 当前概率
  ma_last: float      # D82[-1] MA-20 末值
  std_last: float     # D83[-1] 20σ 末值
输出:
  z: float | None     # (D70 - ma) / std,若 std <= 0 返回 None
逻辑:
  Z-Score 标准定义。符号表示方向(正:偏高,负:偏低)。
状态: 可运行
"""

from typing import Optional


def compute(d70: Optional[float], ma_last: Optional[float],
            std_last: Optional[float]) -> Optional[float]:
    if d70 is None or ma_last is None or std_last is None:
        return None
    if std_last <= 0:
        return None
    return round((d70 - ma_last) / std_last, 2)


if __name__ == "__main__":
    print("0.624 vs ma=0.585 std=0.025 →", compute(0.624, 0.585, 0.025), "σ")
    print("std=0 边界 →", compute(0.5, 0.5, 0))
