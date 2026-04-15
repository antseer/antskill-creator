# S6 — Skill Review（gap 分析）

## 目标

交付后做**字段级 gap 分析**，确保引用文档之间、文档与实现之间没有脱节。

## 方法论

**字段对照矩阵。** 逐字段检查每个引用文档的一致性。

## 何时触发 S6

- S5 交付后，用户说"review / 检查 / 对照"
- 工程师开始实现后，发现文档有矛盾
- 版本迭代时，检查旧文档是否过时

## gap 分析步骤

### Step 1: 构建字段清单

从 `api-spec.md` 提取所有字段名，形成检查清单：

```
字段: apy_base
├── api-spec.md: 定义了吗？类型对吗？
├── backend-computation.md: 有计算逻辑吗？
├── business-spec.md: 有业务规则吗？
├── ai-prompts.md: 在输入/输出 Schema 里吗？
├── viz-specs.md: 有渲染规则吗？
└── frontend Demo: 实际显示了吗？
```

### Step 2: 逐字段扫描

对每个字段，在每个引用文档中搜索，记录以下状态：

| 状态 | 含义 |
|------|------|
| ✅ 一致 | 定义、类型、逻辑完全匹配 |
| ⚠️ 偏差 | 有提及但细节不一致（如类型不同、名称不同） |
| ❌ 缺失 | 该文档应该有但没有 |
| ➖ 不适用 | 该字段不需要出现在这个文档中 |

### Step 3: 输出差距矩阵

```markdown
| 字段 | api-spec | backend | business | ai-prompts | viz-specs | Demo |
|------|----------|---------|----------|------------|-----------|------|
| apy_base | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| vol_30d | ✅ | ✅ | ❌ | ⚠️ | ✅ | ✅ |
| tier | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
```

### Step 4: 分级处理

| 级别 | 条件 | 行动 |
|------|------|------|
| 🔴 Critical | business-spec 或 api-spec 有 ❌/⚠️ | 立即修复 |
| 🟡 Warning | backend 或 ai-prompts 有 ❌/⚠️ | 本次迭代修复 |
| 🟢 Info | viz-specs 或 Demo 有 ❌/⚠️ | 下次迭代修复 |

### Step 5: 写入 SKILL-REVIEW.md

将差距矩阵和修复计划写入 `references/SKILL-REVIEW.md`。

## 自动化辅助

可用以下脚本辅助检查：

```python
# 伪代码 — 自动提取字段名并交叉检查
import re, os

def extract_fields(filepath):
    """从 markdown 中提取所有被反引号包裹的字段名"""
    with open(filepath) as f:
        return set(re.findall(r'`(\w+)`', f.read()))

ref_dir = 'references/'
all_fields = {}
for fname in os.listdir(ref_dir):
    if fname.endswith('.md'):
        all_fields[fname] = extract_fields(os.path.join(ref_dir, fname))

# 以 api-spec 的字段为基准，检查其他文档
base = all_fields.get('api-spec.md', set())
for doc, fields in all_fields.items():
    if doc == 'api-spec.md': continue
    missing = base - fields
    if missing:
        print(f"⚠️ {doc} 缺失字段: {missing}")
```

## 质量门 → 见 quality/gates.md S6 部分
