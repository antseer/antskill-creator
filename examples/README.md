# AntSkill Creator v3.0 — Examples

本目录包含 4 个参考示例，覆盖从轻量参考到完整 Skill 包的不同粒度。

---

## 1. DualYield（双币投军师）— 完整 C 双模范式 ⭐ 推荐

`dualyield/`

**最完整的示例**。包含完整的 4 层 Pipeline 代码 + PRD + 技术文档 + 前端 + 单测。

适合参考：需要完整的可运行 Pipeline + 生产规范的项目。

---

## 2. Yield Desk（稳定币理财桌）— 完整 C 双模范式

`yield-desk/`

与 DualYield 同等完整度，额外包含 **1060 行分层 PRD**（`PRD-YieldDesk-v2-完整分层规范.md`），是 PRD 写法的最佳参考。

---

## 3. Yield Desk Ref（轻量代码参考）

`yield-desk-ref/`

5 个核心 Python 文件，可直接阅读 L2/L3 代码写法。

---

## 4. SeerClaw Scanner（规范型 B 范式标杆）

`seerclaw-ref/`

展示 v3 规范型范式的标准结构。不含 Pipeline 代码。

---

## 使用建议

| 需求 | 参考 |
|------|------|
| 完整 Skill 包结构 | `dualyield/` |
| PRD 写法 | `yield-desk/PRD-YieldDesk-v2-完整分层规范.md` |
| L2/L3 代码 | `yield-desk-ref/` |
| 规范型 B 范式 | `seerclaw-ref/` |
| 单测写法 | `dualyield/tests/test_l2.py` |
| 前端写法 | `yield-desk/frontend/yield-desk.html` |
