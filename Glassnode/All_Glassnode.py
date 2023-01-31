# Copyright (c) 2020 David C. Ronquillo

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import datetime
from datetime import timezone

import time

# Glassnode input paramters

#Base cryptocurrency symbol of interest
digital_asset = input('Digital Asset: ')

##Desired date range
#Start (since) date
since_date = input('Enter `start` date in YYYY-MM-DD format: ')

if since_date:
    since_year, since_month, since_day = map(int, since_date.split('-'))
    since_dt = datetime(since_year, since_month, since_day)
    since_timestamp = int(since_dt.replace(tzinfo=timezone.utc).timestamp())    # Transform dates to unix timestamp
else:
    since_dt = ''
    since_timestamp = ''

#End (until) date
until_date = input('Enter `end` date in YYYY-MM-DD format: ')

if until_date:
    until_year, until_month, until_day = map(int, until_date.split('-'))
    until_dt = datetime(until_year, until_month, until_day)
    until_timestamp = int(until_dt.replace(tzinfo=timezone.utc).timestamp())    # Transform dates to unix timestamp
else:
    until_dt = ''
    until_timestamp = ''

#frequency interval unit length  
frequency_interval = input('Interval (1h, 24h, 10m, 1w, 1month): ')

#Input Optional currency denomination
currency = input('Optional currency denomination (eg USD): ')

if digital_asset == 'BTC':
    glassnode = {'glassnode_1': 'active_count,sending_count,receiving_count,new_non_zero_count,count,block_height,block_count,block_interval_mean,block_interval_median,block_size_sum,block_size_mean,utxo_created_count,utxo_spent_count,utxo_count,utxo_created_value_sum,utxo_created_value_mean,utxo_created_value_median,utxo_spent_value_sum,utxo_spent_value_mean,utxo_spent_value_median,volume_sum,volume_mean,volume_median,difficulty_ribbon,sopr',
                'glassnode_2': 'stock_to_flow_ratio,purpose_etf_holdings_sum,purpose_etf_flows_sum,qbtc_holdings_sum,qbtc_flows_sum,qbtc_aum_sum,qbtc_premium_percent,qbtc_market_price_usd,marketcap_usd,price_drawdown_relative,difficulty_latest,hash_rate_mean,current,active_more_1y_percent,count,rate,size_sum,size_mean,transfers_volume_sum,transfers_volume_mean,transfers_volume_median',
                'glassnode_3': 'non_zero_count,min_point_zero_1_count,min_point_1_count,min_1_count,min_10_count,min_100_count,min_1k_count,min_10k_count,utxo_profit_relative,utxo_profit_count,utxo_loss_count,futures_funding_rate_perpetual,futures_funding_rate_perpetual_all,futures_open_interest_sum,futures_estimated_leverage_ratio',
                'glassnode_4': 'balance_exchanges_relative,exchange_net_position_change,balance_exchanges_all,balance_exchanges,fee_ratio_multiple,cdd,cdd_supply_adjusted,cdd_supply_adjusted_binary,reserve_risk,cvdd,cyd,cyd_supply_adjusted,cdd90_age_adjusted,investor_capitalization,realized_profits_to_value_ratio',
                'glassnode_5': 'balanced_price_usd,puell_multiple,average_dormancy,average_dormancy_supply_adjusted,rhodl_ratio,liveliness,nvt,nvts,velocity,realized_profit,realized_loss,net_realized_profit_loss,realized_profit_loss_ratio,difficulty_ribbon_compression,hash_ribbon,sopr_adjusted,asol,msol,soab,sol_1h,sol_1h_24h,sol_1d_1w,sol_1w_1m,sol_1m_3m,sol_3m_6m,sol_6m_12m,sol_1y_2y,sol_2y_3y,sol_3y_5y,sol_5y_7y,sol_7y_10y,sol_more_10y,ssr,ssr_oscillator,stock_to_flow_deflection,net_unrealized_profit_loss',
                'glassnode_6': 'unrealized_profit,unrealized_loss,mvrv,mvrv_z_score,marketcap_realized_usd,deltacap_usd,price_realized_usd,revenue_sum,revenue_from_fees,volume_mined_sum,thermocap,marketcap_thermocap_ratio,current_adjusted,issued,inflation_rate,hodl_waves,rcap_hodl_waves,active_more_2y_percent,active_more_3y_percent,active_more_5y_percent,active_24h,active_1d_1w,active_1w_1m,active_1m_3m,active_3m_6m,active_6m_12m,active_1y_2y,active_2y_3y,active_3y_5y,active_5y_7y,active_7y_10y,active_more_10y,profit_relative',
                'glassnode_7': 'profit_sum,loss_sum,transfers_volume_to_exchanges_sum,transfers_volume_from_exchanges_sum,transfers_volume_exchanges_net,transfers_to_exchanges_count,transfers_from_exchanges_count,transfers_volume_to_exchanges_mean,transfers_volume_from_exchanges_mean,transfers_volume_adjusted_sum,transfers_volume_adjusted_mean,transfers_volume_adjusted_median'}
elif digital_asset == 'ETH':
    glassnode = {'glassnode_1': 'active_count,sending_count,receiving_count,new_non_zero_count,count,block_height,block_count,block_interval_mean,block_interval_median,block_size_sum,block_size_mean,staking_deposits_count,staking_volume_sum,staking_validators_count,staking_total_deposits_count,staking_total_volume_sum,staking_total_validators_count,staking_phase_0_goal_percent,volume_sum,volume_mean,volume_median,gas_used_sum,gas_used_mean,gas_used_median,gas_price_mean,gas_price_median,gas_limit_tx_mean,gas_limit_tx_median',
                'glassnode_2': 'sopr,marketcap_usd,price_usd_close,price_usd_ohlc,price_drawdown_relative,difficulty_latest,hash_rate_mean,uniswap_transaction_count,uniswap_volume_sum,uniswap_liquidity_latest,current,count,rate,transfers_count,transfers_rate,transfers_volume_sum,transfers_volume_mean,transfers_volume_median,non_zero_count,min_point_zero_1_count,min_point_1_count,min_1_count,min_10_count,min_100_count,min_1k_count',
                'glassnode_3': 'min_10k_count,min_32_count,futures_funding_rate_perpetual,futures_funding_rate_perpetual_all,futures_estimated_leverage_ratio,investor_capitalization',
                'glassnode_4': 'balance_exchanges_relative,exchange_net_position_change,balance_exchanges_all,balance_exchanges,supply_contracts,balance_1pct_holders,gini,herfindahl,fee_ratio_multiple,cdd,average_dormancy,liveliness,nvt,nvts,velocity,asol,msol,net_unrealized_profit_loss,unrealized_profit,unrealized_loss,mvrv,mvrv_z_score,marketcap_realized_usd,price_realized_usd,revenue_sum,revenue_from_fees',
                'glassnode_5': 'thermocap,marketcap_thermocap_ratio,issued,inflation_rate,hodl_waves,active_24h,active_1d_1w,active_1w_1m,active_1m_3m,active_3m_6m,active_6m_12m,active_1y_2y,active_2y_3y,active_3y_5y,active_5y_7y,active_7y_10y,active_more_10y,profit_relative,profit_sum,loss_sum,transfers_volume_to_exchanges_sum,transfers_volume_from_exchanges_sum,transfers_volume_exchanges_net,transfers_to_exchanges_count,transfers_from_exchanges_count,transfers_volume_to_exchanges_mean,transfers_volume_from_exchanges_mean,contract_calls_external_count,contract_calls_internal_count'}
else:
    glassnode = {'glassnode_1': 'active_count,sending_count,receiving_count,new_non_zero_count,count,marketcap_usd,price_usd_close,price_usd_ohlc,price_drawdown_relative,uniswap_transaction_count,uniswap_volume_sum,uniswap_liquidity_latest,current,transfers_count,transfers_rate,transfers_volume_sum,transfers_volume_mean,transfers_volume_median,non_zero_count,balance_exchanges_relative,exchange_net_position_change,balance_exchanges_all,balance_exchanges,supply_contracts,balance_1pct_holders,gini,herfindahl',
                'glassnode_2': 'nvt,nvts,velocity,transfers_volume_to_exchanges_sum,transfers_volume_from_exchanges_sum,transfers_volume_exchanges_net,transfers_to_exchanges_count,transfers_from_exchanges_count,transfers_volume_to_exchanges_mean,transfers_volume_from_exchanges_mean'}

for n in range(len(list(glassnode.keys()))):

    time.sleep(7)

    #Input desired tier 1 `metric_id` metrics
    input_metric_ids = glassnode[list(glassnode.keys())[n]]
    metric_ids = input_metric_ids.split(',')

    key_name = list(glassnode.keys())[n]

    #Obtains 'data_categories' metrics from list of 'metric_id' inputs
    exec(open('.../glassnode_data_cat_from_sub_cat.py').read())

    param_dict={
        'a': digital_asset,                                 #Base cryptocurrency symbol of interest
    }

    if since_timestamp:
        param_dict['s'] = since_timestamp,                               #Since, unix timestamp
    if until_timestamp:
        param_dict['u'] = until_timestamp,                               #Until, unix timestamp
    if frequency_interval:
        param_dict['i'] = frequency_interval,                            #frequency interval unit length  
    if currency:
        param_dict['c'] = currency,

    if frequency_interval == '24h' or frequency_interval == '1h':
        exec(open('.../Glassnode_OHLC.py').read())
    else:
        exec(open('.../Glassnode_Close.py').read())
