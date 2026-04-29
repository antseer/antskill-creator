# MCP Tools Reference（V2）

> 19 个 MCP 工具 | 4 大领域 | 234 query_types | 8 个数据源
>
> 更新时间：2026-03-16

---

## 工具总览

| 领域 | 工具名 | query_types | 说明 |
|------|--------|-------------|------|
| **On-Chain** | ant_protocol_tvl_yields_revenue | 19 | 协议 TVL / 收益率 / 收入 |
| | ant_protocol_ecosystem | 6 | 协议生态系统元信息 |
| | ant_bridge_fund_flow | 5 | 跨链桥资金流向 |
| | ant_smart_money | 6 | 聪明钱追踪 |
| | ant_fund_flow | 17 | 交易所/矿工/巨鲸资金流 |
| | ant_token_analytics | 26 | 代币链上数据与深度分析 |
| | ant_stablecoin | 11 | 稳定币数据 |
| | ant_meme | 9 | MEME 代币热度 |
| | ant_address_profile | 9 | 钱包画像分析 |
| | ant_perp_dex | 6 | 去中心化衍生品 |
| **CeFi** | ant_futures_market_structure | 32 | 期货市场结构 |
| | ant_futures_liquidation | 9 | 期货爆仓 |
| | ant_market_indicators | 18 | 市场指标 |
| | ant_spot_market_structure | 24 | 现货市场结构 |
| **TradFi** | ant_etf_fund_flow | 16 | ETF 资金流 |
| | ant_us_stock_tokens | 11 | 美股代币化资产 |
| | ant_precious_metal_tokens | 11 | 贵金属代币化资产 |
| **Macro & Sentiment** | ant_macro_economics | 9 | 宏观经济指标 |
| | ant_market_sentiment | 15 | 市场舆情 |

---

## 1. On-Chain 链上数据（10 个工具）

### 1.1 ant_protocol_tvl_yields_revenue

**协议 TVL / 收益率 / 收入**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query_type | str | _必填_ | 查询类型 |
| protocol | str | None | 协议名称（如 "aave"） |
| chain | str | None | 链名称（如 "Ethereum"） |
| period | str | "24h" | 时间周期 |
| limit | int | 10 | 返回条数 |
| sort_by | str | "tvl" | 排序字段 |
| sort_order | str | "desc" | 排序方向 |
| project | str | None | 项目名 |
| token_symbol | str | None | 代币符号 |
| min_tvl_usd | int | None | 最小 TVL 筛选 |
| min_apy | float | None | 最小 APY 筛选 |
| pool_id | str | None | 池子 ID |
| timestamp | int | None | 时间戳 |
| data_type | str | None | 数据类型 |
| marketplace | str | None | 市场平台 |
| base_asset | str | None | 基础资产 |

**Query Types (19):**

| query_type | 说明 | 必需参数 |
|-----------|------|----------|
| protocol_tvl | 协议 TVL（总锁仓量） | protocol |
| protocol_volume | 协议 DEX 交易量 | protocol |
| protocol_fees | 协议手续费 | protocol |
| protocol_revenue | 协议收入 | protocol |
| protocol_overview | 协议全部指标汇总 | protocol |
| protocol_inflows | 协议资金净流入/流出 | protocol, timestamp |
| token_protocols | 查询持有某代币的协议 | token_symbol |
| chain_tvl_history | 全链/单链历史 TVL 时间序列 | — (可选 chain) |
| chain_assets | 各链资产构成分类 | — |
| dex_overview | 全网 DEX 交易量排名 | — (可选 chain) |
| fees_overview | 全网协议手续费/收入排名 | — (可选 chain, data_type) |
| yield_pools | DeFi 流动性池 APY | — |
| yield_borrow | 借贷池利率 | — |
| yield_lsd | LSD 收益率 | — |
| yield_pool_history | 单池历史 APY | pool_id |
| yield_lend_borrow_history | 单池借贷利率历史 | pool_id |
| yield_pools_with_address | 收益池含合约地址 | — |
| yield_perps | 永续合约资金费率 | — (可选 marketplace, base_asset) |
| chains | 所有公链及其 TVL | — |

---

### 1.2 ant_protocol_ecosystem

**协议生态系统**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query_type | str | _必填_ | 查询类型 |
| limit | int | 10 | 返回条数 |

**Query Types (6):**

| query_type | 说明 |
|-----------|------|
| ecosystem_hacks | 安全事件 / 黑客攻击记录 |
| ecosystem_categories | DeFi 协议分类 |
| ecosystem_oracles | 预言机覆盖数据 |
| ecosystem_raises | 项目融资记录 |
| ecosystem_entities | 机构实体持仓 |
| ecosystem_treasuries | 协议金库持仓 |

---

### 1.3 ant_bridge_fund_flow

**跨链桥资金流向**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query_type | str | _必填_ | 查询类型 |
| bridge_id | int | None | 桥 ID |
| bridge_name | str | None | 桥名称 |
| chain | str | None | 链名称 |
| date | str | None | 日期 |
| start_timestamp | int | None | 开始时间戳 |
| end_timestamp | int | None | 结束时间戳 |
| source_chain | str | None | 来源链 |
| address | str | None | 地址 |
| limit | int | 10 | 返回条数 |

**Query Types (5):**

| query_type | 说明 | 必需参数 |
|-----------|------|----------|
| bridges_list | 所有跨链桥列表及交易量 | — |
| bridges_volume | 单桥按链拆分的交易量 | bridge_id 或 bridge_name |
| bridges_daily_stats | 指定链的日度资金流入流出 | chain |
| bridges_chain_history | 指定链跨链桥历史日存取款量 | chain |
| bridges_transactions | 跨链桥交易流水 | bridge_id |

---

### 1.4 ant_smart_money

**聪明钱追踪**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query_type | str | _必填_ | 查询类型 |
| chains | str (JSON) | None | 链筛选，如 `'["ethereum"]'` |
| filters | str (JSON) | None | 过滤条件 |
| order_by | str (JSON) | None | 排序规则 |
| pagination | str (JSON) | None | 分页参数 |
| extra | str (JSON) | None | 扩展参数 |

**Query Types (6):**

| query_type | 说明 |
|-----------|------|
| netflows | 聪明钱代币净流量 |
| holdings | 当前持仓 |
| historical_holdings | 历史持仓 |
| dex_trades | DEX 交易记录 |
| dcas | Jupiter DCA 定投订单（Solana） |
| perp_trades | Hyperliquid 永续合约交易 |

---

### 1.5 ant_fund_flow

**资金流**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query_type | str | _必填_ | 查询类型 |
| asset | str | None | 资产（btc/eth/stablecoin/erc20/xrp） |
| exchange | str | None | 交易所 |
| miner | str | None | 矿池 |
| token | str | None | 代币 |
| symbol | str | None | 交易对符号 |
| window | str | "day" | 时间窗口 |
| from_date | str | None | 开始日期 |
| to_date | str | None | 结束日期 |
| limit | int | 100 | 返回条数 |

**链上资金流 Query Types (12):**

| query_type | 说明 |
|-----------|------|
| exchange_reserve | 交易所储备量 |
| exchange_netflow | 交易所净流量 |
| exchange_inflow | 交易所流入 |
| exchange_outflow | 交易所流出 |
| exchange_transactions_count | 交易所交易笔数 |
| miner_reserve | 矿工储备量 |
| miner_netflow | 矿工净流量 |
| miner_inflow | 矿工流入 |
| miner_outflow | 矿工流出 |
| exchange_whale_ratio | 交易所巨鲸比率 |
| mpi | 矿工持仓指数 |
| fund_flow_ratio | 资金流比率 |

**中心化交易所链上监控 Query Types (5):**

| query_type | 说明 |
|-----------|------|
| centralized_exchange_assets | 交易所链上资产总览 |
| centralized_exchange_balance_list | 交易所余额列表 |
| centralized_exchange_balance_chart | 交易所余额图表 |
| centralized_exchange_transfers | 交易所转账记录 |
| centralized_exchange_whale_transfer | 巨鲸转账 V2 |

---

### 1.6 ant_token_analytics

**代币分析**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query_type | str | _必填_ | 查询类型 |
| asset | str | None | 资产（btc/eth） |
| exchange | str | None | 交易所 |
| market | str | None | 市场类型 |
| window | str | "day" | 时间窗口 |
| from_date | str | None | 开始日期 |
| to_date | str | None | 结束日期 |
| limit | int | 100 | 返回条数 |
| token_address | str | None | 代币合约地址 |
| chain | str | None | 链名称 |
| timeframe | str | None | 时间范围 |
| label_type | str | None | 标签类型 |
| filters | str (JSON) | None | 过滤条件 |
| pagination | str (JSON) | None | 分页参数 |
| extra | str (JSON) | None | 扩展参数 |

**链上网络数据 Query Types (13):**

| query_type | 说明 |
|-----------|------|
| supply | 代币供应量 |
| transactions_count | 链上交易笔数 |
| addresses_count | 活跃地址数 |
| tokens_transferred | 链上转账量 |
| blockreward | 区块奖励 |
| difficulty | 挖矿难度 |
| hashrate | 全网算力 |
| fees | 链上手续费 |
| price_ohlcv | 价格 OHLCV |
| nvt | NVT 比率 |
| nvt_golden_cross | NVT 金叉信号 |
| stock_to_flow | S2F 模型 |
| mvrv | MVRV 指标 |

**代币深度分析 Query Types (13):**

| query_type | 说明 |
|-----------|------|
| token_screener | 代币筛选器 |
| perp_screener | 永续合约筛选器 |
| flow_intelligence | 资金流向情报 |
| flows | 流入流出 |
| who_bought_sold | 买卖方分析 |
| dex_trades | DEX 交易 |
| perp_trades | 合约交易 |
| transfers | 代币转账 |
| jup_dca | Jupiter DCA |
| holders | 持有者分析 |
| perp_positions | 合约仓位 |
| pnl_leaderboard | 盈亏排行榜 |
| perp_pnl_leaderboard | 合约盈亏排行榜 |

---

### 1.7 ant_stablecoin

**稳定币**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query_type | str | _必填_ | 查询类型 |
| stablecoin | str | None | 稳定币名称 |
| stablecoin_id | int | None | 稳定币 ID |
| chain | str | None | 链名称 |
| limit | int | 10 | 返回条数 |
| sort_by | str | "mcap" | 排序字段 |
| sort_order | str | "desc" | 排序方向 |
| window | str | "day" | 时间窗口 |
| from_date | str | None | 开始日期 |
| to_date | str | None | 结束日期 |

**Query Types (11):**

| query_type | 说明 | 必需参数 |
|-----------|------|----------|
| mcap | 稳定币市值排行 | — |
| price | 稳定币当前价格 | — |
| chain_distribution | 各链流通量分布 | — |
| dominance | 市场主导率 | — |
| overview | 综合查询 | — |
| detail | 单个稳定币详情 | stablecoin_id |
| history_all | 全网历史总流通量 | — |
| history_chain | 指定链历史流通量 | chain |
| chains | 各链当前流通量快照 | — |
| prices_history | 历史每日价格 | — |
| supply_network | 链上网络供应量历史 | — |

---

### 1.8 ant_meme

**MEME 代币**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query_type | str | _必填_ | 查询类型 |
| chain_id | str | None | 链 ID（如 "solana"） |
| token_address | str | None | 代币地址 |
| token_addresses | str | None | 逗号分隔地址列表 |
| pair_id | str | None | 交易对 ID |
| query | str | None | 搜索关键词 |
| limit | int | 10 | 返回条数 |

**Query Types (9):**

| query_type | 说明 | 必需参数 |
|-----------|------|----------|
| trending_tokens | 最新热门代币 | — |
| boost_latest | 最新 Boost 代币 | — |
| boost_top | Boost 排行榜 | — |
| community_takeover | 社区接管项目 | — |
| token_info | 代币详情 | chain_id, token_addresses |
| token_pairs | 代币交易对 | chain_id, token_address |
| pair_info | 交易对详情 | chain_id, pair_id |
| search_pairs | 搜索交易对 | query |
| paid_orders | 代币付费订单 | chain_id, token_address |

---

### 1.9 ant_address_profile

**钱包画像**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query_type | str | _必填_ | 查询类型 |
| address | str | None | 钱包地址 |
| entity_name | str | None | 实体名称 |
| chain | str | None | 链名称 |
| date | str (JSON) | None | 日期范围 |
| group_by | str | None | 分组字段 |
| filters | str (JSON) | None | 过滤条件 |
| pagination | str (JSON) | None | 分页参数 |
| extra | str (JSON) | None | 扩展参数 |

**Query Types (9):**

| query_type | 说明 | 必需参数 |
|-----------|------|----------|
| current_balance | 当前余额 | address, chain |
| historical_balances | 历史余额 | address, chain |
| transactions | 交易记录 | address, chain |
| counterparties | 交易对手方 | address, chain |
| pnl_summary | 盈亏汇总 | address, chain |
| pnl | 盈亏明细 | address, chain |
| related_wallets | 关联钱包 | address, chain |
| labels | 地址标签 | address, chain |
| transaction_lookup | 交易哈希查询 | extra (含 tx_hash) |

---

### 1.10 ant_perp_dex

**去中心化衍生品**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query_type | str | _必填_ | 查询类型 |
| symbol | str | None | 币种符号 |
| user_address | str | None | 用户地址 |
| address | str | None | 地址 |

**Query Types (6):**

| query_type | 说明 | 必需参数 |
|-----------|------|----------|
| perp_dex_whale_alert | 鲸鱼仓位变动预警 | — |
| perp_dex_whale_position | 鲸鱼大仓位列表 | — |
| perp_dex_position_by_coin | 按币种查持仓分布 | symbol |
| perp_dex_position_by_address | 地址持仓快照 | user_address |
| perp_dex_wallet_position_distribution | 钱包持仓规模分布 | — |
| perp_dex_wallet_pnl_distribution | 钱包盈亏分布 | — |

---

## 2. CeFi 中心化金融（4 个工具）

### 2.1 ant_futures_market_structure

**期货市场结构** — 32 query_types

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query_type | str | _必填_ | 查询类型 |
| symbol | str | "BTC" | 交易对 |
| exchange | str | None | 交易所 |
| interval | str | None | 时间间隔 |
| limit | int | None | 返回条数 |
| model | int | 1 | 模型参数 |
| range | str | None | 时间范围 |
| exchange_list | str | None | 交易所列表（逗号分隔） |
| usd | int | None | 本金（套利计算） |
| min_amount | int | None | 最小金额 |
| state | int | None | 状态 |
| start_time | int | None | 开始时间戳 |
| end_time | int | None | 结束时间戳 |

| 子分类 | query_type | 说明 |
|--------|-----------|------|
| 交易市场 | futures_market_snapshot | 合约市场快照 |
| | futures_pairs_market | 交易对行情快照 |
| | futures_price_change | 价格涨跌幅 |
| | futures_price_history | OHLC 历史蜡烛图 |
| OI | futures_oi_history | 单交易所 OI 历史 |
| | futures_oi_aggregated | 聚合 OI 历史 |
| | futures_oi_stablecoin | 稳定币保证金 OI |
| | futures_oi_coin_margin | 币本位保证金 OI |
| | futures_oi_exchange_list | 交易所 OI 排名 |
| | futures_oi_exchange_history | 交易所 OI 历史 |
| 资金费率 | futures_funding_rate_history | 单交易所资金费率历史 |
| | futures_funding_rate_exchange_list | 各交易所资金费率 |
| | futures_funding_rate_oi_weight | OI 加权资金费率 |
| | futures_funding_rate_vol_weight | 成交量加权资金费率 |
| | futures_funding_rate_accumulated | 累计资金费率 |
| | futures_funding_rate_arbitrage | 资金费率套利机会 |
| 多空比 | futures_long_short_global | 全市场多空比 |
| | futures_long_short_top_account | 大户账户多空比 |
| | futures_long_short_top_position | 大户持仓多空比 |
| | futures_taker_ratio_exchange | 主动买卖比率 |
| | futures_net_position | 净多/空仓位 |
| 订单簿 | futures_orderbook_ask_bids | 单交易所订单簿 |
| | futures_orderbook_aggregated | 聚合订单簿 |
| | futures_orderbook_history | 历史挂单深度 |
| | futures_orderbook_large_orders | 大额限价挂单 |
| | futures_orderbook_large_orders_history | 历史大额挂单 |
| 买卖/CVD | futures_taker_flow | 单交易所主动买卖 |
| | futures_taker_flow_aggregated | 聚合主动买卖 |
| | futures_footprint | Footprint 图 |
| | futures_cvd | 单交易对 CVD |
| | futures_cvd_aggregated | 聚合 CVD |
| | futures_netflow | 合约净资金流向 |

---

### 2.2 ant_futures_liquidation

**期货爆仓** — 9 query_types

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query_type | str | _必填_ | 查询类型 |
| symbol | str | "BTC" | 交易对 |
| exchange | str | None | 交易所 |
| interval | str | None | 时间间隔 |
| limit | int | None | 返回条数 |
| model | int | 1 | 模型参数 |
| range | str | None | 时间范围 |
| min_amount | int | None | 最小金额 |

| 子分类 | query_type | 说明 |
|--------|-----------|------|
| 爆仓历史 | futures_liquidation_history | 单交易所爆仓历史 |
| | futures_liquidation_aggregated | 聚合爆仓历史 |
| | futures_liquidation_coin_list | 币种爆仓排行 |
| | futures_liquidation_exchange_list | 交易所爆仓排行 |
| 爆仓订单 | futures_liquidation_order | 单笔爆仓订单 |
| 爆仓地图 | futures_liquidation_map | 爆仓价位地图 |
| | futures_liquidation_aggregated_map | 聚合爆仓地图 |
| 热力图 | futures_liquidation_heatmap | 爆仓热力图 |
| | futures_liquidation_agg_heatmap | 聚合爆仓热力图 |

---

### 2.3 ant_market_indicators

**市场指标** — 18 query_types

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query_type | str | _必填_ | 查询类型 |
| symbol | str | "BTC" | 交易对 |
| exchange | str | None | 交易所 |
| interval | str | None | 时间间隔 |
| limit | int | None | 返回条数 |
| window | int | None | 窗口期 |
| series_type | str | None | 序列类型 |
| fast_window | int | None | MACD 快线 |
| slow_window | int | None | MACD 慢线 |
| signal_window | int | None | MACD 信号线 |
| mult | float | None | 布林带乘数 |

| 子分类 | query_type | 说明 |
|--------|-----------|------|
| 合约技术 | rsi | RSI 相对强弱指标 |
| | basis | 期现基差 |
| | ma | 移动平均线 |
| | ema | 指数移动平均线 |
| | boll | 布林带 |
| | macd | MACD 指标 |
| | macd_list | 币种 MACD 信号列表 |
| | whale_index | 鲸鱼指数 |
| | cgdi | 衍生品贪婪恐惧指数 |
| | cdri | 衍生品风险指数 |
| | atr | 平均真实波幅 |
| 现货行情 | netflow | 现货净资金流向 |
| | orderbook_ask_bids | 现货订单簿 |
| | taker_flow | 现货主动买卖 |
| | taker_flow_aggregated | 聚合现货买卖 |
| 现货技术 | coinbase_premium | Coinbase 溢价指数 |
| | bitfinex_margin | Bitfinex 保证金多空 |
| 借贷 | borrow_rate | 杠杆借贷利率 |

---

### 2.4 ant_spot_market_structure

**现货市场结构** — 24 query_types

适用范围：加密原生代币（BTC/ETH/SOL 等）及通用市场数据查询。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query_type | str | _必填_ | 查询类型 |
| coin_id | str | None | 代币 ID（如 "bitcoin"） |
| ids | str | None | 批量 ID |
| vs_currency | str | "usd" | 计价货币 |
| platform_id | str | None | 平台 ID |
| contract_address | str | None | 合约地址 |
| contract_addresses | str | None | 批量合约地址 |
| days | str | "7" | 天数 |
| date | str | None | 日期 |
| from_timestamp | str | None | 开始时间戳 |
| to_timestamp | str | None | 结束时间戳 |
| order | str | "market_cap_desc" | 排序 |
| per_page | int | 50 | 每页条数 |
| page | int | 1 | 页码 |
| category | str | None | 分类 |
| query | str | None | 搜索关键词 |

| 子分类 | query_type | 说明 |
|--------|-----------|------|
| 价格 | simple_price | 批量查价格 |
| | simple_token_price | 合约地址查价格 |
| | supported_vs_currencies | 支持的计价货币 |
| 详情 | coin_detail | 代币完整详情 |
| | coin_tickers | 交易所行情 |
| 历史 | coin_market_chart | 历史价格图表 |
| | coin_market_chart_range | 指定范围历史图表 |
| | coin_ohlc | OHLC K线 |
| | coin_history | 指定日期快照 |
| 合约 | coin_contract | 合约代币数据 |
| | coin_contract_market_chart | 合约历史图表 |
| | coin_contract_market_chart_range | 合约范围图表 |
| 列表 | coins_list | 代币列表 |
| | coins_markets | 市场排行 |
| | coins_list_new | 最近上线代币 |
| | coins_top_gainers_losers | 涨跌幅榜 |
| 全局 | ping | API 状态检查 |
| | global_stats | 全局市场统计 |
| | global_defi | DeFi 市场统计 |
| | exchange_rates | BTC 汇率 |
| | search_trending | 热搜代币 |
| | coins_categories | 分类市场数据 |
| | coins_categories_list | 分类列表 |
| | asset_platforms | 资产平台列表 |
| | entities_list | 持仓实体列表 |
| | search | 搜索 |
| | global_market_cap_chart | 全球市值图表 |
| | companies_public_treasury | 公司持仓 |
| | token_lists | 平台代币列表 |

---

## 3. TradFi 传统金融（3 个工具）

### 3.1 ant_etf_fund_flow

**ETF 资金流** — 16 query_types

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query_type | str | _必填_ | 查询类型 |
| symbol | str | None | 币种符号 |
| interval | str | None | 时间间隔 |
| limit | int | None | 返回条数 |
| ticker | str | None | ETF 代码（如 "GBTC"） |
| range | str | None | 时间范围 |

| 子分类 | query_type | 说明 |
|--------|-----------|------|
| BTC ETF (US) | btc_etf_list | BTC ETF 列表 |
| | btc_etf_flow | BTC ETF 每日资金流 |
| | btc_etf_net_assets | BTC ETF 净资产 |
| | btc_etf_premium_discount | BTC ETF 溢折价 |
| | btc_etf_history | BTC ETF 综合历史 |
| | btc_etf_price | BTC ETF 股价 OHLC |
| | btc_etf_detail | BTC ETF 详情 |
| | btc_etf_aum | BTC ETF AUM |
| BTC ETF (HK) | hk_btc_etf_flow | 香港 BTC ETF 资金流 |
| ETH ETF | eth_etf_list | ETH ETF 列表 |
| | eth_etf_flow | ETH ETF 资金流 |
| | eth_etf_net_assets | ETH ETF 净资产 |
| 信托基金 | grayscale_holdings | 信托持仓列表 |
| | grayscale_premium | 灰度溢折价 |
| SOL/XRP | sol_etf_flow | SOL ETF 资金流 |
| | xrp_etf_flow | XRP ETF 资金流 |

---

### 3.2 ant_us_stock_tokens

**美股代币化资产（RWA）** — 11 query_types

适用范围：传统美股经链上代币化后的产品（Ondo、BackedFi xStocks 系列）。

主要代币：tesla-xstock (TSLAX), nvidia-xstock (NVDAX), alphabet-xstock (GOOGLX), coinbase-xstock (COINX), nvidia-ondo-tokenized-stock (NVDAON), tesla-ondo-tokenized-stock (TSLAON), microsoft-ondo-tokenized-stock (MSFTON)

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query_type | str | _必填_ | 查询类型 |
| coin_id | str | None | 代币 ID |
| ids | str | None | 批量 ID |
| vs_currency | str | "usd" | 计价货币 |
| platform_id | str | None | 平台 ID |
| contract_address | str | None | 合约地址 |
| contract_addresses | str | None | 批量合约地址 |
| days | str | "7" | 天数 |
| date | str | None | 日期 |
| from_timestamp | str | None | 开始时间戳 |
| to_timestamp | str | None | 结束时间戳 |

| query_type | 说明 |
|-----------|------|
| simple_price | 批量查价格 |
| simple_token_price | 合约地址查价格 |
| coin_detail | 代币完整详情 |
| coin_tickers | 交易所行情 |
| coin_market_chart | 历史价格图表 |
| coin_market_chart_range | 指定范围历史图表 |
| coin_ohlc | OHLC K线 |
| coin_history | 指定日期快照 |
| coin_contract | 合约代币数据 |
| coin_contract_market_chart | 合约历史图表 |
| coin_contract_market_chart_range | 合约范围图表 |

---

### 3.3 ant_precious_metal_tokens

**贵金属代币化资产（RWA）** — 11 query_types

适用范围：黄金、白银等实物资产经链上代币化后的产品。

主要代币：tether-gold (XAUT), pax-gold (PAXG), kinesis-gold (KAU), matrixdock-gold (XAUM), kinesis-silver (KAG), ishares-silver-trust-ondo-tokenized-stock (SLVON)

参数和 query_types 与 ant_us_stock_tokens 完全相同（见 3.2）。

---

## 4. Macro & Sentiment 宏观与舆情（2 个工具）

### 4.1 ant_macro_economics

**宏观经济** — 9 query_types

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query_type | str | _必填_ | 查询类型 |
| interval | str | None | 频率 |
| maturity | str | None | 债券期限 |

| 子分类 | query_type | 说明 |
|--------|-----------|------|
| 经济增长 | real_gdp | 美国实际 GDP |
| | real_gdp_per_capita | 人均 GDP |
| 通胀 | cpi | 消费者价格指数 |
| | inflation | 年度通胀率 |
| | expectation | 消费者通胀预期 |
| 利率 | federal_funds_rate | 联邦基金利率 |
| | treasury_yield | 国债收益率 |
| 劳动力 | unemployment | 失业率 |
| | nonfarm | 非农就业 |

---

### 4.2 ant_market_sentiment

**市场舆情** — 15 query_types

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query_type | str | _必填_ | 查询类型 |
| coin | str | None | 代币标识（如 "bitcoin"） |
| topic | str | None | 话题名称 |
| category | str | None | 分类标识 |
| network | str | None | 社交网络 |
| creator_id | str | None | 创作者 ID |
| sort | str | "galaxy_score" | 排序字段 |
| limit | int | 50 | 返回条数 |
| desc | bool | True | 降序 |
| page | int | None | 页码 |
| bucket | str | "day" | 时间粒度 |
| interval | str | None | 时间范围 |
| start | int | None | 开始时间戳 |
| end | int | None | 结束时间戳 |

| 子分类 | query_type | 说明 | 必需参数 |
|--------|-----------|------|----------|
| 代币情绪 | coins_list | 代币情绪评分排名 | — |
| | coin_detail | 单代币详细情绪 | coin |
| | coin_time_series | 情绪时间序列 | coin |
| | coin_meta | 代币元数据 | coin |
| 话题 | topics_list | 热门话题列表 | — |
| | topic_detail | 话题详情 | topic |
| | topic_time_series | 话题时间序列 | topic |
| | topic_posts | 话题帖子 | topic |
| | topic_news | 话题新闻 | topic |
| | topic_creators | 话题创作者 | topic |
| 分类 | categories_list | 所有分类 | — |
| | category_detail | 分类详情 | category |
| | category_topics | 分类话题 | category |
| 创作者 | creators_list | 创作者列表 | — |
| | creator_detail | 创作者详情 | network, creator_id |
