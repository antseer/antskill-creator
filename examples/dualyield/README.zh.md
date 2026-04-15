# DualYield

双币投 / DCI 推荐助手：帮用户在多家 CEX 中找到“收益高、且大概率不会被行权”的档位。

> **状态：PM 规格包 / 工程交接包**
>
> 这不是一个已经联调完成、可直接上线的成品 skill，而是一个适合分享给技术同事继续开发的 handoff package。

## 包内有什么

- 双币投产品 + 技术 PRD
- L1→L2→L3 pipeline 骨架
- 完整度较高的 L2 评分引擎与测试
- 模板式 L3 结论生成
- 高保真前端原型
- 平台元数据
- 技术入门与待办文档

## 当前判断

### 已经比较强的部分
- L2 计算层最成熟，当前 `32/32` 测试通过
- PRD 细致，已经足够指导工程继续落地
- 前端高保真原型表达力强，交接价值高
- 技术 onboarding 和 TODO 文档已存在
- L3 模板结论逻辑已具备，不依赖 LLM 也能工作

### 明显还没做完的部分
- Antseer 和各家交易所连接器大多还是存根
- 前端还在使用 mock 数据，没有接真实 orchestrator 输出
- pipeline 原先存在 L3 接线断点，整体仍未完成真实数据联调
- 缓存 / 环境变量 / API 集成还没收尾
- 在这次包装前，整个 skill 缺少 GitHub 分享门面

## 建议阅读顺序

1. `HANDOFF-REVIEW.md`
2. `TODO-TECH.md`
3. `docs/PRD.md`
4. `docs/TECH-ONBOARDING.md`

## 快速开始

```bash
python3 -m unittest tests.test_l2 -v
```

可选 smoke test：

```bash
python3 - <<'PY'
import asyncio, sys
sys.path.insert(0, '.')
from pipeline.orchestrator import run_pipeline
print(asyncio.run(run_pipeline({"intent":"earn_yield","underlying":"BTC","principal":10000,"durations":[7,14],"risk":"balanced"})))
PY
```

## 分享目的

这个包的目标不是“展示已经做完”，而是让技术同事拿到后能快速知道：
- 哪些逻辑已经能直接复用
- 哪些链路还没接完
- 当前产品意图是什么
- 应该从哪里继续实现
