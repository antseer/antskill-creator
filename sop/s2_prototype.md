# S2 — 快速原型

## 目标

在 1 次交互内产出一个**可交互的 Mock Demo HTML**，验证信息架构和视觉方向。

## 方法论

**Hero 区定生死。** 如果 Hero 区 3 秒内无法让用户理解核心信息，整个 Skill 就失败了。

## 6 步清单

### Step 1: 确定视觉基调
- 查 SKILL.md §5 视觉差异化登记表
- 选一个未使用的主色 + Display 字体 + Hero 类型
- 确定整体气质（军师/编辑部/实验室/控制台/...）

### Step 2: 设计 Hero 区
- **必须有结论**：不允许 Hero 区只放输入表单
- 默认状态 vs 有数据状态：
  - 默认状态：引导语 + 操作提示（例："点击开始分析"）
  - 有数据状态：TOP 推荐 + 一句话 why + 核心指标
- 首屏高度 ≤ 85vh

### Step 3: 设计左侧输入面板
- 最多 5 个输入项
- 每个输入有合理默认值
- 用户可以不改任何东西直接点"开始"

### Step 4: 设计中间层（论据区）
- 1-3 个可视化组件（图表/表格/卡片）
- 每个组件必须支撑 Hero 区的结论
- 不放与结论无关的装饰性数据

### Step 5: 设计信任层
- 方法论说明（1-2 段话）
- 风险提示（至少 2 条）
- 原始数据（可折叠）

### Step 6: Mock 数据 + 交互
- 用程序生成 Mock 数据（随机但合理）
- 至少实现"切换输入 → 重新渲染"的交互
- 底部标注 "Mock Data — Powered by Antseer.ai"

## 视觉规范

### 布局
- 左侧输入面板：280-320px 固定
- 右侧内容区：自适应
- 最大宽度 1440px，居中
- 移动端：输入面板变顶部可折叠

### 字体
- Display/标题：从未使用字体池选取（Cormorant Garamond, Fraunces, Playfair Display, DM Serif, Libre Baskerville, Source Serif Pro）
- 正文：system-ui 或 Inter
- 等宽/数据：JetBrains Mono 或 Fira Code

### 色彩
- 背景：`#0a0a0f` ~ `#111118`（深色系）
- 文字：`#e8e8ed`（主）/ `#8a8a9a`（次）
- 主色：从 SKILL.md §5 可用色池选取
- 成功/警告/危险：`#22c55e` / `#f59e0b` / `#ef4444`

### 组件
- 单文件 HTML（CSS + JS 内联）
- React via CDN（可选）
- 图表用 D3 或 Recharts
- 无 localStorage（用内存状态）

## 质量门 → 见 quality/gates.md S2 部分
