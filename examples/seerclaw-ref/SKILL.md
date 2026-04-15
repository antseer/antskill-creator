# SeerClaw Scanner — SKILL.md

> AI 驱动的智能合约安全扫描器。用户粘贴合约地址或代码，获得多维度安全评估报告。

---

## §1 Scope

### 做什么
对 EVM 链上的智能合约进行自动化安全扫描，产出可读的风险评估报告，包括：漏洞检测、代码质量评分、权限风险分析、历史事件关联。

### 不做什么
- 不替代专业审计（明确标注"非正式审计"）
- 不扫描非 EVM 链（Solana / Move 等）
- 不提供合规/法律建议

### 用户画像
DeFi 投资者和开发者，需要在投资/交互前快速评估合约安全性。具备基础区块链知识但不一定能读 Solidity。

---

## §2 Source of Truth Order

```
1. 本文件 §6
2. references/business-spec.md
3. references/api-spec.md
4. references/backend-computation.md
5. references/implementation-guide.md
6. references/ai-prompts.md
7. references/viz-specs.md
8. 前端 Demo
```

---

## §3 Package Contents

```
seerclaw-scanner/
├── SKILL.md
├── README.md
├── openai.yaml
├── VERSION
├── references/
│   ├── business-spec.md
│   ├── api-spec.md
│   ├── backend-computation.md
│   ├── implementation-guide.md
│   ├── ai-prompts.md
│   ├── viz-specs.md
│   ├── prototype-notes.md
│   ├── TestSuite.md
│   └── SKILL-REVIEW.md
├── templates/
│   ├── ai-input.json
│   └── ai-output.json
├── scripts/
│   └── validate-ai-output.js
├── assets/
│   ├── icon-small.svg
│   └── icon-card.svg
└── frontend/
    └── seerclaw.html
```

---

## §4 Workflow

```
L1: Etherscan API + Sourcify + DeFiLlama → contract bytecode + source + TVL
L2: Static analysis → pattern matching → severity scoring → risk matrix
L3: LLM → executive summary + vulnerability narratives + recommendations
L4: Data + narratives → SecurityCard + VulnList + RiskRadar + CodeViewer
```

---

## §5 Input Contract

### 用户输入
| 字段 | 类型 | 必填 | 默认值 |
|------|------|------|--------|
| contract_address | string | ✅ | — |
| chain | enum | ✅ | ethereum |

### 外部数据
| 数据源 | 端点 | 刷新 | 延迟 |
|--------|------|------|------|
| Etherscan | /api?module=contract | Per request | <2s |
| Sourcify | /server/check-all-by-addresses | Per request | <3s |
| DeFiLlama | /protocol/{name} | 5min cache | <1s |

---

## §6 Non-negotiable Rules

1. 扫描结果首行必须是风险等级（Critical / High / Medium / Low / Safe）
2. 每个发现的漏洞必须有修复建议
3. 必须标注"本报告为自动化扫描，不替代专业审计"
4. 不提供"安全"的绝对保证
5. 合约源码不可用时必须明确告知并降级为字节码分析

---

## §7 Implementation Checklist

- [ ] L1: Etherscan API 接入（含多链支持）
- [ ] L1: Sourcify 源码获取
- [ ] L2: 重入漏洞检测模式
- [ ] L2: 权限集中风险检测
- [ ] L2: 风险评分算法
- [ ] L3: Prompt 调优（4 个测试合约）
- [ ] L4: 前端容器实现
- [ ] L4: 代码高亮 + 漏洞标注

---

## §8 Footer

- 版本: 1.0.0
- 范式: B 规范型
- 创建: 2025-03-01
