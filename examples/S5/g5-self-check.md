# G5 · Skill 半成品交付门禁自查

> **对应 SOP**: `sop/s5_skill_delivery.md`
> **对应门禁**: `quality/G5_skill_delivery.md`
> **自查时间**: 2026-04-16
> **交付包**: `polymarket-drift-radar/` · v0.1.0 · semi-finished

---

## 🔴 Critical 项(必过)

### G5.1 · 工程目录结构
- ✅ 根目录包含:`SKILL.md` / `VERSION` / `skill-prd.md` / `data-prd.md` / `mcp-audit.md`(附赠)/ `review-report.md` / `frontend/` / `layers/`
- ✅ `layers/` 下 5 个子目录:`L1-data / L2-aggregation / L3-compute / L4-llm / L5-presentation`
- ✅ 每个 layers 子目录有 `README.md`
- ✅ 不涉及的层:本 Skill 四层都涉及,无需显式"不涉及"声明

**→ G5.1 通过**

### G5.2 · 交付版 SKILL.md
- ✅ frontmatter YAML 合法(已 yaml.safe_load 验证,见下方 §自动化验证)
- ✅ 含 `name / version / status: semi-finished / description`
- ✅ `layers` 字段列出 L1-A / L1-B / L2 / L3 / L4 / L5 具体条目
- ✅ `mcp_gap_summary` 汇总 `P0: 1 / P1: 1 / P2: 1`
- ✅ description 含 **2 个触发示例**(非泛泛介绍)
- ✅ 正文含「分层设计概述 / MCP 依赖 / 后端续写入口」三段

**→ G5.2 通过**

### G5.3 · L1-data 层
- ✅ `mcp-required.md` 列 4 条 L1-A 工具 + 入参 + 出参 + 使用模块
- ✅ `mcp-missing.md` 指向 `data-prd.md` 的 DATA-01 / DATA-02
- ✅ `data-prd.md` 每个 L1-B 条目含完整期望接口(endpoint / 入参表 / 出参 schema / 刷新频率 / 鉴权 / 实现建议)
- ✅ 每个 L1-B 条目含降级策略(前端表现 + L3/L4 兜底 + 用户感知)

**→ G5.3 通过**

### G5.4 · L2-aggregation 层
- ✅ `interfaces.md` 指向 `data-prd.md` 的 DATA-03
- ✅ DATA-03 含期望接口形态
- ✅ 含降级路径表("L3 无法兜底 / L4 完全兜底 / 说服力下降但不影响可用性")

**→ G5.4 通过**

### G5.5 · L3-compute 层
- ✅ 11 个 .py 文件覆盖 PRD §2.5 全部 L3 条目
- ✅ 每个脚本头部五段注释齐全(模块 / 输入 / 输出 / 逻辑 / 状态)
- ✅ 10 个可运行脚本的 `__main__` 均产出合法输出(见下方 §自动化验证)
- ✅ 1 个壳子(`news.py`)函数签名完整 / TODO 明确 / 返回 mock 值不阻塞前端
- ✅ 脚本依赖的 Dxx 均在 PRD 附录 A 中存在

**→ G5.5 通过**

### G5.6 · L4-llm 层
- ✅ 4 个 .md 文件对应 4 个 L4 数据点(D51/D52 联产 + D53 + D122 + D123)
- ✅ 每个 prompt 含 5 段:模块与数据点 / 输入 Schema / 输出 Schema / Prompt 正文 / Fallback 模板函数
- ✅ **Fallback 模板函数全部非空**,且 schema 与 LLM 输出一致
- ✅ Prompt 正文均含 few-shot 示例
- ✅ DATA-01 / DATA-03 缺失时的降级分支在 Fallback 里有显式实现

**→ G5.6 通过**

### G5.7 · L5-presentation 层
- ✅ `frontend/index.html` 存在,是 S4 通过的 `demo-v1-review.html` 的直接拷贝
- ✅ `component-map.md` 存在 · 每组件一条 · 含位置 / 消费字段 / 来源层 / 交互 · 覆盖所有可见动态组件
- ✅ 每个 Dxx 均可追溯到 L1 / L2 / L3 / L4 或标为 STATIC / INPUT

**→ G5.7 通过**

### G5.8 · 端到端可追溯
抽 5 个 L5 组件向上追溯,每一级都能在 layers/ 中找到对应文件:

| L5 组件 | 消费 Dxx | L4 | L3 | L2/L1 |
|---|---|---|---|---|
| 结论关键词(Hero 左上)| D51 | `L4/verdict.md` | - | 输入:D70/D74/D73/D87_len ← L3 bollinger+drift+zscore |
| 当前概率 stat | D70 | - | `L3/extract.take_last` | D80 ← L1-A `price_history` |
| 24H 变化 stat | D71 | - | `L3/delta.delta` | D70+D72 ← L3 extract ← L1-A |
| 异常区间红色覆盖 | D87 | - | `L3/drift.segment_anomaly` | D80/D84/D85 ← L1-A + L3 bollinger |
| 新闻节点竖线 | D91 | - | `L3/news.pick_top_n`(壳子)| **D90 ← L1-B DATA-01**(已登记断点)|

- ✅ 抽样 5 条均可追溯;唯一"断点"是已登记的 L1-B DATA-01 / L2 DATA-03

**→ G5.8 通过**

### G5.9 · 半成品声明
- ✅ `VERSION` = `0.1.0`
- ✅ `SKILL.md` frontmatter `status: semi-finished`
- ✅ `data-prd.md` 头部第一行:**"本 Skill 为半成品,以下接口需后端补齐后 Skill 方可完整运行。"**

**→ G5.9 通过**

---

## 🟡 Important 项

### G5.10 · 配套文件
- ✅ `skill-prd.md` 从 S2 带入,内容与 S4 review 通过版一致(未修改)
- ✅ `review-report.md` 从 S4 带入
- ✅ `data-prd.md` 从 S2 带入,含 P0/P1/P2 完整分级
- ✅ 附赠 `mcp-audit.md`(S2 Part A 产物,便于后端追溯路由判定)
- ⚠️ `tests/` 目录缺失 —— 本 Skill 为范式 B,Skill Card 无明确单测要求;L3 脚本的 `__main__` 块承担了冒烟测试角色

**→ G5.10 通过**(可选项,tests/ 缺失不影响交付)

---

## 自动化验证留痕

```
# 1. YAML frontmatter 合法
$ python3 -c "import yaml; print('ok' if yaml.safe_load(open('SKILL.md').read().split('---')[1]) else 'fail')"
ok

# 2. L3 脚本全部可跑
$ for f in layers/L3-compute/*.py; do python3 "$f" >/dev/null 2>&1 && echo "$f: ok" || echo "$f: FAIL"; done
layers/L3-compute/agg.py: ok
layers/L3-compute/bollinger.py: ok
layers/L3-compute/delta.py: ok
layers/L3-compute/drift.py: ok
layers/L3-compute/extract.py: ok
layers/L3-compute/format.py: ok
layers/L3-compute/news.py: ok
layers/L3-compute/parse.py: ok
layers/L3-compute/volatility.py: ok
layers/L3-compute/volume.py: ok
layers/L3-compute/zscore.py: ok

# 3. L4 Fallback 全部可跑(提取 code block 后 exec)
见 S5 交付对话记录,4/4 通过并产出预期 schema

# 4. 前端 HTML 包含所有关键 data-binding
$ grep -oE 'data-binding="[^"]+"' frontend/index.html | grep -oE 'D[0-9]+' | sort -u | wc -l
94
```

---

## 门禁结论

**🟢 G5 全部通过** · 可打包交付后端续写。

### 后端接手后的首个工作项建议

1. 启动 DATA-01 MCP 工具实现(P0,1-2 周)
2. 并行启动 DATA-03 历史统计预计算(P1,可与 DATA-01 解耦)
3. DATA-01 落地后,把 `layers/L3-compute/news.py` 的 mock 分支替换为真实调用
4. 交付到 Skillhub 时,去掉 `frontend/index.html` 的 state-switcher(demo-only 控件),并把 D06 `stage-chip` 文案从"demo-v1"改为"v0.1.0"
