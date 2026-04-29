# Layer README 模板

> 在 Skill 半成品交付(S5)时,`layers/L1-data/` `layers/L2-aggregation/` `layers/L3-compute/` `layers/L4-llm/` `layers/L5-presentation/` 每个子目录都要放一份 README.md。
> 下面给出每层的填写模板,直接按对应模板复制填充。

---

## layers/L1-data/README.md

```markdown
# L1 · 数据接入层

## 本层职责
从 MCP 拉取原始数据。本 Skill 不对此层做任何加工,只负责调用。

## 责任方
- L1-A: Skill 运行时直接调 MCP(后端已实现工具)
- L1-B: **后端**(需新建 MCP 原始工具,见 mcp-missing.md)

## 交付物
- `mcp-required.md` — L1-A 已有工具清单 + 入参出参
- `mcp-missing.md` — L1-B 缺口指针(→ 根目录 data-prd.md)

## 消费下游
- L3 脚本读 L1-A 的出参做派生计算
- L4 prompt 直接引用 L1-A / L1-B 的字段
- L5 组件偶尔直接消费 L1-A(如标签、ID 列表)

## 本 Skill 涉及
- L1-A: ✅ 涉及
- L1-B: ✅ 涉及(1 条 DATA-01 P0)

或

- L1-A: ✅ 涉及
- L1-B: ❌ 不涉及,原因:本 Skill 所需原始数据 MCP 均已提供
```

---

## layers/L2-aggregation/README.md

```markdown
# L2 · MCP 新建聚合接口层

## 本层职责
跨实体 / 跨时间 / 跨维度的聚合计算。成本高、应缓存、多 Skill 复用 → 应做成 MCP 接口而非 Skill 脚本。

## 责任方
**后端**(需新建 MCP 聚合接口,见 interfaces.md)

## 交付物
- `interfaces.md` — L2 缺口指针 + 降级路径

## 消费下游
- L3 脚本直接消费 L2 聚合结果
- L4 prompt 偶尔直接引用
- L5 偶尔直接展示(如趋势小图)

## 本 Skill 涉及
- L2: ✅ 涉及(1 条 DATA-02 P1,含降级路径)

或

- L2: ❌ 不涉及,原因:本 Skill 无跨时间/跨实体聚合需求
```

---

## layers/L3-compute/README.md

```markdown
# L3 · Skill 脚本计算层

## 本层职责
本 Skill 私有的轻量计算。滚动窗口、派生字段、归一化、排序等。每次请求实时跑。

## 责任方
**Skill 开发者**(PM 已交付可运行脚本或壳子+TODO)

## 脚本状态约定

每个 .py 头部注释必须有"状态"字段:
- `状态: 可运行` — 函数已实现,有基本测试可跑通
- `状态: 壳子+TODO` — 函数签名完整,body 是 TODO + 临时占位返回值,blocked 原因写清楚

## 交付物

| 文件 | 状态 | 对应 Dxx | Blocked By |
|---|---|---|---|
| `bollinger.py` | 可运行 | D31, D32 | — |
| `volatility.py` | 可运行 | D13 | — |
| `delta.py` | 可运行 | D11 | — |
| `extract.py` | 可运行 | D10, D12 | — |
| `sentiment_score.py` | 壳子+TODO | D52(辅助) | DATA-01 (ant_news.by_market) |

## 单测
见 `tests/` (若范式 A/C 要求)

## 本 Skill 涉及
- L3: ✅ 涉及

或

- L3: ❌ 不涉及,原因:所有派生计算都是跨时间聚合(归 L2)或自然语言(归 L4)
```

---

## layers/L4-llm/README.md

```markdown
# L4 · LLM 结构化层

## 本层职责
需要大模型做自然语言生成 / 主观判断 / 结构化解读的数据。

## 责任方
**Skill 开发者**(PM 已交付 prompt + 输入输出 schema + Fallback)

## Prompt 文件必包含 5 段
1. 模块与数据点(归属哪个模块 Mx,产出哪个 Dxx)
2. 输入 Schema(TypeScript 或 JSON Schema)
3. 输出 Schema
4. Prompt 正文(含至少 1 个 few-shot 示例)
5. **Fallback 模板函数**(LLM 不可用时的降级,输出 schema 必须与 LLM 正常输出一致)

## 铁律
**无 Fallback 的 prompt 禁止交付,门禁会查。**

## 交付物

| 文件 | 对应 Dxx | Fallback 策略 |
|---|---|---|
| `hero-verdict.md` | D05 | 按 D51 映射固定短语 |
| `drift-summary.md` | D50 | 按 Z-Score 分级模板化 |
| `state-guidance.md` | D51 | 按 risk_level 硬映射 |
| `risk-notes.md` | D52 | 固定 2-3 条通用提示 |

## Eval
见 `<name>.eval.md`(若已交付)

## 本 Skill 涉及
- L4: ✅ 涉及

或

- L4: ❌ 不涉及,原因:本 Skill 所有输出均为结构化数据,无自然语言需求
```

---

## layers/L5-presentation/README.md

```markdown
# L5 · 前端展示层

## 本层职责
HTML / CSS / JS 组件,消费上游各层数据并渲染。

## 责任方
**Skill 开发者**(PM 已交付 `frontend/index.html` + `component-map.md`)

## 铁律
**L5 不得自造数据**。每个动态字段必须追溯到 L1-A / L1-B / L2 / L3 / L4 的某个 Dxx。

## 交付物
- `../../frontend/index.html` — 高保真前端定稿,已过 G3 + G4 门禁
- `component-map.md` — **每个组件一条**,映射到上游数据层

## component-map.md 字段
| 组件 | 位置 | 消费字段(Dxx) | 来源层 | 交互行为 |

## 数据契约
HTML 里每个动态字段必须对应 PRD 附录 A 中的 Dxx。契约不符 = G5 门禁不过。

## 视觉登记
已登记于 `design-system/visual-registry.md`,主色 / Display 字体 / Hero 类型与所有已有 Skill 显著不同。

## 本 Skill 涉及
- L5: ✅ 涉及(所有 Skill 都有 L5)
```

---

## 共同自查

每份 README 必须包含:
- [ ] 本层职责(一句话)
- [ ] 责任方(PM / 后端 / Skill 运行时)
- [ ] 交付物清单
- [ ] 本 Skill 涉及本层与否(显式声明,不涉及要写原因)
