# L3 · Skill 脚本计算

> Skill 特有的、不适合放 MCP 聚合的计算:滚动窗口指标、异常分段、格式化、取值引用。

## 责任
- 从 L1-A 原始数据派生数值指标(D70–D87 等)
- 把时序切片、字符串化、编号,供 L4/L5 直接消费
- 降级场景:若 L1-B(DATA-01)未落地,`news.py` 走 TODO 壳子路径

## 交付物

| 脚本 | 函数 | 对应 Dxx | 状态 |
|---|---|---|---|
| `parse.py` | `url_to_market_id` | 辅(M1) | ✅ 可运行 |
| `extract.py` | `take_last` · `point_at` | D70 · D72 · D58 | ✅ 可运行 |
| `delta.py` | `delta` | D71 | ✅ 可运行 |
| `volatility.py` | `std_window` | D73 | ✅ 可运行 |
| `bollinger.py` | `rolling_ma` · `rolling_std` · `band` | D82 · D83 · D84 · D85 | ✅ 可运行 |
| `zscore.py` | `compute` | D74 | ✅ 可运行 |
| `agg.py` | `sum_volume` | D75 | ✅ 可运行 |
| `drift.py` | `mark_anomaly` · `segment_anomaly` · `count_segments` · `peak_of_last` | D86 · D87 · D54 · D55 | ✅ 可运行 |
| `volume.py` | `mark_in_drift` | D95 | ✅ 可运行 |
| `format.py` | `format_timestamp` · `relative_time` · `conclusion_question` | D43 · D106 · D120 | ✅ 可运行 |
| `news.py` | `pick_top_n` · `number_by_time` | D91 · D93 | ⚠️ **壳子+TODO**(依赖 DATA-01 落地) |

共 11 个脚本,覆盖 PRD §2.5 全部 L3 条目。

## 依赖
- 上游: L1-A (`price_history` 返回 D80/D81 原始时序);L1-B 未落地时 `news.py` 接受空列表
- 下游: L4-llm 消费 `{D70, D74, D73, D87_len, ...}`;L5-presentation 直接消费 D70/D71/D73/D74/D75/D43 等

## 状态
10 个可运行 · 1 个壳子+TODO(`news.py`,等 DATA-01 落地)

## 可运行脚本的验证方式

每个脚本 `if __name__ == '__main__':` 块内有 mock 输入示例,直接 `python3 <script>.py` 即可观察输出合法性。
