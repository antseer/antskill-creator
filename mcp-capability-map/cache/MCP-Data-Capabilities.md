# third-mcp-server 数据能力与 Tools 实现文档

**更新日期：** 2026-04-24
**目的：** 内部技术/产品排查，完整梳理现有数据能力与 tool 实现细节

---

## 一、数据能力总览

### 1.1 数据类型覆盖

| 数据类型 | 覆盖范围 | 数据源 |
|---------|---------|-------|
| **Token 价格/行情** | 现货价格、OHLCV、K线、24h ticker、历史价格 | CoinGecko、Binance |
| **DeFi 协议数据** | TVL、Volume、Fees、Revenue、Yields、Lending、Borrow | DeFiLlama |
| **链上资金流** | 交易所储备、净流量、流入/流出、矿工流、鲸鱼比率 | CryptoQuant、Coinglass |
| **Smart Money** | 聪明钱追踪、持仓、历史持仓、DEX 交易、DCA、合约交易 | Nansen |
| **地址画像** | 钱包标签、余额、交易对手、PnL、相关钱包、聪明钱深度分析 | Nansen、Antseer |
| **稳定币数据** | 市值、价格、链分布、主导地位、供应网络、历史变化 | DeFiLlama、CryptoQuant |
| **跨链桥** | 桥列表、成交量、日统计、链历史、交易明细 | DeFiLlama |
| **永续 DEX** | 鲨鱼警报、持仓分布、聪明钱扫描、DEX 衍生品概览 | Coinglass、Antseer、DeFiLlama |
| **期货市场** | 持仓量、资金费率、清算、多空比、Orderbook、CVD | Coinglass |
| **期权** | IV 链、ATM IV、期限结构、Skew、DVOL | Deribit |
| **现货市场（CoinGecko）** | 价格、市值、分类、全球指标、趋势、交易所汇率、上市公司持仓 | CoinGecko |
| **ETF 基金流** | BTC/ETH/SOL/XRP ETF 流量、净值、溢价、持有量 | Coinglass |
| **宏观经济** | GDP、CPI、通胀、利率、失业率、非农 | AlphaVantage |
| **股票** | 报价、OHLCV、基本面、技术指标、指数 | AlphaVantage |
| **社交情绪** | 币种/话题/分类/创作者数据、时序分析 | LunarCrush |
| **Meme/Token 发现** | Trending、Boost、社区接管、付费推广、Token/Pair 搜索 | DexScreener |
| **预测市场** | 事件搜索、定价、订单簿、交易、排行榜、关联新闻、漂移统计、URL 解析 | Polymarket、LunarCrush |
| **CEX 理财** | 灵活存款、定期存款、DCI 双币投 | Binance、OKX、Bybit、Bitget、KuCoin、Gate |
| **CEX 安全评估** | 信任分、评级、牌照、成立年份 | CoinGecko |
| **DEX 滑点询价** | EVM 链内多 DEX 路由实时滑点报价 | ParaSwap |
| **跨链桥询价** | 多链桥接费用、Gas、路由对比 | LI.FI |
| **Token 链上分析** | 供应、NVT、MVRV、S2F、哈希率、难度、发行量 | CryptoQuant、DeFiLlama |
| **永续市场信号** | 资金费率套利、基差、多交易所divergence | Binance、OKX、Bybit、Coinglass |
| **Gas 追踪** | EVM 链实时 Gas 费 | Etherscan、公共 RPC |

### 1.2 数据源 Providers 概览

| Provider | 类型 | 关键数据 | API Key |
|---------|-----|---------|--------|
| **DeFiLlama** | DeFi 协议 | TVL、Yields、Fees、Bridges、Stablecoins、Emissions | 可选 Pro key |
| **CoinGecko** | 全局加密数据 | 价格、市值、分类、交易所、全球指标、CEX 安全 | 可选 Pro key |
| **Coinglass** | 衍生品/机构 | 期货 OI/清算/资金费率、ETF、指标、链上交易所流 | 必需 |
| **CryptoQuant** | 链上流量 | BTC/ETH/Stablecoin 交易所流量、矿工流、网络指标 | 必需 |
| **Nansen** | Smart Money | 钱包追踪、TGM、地址画像 | 必需 |
| **AlphaVantage** | 宏观经济 + 股票 | GDP、CPI、利率、股票 OHLCV、技术指标、指数 | 必需 |
| **Deribit** | 期权 | IV、Term Structure、Skew、DVOL | 无需（公开） |
| **DexScreener** | DEX/Meme | Trending Token、Pair 信息、Boost | 无需 |
| **ParaSwap** | DEX 滑点 | EVM 链内多 DEX 路由实时滑点 | 无需 |
| **LI.FI** | 跨链桥 | 桥接费用、Gas、路由对比 | 无需 |
| **Polymarket** | 预测市场 | Events、Market、Pricing、Activity | 无需 |
| **LunarCrush** | 社交数据 | 币种/话题/分类/创作者、时序数据 | 可选 |
| **Binance** | CEX | 现货/期货行情、理财产品 | 可选 signed |
| **OKX** | CEX | 理财（Savings/Staking/DCI）、资金费率 | 需 API key |
| **Bybit** | CEX | DCI 双币投（公开）、资金费率 | 无需/可选 |
| **Hyperliquid** | 永续 DEX | 用户交易统计、持仓数据 | 无需（公开） |
| **Antseer** | Smart Money（内部） | BTC/ETH/SOL 聪明钱分析、K线、地址深度分析 | 无需 |
| **Etherscan** | 链上数据 | Gas Oracle | 需 API key |

---

## 二、Domain 工具总览（39 tools）

### 2.1 OnChain 域（19 tools）
链上数据全景：DeFi 协议、资金流、Smart Money、稳定币、Meme、地址画像、永续 DEX、Gas、DEX/桥询价。

| Tool | 能力描述 | 底层数据源 |
|------|---------|----------|
| `ant_protocol_tvl_yields_revenue` | DeFi 协议 TVL/Volume/Fees/Revenue、Yield 池、链 TVL（19） | DeFiLlama |
| `ant_protocol_ecosystem` | 生态数据：黑客事件、分类、预言机、融资、实体、国库（6） | DeFiLlama |
| `ant_bridge_fund_flow` | 跨链桥：桥列表、成交量、日统计、链历史、交易（5） | DeFiLlama |
| `ant_smart_money` | Smart Money：净流量、持仓、DEX 交易、DCA、合约（6） | Nansen |
| `ant_fund_flow` | 交易所/矿工储备与流量、鲸鱼指标、CEX 链上监控（17） | CryptoQuant + Coinglass |
| `ant_token_analytics` | Token 链上指标 + Nansen TGM + 发行量（28） | CryptoQuant + Nansen + DeFiLlama |
| `ant_stablecoin` | 稳定币市值/价格/链分布/历史/供应网络（11） | DeFiLlama + CryptoQuant |
| `ant_meme` | Meme Token：Trending/Boost/CTO/付费推广/搜索（9） | DexScreener |
| `ant_address_profile` | 地址画像：余额/交易/PnL/标签/相关钱包/深度分析（10） | Nansen + Antseer |
| `ant_perp_dex` | 永续 DEX：鲨鱼仓位/持仓分布/聪明钱/DEX 概览（11） | Coinglass + Antseer + DeFiLlama |
| `ant_defi_pool_detail` | DeFi 池详情：协议、链、TVL、APY | DeFiLlama |
| `ant_defi_pool_history` | DeFi 池历史 TVL/Volume/APY 时序 | DeFiLlama |
| `ant_protocol_safety` | 协议安全：审计、黑客历史、风险评分 | DeFiLlama |
| `ant_yield_aggregate` | Yield 聚合：多源收益率汇总/排名 | DeFiLlama + 多 CEX |
| `ant_perp_market_hint` | 永续市场信号：funding 套利/基差/divergence | Binance + OKX + Bybit + Coinglass |
| `ant_hyperliquid_user_trade_stats` | Hyperliquid 用户交易统计 | Hyperliquid |
| `ant_gas_tracker` | EVM 链 Gas 费实时追踪 | Etherscan + 公共 RPC + CoinGecko |
| `ant_dex_swap_quote` | EVM 链 DEX 滑点询价（1） | ParaSwap |
| `ant_bridge_cross_chain_quote` | 跨链桥接询价（1） | LI.FI |

### 2.2 CeFi 域（6 tools）
中心化交易所数据：期货市场结构、清算、技术指标、CoinGecko 现货市场、CEX 理财产品、CEX 安全评估。

| Tool | 能力描述 | 底层数据源 |
|------|---------|----------|
| `ant_futures_market_structure` | 期货：OI/资金费率/多空比/Orderbook/Taker Flow/CVD（32） | Coinglass |
| `ant_futures_liquidation` | 期货清算：历史/热力图/地图/订单（9） | Coinglass |
| `ant_market_indicators` | 技术指标：RSI/Basis/MA/BOLL/MACD/鲸鱼/现货指标（18） | Coinglass |
| `ant_spot_market_structure` | CoinGecko 全功能：价格/市值/分类/全球/趋势/上市公司（29） | CoinGecko |
| `ant_cex_earn` | CEX 理财：活期/定期/DCI 双币投（18 路由） | Binance + OKX + Bybit + Bitget + KuCoin + Gate |
| `ant_cex_safety` | CEX 安全评估：信任分/评级/牌照/年份 | CoinGecko |

### 2.3 TradFi 域（3 tools）
传统金融资产：ETF 基金流（BTC/ETH/SOL/XRP/Grayscale）、美股 Token、贵金属 Token。

| Tool | 能力描述 | 底层数据源 |
|------|---------|----------|
| `ant_etf_fund_flow` | ETF：BTC/ETH/SOL/XRP 流量/净值/溢价/Grayscale（16） | Coinglass |
| `ant_us_stock_tokens` | 美股 Token 价格/行情（11） | CoinGecko |
| `ant_precious_metal_tokens` | 贵金属 Token 价格/行情（11） | CoinGecko |

### 2.4 Macro 域（2 tools）
宏观经济与社交情绪：美国宏观指标（GDP/CPI/利率/非农）、LunarCrush 社交数据。

| Tool | 能力描述 | 底层数据源 |
|------|---------|----------|
| `ant_macro_economics` | 宏观经济：GDP/CPI/通胀/利率/失业率/非农（9） | AlphaVantage |
| `ant_market_sentiment` | 社交情绪：币种/话题/分类/创作者（15） | LunarCrush |

### 2.5 Stock 域（2 tools）
美股数据：个股报价/OHLCV/基本面/技术指标/搜索/日历，以及主要股票指数（S&P 500/Dow/VIX）。

| Tool | 能力描述 | 底层数据源 |
|------|---------|----------|
| `ant_stock_data` | 股票：报价/OHLCV/基本面/技术指标/搜索/日历/指数（19） | AlphaVantage |
| `ant_index_data` | 美国主要股票指数 OHLC（S&P 500/Dow/NASDAQ/VIX） | AlphaVantage |

### 2.6 Binance 域（2 tools）
Binance 交易所直连：现货和期货的行情、K 线、OI、资金费率、多空比。

| Tool | 能力描述 | 底层数据源 |
|------|---------|----------|
| `ant_binance_spot` | 现货行情：24h Ticker/K线（2） | Binance |
| `ant_binance_futures` | 期货行情：Ticker/K线/OI/资金费率/多空比（7） | Binance Futures |

### 2.7 Prediction 域（4 tools）
Polymarket 预测市场全链路：事件发现、定价/订单簿、交易活跃度/排行榜、关联新闻、漂移分析。

| Tool | 能力描述 | 底层数据源 |
|------|---------|----------|
| `ant_prediction_event` | 预测事件：搜索/热门/详情/市场/标签/URL 解析（6） | Polymarket |
| `ant_prediction_pricing` | 预测定价：价格快照/订单簿/价格历史（3） | Polymarket CLOB |
| `ant_prediction_activity` | 预测活动：近期交易/OI/持有者/排行榜/概览/漂移统计（6） | Polymarket |
| `ant_prediction_news` | 预测市场关联新闻：按市场/关键词查新闻、impact 分级（2） | LunarCrush |

### 2.8 Options 域（1 tool）
加密期权市场：IV 链、ATM 波动率、期限结构、Skew、DVOL 指数，覆盖 BTC/ETH/SOL。

| Tool | 能力描述 | 底层数据源 |
|------|---------|----------|
| `ant_deribit_options` | 期权：IV链/ATM IV/期限结构/Skew/DVOL（5） | Deribit 公开 API |

---

## 三、Tool query_type 详细清单

### 3.1 OnChain 域

#### ant_protocol_tvl_yields_revenue（19）
查询 DeFi 协议的 TVL、成交量、手续费、收入，以及各链 TVL 历史、DEX 概览和各类 Yield 池数据。

| query_type | 数据源 |
|---|---|
| `protocol_tvl` | DeFiLlama 协议 TVL |
| `protocol_volume` | DeFiLlama 协议成交量 |
| `protocol_fees` | DeFiLlama 协议手续费 |
| `protocol_revenue` | DeFiLlama 协议收入 |
| `protocol_overview` | DeFiLlama 协议综合 |
| `protocol_inflows` | DeFiLlama 协议资金流入 |
| `token_protocols` | DeFiLlama Token 所属协议 |
| `chain_tvl_history` | DeFiLlama 链 TVL 历史 |
| `chain_assets` | DeFiLlama 链上资产 |
| `dex_overview` | DeFiLlama DEX 概览 |
| `fees_overview` | DeFiLlama 手续费概览 |
| `yield_pools` | DeFiLlama Yield 池列表 |
| `yield_borrow` | DeFiLlama 借贷池 |
| `yield_lsd` | DeFiLlama LSD 利率 |
| `yield_pool_history` | DeFiLlama 池历史 |
| `yield_lend_borrow_history` | DeFiLlama 借贷历史 |
| `yield_pools_with_address` | DeFiLlama 含地址池 |
| `yield_perps` | DeFiLlama 永续池 |
| `chains` | DeFiLlama 支持链列表 |

#### ant_protocol_ecosystem（6）
查询 DeFi 生态事件与元数据：黑客攻击、协议分类、预言机、融资、实体和国库资产。

| query_type | 数据源 |
|---|---|
| `ecosystem_categories` | DeFiLlama 协议分类 |
| `ecosystem_hacks` | DeFiLlama 黑客事件 |
| `ecosystem_oracles` | DeFiLlama 预言机 |
| `ecosystem_raises` | DeFiLlama 融资 |
| `ecosystem_treasuries` | DeFiLlama 国库 |
| `ecosystem_entities` | DeFiLlama 实体 |

#### ant_bridge_fund_flow（5）
查询跨链桥的列表、成交量、日统计、链历史及交易明细。

| query_type | 数据源 |
|---|---|
| `bridges_list` | DeFiLlama 桥列表 |
| `bridges_volume` | DeFiLlama 桥成交量 |
| `bridges_daily_stats` | DeFiLlama 桥日统计 |
| `bridges_chain_history` | DeFiLlama 桥链历史 |
| `bridges_transactions` | DeFiLlama 桥交易明细 |

#### ant_smart_money（6）
追踪链上 Smart Money 的净流量、持仓、DEX 交易、DCA 定投和合约交易。

| query_type | 数据源 |
|---|---|
| `netflows` | Nansen Smart Money 净流量 |
| `holdings` | Nansen 实时持仓 |
| `historical_holdings` | Nansen 历史持仓 |
| `dex_trades` | Nansen DEX 交易 |
| `dcas` | Nansen DCA 定投 |
| `perp_trades` | Nansen 合约交易 |

#### ant_fund_flow（17）
查询交易所/矿工的 BTC/ETH 储备与净流量、鲸鱼指标，以及中心化交易所链上资产和转账监控。

| query_type | 数据源 |
|---|---|
| `exchange_reserve` | CryptoQuant 交易所储备 |
| `exchange_netflow` | CryptoQuant 交易所净流量 |
| `exchange_inflow` | CryptoQuant 交易所流入 |
| `exchange_outflow` | CryptoQuant 交易所流出 |
| `exchange_transactions_count` | CryptoQuant 交易所交易笔数 |
| `miner_reserve` | CryptoQuant 矿工储备 |
| `miner_netflow` | CryptoQuant 矿工净流量 |
| `miner_inflow` | CryptoQuant 矿工流入 |
| `miner_outflow` | CryptoQuant 矿工流出 |
| `exchange_whale_ratio` | CryptoQuant 鲸鱼比率 |
| `mpi` | CryptoQuant 矿工持仓指数 |
| `fund_flow_ratio` | CryptoQuant 资金流比率 |
| `centralized_exchange_assets` | Coinglass CEX 链上资产 |
| `centralized_exchange_balance_list` | Coinglass CEX 余额列表 |
| `centralized_exchange_balance_chart` | Coinglass CEX 余额图表 |
| `centralized_exchange_transfers` | Coinglass CEX 转账 |
| `centralized_exchange_whale_transfer` | Coinglass 鲸鱼转账 |

#### ant_token_analytics（28）
Token 链上指标（供应/NVT/MVRV/S2F/哈希率）+ Nansen TGM 筛选器/Flow/持有者/PnL + Token 发行量。

| query_type | 数据源 |
|---|---|
| `supply` | CryptoQuant 代币供应 |
| `transactions_count` | CryptoQuant 交易笔数 |
| `addresses_count` | CryptoQuant 地址数 |
| `tokens_transferred` | CryptoQuant 转移量 |
| `blockreward` | CryptoQuant 出块奖励 |
| `difficulty` | CryptoQuant 难度 |
| `hashrate` | CryptoQuant 哈希率 |
| `fees` | CryptoQuant 手续费 |
| `price_ohlcv` | CryptoQuant 价格 OHLCV |
| `nvt` | CryptoQuant NVT 指标 |
| `nvt_golden_cross` | CryptoQuant NVT 金叉 |
| `stock_to_flow` | CryptoQuant Stock-to-Flow |
| `mvrv` | CryptoQuant MVRV |
| `token_screener` | Nansen TGM Token 筛选器 |
| `flow_intelligence` | Nansen TGM Flow 智能 |
| `holders` | Nansen TGM 持有者 |
| `flows` | Nansen TGM 资金流 |
| `who_bought_sold` | Nansen TGM 谁买谁卖 |
| `dex_trades` | Nansen TGM DEX 交易 |
| `transfers` | Nansen TGM 转账 |
| `jup_dca` | Nansen TGM Jupiter DCA |
| `pnl_leaderboard` | Nansen TGM PnL 排行 |
| `perp_screener` | Nansen TGM 合约筛选 |
| `perp_pnl_leaderboard` | Nansen TGM 合约 PnL 排行 |
| `perp_positions` | Nansen TGM 合约持仓 |
| `perp_trades` | Nansen TGM 合约交易 |
| `emissions` | DeFiLlama Token 发行总览 |
| `emission_detail` | DeFiLlama 单协议发行详情 |

#### ant_stablecoin（11）
稳定币市值、价格、各链分布、主导地位、供应网络及历史变化趋势。

| query_type | 数据源 |
|---|---|
| `mcap` | DeFiLlama 稳定币市值 |
| `price` | DeFiLlama 稳定币价格 |
| `chain_distribution` | DeFiLlama 链分布 |
| `dominance` | DeFiLlama 主导地位 |
| `overview` | DeFiLlama 综合概览 |
| `detail` | DeFiLlama 单币详情 |
| `history_all` | DeFiLlama 全链市值历史 |
| `history_chain` | DeFiLlama 按链历史 |
| `chains` | DeFiLlama 稳定币支持链 |
| `prices_history` | DeFiLlama 价格历史 |
| `supply_network` | CryptoQuant 供应网络 |

#### ant_meme（9）
Meme Token 发现：热门/Boost 排名/社区接管/付费推广/Token 与交易对搜索。

| query_type | 数据源 |
|---|---|
| `trending_tokens` | DexScreener 热门 Token |
| `boost_latest` | DexScreener 最新 Boost |
| `boost_top` | DexScreener Boost 排行 |
| `community_takeover` | DexScreener 社区接管 |
| `token_info` | DexScreener Token 详情 |
| `token_pairs` | DexScreener Token 交易对 |
| `pair_info` | DexScreener 交易对详情 |
| `search_pairs` | DexScreener 搜索 |
| `paid_orders` | DexScreener 付费推广 |

#### ant_address_profile（10）
钱包地址画像：余额、交易历史、交易对手、PnL、标签、相关钱包、聪明钱深度分析。

| query_type | 数据源 |
|---|---|
| `current_balance` | Nansen 当前余额 |
| `historical_balances` | Nansen 历史余额 |
| `transactions` | Nansen 交易历史 |
| `counterparties` | Nansen 交易对手 |
| `related_wallets` | Nansen 相关钱包 |
| `pnl_summary` | Nansen PnL 汇总 |
| `pnl` | Nansen 详细 PnL |
| `labels` | Nansen 钱包标签 |
| `transaction_lookup` | Nansen 单笔交易查询 |
| `smart_money_analyze` | Antseer 聪明钱深度分析 |

#### ant_perp_dex（11）
永续 DEX 数据：鲨鱼仓位/持仓分布/盈亏分布/聪明钱扫描/DEX 衍生品概览。

| query_type | 数据源 |
|---|---|
| `perp_dex_whale_alert` | Coinglass 鲨鱼仓位警报 |
| `perp_dex_whale_position` | Coinglass 鲨鱼大仓位 |
| `perp_dex_position_by_coin` | Coinglass 按币种持仓 |
| `perp_dex_position_by_address` | Coinglass 按地址持仓 |
| `perp_dex_wallet_position_distribution` | Coinglass 持仓规模分布 |
| `perp_dex_wallet_pnl_distribution` | Coinglass 盈亏分布 |
| `smart_money_scan` | Antseer 聪明钱扫描 + Hyperliquid 增强 |
| `smart_money_chart` | Antseer K线 + markers |
| `perp_dex_overview` | DeFiLlama 衍生品 DEX 概览 |
| `perp_dex_protocol_detail` | DeFiLlama 单协议详情 |
| `perp_dex_metrics` | DeFiLlama 衍生品指标 |

#### ant_dex_swap_quote（1）
EVM 链内 DEX 滑点询价：多路由对比、最优路径、滑点百分比。

| query_type | 数据源 |
|---|---|
| `slippage_quote` | ParaSwap EVM 链 DEX 滑点询价 |

#### ant_bridge_cross_chain_quote（1）
跨链桥接询价：费用、Gas、路由对比、预计耗时。

| query_type | 数据源 |
|---|---|
| `cross_chain_quote` | LI.FI 跨链桥接询价 |

#### 直接参数工具（无 query_type 分发）

| Tool | 功能 | 数据源 |
|------|------|--------|
| `ant_defi_pool_detail` | DeFi 池详情（需 pool_id/pool_ids） | DeFiLlama |
| `ant_defi_pool_history` | DeFi 池历史时序（需 pool_id/pool_ids） | DeFiLlama |
| `ant_protocol_safety` | 协议安全风险评估（需 protocol_slug）；YAML 覆盖 31 个协议，含赎回期/容量字段 | DeFiLlama + YAML |
| `ant_yield_aggregate` | 多源 Yield 聚合排名；`include_safety=True` 时含赎回期/容量字段 | DeFiLlama + 多 CEX |
| `ant_perp_market_hint` | 永续市场信号/divergence | Binance + OKX + Bybit + Coinglass |
| `ant_hyperliquid_user_trade_stats` | HL 用户交易统计 | Hyperliquid |
| `ant_gas_tracker` | EVM Gas 实时追踪 | Etherscan + RPC + CoinGecko |

**`ant_protocol_safety` / `ant_yield_aggregate(include_safety=True)` 新增 safety 字段：**

| 字段 | 类型 | 含义 |
|---|---|---|
| `redeem_delay_hours` | float\|null | 申请赎回后最短到账等待（小时）；即时=0.05，排队型为排队最短预期 |
| `redeem_delay_hours_max` | float\|null | 最长等待（null=固定值）|
| `redeem_type` | string | `instant`\|`queue`\|`fixed`\|`maturity` |
| `has_withdrawal_queue` | bool | 是否存在链上赎回排队 |
| `capacity_cap_usd` | float\|null | 协议级总额度上限；null=无明确上限 |

**YAML 已覆盖协议（31 条）：** aave-v3、compound-v3、morpho-blue、spark、pendle、curve、fluid、ethena、venus-core-pool、justlend、lido、rocket-pool、frax、stader、ankr、jito、eigenlayer、ether.fi、symbiotic、karak、uniswap、balancer、convex、gmx、yearn、beefy、maker、liquity、kamino、marginfi、across-protocol

---

### 3.2 CeFi 域

#### ant_futures_market_structure（32）
期货市场全面结构数据：OI、资金费率、多空比、Orderbook、Taker Flow、CVD、净头寸。

| query_type | 数据源 |
|---|---|
| `futures_market_snapshot` | Coinglass 合约市场快照 |
| `futures_pairs_market` | Coinglass 交易对行情 |
| `futures_price_change` | Coinglass 价格涨跌幅 |
| `futures_price_history` | Coinglass OHLC 历史 |
| `futures_oi_history` | Coinglass 单交易所 OI 历史 |
| `futures_oi_aggregated` | Coinglass 聚合 OI 历史 |
| `futures_oi_stablecoin` | Coinglass 稳定币合约 OI |
| `futures_oi_coin_margin` | Coinglass 币本位合约 OI |
| `futures_oi_exchange_list` | Coinglass 各交易所 OI 排名 |
| `futures_oi_exchange_history` | Coinglass 各交易所 OI 历史 |
| `futures_funding_rate_history` | Coinglass 资金费率历史 |
| `futures_funding_rate_exchange_list` | Coinglass 各交易所费率 |
| `futures_funding_rate_oi_weight` | Coinglass OI 加权费率 |
| `futures_funding_rate_vol_weight` | Coinglass 成交量加权费率 |
| `futures_funding_rate_accumulated` | Coinglass 累计费率 |
| `futures_funding_rate_arbitrage` | Coinglass 费率套利机会 |
| `futures_long_short_global` | Coinglass 全市场多空比 |
| `futures_long_short_top_account` | Coinglass 大户账户多空比 |
| `futures_long_short_top_position` | Coinglass 大户持仓多空比 |
| `futures_taker_ratio_exchange` | Coinglass 主动买卖比率 |
| `futures_net_position` | Coinglass 净仓位 |
| `futures_orderbook_ask_bids` | Coinglass 订单簿 |
| `futures_orderbook_aggregated` | Coinglass 聚合订单簿 |
| `futures_orderbook_history` | Coinglass 历史订单簿热力图 |
| `futures_orderbook_large_orders` | Coinglass 大额挂单 |
| `futures_orderbook_large_orders_history` | Coinglass 历史大额挂单 |
| `futures_taker_flow` | Coinglass 主动买卖 |
| `futures_taker_flow_aggregated` | Coinglass 聚合主动买卖 |
| `futures_footprint` | Coinglass Footprint 图 |
| `futures_cvd` | Coinglass CVD |
| `futures_cvd_aggregated` | Coinglass 聚合 CVD |
| `futures_netflow` | Coinglass 合约净资金流 |

#### ant_futures_liquidation（9）
期货清算数据：清算历史、价格地图、热力图、各交易所/币种排行、单笔订单。

| query_type | 数据源 |
|---|---|
| `futures_liquidation_history` | Coinglass 单交易所清算历史 |
| `futures_liquidation_aggregated` | Coinglass 聚合清算历史 |
| `futures_liquidation_coin_list` | Coinglass 各币种清算排行 |
| `futures_liquidation_exchange_list` | Coinglass 各交易所清算排行 |
| `futures_liquidation_order` | Coinglass 单笔清算订单 |
| `futures_liquidation_map` | Coinglass 清算价位地图 |
| `futures_liquidation_aggregated_map` | Coinglass 聚合清算地图 |
| `futures_liquidation_heatmap` | Coinglass 清算热力图 |
| `futures_liquidation_agg_heatmap` | Coinglass 聚合清算热力图 |

#### ant_market_indicators（18）
合约/现货技术指标：RSI、Basis、MA/EMA/BOLL/MACD、鲸鱼指数、Coinbase 溢价、借贷利率。

| query_type | 数据源 |
|---|---|
| `rsi` | Coinglass RSI 指标列表 |
| `basis` | Coinglass 期现基差 |
| `ma` | Coinglass 移动平均线 |
| `ema` | Coinglass 指数移动平均 |
| `boll` | Coinglass 布林带 |
| `macd` | Coinglass MACD 历史 |
| `macd_list` | Coinglass 各币种 MACD 信号 |
| `whale_index` | Coinglass 鲸鱼指数 |
| `cgdi` | Coinglass 衍生品贪婪恐惧指数 |
| `cdri` | Coinglass 衍生品风险指数 |
| `atr` | Coinglass ATR |
| `netflow` | Coinglass 现货净资金流 |
| `orderbook_ask_bids` | Coinglass 现货订单簿 |
| `taker_flow` | Coinglass 现货主动买卖 |
| `taker_flow_aggregated` | Coinglass 现货聚合主动买卖 |
| `coinbase_premium` | Coinglass Coinbase 溢价 |
| `bitfinex_margin` | Coinglass Bitfinex 保证金 |
| `borrow_rate` | Coinglass 借贷利率 |

#### ant_spot_market_structure（29）
CoinGecko 全功能查询：价格、市值、分类、全球指标、趋势、交易所汇率、上市公司持仓。

| query_type | 数据源 |
|---|---|
| `simple_price` | CoinGecko 简单价格 |
| `simple_token_price` | CoinGecko 合约地址价格 |
| `supported_vs_currencies` | CoinGecko 支持法币 |
| `coin_detail` | CoinGecko 币详情 |
| `coin_tickers` | CoinGecko 币 Ticker |
| `coin_market_chart` | CoinGecko 市场图表 |
| `coin_market_chart_range` | CoinGecko 指定日期范围图表 |
| `coin_ohlc` | CoinGecko OHLC |
| `coin_history` | CoinGecko 历史快照 |
| `coin_contract` | CoinGecko 合约详情 |
| `coin_contract_market_chart` | CoinGecko 合约图表 |
| `coin_contract_market_chart_range` | CoinGecko 合约指定范围图表 |
| `coins_list` | CoinGecko 全币列表 |
| `coins_markets` | CoinGecko 市值排行 |
| `coins_list_new` | CoinGecko 新上线币 |
| `coins_top_gainers_losers` | CoinGecko 涨跌幅排行 |
| `ping` | CoinGecko API 健康检查 |
| `global_stats` | CoinGecko 全球统计 |
| `global_defi` | CoinGecko DeFi 全球统计 |
| `exchange_rates` | CoinGecko BTC 汇率 |
| `search_trending` | CoinGecko 热搜 |
| `coins_categories` | CoinGecko 币种分类 |
| `coins_categories_list` | CoinGecko 分类列表 |
| `asset_platforms` | CoinGecko 资产平台 |
| `entities_list` | CoinGecko 实体列表 |
| `search` | CoinGecko 搜索 |
| `global_market_cap_chart` | CoinGecko 全球市值图 |
| `companies_public_treasury` | CoinGecko 上市公司持仓 |
| `token_lists` | CoinGecko Token Lists |

#### ant_cex_earn
多交易所统一理财产品查询：活期/定期/DCI 双币投，支持 6 家 CEX。

调用参数：`query_type` + `exchange`（默认 binance）

**交易所 × query_type 支持矩阵：**

| exchange | `flexible_products` | `locked_products` | `dci_products` | 备注 |
|---|---|---|---|---|
| `binance` | ✓ | ✓ | ✓ | 含 `binance_personal_quota` 个人配额查询 |
| `okx` | ✓ | ✓ | ✓ | locked 含赎回期/快速赎回字段 |
| `bybit` | ✓ | ✓ | ✓ | 全部公开端点，无需 API key |
| `bitget` | ✓ | ✓ | ✓⚠ | dci 为 SharkFin 结构化产品替代 |
| `kucoin` | ✓ | ✓ | ✓⚠ | dci 需账号 KYC ≥ 1，否则返回友好错误 |
| `gate` | ✓ | ✓ | — | flexible = Uni-Lending 利率；dci 待配置 |

**全量 query_type 清单：**

| query_type | exchange | 数据源 |
|---|---|---|
| `flexible_products` | binance | Binance Simple Earn Flexible |
| `flexible_products` | okx | OKX Savings lending rate |
| `flexible_products` | bybit | Bybit `/v5/earn/product?category=FlexibleSaving` 公开 |
| `flexible_products` | bitget | Bitget `/api/v2/earn/loan/public/coinInfos` 公开 |
| `flexible_products` | kucoin | KuCoin `/api/v3/project/marketInterestRate` 公开 |
| `flexible_products` | gate | Gate `/api/v4/earn/uni/currencies` 公开 |
| `locked_products` | binance | Binance Simple Earn Locked |
| `locked_products` | okx | OKX Staking-DeFi offers |
| `locked_products` | bybit | Bybit `/v5/earn/product?category=OnChain` 公开 |
| `locked_products` | bitget | Bitget `/api/v2/earn/savings/product` |
| `locked_products` | kucoin | KuCoin `/api/v3/earn/saving/products` |
| `locked_products` | gate | Gate `/api/v4/earn/structured/products` 公开 |
| `dci_products` | binance | Binance Dual Investment |
| `dci_products` | okx | OKX SFP-DCD |
| `dci_products` | bybit | Bybit `/v5/earn/advance/product` + `/product-extra-info` 公开 |
| `dci_products` | bitget | Bitget SharkFin `/api/v2/earn/sharkfin/product`（真实 DCI 被 Cloudflare 阻断）|
| `dci_products` | kucoin | KuCoin `/api/v1/earn/dual-investment-products`（需 KYC ≥ 1）|
| `binance_personal_quota` | binance | Binance `/sapi/v1/simple-earn/*/personalLeftQuota` 按需查询 |

注：
- `binance_personal_quota` 需传 `product_id` 和 `product_type`（flexible/locked）。
- Binance `locked_products` 已归一化（含 `redeem_delay_hours`、`max_amount_per_user`），与其他交易所格式统一。
- Gate `flexible_products` 的 `apy` 字段为 null，利率为小时上限（参见 `raw_fields.max_apy_cap_pct`）。
- HTX：官方无理财 REST API，不支持。

**统一行结构字段说明（所有交易所）：**

| 字段 | 类型 | 含义 |
|---|---|---|
| `redeem_delay_hours` | float\|null | 申请赎回后最短到账等待时间（小时）|
| `redeem_delay_hours_max` | float\|null | 排队/动态情况下最长等待（null=固定值）|
| `fast_redeem_available` | float\|null | OKX 快速赎回当前可用量 |
| `fast_redeem_daily_limit` | float\|null | OKX 快速赎回日限额 |
| `remaining_capacity` | float\|null | 产品剩余可申购额度 |
| `max_amount_per_user` | float\|null | 单用户额度上限 |
| `min_amount` | float\|null | 最低申购金额 |
| `lock_days` | int | 锁仓天数（0=活期）|
| `is_sold_out` | bool | 是否售罄 |
| `can_purchase` | bool | 当前是否可申购 |

#### ant_cex_safety（直接参数）

功能：CEX 安全评估（信任分、评级、牌照、成立年份）。数据源：CoinGecko Pro `/exchanges/{id}`。

---

### 3.3 TradFi 域

#### ant_etf_fund_flow（16）
现货 ETF 基金流：BTC/ETH/SOL/XRP ETF 流量、净值、溢价/折价、Grayscale 持仓。

| query_type | 数据源 |
|---|---|
| `btc_etf_list` | Coinglass BTC ETF 列表 |
| `btc_etf_flow` | Coinglass BTC ETF 日流 |
| `btc_etf_net_assets` | Coinglass BTC ETF 净值 |
| `btc_etf_premium_discount` | Coinglass BTC ETF 溢价 |
| `btc_etf_history` | Coinglass BTC ETF 历史 |
| `btc_etf_price` | Coinglass BTC ETF 价格 |
| `btc_etf_detail` | Coinglass BTC ETF 详情 |
| `btc_etf_aum` | Coinglass BTC ETF AUM |
| `hk_btc_etf_flow` | Coinglass 香港 BTC ETF |
| `eth_etf_list` | Coinglass ETH ETF 列表 |
| `eth_etf_flow` | Coinglass ETH ETF 流量 |
| `eth_etf_net_assets` | Coinglass ETH ETF 净值 |
| `grayscale_holdings` | Coinglass Grayscale 持仓 |
| `grayscale_premium` | Coinglass Grayscale 溢价 |
| `sol_etf_flow` | Coinglass SOL ETF |
| `xrp_etf_flow` | Coinglass XRP ETF |

#### ant_us_stock_tokens / ant_precious_metal_tokens（各 11）
CoinGecko 上的美股 Token（如 PMT）和贵金属 Token（如 PAXG）实时价格与行情数据。

| query_type | 数据源 |
|---|---|
| `simple_price` | CoinGecko 简单价格 |
| `simple_token_price` | CoinGecko 合约价格 |
| `coin_detail` | CoinGecko 币详情 |
| `coin_tickers` | CoinGecko Ticker |
| `coin_market_chart` | CoinGecko 市场图表 |
| `coin_market_chart_range` | CoinGecko 指定范围图表 |
| `coin_ohlc` | CoinGecko OHLC |
| `coin_history` | CoinGecko 历史快照 |
| `coin_contract` | CoinGecko 合约详情 |
| `coin_contract_market_chart` | CoinGecko 合约图表 |
| `coin_contract_market_chart_range` | CoinGecko 合约指定范围图表 |

---

### 3.4 Macro 域

#### ant_macro_economics（9）
美国宏观经济指标：GDP、CPI、通胀预期、联邦基金利率、国债收益率、失业率、非农就业。

| query_type | 数据源 |
|---|---|
| `real_gdp` | AlphaVantage REAL_GDP |
| `real_gdp_per_capita` | AlphaVantage REAL_GDP_PER_CAPITA |
| `cpi` | AlphaVantage CPI |
| `inflation` | AlphaVantage INFLATION |
| `expectation` | AlphaVantage INFLATION_EXPECTATION |
| `federal_funds_rate` | AlphaVantage FEDERAL_FUNDS_RATE |
| `treasury_yield` | AlphaVantage TREASURY_YIELD |
| `unemployment` | AlphaVantage UNEMPLOYMENT |
| `nonfarm` | AlphaVantage NONFARM_PAYROLL |

#### ant_market_sentiment（15）
社交情绪全功能：币种/话题/分类/创作者数据，时序分析、帖子、新闻。

| query_type | 数据源 |
|---|---|
| `coins_list` | LunarCrush 币种列表 |
| `coin_detail` | LunarCrush 币种详情 |
| `coin_time_series` | LunarCrush 币种时序 |
| `coin_meta` | LunarCrush 币种元数据 |
| `topics_list` | LunarCrush 话题列表 |
| `topic_detail` | LunarCrush 话题详情 |
| `topic_time_series` | LunarCrush 话题时序 |
| `topic_posts` | LunarCrush 话题帖子 |
| `topic_news` | LunarCrush 话题新闻 |
| `topic_creators` | LunarCrush 话题创作者 |
| `categories_list` | LunarCrush 分类列表 |
| `category_detail` | LunarCrush 分类详情 |
| `category_topics` | LunarCrush 分类话题 |
| `creators_list` | LunarCrush 创作者列表 |
| `creator_detail` | LunarCrush 创作者详情 |

---

### 3.5 Stock 域

#### ant_stock_data（19）
股票全功能查询：实时报价、OHLCV 时序、基本面（P/E/EPS/财报）、技术指标、搜索、日历、指数。

| query_type | 数据源 |
|---|---|
| `quote` | AlphaVantage GLOBAL_QUOTE |
| `daily` | AlphaVantage TIME_SERIES_DAILY |
| `weekly` | AlphaVantage TIME_SERIES_WEEKLY |
| `monthly` | AlphaVantage TIME_SERIES_MONTHLY |
| `intraday` | AlphaVantage TIME_SERIES_INTRADAY |
| `overview` | AlphaVantage OVERVIEW |
| `earnings` | AlphaVantage EARNINGS |
| `income_statement` | AlphaVantage INCOME_STATEMENT |
| `balance_sheet` | AlphaVantage BALANCE_SHEET |
| `cash_flow` | AlphaVantage CASH_FLOW |
| `rsi` | AlphaVantage RSI |
| `sma` | AlphaVantage SMA |
| `ema` | AlphaVantage EMA |
| `macd` | AlphaVantage MACD |
| `bbands` | AlphaVantage BBANDS |
| `adx` | AlphaVantage ADX |
| `search` | AlphaVantage SYMBOL_SEARCH |
| `earnings_calendar` | AlphaVantage EARNINGS_CALENDAR |
| `index_data` | AlphaVantage INDEX_DATA (Premium) |

#### ant_index_data

专用股票指数工具。支持: SPX, DJI, COMP, NDX, VIX, RUT。数据源: AlphaVantage INDEX_DATA (Premium)。

---

### 3.6 Binance 域

#### ant_binance_spot（2）
Binance 现货行情：24h Ticker 和 K 线数据。

| query_type | 数据源 |
|---|---|
| `ticker_24h` | Binance `/api/v3/ticker/24hr` |
| `klines` | Binance `/api/v3/klines` |

#### ant_binance_futures（7）
Binance 期货行情：Ticker、K 线、OI 历史、资金费率、多空比、合约信息。

| query_type | 数据源 |
|---|---|
| `ticker_24h` | Binance Futures `/fapi/v1/ticker/24hr` |
| `klines` | Binance Futures `/fapi/v1/klines` |
| `oi_history` | Binance Futures OI 历史 |
| `funding_rate` | Binance Futures 当前资金费率 |
| `funding_rate_history` | Binance Futures 费率历史 |
| `long_short_ratio` | Binance Futures 多空比 |
| `exchange_info` | Binance Futures 合约信息 |

---

### 3.7 Prediction 域

#### ant_prediction_event（6）
搜索和浏览 Polymarket 预测市场事件，支持 URL 解析直接提取 event_id/condition_id。

| query_type | 数据源 |
|---|---|
| `search_events` | Polymarket Gamma 事件搜索 |
| `trending_events` | Polymarket Gamma 热门事件 |
| `event_detail` | Polymarket Gamma 事件详情 |
| `market_detail` | Polymarket Gamma 市场详情 |
| `list_tags` | Polymarket Gamma 标签列表 |
| `parse_market_url` | Polymarket Gamma URL 解析（从 polymarket.com 链接提取 event_id/condition_id） |

#### ant_prediction_pricing（3）
预测市场实时定价：中间价/价差/最新成交、订单簿、价格历史走势。

| query_type | 数据源 |
|---|---|
| `market_prices` | Polymarket CLOB 价格快照 |
| `order_book` | Polymarket CLOB 订单簿 |
| `price_history` | Polymarket CLOB 价格历史 |

#### ant_prediction_activity（6）
预测市场交易活跃度：近期交易、OI、大户持仓、排行榜、市场概览、历史漂移回归统计。

| query_type | 数据源 |
|---|---|
| `recent_trades` | Polymarket Data 近期交易 |
| `open_interest` | Polymarket Data 持仓量 |
| `top_holders` | Polymarket Data 前 N 持有者 |
| `leaderboard` | Polymarket Data 排行榜 |
| `market_overview` | Polymarket Data 市场概览 |
| `similar_drift_stats` | 历史漂移回归统计（按 category/sigma/direction 分桶预计算） |

#### ant_prediction_news（2）
预测市场关联新闻：从市场标题自动提取关键词查询主流媒体新闻，支持 impact 分级和时间过滤。

| query_type | 数据源 |
|---|---|
| `by_market` | LunarCrush topic_news（按市场关键词获取关联新闻 + impact 分级） |
| `cache_stats` | 新闻缓存统计 |

---

### 3.8 Options 域

#### ant_deribit_options（5）
加密期权数据：IV 链、ATM 隐含波动率、期限结构、偏斜率、DVOL 指数，覆盖 BTC/ETH/SOL。

| query_type | 数据源 |
|---|---|
| `iv_chain` | Deribit 隐含波动率链（BTC/ETH/SOL） |
| `atm_iv` | Deribit ATM 隐含波动率 |
| `term_structure` | Deribit 期限结构 |
| `skew` | Deribit 偏斜率 |
| `dvol` | Deribit DVOL 指数（仅 BTC/ETH） |
