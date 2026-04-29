"""
模块: M2 · 漂移分析(新闻节点部分)
对应数据点: D91 (Top N 筛后新闻) · D93 (新闻序号编号)
输入:
  d90: list[dict]            # 按市场的新闻原始列表(来自 L1-B · DATA-01 · ant_news.by_market)
                             # 每项 schema: {t, title, source, url, impact, summary?, category?}
  d87: list[dict]            # 异常区间分段(D87 · 来自 drift.py)
  n:   int = 3               # Top N
输出:
  D91: list[dict]            # 筛后新闻,保留 d90 原字段 + 注入 aligned_drift_index?
  D93: list[int]             # 按 t 升序的 1..N 编号
逻辑:
  1. 对每条 news,判断其 t 是否落在某 d87 区间内,记录 aligned_drift_index
  2. 优先保留"对齐到 d87 区间的 news",其次按 impact(high > mid > low)排序
  3. 取前 n 条
  4. 按 t 升序编号 1..N
状态: 🚧 壳子 + TODO
  - 依赖 L1-B · DATA-01 (ant_news.by_market) 落地后才能有真数据喂入
  - 未落地时:前端走 D155 降级态,本函数接受空列表 → 返回空列表,不阻塞整条管线
  - 待 DATA-01 落地后(阶段 2):
    * 实现 IMPACT_RANK 比较
    * 实现 aligned_drift_index 注入(二分或线性)
    * 补 tests/test_news.py
"""

from typing import List, Dict, Any
from datetime import datetime

IMPACT_RANK = {"high": 3, "mid": 2, "low": 1}


def _parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def pick_top_n(d90: List[Dict[str, Any]],
               d87: List[Dict[str, Any]],
               n: int = 3) -> List[Dict[str, Any]]:
    """
    D91 · 筛后新闻 Top N

    TODO(DATA-01): 真实逻辑需等 ant_news.by_market 落地后才能 end-to-end 调试。
    当前壳子保证:
      - d90=[] 时返回 [](对应前端降级态 D155)
      - d90 非空时返回前 n 条按 impact 降序 + t 升序的结果,暂不处理 d87 对齐
    """
    if not d90:
        return []

    # 临时排序策略(MVP):impact 降序 → t 升序
    # 待实现的完整策略见文件头 logic 段
    sorted_news = sorted(
        d90,
        key=lambda x: (-IMPACT_RANK.get(x.get("impact", "low"), 0), x.get("t", ""))
    )
    return sorted_news[:n]


def number_by_time(d91: List[Dict[str, Any]]) -> List[int]:
    """D93 · 按 t 升序编号 1..N(传入的 d91 无序时内部重排)"""
    if not d91:
        return []
    ordered = sorted(range(len(d91)), key=lambda i: d91[i].get("t", ""))
    # 返回一个跟 d91 原顺序等长的编号数组:d91[k] 的编号是 rank_of(k)+1
    rank = [0] * len(d91)
    for r, idx in enumerate(ordered):
        rank[idx] = r + 1
    return rank


if __name__ == "__main__":
    # 验证空输入不崩
    assert pick_top_n([], [], n=3) == []
    assert number_by_time([]) == []

    # 验证非空 mock
    mock_news = [
        {"t": "2026-04-13T16:00:00Z", "title": "Fundraising disclosure", "impact": "mid"},
        {"t": "2026-04-08T09:00:00Z", "title": "Swing-state address",    "impact": "high"},
        {"t": "2025-11-15T14:00:00Z", "title": "Court ruling",           "impact": "high"},
        {"t": "2026-04-01T00:00:00Z", "title": "Low-impact tweet",       "impact": "low"},
    ]
    top = pick_top_n(mock_news, d87=[], n=3)
    print("Top 3:", [t["title"] for t in top])
    print("序号:", number_by_time(top))
    print("(当前为壳子;真正对齐 D87 区间的逻辑待 DATA-01 落地后实现)")
