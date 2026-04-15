# DualYield — 技术待办清单

> 🔴 阻塞上线 · 🟡 上线后优化 · 🟢 锦上添花

---

## 🔴 P0 — 阻塞上线

### 1. Antseer 端点确认
**文件**: `pipeline/l1_data/sources/antseer.py`
- [ ] 确认 Antseer 是否有 DCI 产品聚合端点
- [ ] 确认市场数据端点 (K线+现货价)
- [ ] 实现 `fetch_dci_products()` + `fetch_market()`
- [ ] 字段映射到统一 schema

### 2. Binance DCI 接入
**文件**: `pipeline/l1_data/sources/binance.py`
- [ ] 填入 API Key + Secret
- [ ] 实现产品列表获取 + K 线获取
- [ ] 验证签名

### 3. 前端集成真实数据
**文件**: `frontend/dualyield.html`
- [ ] 替换 mock 数据为 orchestrator 输出
- [ ] 确定注入方式 (fetch API / 模板替换)

---

## 🟡 P1 — 上线后一周

### 4. OKX / Bybit / Bitget / KuCoin 接入
**文件**: `pipeline/l1_data/sources/cex_others.py`
- [ ] 每家: 签名实现 + 字段映射 + 错误处理 (各 0.5 天)

### 5. Redis 缓存
- [ ] 产品缓存 TTL 10min, 市场缓存 TTL 1min

### 6. Deribit IV 接入
- [ ] 公开 API, 补充波动率估算精度

---

## 🟢 P2 — 后续迭代

### 7. LLM 增强结论
- [ ] 接入 Claude Sonnet 生成带 TA 解读的结论

### 8. 阶梯利率
- [ ] 部分 CEX 对大额有阶梯 APR, 按本金取对应档

### 9. platform_meta 自动更新
- [ ] 定期抓取 PoR 状态

---

## 文件变更地图

```
需要改动:
  pipeline/l1_data/sources/antseer.py     ← P0
  pipeline/l1_data/sources/binance.py     ← P0
  pipeline/l1_data/sources/cex_others.py  ← P1
  pipeline/l1_data/fetcher.py             ← P1 (加缓存)
  frontend/dualyield.html                 ← P0 (真实数据)

不需要改动:
  pipeline/l2_compute/                    ✅ 完成, 32/32 测试通过
  pipeline/l3_decision/                   ✅ 模板模式完成
  pipeline/orchestrator.py                ✅ 完成
  data/platform_meta.yaml                 ✅ 完成
```
