# {{SKILL_NAME}} — Implementation Guide

> 前端 + AI 架构指南：容器组件、数据绑定、Production-vs-Prototype、降级 UI。SoT 优先级第 5 位。

---

## 1. 容器组件清单

| # | 组件名 | 用途 | 数据来源 |
|---|--------|------|----------|
| C1 | HeroCard | TOP 推荐卡片 | L2 rank + L3 brief |
| C2 | StatsBar | 统计摘要 | L2 market_stats |
| C3 | RankingGrid | 排行榜表格 | L2 scored_products |
| C4 | RadarCompare | 多维雷达对比 | L2 dims |
| C5 | NarrativeCard | 军师/分析师文案 | L3 output |
| C6 | TrustFooter | 方法论 + 风险 | 静态 + L2 meta |
| C7 | ErrorCard | 全局错误 | L1 error |
| {{C8}} | {{...}} | {{...}} | {{...}} |

### C1 HeroCard Props

```typescript
interface HeroCardProps {
  rank: number;                // 1-3
  platform: string;            // "Binance"
  productName: string;
  primaryMetric: number;       // APY 小数
  primaryLabel: string;        // "APY"
  secondaryMetrics: Array<{label: string; value: string}>;
  oneLiner: string;            // L3 brief_for_card
  accentColor: string;
  isBest: boolean;             // rank === 1
}
```

---

## 2. 数据绑定流程

```
L1 RawProduct[]
  ↓ l2_compute.run()
L2 { scored_products, market_stats, anomaly_alerts }
  ↓ l3_decision.run()
L3 { headline, top1_reason, ..., brief_for_card }
  ↓ bind to containers
L4 Components:
  HeroCard ← scored_products[0..2] + brief_for_card[0..2]
  StatsBar ← market_stats
  RankingGrid ← scored_products (all)
  RadarCompare ← scored_products (selected) .dims
  NarrativeCard ← headline + top1_reason + opportunity_cost + risk_warning
  TrustFooter ← static content + anomaly_narratives
```

---

## 3. Production-vs-Prototype 标注

| 行为 | Demo（原型） | Production（生产） |
|------|-------------|-------------------|
| 数据获取 | Mock 数据在 JS 里 | 后端 API → Redis 缓存 |
| L2 计算 | 在浏览器 JS 里 | 在后端 Python |
| L3 LLM 调用 | 直接 fetch Anthropic API | 后端代理 + 缓存 + 限流 |
| 认证 | 无 | API Key 加密存储 |
| 错误处理 | console.log | 结构化错误码 + ErrorCard |
| 并发 | 单用户 | 多用户 + 请求排队 |
| 刷新 | 手动点击 | 定时任务 + WebSocket 推送 |

**规则**：
- Demo 的**视觉和交互逻辑**是参考标准 ✅
- Demo 的**数据获取方式和计算位置**不是参考标准 ❌

---

## 4. 降级 UI 规范

### 全局错误卡

```html
<div class="error-card">
  <span class="icon">⚠</span>
  <h3>{{数据源名称}} 暂时不可用</h3>
  <p>最后成功时间: {{timestamp}}</p>
  <button onclick="retry()">🔄 重试</button>
  <button onclick="useCache()">使用缓存数据</button>
</div>
```

### 部分失败

如果 N 个数据源中 M 个成功：
- 展示成功部分的完整结果
- 在顶部放黄色横幅："{N-M} 个数据源暂不可用，结果可能不完整"
- 每个失败源在对应位置放 ErrorCard

### L3 降级

LLM 不可用时：
- HeroCard 正常展示（数据来自 L2）
- NarrativeCard 使用 Fallback 模板文案
- 标注 "AI 分析暂不可用，仅展示数据排名"

### Retry 时序

1s → 3s → 10s → 停止自动重试，保留手动按钮

---

## 5. Production Checklist

### 🔴 P0（上线阻塞）

- [ ] L1: 主数据源 API 接入完成
- [ ] L1: 降级策略实现（Fallback + 缓存）
- [ ] L2: 评分算法后端实现 + 单测 100% 通过
- [ ] L3: Prompt 部署 + Fallback 实现
- [ ] L4: ErrorCard + Retry 实现
- [ ] 安全: API Key 加密存储

### 🟡 P1（上线后 1 周内）

- [ ] L1: 全部 Fallback 数据源接入
- [ ] L2: 异常检测规则上线
- [ ] L3: Prompt 调优（基于真实数据跑 4 个测试场景）
- [ ] 监控: L1 成功率 + L3 延迟 + 用户交互埋点

### 🟢 P2（迭代优化）

- [ ] L2: 历史时序数据接入（30 日统计）
- [ ] L4: 移动端适配优化
- [ ] 缓存: Redis TTL 调优
- [ ] A/B 测试: 权重矩阵对比
