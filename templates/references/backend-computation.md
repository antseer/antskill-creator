# {{SKILL_NAME}} — Backend Computation

> 计算逻辑：L2 Pipeline 每一步的伪代码、评分公式、异常检测。SoT 优先级第 4 位。

---

## 1. L2 Pipeline 概览

```
RawProduct[] → Step1 Filter → Step2 Enrich → Step3 Derive
  → Step4 Normalize → Step5 Score → Step6 Rank → Step7 AnomalyDetect
  → ScoredProduct[]
```

---

## 2. Step 1: Filter（过滤）

```python
def filter_products(raw: list[RawProduct], user: UserContext) -> list[RawProduct]:
    result = []
    for p in raw:
        # F1: {{过滤规则 1}}
        if {{condition_1}}:
            continue
        # F2: {{过滤规则 2}}
        if {{condition_2}}:
            continue
        result.append(p)
    return result
```

---

## 3. Step 2: Enrich（补全）

```python
def enrich(products: list, meta: dict) -> list:
    for p in products:
        # 从元数据补全安全信息
        m = meta.get(p.platform, {})
        p.tier = m.get('tier', 'unknown')
        p.audit_count = m.get('audit_count', 0)
        p.has_insurance = m.get('has_insurance', False)
        # {{其他补全逻辑}}
    return products
```

---

## 4. Step 3: Derive（衍生计算）

```python
def derive(products: list, history: dict) -> list:
    for p in products:
        # 衍生字段 1: {{字段名}}
        # 公式: {{formula}}
        p.{{derived_field}} = {{computation}}
        
        # 衍生字段 2: 30 日 APY 波动率
        if p.id in history:
            series = history[p.id]  # list of daily APY
            p.apy_vol_30d = std(series[-30:])
        else:
            p.apy_vol_30d = None  # 标注为缺失
    return products
```

---

## 5. Step 4: Normalize（归一化）

每个维度映射到 0-100：

```python
def normalize(value, min_val, max_val, invert=False):
    """
    线性归一化到 0-100
    invert=True 时值越小分越高（如锁仓天数）
    """
    if max_val == min_val:
        return 50  # 无法区分时给中间值
    score = (value - min_val) / (max_val - min_val) * 100
    score = max(0, min(100, score))
    return (100 - score) if invert else score
```

### 各维度归一化参数

| 维度 | 字段 | min | max | invert | 说明 |
|------|------|-----|-----|--------|------|
| 收益 | `apy` | 0 | {{max_apy}} | No | 越高越好 |
| 安全 | `safety_score` | 0 | 100 | No | 由 calc_safety 直接产出 |
| 便利 | `lock_days` | 0 | {{max_lock}} | Yes | 天数越少越便利 |
| 容量 | `capacity_usd` | 0 | {{max_cap}} | No | 越大越好 |
| 稳定 | `apy_vol_30d` | 0 | {{max_vol}} | Yes | 波动越小越稳定 |

---

## 6. Step 5: Score（评分）

### 安全评分子函数

```python
def calc_safety(product, meta):
    score = 0
    # 基础分: Tier
    tier_scores = {'Tier-1': 40, 'Tier-2': 25, 'Tier-3': 10, 'unknown': 0}
    score += tier_scores.get(product.tier, 0)
    
    # 审计加分: 每次审计 +8，上限 25
    score += min(product.audit_count * 8, 25)
    
    # 保险加分
    if product.has_insurance:
        score += 10
    
    # {{其他安全因素}}
    
    return min(score, 100)
```

### 综合评分

```python
def calc_total(dims: dict, weights: dict) -> float:
    """
    dims: {'yield': 75, 'safety': 80, 'convenience': 60, ...}
    weights: {'yield': 0.30, 'safety': 0.25, ...}
    """
    return sum(dims[k] * weights[k] for k in dims)
```

### 权重矩阵

| 偏好组合 | yield | safety | convenience | capacity | stability |
|----------|-------|--------|-------------|----------|-----------|
| 默认 | 0.30 | 0.25 | 0.20 | 0.10 | 0.15 |
| 安全优先 | 0.20 | 0.40 | 0.15 | 0.10 | 0.15 |
| 收益优先 | 0.45 | 0.15 | 0.15 | 0.10 | 0.15 |
| {{自定义}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

---

## 7. Step 6: Rank（排序）

```python
products.sort(key=lambda p: p.total_score, reverse=True)
for i, p in enumerate(products):
    p.rank = i + 1
```

---

## 8. Step 7: Anomaly Detect（异常检测）

| 规则名 | 条件 | 严重级别 | 叙事模板 |
|--------|------|----------|----------|
| `YIELD_OUTLIER` | `apy > mean + 3*std` | warning | "收益率是同类的 {ratio:.1f}倍..." |
| `YIELD_DECLINING` | `apy_30d_trend < -0.20` | info | "过去 30 天收益率下降了 {pct}%..." |
| `CAPACITY_LOW` | `capacity_usd < principal * 2` | warning | "剩余容量仅 ${cap:,.0f}..." |
| {{自定义}} | {{condition}} | {{level}} | {{template}} |
