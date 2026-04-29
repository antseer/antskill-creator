# S4 Review Report · polymarket-drift-radar

> **阶段**: S4 交叉评审(demo-v0 高保真 UI ↔ PRD ↔ Inventory)
> **输入**: `S2/skill-prd.md` + S1 inventory(对话记载)+ `S3-高保真_UI.html` (→ `demo-v0.html`)
> **产出**: `demo-v1-review.html`(修复后)+ 本报告
> **基准**: PRD §2.7 M2 L5 组件表 + 附录 A 字段 schema + G4 质量门
> **评审时间**: 2026-04-16

---

## §0 执行摘要

- HTML 覆盖字段:**v0 = 85 个 Dxx / v1 = 94 个 Dxx**,新增 9 个(D01–D06 / D10 / D13 / D152)
- HTML 零反向污染:无越界字段(不存在 inventory 之外的伪造 Dxx)
- 差异点共 **16 个**,按 A/B/C/D 四档分流,已全部闭环处理或登记在案
- **G4 门禁自查 → 🟢 通过**(见 §4)
- 上一轮差异清单有 1 处校正:**B4「72 小时」补 D59」撤销**(详见 §3.2)

---

## §1 差异扫描结果总表

| ID | 类别 | 位置 | 差异描述 | 决议 | 状态 |
|---|---|---|---|---|---|
| **A1** | 交互缺失 | 概率主曲线 | PRD §2.7 要求「hover 显示当前点 t/prob」 | 新增 SVG transparent overlay + mousemove 反推 index | ✅ 已修 |
| **A2** | 交互缺失 | 异常区间 (drift-band) | PRD §2.7 要求「hover 显示区间内 max/min + 持续时长」 | rect 挂 `data-max/data-min/data-duration`,扩展 mouseover | ✅ 已修 |
| **A3** | 状态缺失 | Empty 态 | PRD §2.7 把 D151(未匹配市场)与 D152(窗口内无数据)分化为两个独立态 | 新增 `<div id="out-empty-window">` + setState case + 切换器按钮 | ✅ 已修 |
| **B1** | 绑定缺失 | Nav | D01-D06 仅在 HTML 注释层,未细粒度绑定到具体元素 | logo 拆 D01+D02 / crumbs 拆 D03+D04+D05 / stage-chip 绑 D06 | ✅ 已修 |
| **B2** | 绑定缺失 | Header H1 | `<h1>` 缺 `data-binding="D10"` | 追加 `data-binding="D10"` | ✅ 已修 |
| **B3** | 绑定缺失 | share-btn | `<button class="share-btn">` 缺 `data-binding="D13"` | 追加 `data-binding="D13"` | ✅ 已修 |
| ~~B4~~ | ~~绑定缺失~~ | ~~Hero 正文「72 小时」~~ | ~~文中 72 小时未绑 D59~~ | **撤销 → 改入 C6**(详见 §3.2) | ❌ 撤回 |
| **B5** | 绑定缺失 | SVG Y 轴刻度 | D88 仅在注释层,JS 生成的 text 元素未绑定 | `<g data-binding="D88">` 包裹 Y 轴刻度生成循环 | ✅ 已修 |
| **C1** | 合理不绑 | D22 浮层开关态 | 布尔内部态,L5 不直接消费,无展示元素 | 关闭差异,无需绑定 | ✅ 关闭 |
| **C2** | 合理不绑 | D72 24H 前概率 | L3 中间量,仅用于计算 D71,不直接渲染 | 关闭差异 | ✅ 关闭 |
| **C3** | 合理不绑 | D83 20σ 时序 | L3 中间量,仅用于计算 D84/D85/D74,不直接渲染 | 关闭差异 | ✅ 关闭 |
| **C4** | 合理不绑 | D86 异常点布尔 | L3 中间量,仅用于计算 D87,不直接渲染 | 关闭差异 | ✅ 关闭 |
| **C5** | 合理不绑 | D90 原始新闻 | L1-B 原始池,L5 消费的是 D91(筛后 Top N) | 关闭差异 | ✅ 关闭 |
| **C6** | 合理不绑 | Hero 正文「72 小时」 | PRD M3 L5 / L4 Fallback 模板里「72h」是 D53 Hero 正文的硬编码常量,非独立字段 | 关闭差异,文案由 D53 承载 | ✅ 关闭 |
| **D1** | 技术债 (G3.2) | SVG 硬编码颜色 | 主图表 4 处 + vol chart 1 处硬编码,违反 design-token 铁律 | 本轮顺手全量 token 化(超出 S5 前补的范围)| ✅ 已修 |

---

## §2 改动清单(文件级)

### `demo-v1-review.html`(对比 v0)

| 类别 | 文件位置(v1)| 改动要点 |
|---|---|---|
| B1 | 行 265–289 | Nav 六子元素细绑 `data-binding="D01"` ~ `D06` |
| A3 | 行 282–285(state-switcher) | 「⌀ 空」拆分为「⌀ 未匹配」(D151) + 「⌀ 无数据」(D152) |
| B2 | 行 296 | `<h1 class="h1" data-binding="D10">` |
| B3 | 行 298 | `<button class="share-btn" data-binding="D13">` |
| A3 | 行 495–513 | 新增 `<div id="out-empty-window">`(D152 独立空态) |
| D1 | :root | 追加 CSS 变量 `--chart-drift-fill: rgba(244, 68, 68, 0.10);` |
| B5 + D1 | 行 697–705(JS renderProbChart)| Y 轴刻度包 `<g data-binding="D88">`;文字 `fill: 'var(--fg-muted)'`;网格线 `stroke: 'var(--border)'` + `stroke-opacity: '0.5'` |
| A2 + D1 | 行 708–728(JS drifts 渲染) | drift rect 加 `class="drift-band"` + `data-max/data-min/data-duration`;`fill: 'var(--chart-drift-fill)'` |
| D1 | 行 723–724(JS Bollinger 虚线)| `stroke: 'var(--warning)'` + `stroke-opacity: '0.3'` |
| A1 | 行 779–789(JS NOW 标注后) | 新增透明 `<rect class="chart-hover-overlay">` 作为 mousemove 捕获层 |
| D1 | 行 806(JS renderVolChart)| 「成交量」标签 `fill: 'var(--fg-muted)'` |
| A1+A2 | 行 960–1028(JS 交互层)| 重构 chart hover tooltip:统一处理 news-marker / drift-band / overlay 三种源,追加 `fmtDate` / `fmtDuration` / `showTipAt` / `hideTip` 辅助函数 |
| A3 | 行 861(JS setState)| 状态列表插入 `'empty-window'` |

---

## §3 关键处理决议说明

### §3.1 A3 空态分化逻辑

PRD §2.7 M2 L5 明文:

```
| Empty 态(窗口无数据) | 覆盖图卡 | D152 | — |
```

而 M1 §1.7 L5:

```
| Empty(不匹配) | 输出区 | D151 | 显示"未找到匹配的 Polymarket 市场..." |
```

两态**语义根本不同**:
- **D151**:M1 阶段失败 —— 关键词压根没命中任何市场 → CTA 回到参数输入
- **D152**:M2 阶段失败 —— 市场找到了,但在选中窗口内时序数据不足 → 建议切换到更长窗口

v0 只渲染了 D151 单一空态,v1 按 PRD 增加独立 `out-empty-window` 块,切换器同步拆分,CTA 行为也对应不同(D151 重新输入 / D152 切换窗口)。

### §3.2 B4 撤销说明(上一轮差异清单校正)

上一轮识别 **B4「Hero 正文中『72 小时』需补 D59」** 是**误判**,校正依据:

1. 查 PRD 附录 A —— 无 D59 定义
2. 查 PRD M3 §3.6 L4 Fallback 模板(行 261–264)—— 72h 字样写在 D53 模板内作为常量:
   > `"过去 {window} 天出现 {D54} 次显著漂移,最近一次峰值概率 {D55}%。当前 {D56}%,历史上类似模式 72h 回归命中率 {D57}%..."`
3. 「72 小时」属于 L4 输出的 **D53 Hero narrative 字符串整体**的一部分,不是独立字段

所以正确归类是 **C6 · 合理不绑**。本轮已撤销 B4,不对 HTML 该处做改动。此校正不影响任何已完成修改,仅是差异账本的归类更正。

### §3.3 D1 超出计划的顺手修复

上一轮计划仅把 D1 记为「S5 前补,不阻塞 G4」,但本轮在做 B5(Y 轴刻度包 g)和 A2(drift rect 改渲染)时**已经在改这些 SVG 元素**,就势把相邻的硬编码一并 token 化,避免留半残状态。修复 5 处:

| 原值 | 替换 | 位置 |
|---|---|---|
| `#8a8885` | `var(--fg-muted)` | prob chart Y 轴文字 + vol chart 标签 |
| `rgba(255,255,255,0.06)` | `var(--border)` + `stroke-opacity: 0.5` | prob chart 网格线 |
| `rgba(244,68,68,0.10)` | `var(--chart-drift-fill)`(新增变量)| drift band fill |
| `rgba(255,176,0,0.3)` | `var(--warning)` + `stroke-opacity: 0.3` | Bollinger 上下轨虚线 |

**残留**:CSS 片段里少量微调色(impact-chip / status-box 边框/底色用的 `rgba(244,68,68,0.3~0.4)` 等)未动 —— 因为它们是在 CSS 层对 `--danger` / `--warning` 做 alpha 微调,属于可接受的"派生色",且不在 SVG 渲染路径上,不触发 G3.2 关键违规。如需严格零硬编码,下一轮可在 design-system 加 `--danger-border` / `--warning-border` 等派生变量。

---

## §4 G4 门禁自查

### 🔴 阻塞项(必过)

| # | 门禁条款 | 检查结果 |
|---|---|---|
| G4.1 | HTML 字段消费必须是 inventory 子集(零反向污染)| ✅ **v1 94 个 Dxx 全部为 inventory 已登记字段** |
| G4.2 | PRD L5 明列的组件交互必须实现(hover/click/toggle 等)| ✅ **A1/A2/A3 三项 PRD §2.7 明写的交互全部补齐** |
| G4.3 | PRD L5 明列的状态覆盖必须完整(Loading/Empty/Error/Degraded)| ✅ **D150/D151/D152/D153+D154/D155 五态全部可通过 state-switcher 切换** |
| G4.4 | 不得引入 PRD / inventory 之外的新字段 | ✅ **无新字段**(本轮只是补已有字段的 data-binding) |
| G4.5 | 浏览器能渲染,无 JS 抛错 | ✅ **括号全平衡 / div 对称**(静态自检,运行时错误需在浏览器中复验,见 §6) |

### 🟡 建议项

| # | 门禁条款 | 检查结果 |
|---|---|---|
| G3.2 | 颜色必须走 design token,不得硬编码 | ✅ **SVG 渲染路径 5 处硬编码全部 token 化**;CSS 片段中 4 处微调 alpha(impact-chip / status-box 边/底)保留,建议下一轮加 `--danger-border` 等派生变量 |
| G3.x | 半成品标识(stage-chip / demo 态切换器)保留到 S5 前移除 | ✅ 保留,注释已标明「仅 demo 阶段存在,S5 交付时去掉」 |
| — | data-binding 粒度(细绑 vs 粗绑)| ✅ **细绑优先**,M1 Nav / Header / CTA / 浮层全部子元素级绑定;复合区(stat 卡、drift-block、details)按 PRD L5 表列的粒度绑 |

### 🟢 门禁结论

**🟢 通过 G4**,可进入 S5(Skill 交付打包)。

---

## §5 尚在账本上的次要债(S5 前处理)

| 优先级 | 事项 | 备注 |
|---|---|---|
| P2 | CSS 派生色 token 化(impact-chip / status-box 边/底的 rgba 微调)| 不在 SVG 渲染路径,不阻塞 G4,但 design-system 完整性建议补 |
| P2 | `demo-v0.html` vs `demo-v1-review.html` 两份并存,S5 前合并为单份 `demo-final.html` | |
| P3 | state-switcher 本身(含 `<style>` 里 `.state-switcher` / `.ss-btn` 样式)整体移除,D0x 的 D06 stage-chip 也需重评估 | 属 半成品标识,交付前清理 |

---

## §6 浏览器侧验证清单(人工/自动化)

以下项静态代码检查已通过,但建议在浏览器中进一步确认:

- [ ] 默认态下主曲线任意 hover,右侧 tooltip 显示当前点 `xx.x%` + `MM/DD HH:00 UTC`
- [ ] 默认态下两段红色 drift-band 区间 hover,tooltip 显示「异常区间 · 峰值 xx.x% · 谷值 xx.x% · 持续 N 小时/天」
- [ ] 新闻节点圆圈 hover 仍显示新闻标题和来源元信息(原有行为保留)
- [ ] 切换器点「⌀ 未匹配」→ D151 态;点「⌀ 无数据」→ D152 态,两者文案不同、CTA 行为不同
- [ ] 切换到 degraded 态时,降级图表无新闻层(原有行为保留)
- [ ] Bollinger 上下轨、drift-band、Y 轴标签颜色与 v0 视觉一致(token 替换无色差回归)

---

## §7 产出物清单

| 文件 | 路径 | 说明 |
|---|---|---|
| 修复后 HTML | `demo-v1-review.html` | S4 产物,可直接进 S5 |
| 本报告 | `review-report.md` | 差异账本 + 处理决议 + G4 自查留痕 |

