"""
模块: M2 · 漂移分析
对应数据点:
  D82 (MA-20 时序) · D83 (20σ 时序) · D84 (Bollinger 上轨) · D85 (Bollinger 下轨)
输入:
  d80: list[{t, prob}]  # 概率时序(L1-A)
  N:   int = 20         # 滚动窗口长度
  k:   float = 2.0      # Bollinger sigma 倍数
输出:
  D82: list[{t, ma}]
  D83: list[{t, std}]
  D84: list[{t, upper}]
  D85: list[{t, lower}]
  前 N-1 项 ma/std/upper/lower 字段为 None(warming up)。
逻辑:
  - rolling_ma: 滑窗算术平均
  - rolling_std: 滑窗总体标准差(与前端 JS 版本一致,除以 N 而非 N-1)
  - band: ma ± k × std
状态: 可运行。与 frontend/index.html 中的 rollingBands 逻辑等价。
"""

import math
from typing import List, Dict, Any, Optional


def rolling_ma(d80: List[Dict[str, Any]], N: int = 20) -> List[Dict[str, Any]]:
    out = []
    for i, item in enumerate(d80):
        if i < N - 1:
            out.append({"t": item["t"], "ma": None})
            continue
        window = [d80[k]["prob"] for k in range(i - N + 1, i + 1)]
        out.append({"t": item["t"], "ma": sum(window) / N})
    return out


def rolling_std(d80: List[Dict[str, Any]], N: int = 20,
                ma_series: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    if ma_series is None:
        ma_series = rolling_ma(d80, N)
    out = []
    for i, item in enumerate(d80):
        if i < N - 1 or ma_series[i]["ma"] is None:
            out.append({"t": item["t"], "std": None})
            continue
        ma = ma_series[i]["ma"]
        window = [d80[k]["prob"] for k in range(i - N + 1, i + 1)]
        std = math.sqrt(sum((x - ma) ** 2 for x in window) / N)
        out.append({"t": item["t"], "std": std})
    return out


def band(ma_series: List[Dict[str, Any]], std_series: List[Dict[str, Any]],
         k: float = 2.0) -> List[Dict[str, Any]]:
    """
    返回同时带 upper / lower 的 band 序列。
    - 正 k 用于 D84 上轨,负 k 用于 D85 下轨(调用方用 band(..., k=+2) / band(..., k=-2))
    - 为方便 L5 一次性消费,此实现同时返回 upper / lower 便于统一 render
    """
    out = []
    for i, item in enumerate(ma_series):
        ma = item["ma"]
        std = std_series[i]["std"] if i < len(std_series) else None
        if ma is None or std is None:
            out.append({"t": item["t"], "upper": None, "lower": None})
        else:
            out.append({"t": item["t"], "upper": ma + k * std, "lower": ma - k * std})
    return out


if __name__ == "__main__":
    from datetime import datetime, timedelta, timezone
    base = datetime(2026, 4, 16, 12, 0, 0, tzinfo=timezone.utc)
    series = [
        {"t": (base - timedelta(hours=29 - i)).isoformat(),
         "prob": 0.60 + 0.02 * math.sin(i * 0.5)}
        for i in range(30)
    ]
    ma = rolling_ma(series, N=20)
    sd = rolling_std(series, N=20, ma_series=ma)
    bd = band(ma, sd, k=2.0)
    print("D82 末尾 ma:", round(ma[-1]["ma"], 4))
    print("D83 末尾 std:", round(sd[-1]["std"], 4))
    print("D84 末尾 upper:", round(bd[-1]["upper"], 4))
    print("D85 末尾 lower:", round(bd[-1]["lower"], 4))
