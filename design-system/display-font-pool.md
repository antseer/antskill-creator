# Display Font Pool — 可用 Display 字体池

> **每个 Skill 的 `--display-font` 变量必须从本池选择**，且未被 `visual-registry.md` 占用。
> Display 字体**仅用于 Hero 区一级大字**（Skill 名、核心结论、大号数字标题），正文、输入、按钮依然用 Inter。

---

## §1 字体池

所有字体必须是 Google Fonts 可直接加载的 open-source 字体，保证生产可用。

| 字体 | 风格 | 权重 | 气质 | 适合主题 | 占用状态 |
|------|------|------|------|----------|---------|
| **Cormorant Garamond** | Serif / 古典 | 400-700 | 编辑部 / 专栏 | 分析 / 研究 / 长文 | 已占用（DualYield） |
| **Fraunces** | Serif / 可变字形 | 400-900 | 仪表盘 / 科技感衬线 | 监控 / 实验台 | 已占用（Yield Desk） |
| **Playfair Display** | Serif / 高对比衬线 | 400-900 | 杂志 / 封面 | 推荐榜单 / 精选 | 可用 |
| **DM Serif Display** | Serif / 现代衬线 | 400 | 时装编辑 / 现代 | 时尚 / 潮流 | 可用 |
| **Libre Baskerville** | Serif / 新闻 | 400-700 | 报纸 / 新闻 | 新闻聚合 / 快报 | 可用 |
| **Source Serif Pro** | Serif / 学术 | 400-900 | 学术 / 期刊 | 研究报告 / 长文 | 可用 |
| **Space Grotesk** | Sans / 几何 | 300-700 | 控制台 / 赛博 | 实时监控 / 量化 | 可用 |
| **Archivo** | Sans / 工业 | 100-900 | 工业 / 制图 | 工程指标 / 架构图 | 可用 |
| **Instrument Serif** | Serif / 新锐 | 400 | 杂志 / 艺术 | 新概念 / 品牌展示 | 可用 |
| **Grotesk Display** | Sans / 细长 | 400-700 | 架构师 / 图表 | 流程 / 架构 | 可用 |
| **IBM Plex Serif** | Serif / 技术 | 400-700 | 技术出版物 | 白皮书 / 文档 | 可用 |
| **Syne** | Sans / 扭曲 | 400-800 | 实验室 / 前沿 | 先锋 / 创新 | 可用 |

---

## §2 字体使用规则

### 允许的使用范围

✅ **Hero 区 H1**（Skill 名，22-40px）
✅ **Hero 区 Display 数字**（核心大数字，48-80px）
✅ **章节首句 / 引言**（如果有）

### 禁止的使用范围

❌ 正文、段落
❌ 输入框、按钮
❌ 表格、chart 标签
❌ tooltip、placeholder
❌ 状态文案（loading / empty / error）

**凡是不在 Hero 区首屏的字，都必须用 Inter。**

---

## §3 字体加载

所有字体通过 Google Fonts 加载：

```html
<!-- 例：使用 Cormorant Garamond -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;700&family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
```

```css
:root {
  --display-font: 'Cormorant Garamond', Georgia, serif;
}

.hero-title {
  font-family: var(--display-font);
  font-weight: 700;
  font-size: 40px;
  line-height: 1.1;
}
```

### 加载权重规则

为避免拖累首屏，每款 Display 字体只加载**必要的权重**：
- 必需：`400` (regular)，`700` (bold)
- 可选：`500` (medium)，如果有中等层级

**不要一次加载全部字重 100-900**，这会让字体文件膨胀 5-10 倍。

---

## §4 选字指南

### 气质匹配

| 气质 | 推荐字体 |
|------|---------|
| 编辑部 / 长文 | Cormorant Garamond、Libre Baskerville、IBM Plex Serif |
| 仪表盘 / 实验台 | Fraunces、Space Grotesk |
| 杂志 / 精选 | Playfair Display、DM Serif Display、Instrument Serif |
| 学术 / 报告 | Source Serif Pro、IBM Plex Serif |
| 控制台 / 量化 | Space Grotesk、Archivo |
| 新闻 / 快报 | Libre Baskerville |
| 前沿 / 先锋 | Syne、Instrument Serif |
| 工程 / 架构 | Archivo、Grotesk Display |

### 主色 + 字体搭配（示例）

| 主色 | 推荐 Display 字体 | 原因 |
|------|------------------|------|
| 古铜金 | Cormorant Garamond | 编辑部 + 古典衬线 |
| 数据紫 | Source Serif Pro | 学术 + 期刊衬线 |
| 警报红 | Space Grotesk | 控制台 + 工业 sans |
| 电气薄荷 | Fraunces | 仪表盘 + 科技衬线 |
| 熔岩橙 | Libre Baskerville | 新闻 + 报纸衬线 |
| 海洋青 | Instrument Serif | 社区 + 新锐 |
| 晨雾青 | IBM Plex Serif | 日报 + 技术 |

---

## §5 扩展申请

当可用字体剩 ≤ 2 款时，向工厂维护者申请扩展。
扩展时需提供：

1. 字体全名 + Google Fonts 链接
2. 授权（必须是 OFL / Apache / SIL 等开源许可）
3. 气质与主题归属
4. 与现有字体池的视觉距离
5. 实际文件大小（Regular + Bold 权重加起来应 ≤ 100KB）
