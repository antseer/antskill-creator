# G2 — 真源同步 + 路由审计 + 双 PRD · 质量门禁

## G2.1 真源同步（🔴）

- [ ] 已执行 `python3 scripts/sync_mcp_truth.py`
- [ ] `mcp-capability-map/cache/manifest.json` 存在
- [ ] 本轮远端 HEAD SHA 已记录到 `mcp-audit.md`

## G2.2 路由审计（🔴）

- [ ] inventory 每行都有归属
- [ ] 无 `待定`
- [ ] L1-A 条目有具体 Tool / 参数
- [ ] L3 条目有脚本位置
- [ ] L4 条目有 fallback

## G2.3 Data PRD（🔴）

- [ ] 所有 L1-B 条目进入 `data-prd.md`
- [ ] 所有 L2 条目进入 `data-prd.md`
- [ ] 每条有接口形态
- [ ] 每条有优先级
- [ ] 每条有降级策略

## G2.4 Skill PRD（🔴）

- [ ] `skill-prd.md` 按模块组织
- [ ] 每模块显式覆盖 L1-L5
- [ ] 附录 A 是字段唯一源
- [ ] 附录 B/C/D 已补齐

## G2.5 缺口不掩盖（🔴）

- [ ] 没把 L1-B / L2 偷偷塞进 L3；若有 L3 临时降级，`data-prd.md` 仍保留对应 L2 缺口和降级说明
- [ ] 所有缺口都能在 `data-prd.md` 找到
