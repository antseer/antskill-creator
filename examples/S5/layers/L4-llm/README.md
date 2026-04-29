# L4 · LLM 结构化层

> 把 L1-A + L3 + L2 的数值/字符串材料,通过 prompt 转成**结构化的自然语言**(结论、副标题、Hero 正文、漂移详解、命中率叙述)。

## 责任
- 为每个需要 LLM 润色的 Dxx 提供 prompt 文件
- **每个 prompt 必须有 Fallback 模板函数**,保证 LLM 不可用时 Skill 仍可运行
- Fallback 输出的 schema 必须与 LLM 正常输出的 schema 一致

## 交付物

| Prompt | 产出数据点 | 模块 | Fallback 类型 |
|---|---|---|---|
| `verdict.md` | D51(结论关键词)+ D52(副标题)| M3 · 解读与建议 | Z-Score 硬阈值映射 |
| `hero-narrative.md` | D53(Hero 正文 2-3 句) | M3 | risk_level × 有无 D57 四套模板 |
| `drift-narrative.md` | D122(漂移详解段落) | M4 · 信任层 | 每个 D87 区间生成固定句式 |
| `hit-rate-narrative.md` | D123(历史命中率段落)| M4 | 无 DATA-03 时通用 Bollinger 方法论描述 |

## 依赖
- 上游:
  - L3:`drift.py`(D87/D54/D55)/`zscore.py`(D74)/`volatility.py`(D73)/`extract.py`(D70/D58)
  - L1-B(通过 L3 `news.py`)/ L2(DATA-03 · D57)
- 下游: L5 前端直接渲染 D51 / D52 / D53 / D122 / D123 字段,不做二次加工

## 状态
- 4 个 prompt 全量交付,含 Fallback 模板函数
- 一旦 L4 服务可用,可直接运行;LLM 不可用时 Fallback 保证 Skill 不阻塞
- **DATA-03 未落地时**:`hero-narrative.md` 和 `hit-rate-narrative.md` 走 Fallback 的「无 D57」分支

## 规范检查

- [x] 每个 prompt 5 段齐全(模块与数据点 / 输入 Schema / 输出 Schema / Prompt 正文 / Fallback 模板函数)
- [x] 每个 prompt 正文含 ≥ 1 个 few-shot 示例
- [x] 每个 Fallback 返回与 LLM 正常输出 schema 一致
- [x] Fallback 函数纯 Python,不依赖外部 LLM / 网络
