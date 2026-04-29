# L5 · 前端展示层

> 把 L1-A / L3 / L4 产出的数值和字符串渲染成用户可见的 UI。纯展示,不做计算加工。

## 责任
- 承载 `frontend/index.html` 的渲染逻辑
- 维护一张组件 ↔ 上游数据层映射表(`component-map.md`),供后端续写时快速定位每个组件的数据来源
- 纯视觉派生(颜色映射、归一化 bar 宽度等)在 L5 内就地完成,不占 L3/L4 名额

## 交付物

| 文件 | 内容 |
|---|---|
| `../../frontend/index.html` | 高保真前端(S4 通过的 `demo-v1-review.html`)|
| `component-map.md` | 每个可见动态组件一条,含 位置 / 消费字段 / 来源层 / 交互 |

## 依赖
- 上游:L1-A(D12 认证状态等容器注入)/ L3(D70–D87 / D43 / D106 / D120 等) / L4(D51–D53 / D122 / D123)
- 旁路:不允许消费 PRD 附录 A / inventory 之外的字段(G4.1 / G5.8 硬约束)

## 状态
- `frontend/index.html` 已通过 S4 · G4 门禁(见根目录 `review-report.md` §4)
- component-map 覆盖 HTML 中所有 `data-binding` 标注的组件 + 5 个状态块

## 关键交互清单(与 `component-map.md` 对齐)

1. 主 CTA → 打开参数浮层(D22 浮层态)
2. 浮层 pill → 切换 D36 时间窗口,联动 Meta chip + chart 标题
3. 浮层子 CTA → 触发 `runtime.execute(D39)`,切 Loading → Default
4. 概率主曲线 hover → tooltip 显示当前点 t / prob(**S4 新增**)
5. 异常区间 hover → tooltip 显示 max / min / 持续时长(**S4 新增**)
6. 新闻节点圆圈 hover → tooltip 显示标题 + 来源
7. 新闻列表条目 click → 跳转 D109 外链(demo 态阻止真跳)
8. 信任层三个 details click → 折叠/展开
9. State-switcher(半成品态) → 切 default / loading / empty (D151) / empty-window (D152) / error / degraded 六态
