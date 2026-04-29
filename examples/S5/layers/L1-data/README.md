# L1 · 数据接入层

> Skill 运行时从外部 MCP 工具取**原始数据**的层。不做加工,只调用。

## 责任
- 暴露 L1-A(已有 MCP 工具)给上层直接调用
- 记录 L1-B(缺失的 MCP 工具)作为后端补齐清单

## 交付物
| 文件 | 内容 |
|---|---|
| `mcp-required.md` | L1-A · 本 Skill 依赖的**已有** MCP 工具清单(工具名 / 入参 / 出参 / 使用模块) |
| `mcp-missing.md` | L1-B · 本 Skill 依赖的**待新建** MCP 工具,指向根目录 `data-prd.md` |

## 依赖
- 上游: Polymarket MCP、NewsAPI(DATA-01 后端补齐后接入)
- 下游: L3-compute(消费 L1 原始数据做计算)、L4-llm(消费 L1-B 新闻文本做摘要)
- 旁路: L5-presentation 不直接跨层消费 L1,必须经过 L3 或 L4

## 状态
- L1-A 可运行(Polymarket MCP 已接入)
- L1-B 待后端补齐 2 条(DATA-01 P0 · DATA-02 P2),详见 `mcp-missing.md`
