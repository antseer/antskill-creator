# Antseer Design System — Skill 工厂视觉强约束

> 所有通过 v4 工厂产出的 Skill，其前端 Demo 与 viz-specs 必须符合本规范。
> 每个 Skill 可在 `visual-registry.md` 里选择**未被占用**的主色、Display 字体、Hero 类型，但**基础色板、间距、圆角、字重、两栏布局**等底层规则不允许被覆盖。

---

## §1 基础画布（所有 Skill 强制）

### 色彩底座

| Token | 色值 | 用途 |
|-------|------|------|
| `bg-page` | `#080807` | 页面底色（暖黑，**不是纯黑**） |
| `bg-nav` | `#0a0a0a` | 顶部 nav 底色 |
| `bg-card` | `#1d1d1a` | 卡片、面板、次级按钮 |
| `bg-muted` | `#121210` | 输入框、代码块、最深内陷面 |
| `bg-accent` | `#2a2926` | 卡片 hover、快捷键 chip |
| `fg-primary` | `#ffffff` | 主文字 |
| `fg-muted` | `#8a8885` | 次文字、占位符、禁用态 |
| `border` | `rgba(255,255,255,0.12)` | 所有分割线、卡片边框、输入框边框 |

### 语义色

| Token | 色值 | 用途 |
|-------|------|------|
| `success` | `#05df72` | 正向（上涨、成功、增长） |
| `warning` | `#ffb000` | 警示、次要 chart 线 |
| `info` | `#1196dd` | 信息提示、辅助 chart 线 |
| `danger` | `#f44` | 负向（下跌、错误、风险） |

### 基础字体

- **唯一家族**：`Inter, ui-sans-serif, system-ui, sans-serif`
- **字重**：`400 / 500 / 700` 三档，不允许其他
- **数值**：所有数字列（价格、收益率、百分比）必须 `font-variant-numeric: tabular-nums`
- **⚠ Antseer 本体没有 Display 字体**。但 v4 工厂允许**每个 Skill 选一款 Display 字体作为差异化**（仅用在 Hero 和一级大字），详见 `display-font-pool.md`

### 间距刻度

`4 / 8 / 10 / 12 / 14 / 16 / 20 / 24 / 32 / 40 / 48 / 56 / 64`（单位 px）

### 圆角

- `6px` — 小 badge、rank chip
- `8px` — **默认**（卡片、输入、次级按钮）
- `12px` — 嵌套面板
- `9999px` — 药丸（主 CTA、chip、inline tab）

### 阴影

**禁用阴影。** 深度来自 4 级背景色阶 `#080807 → #121210 → #1d1d1a → #2a2926` + 12% 白色 hairline。

唯一允许的"发光"是 input/button 聚焦时的绿环：`box-shadow: 0 0 0 1px <主色>`。

---

## §2 两栏布局（Skill 执行页强制）

**这是所有 Skill 执行页的**唯一**规范布局，不可协商**：

```
┌─────────────────────────────────────────────────────────┐
│ Nav (58px fixed, #0a0a0a, 绿色调底边线)                    │
├──────────────┬──────────────────────────────────────────┤
│              │                                          │
│ INPUT ONLY   │              OUTPUT ONLY                 │
│ 280–320 px   │              flex-grow                   │
│              │                                          │
│ PARAMETERS   │   Hero (结论区)                           │
│   ├ 输入项   │   Charts / Tables / Cards (论据区)        │
│   ├ 选择器   │   Methodology / Raw data (信任区，可折叠)  │
│   └ Execute  │                                          │
│              │                                          │
└──────────────┴──────────────────────────────────────────┘
   sticky                    scroll
   top:74px
```

### 左栏硬约束（INPUT ONLY）

- 固定宽度 `280-320px`
- **只放**：输入项、`Execute` 主 CTA、与输入相关的辅助（saved preset、reset to defaults、credit cost note）
- **不放**：任何结果、图表、状态消息、loading、空态、广告、推荐
- `position: sticky; top: 74px;`（58px nav + 16px 呼吸）
- 视口 ≥ 960px 时左栏宽度锁定，输出绝对不得侵占此列

### 右栏硬约束（OUTPUT ONLY）

- `flex-grow`，填满剩余空间
- **所有**执行输出都在这里：charts、tables、tiles、logs、错误、空态、占位
- 右栏内部用 `grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))` 组织 tile，gap 16-20px
- 页面最大宽度 `1220px` 居中

### 响应式（< 960px）

- 左栏变成全宽卡片**移到顶部**
- 输入在上、输出在下（**保持 input-only / output-only 的垂直分离**，不允许穿插）
- H1 从 22px 降到 20px，chart height 降到 320px

---

## §3 组件规范

### 按钮

| 变种 | 背景 | 文字 | 字号/字重 | 圆角 | 内边距 |
|------|------|------|----------|------|--------|
| **Primary (Execute)** | Skill 主色 | **黑 #000** | 18 / 500 | pill | `0 20px`，高 44-48px |
| **Card — active tab** | `#1d1d1a` | Skill 主色 | 14 / 700 | 8px | `0 16px`，高 36-40px |
| **Card — inactive** | `#1d1d1a` | `#8a8885` | 14 / 700 | 8px | `0 16px` |
| **Chip light** | `#fff` | `#000` | 13 / 500 | pill | `0 15px`，高 ~32px |
| **Chip dark** | `#1d1d1a` | `#8a8885` | 13 / 500 | pill | `0 15px` |

**签名配对**：主色（任何 Skill 的主色）底上写 **黑色**文字。不允许绿底白字、绿底绿字。

### 卡片

- 背景 `#1d1d1a`，1px border `rgba(255,255,255,0.12)`
- 圆角 8px，内边距 20-24px
- 无阴影
- 数据高亮 tile 可加顶部短线作为强调

### 输入

- 背景 `#121210`，1px border `rgba(255,255,255,0.12)`
- 白色文字 14px，占位符 `#8a8885`
- 圆角 8px，内边距 `10px 14px`
- Focus: border 变 Skill 主色 + `box-shadow: 0 0 0 1px <主色>`
- Label 在 input 上方 14px / 400，必填标红 `*`

### Badge / Chip

- **Verified**（验证过）：`rgba(<主色>, 0.12)` 底 + 主色文字 + 12/500 + pill + `2px 10px`
- **Rank**（#1 #2）：`#2a2926` 底 + `#8a8885` 文字 + 11px + 6px 圆角

### UPPERCASE 节标签

用 14px / 500 / UPPERCASE 标识输入区或 section（例：`PARAMETERS`、`TICKERS *`）。
letter-spacing: 0（不要加字间距）。

---

## §4 字体层级（基础版 + 差异化扩展）

### 基础层级（Inter，强制）

| 角色 | Size | Weight | Line Height | 变换 |
|------|------|--------|-------------|------|
| Section label (H2) | 16px | 500 | 1.5 | none |
| Uppercase mini label | 14px | 500 | 20px | UPPERCASE |
| Body | 14px | 400 | 1.5 | none |
| Muted body / caption | 14px | 400 | 1.5 | none（色 `#8a8885`） |
| Input | 14px | 400 | 20px | none |
| Primary button | 18px | 500 | 1 | none |
| Secondary button | 14px | 700 | 1 | none |
| Ticker symbol | 22-24px | 700 | — | tabular-nums |
| 大号价格 / 核心数字 | 36-48px | 700 | — | tabular-nums |

### Display 字体（v4 差异化层）

**仅用于 Hero 区的一级标题 + 少量大字**，目的是让每个 Skill 有自己的气质。
- 与基础 Inter 层级共存（正文、输入、按钮都用 Inter）
- 从 `display-font-pool.md` 选一款**未被其他 Skill 占用**的
- 登记到 `visual-registry.md`

例如：
- DualYield 选 Cormorant Garamond（编辑部气质）
- Yield Desk 选 Fraunces（仪表盘气质）
- Polymarket Drift Radar 可以选 Space Grotesk（控制台气质）

---

## §5 图表（金融类）

- **Candle**：up `#05df72` / down `#f44`
- **网格线**：`rgba(255,255,255,0.06)`（非常浅）
- **轴标签**：`#8a8885`，11px
- **当前值虚线**：Skill 主色 dashed，右侧带价格标签
- **成交量柱**：对应涨跌色的 60% 透明度
- **Chart palette 顺序**：Skill 主色 → `#ffb000` → `#1196dd` → `#ffffff` → `#f44`

---

## §6 14 条硬约束（违反则 G2 FAIL）

1. 背景不得使用纯黑 `#000`，必须用暖黑 `#080807`
2. 禁用 drop shadow（只允许 focus ring）
3. 禁用基础层的 Display 字体（只在 Hero 允许差异化字体）
4. 不允许"主色底 + 主色文字"或"白底白字"
5. 按钮圆角只能是 8px（卡片风）或 pill，禁止 12px 或其他
6. 不引入调色板外的强调色（如紫 / 粉 / 薄荷），调色受 `color-pool.md` 约束
7. **禁用 emoji**（任何位置：nav / button / label / tooltip / empty state / 代码注释 / placeholder）。需要图标用 SVG 或 Unicode 几何符号（▶ ● ★ ▲ ▼ ↗ ‹ › ⋯ ⟳ ⊙）或 icon font
8. **左栏禁止出现任何输出**（结果、loading、错误、空态都不行），在 ≥ 960px 视口 output 不得侵入左栏
9. 页面最大宽度 1220px，两栏居中
10. 所有数字列必须 `tabular-nums`
11. 主 CTA 必须是"主色底 + **黑字** + pill + 18/500"，签名配对不可替换
12. Focus ring 必须是 `0 0 0 1px <主色>`，不是其他颜色
13. 所有 border 必须是 `rgba(255,255,255,0.12)`（或绿调 nav 底边线的特例）
14. 不允许在 Skill 内嵌入第三方 UI 框架的默认样式（Bootstrap / MUI / Ant Design）；可用 Tailwind 核心工具类或原子 CSS

---

## §7 快速参考（Claude 执行 S2 时用）

```css
/* 复制粘贴即可用的基础变量 */
:root {
  --bg-page: #080807;
  --bg-nav: #0a0a0a;
  --bg-card: #1d1d1a;
  --bg-muted: #121210;
  --bg-accent: #2a2926;
  --fg: #ffffff;
  --fg-muted: #8a8885;
  --border: rgba(255,255,255,0.12);
  --success: #05df72;
  --warning: #ffb000;
  --info: #1196dd;
  --danger: #f44;

  /* Skill 差异化 — 每个 Skill 替换这两个变量 */
  --primary: /* 从 color-pool.md 选 */;
  --display-font: /* 从 display-font-pool.md 选 */;
}

body {
  background: var(--bg-page);
  color: var(--fg);
  font: 400 14px/1.5 Inter, ui-sans-serif, system-ui, sans-serif;
}

.nav {
  position: fixed; top: 0; left: 0; right: 0;
  height: 58px;
  background: var(--bg-nav);
  border-bottom: 1px solid rgba(27,74,27,0.25);
}

.main {
  max-width: 1220px; margin: 0 auto;
  padding-top: 74px;
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 24px;
}

.sidebar {
  position: sticky; top: 74px;
  /* INPUT ONLY */
}

.content {
  display: flex; flex-direction: column;
  gap: 24px;
  /* OUTPUT ONLY */
}

@media (max-width: 959px) {
  .main { grid-template-columns: 1fr; }
  .sidebar { position: static; }
}

.btn-primary {
  height: 48px; padding: 0 20px;
  background: var(--primary); color: #000;
  font: 500 18px Inter; border: 0;
  border-radius: 9999px; cursor: pointer;
}

.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 20px;
}

.input {
  background: var(--bg-muted);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 14px;
  color: var(--fg);
  font: 400 14px Inter;
}
.input:focus {
  outline: 0;
  border-color: var(--primary);
  box-shadow: 0 0 0 1px var(--primary);
}

.label-upper {
  font: 500 14px/20px Inter;
  text-transform: uppercase;
  color: var(--fg);
  letter-spacing: 0;
}

.num { font-variant-numeric: tabular-nums; }
```
