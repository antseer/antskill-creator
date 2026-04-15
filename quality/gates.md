# 质量门槛 — S1 至 S6

> 每阶段结束时自动执行对应检查清单。🔴 项不通过则打回重做（最多 3 轮）。🟡 项应修复但不阻塞。🟢 项为加分项。

---

## S1 需求采集门槛

| # | 检查项 | 级别 |
|---|--------|------|
| 1 | 7 道画布题均有实质性回答（非"待定"） | 🔴 |
| 2 | Q7 范式已明确选择 A/B/C | 🔴 |
| 3 | 至少 1 个具体数据源被提及 | 🔴 |
| 4 | 用户画像不是"所有人" | 🟡 |
| 5 | 有至少 1 个竞品/替代方案被分析 | 🟡 |

---

## S2 快速原型门槛

| # | 检查项 | 级别 | 自动验证 |
|---|--------|------|----------|
| 1 | Hero 区 3 秒内能理解核心信息 | 🔴 | 人工 |
| 2 | Hero 区有颜色编码提供方向感 | 🔴 | 扫描 CSS 变量 |
| 3 | 主色与已有 Skill 不同 | 🔴 | 对照注册表 |
| 4 | Display 字体与已有 Skill 不同 | 🔴 | 对照注册表 |
| 5 | HTML 无语法错误 | 🔴 | 花括号/标签 balance |
| 6 | Mock 数据合理（无 NaN / undefined / 空数组） | 🔴 | 自动扫描 |
| 7 | 至少 1 个交互能触发数据刷新 | 🔴 | 人工 |
| 8 | 底部有数据来源标注 | 🟡 | 文本搜索 |
| 9 | 有 Loading 状态 | 🟡 | 文本搜索 "loading" |
| 10 | 移动端不横向溢出 | 🟡 | 人工 |

### S2 自动验证脚本

```python
import re

def validate_s2(html_content):
    issues = []
    
    # 花括号 balance
    opens = html_content.count('{')
    closes = html_content.count('}')
    if opens != closes:
        issues.append(f"🔴 花括号不平衡: {{ = {opens}, }} = {closes}")
    
    # 颜色编码检查
    if not re.search(r'#[0-9a-fA-F]{6}', html_content):
        issues.append("🔴 未发现任何颜色编码")
    
    # Mock 数据检查
    for bad in ['NaN', 'undefined', 'null,', '[]']:
        if bad in html_content:
            issues.append(f"🔴 发现可疑 Mock 数据: {bad}")
    
    # Loading 状态
    if 'loading' not in html_content.lower() and 'spinner' not in html_content.lower():
        issues.append("🟡 未发现 Loading 状态")
    
    # 数据来源
    if 'source' not in html_content.lower() and 'powered by' not in html_content.lower():
        issues.append("🟡 未发现数据来源标注")
    
    return issues
```

---

## S3 精修定稿门槛

| # | 检查项 | 级别 |
|---|--------|------|
| 1 | 用户明确说"OK / 定稿 / 可以" | 🔴 |
| 2 | 所有用户反馈点都已处理 | 🔴 |
| 3 | 论据层至少 3 个维度 | 🟡 |
| 4 | 信任层有方法论说明 | 🟡 |
| 5 | 信任层有风险提示 | 🔴 |

---

## S4 PRD 输出门槛

| # | 检查项 | 级别 |
|---|--------|------|
| 1 | `docs/product/PRD.md` 已产出且能讲清完整产品逻辑 | 🔴 |
| 2 | `docs/requirements/` 8 个文档全部产出 | 🔴 |
| 3 | business-spec 覆盖所有业务规则 | 🔴 |
| 4 | api-spec 每个字段有类型定义 | 🔴 |
| 5 | backend-computation 每个公式有伪代码 | 🔴 |
| 6 | ai-prompts 有完整 System Prompt | 🔴 |
| 7 | ai-prompts 有输入输出 JSON Schema | 🔴 |
| 8 | ai-prompts 有 Fallback 模板 | 🔴 |
| 9 | viz-specs 覆盖每个可见元素 | 🟡 |
| 10 | implementation-guide 有 Production-vs-Prototype 标注 | 🟡 |
| 11 | TestSuite 覆盖所有边界条件 | 🟡 |
| 12 | `delivery/SKILL.md` 8 章节齐全 | 🔴 |
| 13 | PRD 与 requirements 之间无字段/口径冲突 | 🔴 |
| 14 | docs 与 implementation 的边界清晰，无职责混放 | 🔴 |

---

## S5 包交付门槛

| # | 检查项 | 级别 | 自动验证 |
|---|--------|------|----------|
| 1 | `delivery/SKILL.md` 存在且 8 章节齐全 | 🔴 | 扫描标题 |
| 2 | `delivery/README.md` 存在 | 🔴 | 文件检查 |
| 3 | `delivery/README.zh.md` 存在 | 🔴 | 文件检查 |
| 4 | `delivery/agents/openai.yaml` 存在且 YAML 合法 | 🔴 | yaml.safe_load |
| 5 | `delivery/VERSION` 存在且格式 x.y.z | 🔴 | 正则匹配 |
| 6 | `delivery/assets/` 有 2 个 SVG | 🔴 | 文件检查 |
| 7 | `delivery/templates/ai-input.json` 合法 JSON | 🔴 | json.loads |
| 8 | `delivery/templates/ai-output.json` 合法 JSON | 🔴 | json.loads |
| 9 | `implementation/scripts/validate-ai-output.js` 可运行 | 🟡 | node 执行 |
| 10 | 无 0 字节文件 | 🔴 | 文件大小扫描 |
| 11 | `implementation/frontend/` 存在 Demo | 🟡 | 文件检查 |
| 12 | A/C 范式：单测全过 | 🔴 | pytest |

### S5 自动验证脚本

```python
import os, json, yaml, re

def validate_s5(skill_dir):
    issues = []
    
    # 必须文件
    required = [
        'delivery/SKILL.md', 'delivery/README.md', 'delivery/README.zh.md',
        'delivery/agents/openai.yaml', 'delivery/VERSION',
        'docs/product/PRD.md'
    ]
    for f in required:
        path = os.path.join(skill_dir, f)
        if not os.path.exists(path):
            issues.append(f"🔴 缺失: {f}")
        elif os.path.getsize(path) == 0:
            issues.append(f"🔴 空文件: {f}")
    
    # VERSION 格式
    ver_path = os.path.join(skill_dir, 'delivery/VERSION')
    if os.path.exists(ver_path):
        ver = open(ver_path).read().strip()
        if not re.match(r'^\d+\.\d+\.\d+$', ver):
            issues.append(f"🔴 VERSION 格式错误: {ver}")
    
    # openai.yaml 合法性
    yaml_path = os.path.join(skill_dir, 'delivery/agents/openai.yaml')
    if os.path.exists(yaml_path):
        try:
            yaml.safe_load(open(yaml_path))
        except:
            issues.append("🔴 openai.yaml 不是合法 YAML")
    
    # JSON 文件
    for jf in ['delivery/templates/ai-input.json', 'delivery/templates/ai-output.json']:
        jp = os.path.join(skill_dir, jf)
        if os.path.exists(jp):
            try:
                json.loads(open(jp).read())
            except:
                issues.append(f"🔴 {jf} 不是合法 JSON")
    
    # SVG 资产
    for svg in ['delivery/assets/icon-small.svg', 'delivery/assets/icon-card.svg']:
        sp = os.path.join(skill_dir, svg)
        if not os.path.exists(sp):
            issues.append(f"🔴 缺失: {svg}")
    
    # SKILL.md 8 章节
    skill_md = os.path.join(skill_dir, 'delivery/SKILL.md')
    if os.path.exists(skill_md):
        content = open(skill_md).read()
        required_sections = ['Scope', 'Source of Truth', 'Package Contents',
                           'Workflow', 'Input Contract', 'Non-negotiable Rules',
                           'Implementation Checklist', 'Footer']
        for sec in required_sections:
            if sec.lower() not in content.lower():
                issues.append(f"🟡 SKILL.md 缺少章节: {sec}")
    
    # 0 字节扫描
    for root, dirs, files in os.walk(skill_dir):
        for f in files:
            fp = os.path.join(root, f)
            if os.path.getsize(fp) == 0:
                issues.append(f"🔴 空文件: {os.path.relpath(fp, skill_dir)}")
    
    return issues
```

---

## S6 Skill Review 门槛

| # | 检查项 | 级别 |
|---|--------|------|
| 1 | SKILL-REVIEW.md 有差距矩阵 | 🔴 |
| 2 | 所有 🔴 Critical gap 已修复 | 🔴 |
| 3 | 修复后的文档通过 S4 门槛 | 🔴 |
| 4 | 🟡 Warning gap 有修复计划 | 🟡 |

---

## LLM 自动评估 Prompt

以下 Prompt 可用于让 LLM 自动评估 Skill 包质量：

```markdown
# Skill 包质量评估

你是一个严格的 Skill 包审核员。请审核以下 Skill 包，按品质标准打分。

## 品质标准

⭐⭐⭐ 卓越（90+）
- Hero 区结论直白、有行动力
- 论据层的可视化直接证明结论
- 信任层完整且不啰嗦
- 4 层 Pipeline 清晰分离
- 所有边界条件都有处理方案
- 视觉独特、有记忆点

⭐⭐ 合格（70-89）
- Hero 区有结论但不够犀利
- 论据层覆盖主要维度但有遗漏
- Pipeline 基本分离但有混杂
- 主要边界条件有处理

⭐ 需改进（<70）
- Hero 区缺少结论
- 论据层与结论脱节
- Pipeline 各层职责混乱
- 边界条件大量遗漏

## 请逐项打分并给出改进建议
```

---

## 打回机制

1. 执行对应阶段的检查清单
2. 如有 🔴 项 FAIL → 自动修复
3. 修复后重新检查
4. 最多 3 轮。3 轮后仍有 🔴 → 向用户报告具体问题，请求人工介入
5. 所有 🔴 通过后，才能进入下一阶段
