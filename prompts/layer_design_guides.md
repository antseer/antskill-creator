# L1-L4 层级设计指引

每个 Skill 的 4 层 Pipeline 设计时，使用以下思考清单和模板。

---

## L1 数据层设计指引

### 思考清单

1. **数据源枚举**：这个 Skill 需要哪些数据？每种数据的最佳来源是什么？
2. **优先级排序**：主源 vs Fallback 源。主源不可用时退化到哪？
3. **频率确定**：每种数据的刷新频率？用户可接受的最大延迟？
4. **认证方式**：API Key / OAuth / HMAC / 无认证？
5. **字段映射**：原始字段名 → 内部统一字段名
6. **体量估算**：单次拉取多少条？需要分页吗？
7. **降级方案**：主源挂了 → 用 Fallback → Fallback 也挂了 → 用缓存 → 缓存也没有 → 显示错误卡

### 数据源评估模板

```markdown
| 数据源 | Endpoint | 认证 | 频率上限 | 延迟 | 可靠性 | 备注 |
|--------|----------|------|----------|------|--------|------|
| Antseer | /api/v1/... | API Key | 60/min | <1s | 高 | 主源 |
| DefiLlama | /yields/pools | 无 | 无限制 | <2s | 高 | Fallback |
```

### 统一 Schema 设计原则

- 所有金额用 USD 计价
- 所有比率用小数（0.05 = 5%）
- 所有时间用 ISO 8601 UTC
- 所有 ID 用 `{platform}_{protocol}_{pool}` 格式

---

## L2 计算层设计指引

### 思考清单

1. **过滤**：哪些产品/数据要排除？条件是什么？
2. **衍生**：需要计算哪些新字段？公式是什么？
3. **归一化**：每个维度怎么映射到 0-100？上下界是什么？
4. **评分**：各维度权重？用户可以调权重吗？
5. **排序**：最终排序字段？升序还是降序？
6. **异常检测**：什么算异常？阈值是多少？

### 评分函数设计模板

```python
def calc_score(product, weights):
    """
    评分函数模板
    
    维度: [维度1, 维度2, ...]
    归一化: 每个维度 0-100
    加权求和: final = sum(dim_i * weight_i)
    """
    dims = {}
    
    # 维度 1: 收益
    # 归一化公式: ...
    dims['yield'] = normalize(product.apy, min=0, max=0.20) * 100
    
    # 维度 2: 安全
    # 评分规则: Tier-1 基础 X 分 + 审计 +Y 分 + ...
    dims['safety'] = calc_safety(product)
    
    # 加权求和
    total = sum(dims[k] * weights[k] for k in dims)
    return total, dims
```

### 异常检测模板

```python
ANOMALY_RULES = [
    {
        "name": "YIELD_OUTLIER",
        "condition": "apy > mean + 3*std",
        "severity": "warning",
        "narrative": "收益率是同类均值的 {ratio:.1f} 倍，可能包含不可持续的激励"
    },
    # ...
]
```

### 单测设计原则

- 每个评分维度至少 2 个用例（正常 + 边界）
- 排序结果至少 1 个用例
- 异常检测每条规则至少 1 个用例
- 空输入 / 单条输入 / 大量输入各 1 个用例

---

## L3 决策层设计指引

### 思考清单

1. **角色定义**：AI 在这个 Skill 里扮演什么角色？（军师 / 分析师 / 编辑 / 顾问）
2. **金字塔结构**：headline → top_reason → opportunity_cost → risk_warning → brief_for_card
3. **风险对称**：推荐了什么就必须说对应风险
4. **异常叙事**：L2 检测到的异常怎么翻译成人话？
5. **语气约束**：不含"我认为" / "我觉得" / "建议" + 主观修饰
6. **Fallback**：LLM 不可用时的模板函数

### System Prompt 通用骨架

```markdown
# Role
你是 [角色名]，专注于 [领域]。

# Input
你会收到一个 JSON 对象，包含以下字段：
- user_context: 用户偏好和约束
- market_stats: 市场统计
- scored_products: L2 评分后的产品列表（已排序）
- anomaly_alerts: 异常检测结果

# Output
严格返回以下 JSON，不要包含任何 Markdown 或额外文字：

{
  "headline": "不超过 40 字的核心结论",
  "top1_reason": "80-120 字，解释为什么 TOP 1 最优",
  "opportunity_cost": "包含金额对比的机会成本分析",
  "risk_warning": "至少 40 字的风险提示",
  "anomaly_narratives": ["异常 1 的人话解释", ...],
  "brief_for_card": [
    {"rank": 1, "one_liner": "一句话点评"},
    ...
  ]
}

# Writing Rules
1. 首句即结论 — headline 和 top1_reason 的第一句必须包含平台名或关键数字
2. 金字塔结构 — 结论 > 论据 > 细节
3. 风险对称 — 推荐了什么就必须在 risk_warning 中提及对应风险
4. 机会成本 — opportunity_cost 必须包含"如果选 X 而不选 Y，每年差 Z 美元"的对比
5. 异常叙事 — 把 anomaly_alerts 翻译成普通人能懂的话，包含具体数字
6. 禁止用语 — 不含"我认为"、"我觉得"、"我建议"
```

### Fallback 模板

```python
def fallback_decision(scored_products, user_context):
    """LLM 不可用时的降级输出"""
    top1 = scored_products[0]
    return {
        "headline": f"综合评分最高: {top1['platform']} {top1['product_name']}",
        "top1_reason": f"在{len(scored_products)}个产品中综合评分第一...",
        "opportunity_cost": "LLM 不可用，无法生成机会成本分析",
        "risk_warning": "以上分析基于历史数据，不构成投资建议。",
        "anomaly_narratives": [],
        "brief_for_card": [
            {"rank": i+1, "one_liner": f"综合评分 {p['total_score']:.0f}"}
            for i, p in enumerate(scored_products[:3])
        ]
    }
```

---

## L4 渲染层设计指引

### 思考清单

1. **容器清单**：需要哪些可复用组件？
2. **Props 定义**：每个容器接收什么数据？
3. **数据绑定**：L2 的哪个字段 → 容器的哪个 Prop？
4. **颜色编码**：什么值对应什么颜色？
5. **响应式**：移动端怎么处理？
6. **Loading 状态**：每个组件的加载占位符
7. **空状态**：无数据时显示什么？

### 容器组件模板

```typescript
interface HeroCardProps {
  rank: number;              // 1-3
  platform: string;          // "Binance"
  productName: string;       // "USDT Flexible"
  primaryMetric: number;     // 0.052 (5.2%)
  primaryLabel: string;      // "APY"
  secondaryMetrics: Array<{label: string, value: string}>;
  oneLiner: string;          // L3 产出
  accentColor: string;       // 来自色彩编码规则
}
```

### 颜色编码规则模板

```javascript
const colorRules = {
  // 安全等级
  safety: {
    high:   '#22c55e', // ≥ 80 分
    medium: '#f59e0b', // 50-79 分
    low:    '#ef4444', // < 50 分
  },
  // 收益变化
  yieldTrend: {
    up:     '#22c55e',
    flat:   '#8a8a9a',
    down:   '#ef4444',
  }
};
```
