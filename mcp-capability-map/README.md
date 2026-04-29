# MCP Capability Map

S2 的路由基准只认两样东西：

- `cache/manifest.json`
- `routing-decision-tree.md`

## 使用顺序

1. 先跑 `python3 scripts/sync_mcp_truth.py`
2. 读 `cache/manifest.json`
3. 以缓存后的真源文档做本轮判定

## 目录

- `cache/`：远端真源缓存
- `routing-decision-tree.md`：L1-A / L1-B / L2 / L3 / L4 / L5 判定树

如果远端不可达且没有已验证缓存，就停止 S2。

