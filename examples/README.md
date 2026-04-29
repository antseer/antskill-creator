# Examples — 参考 Skill 案例

> 本目录用于存放工厂使用者自行添加的标杆 Skill 案例,供后续新 Skill 参考。

---

## §1 这个目录是什么?

`examples/` 目录在工厂初始交付时**是空的**。工厂使用者(通常是工厂维护团队 / PM / 设计师)应在首个 Skill 完成后,把交付的 Skill 半成品**裁剪版**放进来作为参考案例。

v5.1 示例目录结构(符合 S5 的分层交付):

```
examples/
├── README.md                       ← 本文件
├── polymarket-drift-radar/         第一个完成的 Skill,作为 B 范式标杆
│   ├── SKILL.md                    分层设计说明 + frontmatter(含 layers + mcp_gap_summary)
│   ├── VERSION                     0.1.0
│   ├── skill-prd.md                模块化 × L1-L5
│   ├── frontend/
│   │   └── index.html              高保真定稿
│   ├── layers/
│   │   ├── L1-data/
│   │   ├── L2-aggregation/
│   │   ├── L3-compute/             可运行脚本示例
│   │   ├── L4-llm/                 prompt + Fallback 示例
│   │   └── L5-presentation/
│   ├── data-prd.md                 P0/P1/P2 分级
│   └── review-report.md
└── yield-desk-lite/                A 范式标杆(若有)
    └── ...
```

---

## §2 放 Example 的标准

一个 Skill 可以作为 example 的条件:

1. ✅ 已通过 G0-G5 全部门禁
2. ✅ 已在生产环境被使用(或已通过人工终审)
3. ✅ **视觉登记表 `design-system/visual-registry.md` 已登记**
4. ✅ 按 L1-L5 分层组织,每层有 README.md
5. ✅ data-prd.md 真实分级(不是模板占位)
6. ✅ 交付版 SKILL.md frontmatter 合法(含 status / layers / mcp_gap_summary)

---

## §3 如何使用 examples/

### 作为新 Skill 的参照

开始做新 Skill 时:

1. 先浏览 `examples/` 里各 Skill 的 SKILL.md,看哪个**业务形态最接近**你要做的
2. 打开对应 Skill 的 `frontend/index.html` 本地预览视觉
3. 读对应 Skill 的 `skill-prd.md` 体会模块 × L1-L5 的颗粒度
4. 读对应 Skill 的 `data-prd.md` 体会期望接口形态的写法
5. **不要复制代码或规范,要对标质量**

### 作为新人入职培训

新加入工厂的 Claude / PM / 设计师通过跑通 examples 里的一个 Skill(从 S0 重走一遍到 S5)来理解流水线。

---

## §4 examples 与工厂本体的关系

```
skill-creator-rick/
├── SKILL.md                  工厂主控(方法论)
├── methodology/              方法论本体(不含业务细节)
├── sop/ + quality/           操作规程 + 门禁
├── design-system/            设计系统(基础层,不含 Skill 具体值)
├── mcp-capability-map/       MCP 地图(基础层,不含具体 Tool 实现)
├── templates/                空白模板(待填充)
└── examples/                 ← 真实的、已落地的 Skill 参考
```

**关系**: `templates/` 是"空白图纸", `examples/` 是"已完工的建筑"。新项目的图纸来自 templates,但对标质量看 examples。

---

## §5 维护责任

- Example 的添加和更新由**工厂维护团队**负责
- 每新增一个 example 时,需要同步更新:
  - `design-system/visual-registry.md` 登记新 Skill 的主色 / 字体 / Hero 类型
  - MCP truth 变动时,只更新 `mcp-capability-map/cache/manifest.json` 和对应缓存文档,不再维护手写能力表
- Example 过期(业务形态已淘汰)时,**迁移到 `examples/archive/`**,不要直接删除
