# {{SKILL_NAME}} — Visualization Specifications

> 可视化像素规范：每个组件的尺寸、颜色编码、排版规则。SoT 优先级第 7 位。

---

## 1. 全局设计 Token

### 颜色

| Token | 值 | 用途 |
|-------|------|------|
| `--bg-primary` | `#0a0a0f` | 主背景 |
| `--bg-card` | `#13131a` | 卡片背景 |
| `--bg-card-hover` | `#1a1a24` | 卡片悬停 |
| `--text-primary` | `#e8e8ed` | 主文字 |
| `--text-secondary` | `#8a8a9a` | 次文字 |
| `--text-muted` | `#55556a` | 弱文字 |
| `--accent` | `{{主色}}` | 主色调 |
| `--accent-dim` | `{{主色 30% opacity}}` | 主色弱化 |
| `--border` | `#1e1e2a` | 边框 |
| `--success` | `#22c55e` | 正面 |
| `--warning` | `#f59e0b` | 警告 |
| `--danger` | `#ef4444` | 危险 |

### 字体

| Token | 值 | 用途 |
|-------|------|------|
| `--font-display` | `'{{Display Font}}', serif` | 标题 / Logo / 大字 |
| `--font-body` | `system-ui, -apple-system, sans-serif` | 正文 |
| `--font-mono` | `'JetBrains Mono', monospace` | 数据 / 代码 |

### 间距

| Token | 值 |
|-------|------|
| `--space-xs` | `4px` |
| `--space-sm` | `8px` |
| `--space-md` | `16px` |
| `--space-lg` | `24px` |
| `--space-xl` | `32px` |
| `--space-2xl` | `48px` |

### 圆角

| Token | 值 |
|-------|------|
| `--radius-sm` | `6px` |
| `--radius-md` | `10px` |
| `--radius-lg` | `16px` |

---

## 2. 布局

| 区域 | 宽度 | 备注 |
|------|------|------|
| 左侧输入面板 | 300px 固定 | 移动端变顶部折叠 |
| 右侧内容区 | `calc(100% - 300px)` | 最大 1140px |
| 整体最大宽度 | 1440px | 居中 |
| 断点 | 768px | < 768px 进入单列 |

---

## 3. 各组件像素规范

### C1 HeroCard

| 属性 | TOP 1 | TOP 2-3 |
|------|-------|---------|
| 高度 | auto, min 180px | auto, min 140px |
| 边框 | 1px solid `var(--accent)` | 1px solid `var(--border)` |
| 背景 | `var(--bg-card)` + accent glow | `var(--bg-card)` |
| 排名字号 | 48px `var(--font-display)` | 36px |
| 产品名字号 | 18px bold | 15px bold |
| APY 字号 | 28px `var(--font-mono)` | 22px |
| 一句话评语 | 13px italic `var(--text-secondary)` | 同 |

### C3 RankingGrid 每行

| 属性 | 值 |
|------|------|
| 行高 | 56px |
| TOP 1 行背景 | `linear-gradient(90deg, accent/8%, transparent)` |
| 列宽 | `40px 1fr 80px 80px 60px 80px 70px` |
| 排名列字号 | 14px `var(--font-mono)` |
| 平台名字号 | 14px bold |
| 数据列字号 | 13px `var(--font-mono)` |

### C4 RadarCompare

| 属性 | 值 |
|------|------|
| 画布尺寸 | 280×280px |
| 轴数 | 5 (收益/安全/便利/容量/稳定) |
| 最多对比 | 4 个产品 |
| 多边形颜色 | 依次使用 accent / secondary / tertiary / quaternary |
| 标签字号 | 11px |

---

## 4. 颜色编码规则

### 安全等级

| 等级 | 条件 | 颜色 | 标签 |
|------|------|------|------|
| 高 | score ≥ 80 | `var(--success)` | "A" |
| 中 | 50 ≤ score < 80 | `var(--warning)` | "B" |
| 低 | score < 50 | `var(--danger)` | "C" |

### APY 趋势

| 趋势 | 条件 | 颜色 | 图标 |
|------|------|------|------|
| 上升 | 30d_trend > +5% | `var(--success)` | ↑ |
| 平稳 | -5% ≤ trend ≤ +5% | `var(--text-muted)` | → |
| 下降 | trend < -5% | `var(--danger)` | ↓ |

### Venue 类型

| 类型 | 颜色 | 标签样式 |
|------|------|----------|
| CEX | `{{color_1}}` | 实心圆点 + 文字 |
| DeFi | `{{color_2}}` | 实心圆点 + 文字 |

---

## 5. 动画

| 元素 | 触发 | 效果 | 时长 |
|------|------|------|------|
| HeroCard TOP 1 | 数据加载完成 | border glow pulse | 3s infinite |
| RankingGrid 行 | hover | background fade | 0.2s ease |
| RadarCompare | 切换对比产品 | 多边形 morph | 0.4s ease-out |
| 左侧面板折叠 | 移动端点击 | slideDown | 0.3s ease |

---

## 6. Loading 状态

| 组件 | Loading 占位 |
|------|-------------|
| HeroCard | 灰色骨架 (shimmer) |
| RankingGrid | 5 行骨架条 |
| RadarCompare | 静态空轴 |
| NarrativeCard | 3 行文字骨架 |
