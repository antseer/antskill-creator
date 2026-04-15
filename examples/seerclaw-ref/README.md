# SeerClaw Scanner

> AI-driven smart contract security scanner — paste an address, get a risk report.

## Quick Start

1. Read `SKILL.md` for architecture overview
2. Check `references/business-spec.md` for risk level definitions
3. Review `references/api-spec.md` for Etherscan/Sourcify integration

## Architecture

```
┌──────────────────────────────────────────────────┐
│                   L4 Rendering                    │
│  SecurityCard → VulnList → RiskRadar → CodeView   │
├──────────────────────────────────────────────────┤
│                   L3 Decision                     │
│  LLM → executive summary + vuln narratives        │
├──────────────────────────────────────────────────┤
│                   L2 Compute                      │
│  Static analysis → pattern match → risk scoring   │
├──────────────────────────────────────────────────┤
│                   L1 Data                          │
│  Etherscan → Sourcify → DeFiLlama                 │
└──────────────────────────────────────────────────┘
```

## License

Proprietary — Antseer.ai
