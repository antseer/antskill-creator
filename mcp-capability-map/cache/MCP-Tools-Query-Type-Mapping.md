# MCP Tools × Query Type × API 映射表

> 19 工具 | 234 query_types | 8 数据平台 | 统计时间：2026-03-16

---

## 总览

| 领域 | 工具数 | query_types | 已实现 | TODO | 数据平台 |
|------|--------|-------------|--------|------|----------|
| On-Chain | 10 | 114 | 108 | 6 | DeFiLlama, Nansen, CryptoQuant, Coinglass, DexScreener |
| CeFi | 4 | 83 | 83 | 0 | Coinglass, CoinGecko |
| TradFi | 3 | 38 | 38 | 0 | Coinglass, CoinGecko |
| Macro & Sentiment | 2 | 24 | 24 | 0 | AlphaVantage, LunarCrush |
| **合计** | **19** | **234** (含 24 未注册) | **228** | **6 TODO** | **8** |

### 数据平台分布

| 平台 | query_types 数 | 覆盖工具 |
|------|---------------|---------|
| Coinglass | ~80 | ant_futures_market_structure, ant_futures_liquidation, ant_market_indicators, ant_fund_flow, ant_perp_dex, ant_etf_fund_flow |
| CoinGecko | ~46 | ant_spot_market_structure, ant_us_stock_tokens, ant_precious_metal_tokens |
| DeFiLlama | ~35 | ant_protocol_tvl_yields_revenue, ant_protocol_ecosystem, ant_bridge_fund_flow, ant_stablecoin |
| Nansen | ~28 | ant_smart_money, ant_token_analytics(TGM), ant_address_profile |
| CryptoQuant | ~26 | ant_fund_flow, ant_token_analytics, ant_stablecoin |
| LunarCrush | 15 | ant_market_sentiment |
| AlphaVantage | 9 | ant_macro_economics |
| DexScreener | 9 | ant_meme |

---

## 1. On-Chain 链上数据

### 1.1 ant_protocol_tvl_yields_revenue（19 types）

| query_type | 平台 | API 端点/模块 | 状态 |
|-----------|------|-------------|------|
| protocol_tvl | DeFiLlama | defillama_protocol_query | ✅ |
| protocol_volume | DeFiLlama | defillama_protocol_query | ✅ |
| protocol_fees | DeFiLlama | defillama_protocol_query | ✅ |
| protocol_revenue | DeFiLlama | defillama_protocol_query | ✅ |
| protocol_overview | DeFiLlama | defillama_protocol_query | ✅ |
| protocol_inflows | DeFiLlama | defillama_protocol_inflows | ✅ |
| token_protocols | DeFiLlama | defillama_token_protocols | ✅ |
| chain_tvl_history | DeFiLlama | defillama_historical_chain_tvl | ✅ |
| chain_assets | DeFiLlama | defillama_chain_assets | ✅ |
| dex_overview | DeFiLlama | defillama_dex_overview | ✅ |
| fees_overview | DeFiLlama | defillama_fees_overview | ✅ |
| yield_pools | DeFiLlama | defillama_yield_query | ✅ |
| yield_borrow | DeFiLlama | defillama_yield_query | ✅ |
| yield_lsd | DeFiLlama | defillama_yield_query | ✅ |
| yield_pool_history | DeFiLlama | defillama_yield_pool_history | ✅ |
| yield_lend_borrow_history | DeFiLlama | defillama_yield_lend_borrow_history | ✅ |
| yield_pools_with_address | DeFiLlama | defillama_yield_pools_old | ✅ |
| yield_perps | DeFiLlama | defillama_yield_perps | ✅ |
| chains | DeFiLlama | defillama_meta_get_info | ✅ |

### 1.2 ant_protocol_ecosystem（6 types）

| query_type | 平台 | API 端点/模块 | 状态 |
|-----------|------|-------------|------|
| ecosystem_hacks | DeFiLlama | defillama_meta_get_info | ✅ |
| ecosystem_categories | DeFiLlama | defillama_meta_get_info | ✅ |
| ecosystem_oracles | DeFiLlama | defillama_meta_get_info | ✅ |
| ecosystem_raises | DeFiLlama | defillama_meta_get_info | ✅ |
| ecosystem_entities | DeFiLlama | defillama_meta_get_info | ✅ |
| ecosystem_treasuries | DeFiLlama | defillama_meta_get_info | ✅ |

### 1.3 ant_bridge_fund_flow（5 types）

| query_type | 平台 | API 端点/模块 | 状态 |
|-----------|------|-------------|------|
| bridges_list | DeFiLlama | defillama_bridges_query | ✅ |
| bridges_volume | DeFiLlama | defillama_bridges_query | ✅ |
| bridges_daily_stats | DeFiLlama | defillama_bridges_query | ✅ |
| bridges_chain_history | DeFiLlama | defillama_bridges_chain_history | ✅ |
| bridges_transactions | DeFiLlama | defillama_bridges_transactions | ✅ |

### 1.4 ant_smart_money（6 types）

| query_type | 平台 | API 端点/模块 | 状态 |
|-----------|------|-------------|------|
| netflows | Nansen | POST smart-money/netflows | ✅ |
| holdings | Nansen | POST smart-money/holdings | ✅ |
| historical_holdings | Nansen | POST smart-money/historical-holdings | ✅ |
| dex_trades | Nansen | POST smart-money/dex-trades | ✅ |
| dcas | Nansen | POST smart-money/dcas | ✅ |
| perp_trades | Nansen | POST smart-money/perp-trades | ✅ |

### 1.5 ant_fund_flow（17 types）

| query_type | 平台 | API 端点/模块 | 状态 |
|-----------|------|-------------|------|
| exchange_reserve | CryptoQuant | /v1/{asset}/exchange-flows/reserve | ✅ |
| exchange_netflow | CryptoQuant | /v1/{asset}/exchange-flows/netflow | ✅ |
| exchange_inflow | CryptoQuant | /v1/{asset}/exchange-flows/inflow | ✅ |
| exchange_outflow | CryptoQuant | /v1/{asset}/exchange-flows/outflow | ✅ |
| exchange_transactions_count | CryptoQuant | /v1/{asset}/exchange-flows/transactions-count | ✅ |
| miner_reserve | CryptoQuant | /v1/btc/miner-flows/reserve | ✅ |
| miner_netflow | CryptoQuant | /v1/btc/miner-flows/netflow | ✅ |
| miner_inflow | CryptoQuant | /v1/btc/miner-flows/inflow | ✅ |
| miner_outflow | CryptoQuant | /v1/btc/miner-flows/outflow | ✅ |
| exchange_whale_ratio | CryptoQuant | /v1/{asset}/flow-indicator/exchange-whale-ratio | ✅ |
| mpi | CryptoQuant | /v1/btc/flow-indicator/mpi | ✅ |
| fund_flow_ratio | CryptoQuant | /v1/{asset}/flow-indicator/fund-flow-ratio | ✅ |
| centralized_exchange_assets | Coinglass | onchain.handle → exchange_assets | ✅ |
| centralized_exchange_balance_list | Coinglass | onchain.handle → balance_list | ✅ |
| centralized_exchange_balance_chart | Coinglass | onchain.handle → balance_chart | ✅ |
| centralized_exchange_transfers | Coinglass | onchain.handle → transfers | ✅ |
| centralized_exchange_whale_transfer | Coinglass | onchain.handle → whale_transfer | ✅ |

### 1.6 ant_token_analytics（26 types）

| query_type | 平台 | API 端点/模块 | 状态 |
|-----------|------|-------------|------|
| supply | CryptoQuant | /v1/{asset}/network-data/supply | ✅ |
| transactions_count | CryptoQuant | /v1/{asset}/network-data/transactions-count | ✅ |
| addresses_count | CryptoQuant | /v1/{asset}/network-data/addresses-count | ✅ |
| tokens_transferred | CryptoQuant | /v1/btc/network-data/tokens-transferred | ✅ |
| blockreward | CryptoQuant | /v1/btc/network-data/blockreward | ✅ |
| difficulty | CryptoQuant | /v1/btc/network-data/difficulty | ✅ |
| hashrate | CryptoQuant | /v1/{asset}/network-data/hashrate | ✅ |
| fees | CryptoQuant | /v1/{asset}/network-data/fees | ✅ |
| price_ohlcv | CryptoQuant | /v1/{asset}/market-data/price-ohlcv | ✅ |
| nvt | CryptoQuant | /v1/btc/network-indicator/nvt | ✅ |
| nvt_golden_cross | CryptoQuant | /v1/btc/network-indicator/nvt-golden-cross | ✅ |
| stock_to_flow | CryptoQuant | /v1/btc/network-indicator/stock-to-flow | ✅ |
| mvrv | CryptoQuant | /v1/btc/market-indicator/mvrv | ✅ |
| token_screener | Nansen | POST token-screener | ✅ |
| perp_screener | Nansen | POST perp-screener | ✅ |
| flow_intelligence | Nansen | POST tgm/flow-intelligence | ✅ |
| flows | Nansen | POST tgm/flows | ✅ |
| who_bought_sold | Nansen | POST tgm/who-bought-sold | ✅ |
| dex_trades | Nansen | POST tgm/dex-trades | ✅ |
| perp_trades | Nansen | POST tgm/perp-trades | ✅ |
| transfers | Nansen | POST tgm/transfers | ✅ |
| jup_dca | Nansen | POST tgm/jup-dca | ✅ |
| holders | Nansen | POST tgm/holders | ✅ |
| perp_positions | Nansen | POST tgm/perp-positions | ✅ |
| pnl_leaderboard | Nansen | POST tgm/pnl-leaderboard | ✅ |
| perp_pnl_leaderboard | Nansen | POST tgm/perp-pnl-leaderboard | ✅ |

> **未注册 TGM 端点（3）：** token_information, token_ohlcv, indicators — 已在 QUERY_TYPE_MAPPING 中定义但未纳入 router
>
> **TODO DeFiLlama emissions（2）：** emissions_unlocks, emissions_schedule — 代码注释中标记待实现

### 1.7 ant_stablecoin（11 types）

| query_type | 平台 | API 端点/模块 | 状态 |
|-----------|------|-------------|------|
| mcap | DeFiLlama | defillama_stablecoin_query | ✅ |
| price | DeFiLlama | defillama_stablecoin_query | ✅ |
| chain_distribution | DeFiLlama | defillama_stablecoin_query | ✅ |
| dominance | DeFiLlama | defillama_stablecoin_query | ✅ |
| overview | DeFiLlama | defillama_stablecoin_query | ✅ |
| detail | DeFiLlama | defillama_stablecoin_detail | ✅ |
| history_all | DeFiLlama | defillama_stablecoin_charts_all | ✅ |
| history_chain | DeFiLlama | defillama_stablecoin_charts_chain | ✅ |
| chains | DeFiLlama | defillama_stablecoin_chains | ✅ |
| prices_history | DeFiLlama | defillama_stablecoin_prices | ✅ |
| supply_network | CryptoQuant | stablecoin_data.handle | ✅ |

### 1.8 ant_meme（9 types）

| query_type | 平台 | API 端点/模块 | 状态 |
|-----------|------|-------------|------|
| trending_tokens | DexScreener | GET /token-profiles/latest/v1 | ✅ |
| boost_latest | DexScreener | GET /token-boosts/latest/v1 | ✅ |
| boost_top | DexScreener | GET /token-boosts/top/v1 | ✅ |
| community_takeover | DexScreener | GET /token-profiles/latest/community-takeover/v1 | ✅ |
| token_info | DexScreener | GET /tokens/v1/{chainId}/{addr} | ✅ |
| token_pairs | DexScreener | GET /token-pairs/v1/{chainId}/{addr} | ✅ |
| pair_info | DexScreener | GET /pairs/v1/{chainId}/{pairId} | ✅ |
| search_pairs | DexScreener | GET /search/v1?q={query} | ✅ |
| paid_orders | DexScreener | GET /orders/v1/{chainId}/{addr} | ✅ |

### 1.9 ant_address_profile（9 types）

| query_type | 平台 | API 端点/模块 | 状态 |
|-----------|------|-------------|------|
| current_balance | Nansen | POST address/current-balance | ✅ |
| historical_balances | Nansen | POST address/historical-balances | ✅ |
| transactions | Nansen | POST address/transactions | ✅ |
| counterparties | Nansen | POST address/counterparties | ✅ |
| pnl_summary | Nansen | POST address/pnl-summary | ✅ |
| pnl | Nansen | POST address/pnl | ✅ |
| related_wallets | Nansen | POST address/related-wallets | ✅ |
| labels | Nansen | POST address/labels | ✅ |
| transaction_lookup | Nansen | POST transaction/lookup | ✅ |

### 1.10 ant_perp_dex（6 types + 3 TODO）

| query_type | 平台 | API 端点/模块 | 状态 |
|-----------|------|-------------|------|
| perp_dex_whale_alert | Coinglass | hyperliquid.handle → whale_alert | ✅ |
| perp_dex_whale_position | Coinglass | hyperliquid.handle → whale_position | ✅ |
| perp_dex_position_by_coin | Coinglass | hyperliquid.handle → position_by_coin | ✅ |
| perp_dex_position_by_address | Coinglass | hyperliquid.handle → position_by_address | ✅ |
| perp_dex_wallet_position_distribution | Coinglass | hyperliquid.handle → wallet_position_dist | ✅ |
| perp_dex_wallet_pnl_distribution | Coinglass | hyperliquid.handle → wallet_pnl_dist | ✅ |
| perp_dex_overview | DeFiLlama | — | ❌ TODO |
| perp_dex_volume_history | DeFiLlama | — | ❌ TODO |
| perp_dex_protocol_detail | DeFiLlama | — | ❌ TODO |

---

## 2. CeFi 中心化金融

### 2.1 ant_futures_market_structure（32 types）

| 子分类 | query_type | 平台 | API 端点 | 状态 |
|--------|-----------|------|---------|------|
| 交易市场 | futures_market_snapshot | Coinglass | futures → market_snapshot | ✅ |
| | futures_pairs_market | Coinglass | futures → pairs_market | ✅ |
| | futures_price_change | Coinglass | futures → price_change | ✅ |
| | futures_price_history | Coinglass | futures → price_history | ✅ |
| OI | futures_oi_history | Coinglass | futures → open_interest | ✅ |
| | futures_oi_aggregated | Coinglass | futures → open_interest (agg) | ✅ |
| | futures_oi_stablecoin | Coinglass | futures → oi_stablecoin | ✅ |
| | futures_oi_coin_margin | Coinglass | futures → oi_coin_margin | ✅ |
| | futures_oi_exchange_list | Coinglass | futures → oi_exchange_list | ✅ |
| | futures_oi_exchange_history | Coinglass | futures → oi_exchange_history | ✅ |
| 资金费率 | futures_funding_rate_history | Coinglass | futures → funding_rate | ✅ |
| | futures_funding_rate_exchange_list | Coinglass | futures → funding_rate (list) | ✅ |
| | futures_funding_rate_oi_weight | Coinglass | futures → funding_rate_oi_weight | ✅ |
| | futures_funding_rate_vol_weight | Coinglass | futures → funding_rate_vol_weight | ✅ |
| | futures_funding_rate_accumulated | Coinglass | futures → funding_rate_accumulated | ✅ |
| | futures_funding_rate_arbitrage | Coinglass | futures → funding_rate_arbitrage | ✅ |
| 多空比 | futures_long_short_global | Coinglass | futures → long_short_ratio | ✅ |
| | futures_long_short_top_account | Coinglass | futures → long_short_top_account | ✅ |
| | futures_long_short_top_position | Coinglass | futures → long_short_top_position | ✅ |
| | futures_taker_ratio_exchange | Coinglass | futures → taker_ratio_exchange | ✅ |
| | futures_net_position | Coinglass | futures → net_position | ✅ |
| 订单簿 | futures_orderbook_ask_bids | Coinglass | futures → order_book_depth | ✅ |
| | futures_orderbook_aggregated | Coinglass | futures → orderbook_aggregated | ✅ |
| | futures_orderbook_history | Coinglass | futures → orderbook_history | ✅ |
| | futures_orderbook_large_orders | Coinglass | futures → orderbook_large_orders | ✅ |
| | futures_orderbook_large_orders_history | Coinglass | futures → orderbook_large_orders_history | ✅ |
| 买卖/CVD | futures_taker_flow | Coinglass | futures → taker_flow | ✅ |
| | futures_taker_flow_aggregated | Coinglass | futures → taker_flow (agg) | ✅ |
| | futures_footprint | Coinglass | futures → footprint | ✅ |
| | futures_cvd | Coinglass | futures → cvd | ✅ |
| | futures_cvd_aggregated | Coinglass | futures → cvd_aggregated | ✅ |
| | futures_netflow | Coinglass | futures → netflow | ✅ |

### 2.2 ant_futures_liquidation（9 types）

| 子分类 | query_type | 平台 | API 端点 | 状态 |
|--------|-----------|------|---------|------|
| 爆仓历史 | futures_liquidation_history | Coinglass | futures → liquidation_history | ✅ |
| | futures_liquidation_aggregated | Coinglass | futures → liquidation_history (agg) | ✅ |
| | futures_liquidation_coin_list | Coinglass | futures → liquidation_coin_list | ✅ |
| | futures_liquidation_exchange_list | Coinglass | futures → liquidation_exchange_list | ✅ |
| 爆仓订单 | futures_liquidation_order | Coinglass | futures → liquidation_order | ✅ |
| 爆仓地图 | futures_liquidation_map | Coinglass | futures → liquidation_map | ✅ |
| | futures_liquidation_aggregated_map | Coinglass | futures → liquidation_map (agg) | ✅ |
| 热力图 | futures_liquidation_heatmap | Coinglass | futures → liquidation_heatmap | ✅ |
| | futures_liquidation_agg_heatmap | Coinglass | futures → liquidation_agg_heatmap | ✅ |

### 2.3 ant_market_indicators（18 types）

| 子分类 | query_type | 平台 | API 端点 | 状态 |
|--------|-----------|------|---------|------|
| 合约技术 | rsi | Coinglass | indic → rsi | ✅ |
| | basis | Coinglass | indic → basis | ✅ |
| | ma | Coinglass | indic → ma | ✅ |
| | ema | Coinglass | indic → ema | ✅ |
| | boll | Coinglass | indic → boll | ✅ |
| | macd | Coinglass | indic → macd_history | ✅ |
| | macd_list | Coinglass | indic → macd_list | ✅ |
| | whale_index | Coinglass | indic → whale_index | ✅ |
| | cgdi | Coinglass | indic → cgdi | ✅ |
| | cdri | Coinglass | indic → cdri | ✅ |
| | atr | Coinglass | indic → atr | ✅ |
| 现货行情 | netflow | Coinglass | spots → netflow | ✅ |
| | orderbook_ask_bids | Coinglass | spots → order_book_depth | ✅ |
| | taker_flow | Coinglass | spots → taker_flow | ✅ |
| | taker_flow_aggregated | Coinglass | spots → taker_flow (agg) | ✅ |
| 现货技术 | coinbase_premium | Coinglass | indic → coinbase_premium | ✅ |
| | bitfinex_margin | Coinglass | indic → bitfinex_margin | ✅ |
| 借贷 | borrow_rate | Coinglass | indic → borrow_interest_rate | ✅ |

### 2.4 ant_spot_market_structure（25 types）

| 子分类 | query_type | 平台 | API 端点 | 状态 |
|--------|-----------|------|---------|------|
| 价格 | simple_price | CoinGecko | GET /simple/price | ✅ |
| | simple_token_price | CoinGecko | GET /simple/token_price/{platform} | ✅ |
| | supported_vs_currencies | CoinGecko | GET /simple/supported_vs_currencies | ✅ |
| 详情 | coin_detail | CoinGecko | GET /coins/{id} | ✅ |
| | coin_tickers | CoinGecko | GET /coins/{id}/tickers | ✅ |
| 历史 | coin_market_chart | CoinGecko | GET /coins/{id}/market_chart | ✅ |
| | coin_market_chart_range | CoinGecko | GET /coins/{id}/market_chart/range | ✅ |
| | coin_ohlc | CoinGecko | GET /coins/{id}/ohlc | ✅ |
| | coin_history | CoinGecko | GET /coins/{id}/history | ✅ |
| 合约 | coin_contract | CoinGecko | GET /coins/{platform}/contract/{addr} | ✅ |
| | coin_contract_market_chart | CoinGecko | GET /coins/{platform}/contract/{addr}/market_chart | ✅ |
| | coin_contract_market_chart_range | CoinGecko | GET /coins/{platform}/contract/{addr}/market_chart/range | ✅ |
| 列表 | coins_list | CoinGecko | GET /coins/list | ✅ |
| | coins_markets | CoinGecko | GET /coins/markets | ✅ |
| | coins_list_new | CoinGecko | GET /coins/list/new (Pro) | ✅ |
| | coins_top_gainers_losers | CoinGecko | GET /coins/top_gainers_losers (Pro) | ✅ |
| 全局 | ping | CoinGecko | GET /ping | ✅ |
| | global_stats | CoinGecko | GET /global | ✅ |
| | global_defi | CoinGecko | GET /global/decentralized_finance_defi | ✅ |
| | exchange_rates | CoinGecko | GET /exchange_rates | ✅ |
| | search_trending | CoinGecko | GET /search/trending | ✅ |
| | coins_categories | CoinGecko | GET /coins/categories | ✅ |
| | coins_categories_list | CoinGecko | GET /coins/categories/list | ✅ |
| | asset_platforms | CoinGecko | GET /asset_platforms | ✅ |
| | search | CoinGecko | GET /search | ✅ |
| | global_market_cap_chart | CoinGecko | GET /global/market_cap_chart (Pro) | ✅ |
| | companies_public_treasury | CoinGecko | GET /companies/public_treasury/{coin_id} | ✅ |
| | token_lists | CoinGecko | GET /asset_platforms/{id}/token_lists | ✅ |
| | entities_list | CoinGecko | GET /companies/public_treasury | ✅ |

---

## 3. TradFi 传统金融

### 3.1 ant_etf_fund_flow（16 types）

| 子分类 | query_type | 平台 | API 端点 | 状态 |
|--------|-----------|------|---------|------|
| BTC ETF (US) | btc_etf_list | Coinglass | etf → btc_list | ✅ |
| | btc_etf_flow | Coinglass | etf → daily_flow (BTC) | ✅ |
| | btc_etf_net_assets | Coinglass | etf → net_assets (BTC) | ✅ |
| | btc_etf_premium_discount | Coinglass | etf → btc_premium_discount | ✅ |
| | btc_etf_history | Coinglass | etf → btc_history | ✅ |
| | btc_etf_price | Coinglass | etf → btc_price | ✅ |
| | btc_etf_detail | Coinglass | etf → btc_detail | ✅ |
| | btc_etf_aum | Coinglass | etf → btc_aum | ✅ |
| BTC ETF (HK) | hk_btc_etf_flow | Coinglass | etf → hk_btc_flow | ✅ |
| ETH ETF | eth_etf_list | Coinglass | etf → eth_list | ✅ |
| | eth_etf_flow | Coinglass | etf → daily_flow (ETH) | ✅ |
| | eth_etf_net_assets | Coinglass | etf → net_assets (ETH) | ✅ |
| 信托基金 | grayscale_holdings | Coinglass | etf → grayscale_holdings | ✅ |
| | grayscale_premium | Coinglass | etf → grayscale_premium | ✅ |
| SOL/XRP ETF | sol_etf_flow | Coinglass | etf → sol_flow | ✅ |
| | xrp_etf_flow | Coinglass | etf → xrp_flow | ✅ |

### 3.2 ant_us_stock_tokens（11 types）

适用范围：美股代币化资产（RWA Tokenized Stocks）

| query_type | 平台 | API 端点 | 状态 |
|-----------|------|---------|------|
| simple_price | CoinGecko | GET /simple/price | ✅ |
| simple_token_price | CoinGecko | GET /simple/token_price/{platform} | ✅ |
| coin_detail | CoinGecko | GET /coins/{id} | ✅ |
| coin_tickers | CoinGecko | GET /coins/{id}/tickers | ✅ |
| coin_market_chart | CoinGecko | GET /coins/{id}/market_chart | ✅ |
| coin_market_chart_range | CoinGecko | GET /coins/{id}/market_chart/range | ✅ |
| coin_ohlc | CoinGecko | GET /coins/{id}/ohlc | ✅ |
| coin_history | CoinGecko | GET /coins/{id}/history | ✅ |
| coin_contract | CoinGecko | GET /coins/{platform}/contract/{addr} | ✅ |
| coin_contract_market_chart | CoinGecko | GET /coins/{platform}/contract/{addr}/market_chart | ✅ |
| coin_contract_market_chart_range | CoinGecko | GET /coins/{platform}/contract/{addr}/market_chart/range | ✅ |

> 主要 coin_id：tesla-xstock, nvidia-xstock, alphabet-xstock, nvidia-ondo-tokenized-stock, tesla-ondo-tokenized-stock, microsoft-ondo-tokenized-stock

### 3.3 ant_precious_metal_tokens（11 types）

适用范围：贵金属及大宗商品代币化资产（RWA Tokenized Commodities）

| query_type | 平台 | API 端点 | 状态 |
|-----------|------|---------|------|
| simple_price | CoinGecko | GET /simple/price | ✅ |
| simple_token_price | CoinGecko | GET /simple/token_price/{platform} | ✅ |
| coin_detail | CoinGecko | GET /coins/{id} | ✅ |
| coin_tickers | CoinGecko | GET /coins/{id}/tickers | ✅ |
| coin_market_chart | CoinGecko | GET /coins/{id}/market_chart | ✅ |
| coin_market_chart_range | CoinGecko | GET /coins/{id}/market_chart/range | ✅ |
| coin_ohlc | CoinGecko | GET /coins/{id}/ohlc | ✅ |
| coin_history | CoinGecko | GET /coins/{id}/history | ✅ |
| coin_contract | CoinGecko | GET /coins/{platform}/contract/{addr} | ✅ |
| coin_contract_market_chart | CoinGecko | GET /coins/{platform}/contract/{addr}/market_chart | ✅ |
| coin_contract_market_chart_range | CoinGecko | GET /coins/{platform}/contract/{addr}/market_chart/range | ✅ |

> 主要 coin_id：tether-gold (XAUT), pax-gold (PAXG), kinesis-gold (KAU), kinesis-silver (KAG), matrixdock-gold (XAUM)

---

## 4. Macro & Sentiment 宏观与舆情

### 4.1 ant_macro_economics（9 types）

| 子分类 | query_type | 平台 | API 端点 | 状态 |
|--------|-----------|------|---------|------|
| 经济增长 | real_gdp | AlphaVantage | REAL_GDP | ✅ |
| | real_gdp_per_capita | AlphaVantage | REAL_GDP_PER_CAPITA | ✅ |
| 通胀 | cpi | AlphaVantage | CPI | ✅ |
| | inflation | AlphaVantage | INFLATION | ✅ |
| | expectation | AlphaVantage | INFLATION_EXPECTATION | ✅ |
| 利率 | federal_funds_rate | AlphaVantage | FEDERAL_FUNDS_RATE | ✅ |
| | treasury_yield | AlphaVantage | TREASURY_YIELD | ✅ |
| 劳动力 | unemployment | AlphaVantage | UNEMPLOYMENT | ✅ |
| | nonfarm | AlphaVantage | NONFARM_PAYROLL | ✅ |

### 4.2 ant_market_sentiment（15 types）

| 子分类 | query_type | 平台 | API 端点 | 状态 |
|--------|-----------|------|---------|------|
| 代币情绪 | coins_list | LunarCrush | GET /public/coins/list/v2 | ✅ |
| | coin_detail | LunarCrush | GET /public/coins/{coin}/v1 | ✅ |
| | coin_time_series | LunarCrush | GET /public/coins/{coin}/time-series/v2 | ✅ |
| | coin_meta | LunarCrush | GET /public/coins/{coin}/meta/v1 | ✅ |
| 话题 | topics_list | LunarCrush | GET /public/topics/list/v1 | ✅ |
| | topic_detail | LunarCrush | GET /public/topic/{topic}/v1 | ✅ |
| | topic_time_series | LunarCrush | GET /public/topic/{topic}/time-series/v1 | ✅ |
| | topic_posts | LunarCrush | GET /public/topic/{topic}/posts/v1 | ✅ |
| | topic_news | LunarCrush | GET /public/topic/{topic}/news/v1 | ✅ |
| | topic_creators | LunarCrush | GET /public/topic/{topic}/creators/v1 | ✅ |
| 分类 | categories_list | LunarCrush | GET /public/categories/list/v1 | ✅ |
| | category_detail | LunarCrush | GET /public/category/{cat}/v1 | ✅ |
| | category_topics | LunarCrush | GET /public/category/{cat}/topics/v1 | ✅ |
| 创作者 | creators_list | LunarCrush | GET /public/creators/list/v1 | ✅ |
| | creator_detail | LunarCrush | GET /public/creator/{net}/{id}/v1 | ✅ |

---

## 未实现 / TODO 汇总

| 工具 | query_type | 计划平台 | 备注 |
|------|-----------|---------|------|
| ant_perp_dex | perp_dex_overview | DeFiLlama | 衍生品 DEX 概览 |
| ant_perp_dex | perp_dex_volume_history | DeFiLlama | 衍生品交易量历史 |
| ant_perp_dex | perp_dex_protocol_detail | DeFiLlama | 单协议衍生品详情 |
| ant_token_analytics | token_information | Nansen | TGM 端点已定义未注册 |
| ant_token_analytics | token_ohlcv | Nansen | TGM 端点已定义未注册 |
| ant_token_analytics | indicators | Nansen | TGM 端点已定义未注册 |
| ant_token_analytics | emissions_unlocks | DeFiLlama | 代码注释标记 TODO |
| ant_token_analytics | emissions_schedule | DeFiLlama | 代码注释标记 TODO |
