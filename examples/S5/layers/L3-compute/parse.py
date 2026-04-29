"""
模块: M1 · 市场识别
对应数据点: 辅助 D32(事件输入归一化)
输入:
  user_input: str  # 用户在浮层输入框的内容(polymarket URL 或关键词)
输出:
  q: str           # 规范化后的查询串,传给 ant_polymarket.search_markets 的 q 参数
  is_url: bool     # 是否识别为 URL(影响上游是否还需要走 search 兜底)
逻辑:
  - 若输入是 polymarket.com 的 event URL,提取 slug 作为 q(将来 DATA-02 落地时直接返回 market_id)
  - 否则原样作为 q
状态: 可运行(regex 实现,为 DATA-02 未落地时的前端兜底路径)
"""

import re

POLYMARKET_EVENT_RE = re.compile(r"polymarket\.com/event/([^/\?#]+)", re.IGNORECASE)


def url_to_market_id(user_input):
    """
    返回 (q, is_url)
    - 若 user_input 命中 polymarket.com/event/<slug>,返回 (slug, True)
    - 否则返回 (user_input.strip(), False)
    """
    if not user_input:
        return "", False
    m = POLYMARKET_EVENT_RE.search(user_input)
    if m:
        slug = m.group(1)
        # slug 形如 "will-trump-win-the-2024-election"
        # 转成可搜索的自然语言关键词
        return slug.replace("-", " "), True
    return user_input.strip(), False


if __name__ == "__main__":
    cases = [
        "Will Trump win the 2024 election?",
        "https://polymarket.com/event/will-trump-win-the-2024-election",
        "polymarket.com/event/fed-rate-cut-march-2026?utm=xxx",
        "",
    ]
    for c in cases:
        print(repr(c), "→", url_to_market_id(c))
