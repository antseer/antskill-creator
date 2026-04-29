# S2 — MCP 真源同步 + 路由审计 + 双 PRD

## 阶段目标

1. 同步 MCP 真源并记录本轮远端 HEAD SHA
2. 产出 `mcp-audit.md`
3. 产出 `data-prd.md`
4. 产出 `skill-prd.md`

## 核心原则

- **先同步真源，再判路由**
- **双 PRD 分工明确**
  - `data-prd.md`：给研发 / 后端 / MCP 团队
  - `skill-prd.md`：给 PM / 产品自己做 Skill
- **L1-B / L2 缺口不能塞进 L3 掩盖**。唯一例外：L1 原始数据已真实覆盖、L3 只是临时性能降级，且 `data-prd.md` 继续登记该 L2 缺口。

## 执行步骤

### Step 1：同步 MCP 真源

运行：

```bash
python3 scripts/sync_mcp_truth.py
```

必须拿到：

- `mcp-capability-map/cache/manifest.json`
- `mcp-capability-map/cache/MCP-Data-Capabilities.md`
- `mcp-capability-map/cache/MCP-Tools-Reference.md`
- `mcp-capability-map/cache/MCP-Tools-Query-Type-Mapping.md`

若远端不可达但已有已验证缓存，可继续；否则停止。

### Step 2：产出路由审计

对 `data-inventory.md` 每个数据点判：

- `L1-A`
- `L1-B`
- `L2`
- `L3`
- `L4`
- `L5`
- `INPUT`
- `STATIC`

输出 `mcp-audit.md`。

### Step 3：产出 Data PRD

把所有 `L1-B` / `L2` 条目写入 `data-prd.md`，每条必须包含：

- 对应数据点
- 调用场景
- 期望接口形态
- 优先级
- 降级策略
- 验收口径

### Step 4：产出 Skill PRD

按功能模块组织 `skill-prd.md`。

每个模块必须显式覆盖：

- `L1`
- `L2`
- `L3`
- `L4`
- `L5`

不涉及的层也必须写明原因。

## 产出物

| 文件 | 用途 |
|---|---|
| `mcp-audit.md` | 路由审计 |
| `data-prd.md` | 研发 MCP 数据提需 |
| `skill-prd.md` | PM / 产品开发 Skill 说明书 |

## 失败模式

- 没同步真源就开始判路由
- 只有 `skill-prd.md` 没有 `data-prd.md`
- 把 L1-B / L2 偷偷降级成 L3
- `skill-prd.md` 只写页面，不写 L1-L5
