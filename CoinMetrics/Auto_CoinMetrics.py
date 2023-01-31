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

# CoinMetrics input paramters

#Input desired `data_category` metrics
data_category = input('Enter Data Category: \n********************\n timeseries (Default)\n catalog \n: ')

if data_category == '':
    data_category = 'timeseries'

if data_category == 'timeseries':
    #Input desired `data_category` metrics
    sub_category = input('Enter Subcategory: \n********************\n asset-metrics (Default) \n pair-metrics \n \
market-trades \n market-openinterest \n market-liquidations \n market-funding-rates \n market-orderbooks \n \
market-quotes \n market-candles \n index-levels \n index-constituents \n mining-pool-tips-summary (Pro API Key Required) \n \
mempool-feerates (Pro API Key Required) \n: ')
    if sub_category == '':
        sub_category = 'asset-metrics'

    if sub_category == 'asset-metrics':
        #Base cryptocurrency symbols of interest
        digital_assets = input('Enter digital assets separated by a comma (lower-case): ')

        #Desired asset metrics
        asset_metrics = 'TxCnt,RevHashRateUSD,FeeTotNtv,FeeTotUSD,RevNtv,RevUSD,HashRate,RevHashRateNtv,RevHashRateUSD,FeeMeanNtv,FeeMeanUSD,AdrBalUSD100Cnt,AdrBalUSD100KCnt,AdrBalUSD10Cnt,AdrBalUSD10KCnt,AdrBalUSD10MCnt,AdrBalUSD1Cnt,AdrBalUSD1KCnt,AdrBalUSD1MCnt,SplyAct10yr,SplyAct180d,SplyAct1d,SplyAct1yr,SplyAct2yr,SplyAct30d,SplyAct3yr,SplyAct4yr,SplyAct5yr,SplyAct7d,SplyAct90d,AdrActCnt,SplyActPct1yr,CapMVRVCur,CapMrktCurUSD,CapRealUSD,NVTAdj,PriceUSD'

        #frequency interval unit length  
        frequency_interval = input('Interval (1b, 1s, 1m, 1h, 1d, 1d-ny-close): ')

        ##Desired date range
        #Start (since) date
        since_date = input('Enter `start` date in YYYY-MM-DDT00:00:00Z format: ')

        #End (until) date
        until_date = input('Enter `end` date in YYYY-MM-DDT00:00:00Z format: ')
        
        #Number of itmes per single page of results (10,000 limit)
        page_size = 10000

        #Human-readable formatting of JSON responses
        pretty = input('Pretty JSON (Default: true): ')
        if pretty == '':
            pretty = 'true'
        
        if since_date == '' and until_date:
            param_dict={
            'assets': digital_assets,                   #Comma separated list of assets
            'metrics': asset_metrics,                   #Comma separated metrics
            'frequency': frequency_interval,            #Frequency interval unit length 
            'end_time' : until_date,                    #End, unix timestamp
            'page_size': page_size,                     #Number of itmes per single page of results (10,000 limit)
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }
        elif until_date == '' and since_date:
            param_dict={
            'assets': digital_assets,                   #Comma separated list of assets
            'metrics': asset_metrics,                   #Comma separated metrics
            'frequency': frequency_interval,            #Frequency interval unit length 
            'start_time': since_date,                   #Start, unix timestamp   
            'page_size': page_size,                     #Number of itmes per single page of results (10,000 limit)
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }
        elif since_date == '' and until_date == '':
            param_dict={
            'assets': digital_assets,                   #Comma separated list of assets
            'metrics': asset_metrics,                   #Comma separated metrics
            'frequency': frequency_interval,            #Frequency interval unit length 
            'page_size': page_size,                     #Number of itmes per single page of results (10,000 limit)
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }
        else:
            param_dict={
            'assets': digital_assets,                   #Comma separated list of assets
            'metrics': asset_metrics,                   #Comma separated metrics
            'frequency': frequency_interval,            #Frequency interval unit length 
            'start_time': since_date,                   #Start, unix timestamp   
            'end_time' : until_date,                    #End, unix timestamp
            'page_size': page_size,                     #Number of itmes per single page of results (10,000 limit)
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }            

    elif sub_category == 'pair-metrics':                ##Need Pro tier to access API Key            
        print('***Need Pro tier to access API Key***')
        #Base cryptocurrency symbols of interest
        asset_pairs = input('Enter hyphenated ditital asset pairs separated by a comma (lower-case): ')

        #Desired asset metrics
        asset_metrics = input('Enter desired asset metrics separated by a comma: ')

        #frequency interval unit length  
        frequency_interval = input('Interval (1h, 1d): ')

        ##Desired date range
        #Start (since) date
        since_date = input('Enter `start` date in YYYY-MM-DDT00:00:00Z format: ')

        #End (until) date
        until_date = input('Enter `end` date in YYYY-MM-DDT00:00:00Z format: ')
        
        #Number of itmes per single page of results (10,000 limit)
        page_size = 10000

        #Human-readable formatting of JSON responses
        pretty = input('Pretty JSON (Default: true): ')
        if pretty == '':
            pretty = 'true'
        
        if since_date == '' and until_date:
            param_dict={
            'pairs': asset_pairs,                       #Comma separated list of assets
            'metrics': asset_metrics,                   #Comma separated metrics
            'frequency': frequency_interval,            #Frequency interval unit length 
            'end_time' : until_date,                    #End, unix timestamp
            'page_size': page_size,                     #Number of itmes per single page of results (10,000 limit)
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }
        elif until_date == '' and since_date:
            param_dict={
            'pairs': asset_pairs,                       #Comma separated list of assets
            'metrics': asset_metrics,                   #Comma separated metrics
            'frequency': frequency_interval,            #Frequency interval unit length 
            'start_time': since_date,                   #Start, unix timestamp   
            'page_size': page_size,                     #Number of itmes per single page of results
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }
        elif since_date == '' and until_date == '':
            param_dict={
            'pairs': asset_pairs,                       #Comma separated list of assets
            'metrics': asset_metrics,                   #Comma separated metrics
            'frequency': frequency_interval,            #Frequency interval unit length 
            'page_size': page_size,                     #Number of itmes per single page of results
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }
        else:
            param_dict={
            'pairs': asset_pairs,                       #Comma separated list of assets
            'metrics': asset_metrics,                   #Comma separated metrics
            'frequency': frequency_interval,            #Frequency interval unit length 
            'start_time': since_date,                   #Start, unix timestamp   
            'end_time' : until_date,                    #End, unix timestamp
            'page_size': page_size,                     #Number of itmes per single page of results
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }

    elif sub_category == 'market-trades' or sub_category == 'market-openinterest' or \
        sub_category == 'market-liquidations' or sub_category == 'market-funding-rates' or \
        sub_category == 'market-orderbooks' or sub_category == 'market-quotes' or \
        sub_category == 'market-candles':                 
        #Base cryptocurrency symbols of interest
        markets = input('Enter markets separated by a comma (eg coinbase-btc-usd-spot, bitmex-XBTUSD-future, binance-BTCUSDT-future): ')

        ##Desired date range
        #Start (since) date
        since_date = input('Enter `start` date in YYYY-MM-DDT00:00:00Z format: ')

        #End (until) date
        until_date = input('Enter `end` date in YYYY-MM-DDT00:00:00Z format: ')
        
        #Number of itmes per single page of results (10,000 limit)
        page_size = 10000

        #Human-readable formatting of JSON responses
        pretty = input('Pretty JSON (Default: true): ')
        if pretty == '':
            pretty = 'true'
        
        if since_date == '' and until_date:
            param_dict={
            'markets': markets,                         #Comma separated list of assets
            'end_time' : until_date,                    #End, unix timestamp
            'page_size': page_size,                     #Number of itmes per single page of results (10,000 limit)
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }
        elif until_date == '' and since_date:
            param_dict={
            'markets': markets,                         #Comma separated list of assets
            'start_time': since_date,                   #Start, unix timestamp   
            'page_size': page_size,                     #Number of itmes per single page of results
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }
        elif since_date == '' and until_date == '':
            param_dict={
            'markets': markets,                         #Comma separated list of assets
            'page_size': page_size,                     #Number of itmes per single page of results
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }
        else:
            param_dict={
            'markets': markets,                         #Comma separated list of assets
            'start_time': since_date,                   #Start, unix timestamp   
            'end_time' : until_date,                    #End, unix timestamp
            'page_size': page_size,                     #Number of itmes per single page of results
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }

        if sub_category == 'market-candles':
            #frequency interval unit length  
            frequency_interval = input('Interval (5m, 10m, 15m, 30m, 1h, 4h, 1d [only 1d available for community]): ')

            param_dict['frequency'] = frequency_interval

    elif sub_category == 'index-levels' or sub_category == 'index-constituents':
        #Index symbols of interest
        index_list = input('Enter indexes separated by a comma (eg CMBIBE): ')

        #frequency interval unit length  
        frequency_interval = input('Interval (15s, 1h, 1d, 1d-ny-close, 1d-sg-close): ')

        ##Desired date range
        #Start (since) date
        since_date = input('Enter `start` date in YYYY-MM-DDT00:00:00Z format: ')

        #End (until) date
        until_date = input('Enter `end` date in YYYY-MM-DDT00:00:00Z format: ')
        
        #Number of itmes per single page of results (10,000 limit)
        page_size = 10000

        #Human-readable formatting of JSON responses
        pretty = input('Pretty JSON (Default: true): ')
        if pretty == '':
            pretty = 'true'
        
        if since_date == '' and until_date:
            param_dict={
            'indexes': index_list,                      #Comma separated list of assets
            'frequency': frequency_interval,            #Frequency interval unit length 
            'end_time' : until_date,                    #End, unix timestamp
            'page_size': page_size,                     #Number of itmes per single page of results (10,000 limit)
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }
        elif until_date == '' and since_date:
            param_dict={
            'indexes': index_list,                      #Comma separated list of assets
            'frequency': frequency_interval,            #Frequency interval unit length 
            'start_time': since_date,                   #Start, unix timestamp   
            'page_size': page_size,                     #Number of itmes per single page of results (10,000 limit)
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }
        elif since_date == '' and until_date == '':
            param_dict={
            'indexes': index_list,                      #Comma separated list of assets
            'frequency': frequency_interval,            #Frequency interval unit length 
            'page_size': page_size,                     #Number of itmes per single page of results (10,000 limit)
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }
        else:
            param_dict={
            'indexes': index_list,                      #Comma separated list of assets
            'frequency': frequency_interval,            #Frequency interval unit length 
            'start_time': since_date,                   #Start, unix timestamp   
            'end_time' : until_date,                    #End, unix timestamp
            'page_size': page_size,                     #Number of itmes per single page of results (10,000 limit)
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }

    elif sub_category == 'mining-pool-tips-summary' or sub_category == 'mempool-feerates':      ##Need Pro tier to access API Key
        print('***Need Pro tier to access API Key***')
        #Base cryptocurrency symbols of interest
        digital_assets = input('Enter digital assets separated by a comma (lower-case): ')

        ##Desired date range
        #Start (since) date
        since_date = input('Enter `start` date in YYYY-MM-DDT00:00:00Z format: ')

        #End (until) date
        until_date = input('Enter `end` date in YYYY-MM-DDT00:00:00Z format: ')
        
        #Number of itmes per single page of results (10,000 limit)
        page_size = 10000

        #Human-readable formatting of JSON responses
        pretty = input('Pretty JSON (Default: true): ')
        if pretty == '':
            pretty = 'true'
        
        if since_date == '' and until_date:
            param_dict={
            'assets': digital_assets,                   #Comma separated list of assets
            'end_time' : until_date,                    #End, unix timestamp
            'page_size': page_size,                     #Number of itmes per single page of results (10,000 limit)
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }
        elif until_date == '' and since_date:
            param_dict={
            'assets': digital_assets,                   #Comma separated list of assets
            'start_time': since_date,                   #Start, unix timestamp   
            'page_size': page_size,                     #Number of itmes per single page of results (10,000 limit)
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }
        elif since_date == '' and until_date == '':
            param_dict={
            'assets': digital_assets,                   #Comma separated list of assets
            'page_size': page_size,                     #Number of itmes per single page of results (10,000 limit)
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }
        else:
            param_dict={
            'assets': digital_assets,                   #Comma separated list of assets
            'start_time': since_date,                   #Start, unix timestamp   
            'end_time' : until_date,                    #End, unix timestamp
            'page_size': page_size,                     #Number of itmes per single page of results (10,000 limit)
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }

#Input desired `data_category` metrics
elif data_category == 'catalog':

    #Input desired `data_category` metrics
    sub_category = input('Enter Subcategory: \n********************\n assets \n metrics \n pairs \n institutions \n \
exchanges \n markets \n indexes \n: ')
    if sub_category == 'assets':
        #Base cryptocurrency symbols of interest
        digital_assets = input('Enter digital assets separated by a comma (lower-case): ')

        #Human-readable formatting of JSON responses
        pretty = input('Pretty JSON (Default: true): ')
        if pretty == '':
            pretty = 'true'
        
            param_dict={
            'assets': digital_assets,                   #Comma separated list of assets
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }
    elif sub_category == 'metrics':
        #Desired asset metrics
        asset_metrics = input('Enter desired asset metrics separated by a comma (lower-case): ')

        #Human-readable formatting of JSON responses
        pretty = input('Pretty JSON (Default: true): ')
        if pretty == '':
            pretty = 'true'
        
            param_dict={
            'metrics': asset_metrics,                   #Comma separated metrics
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }
    elif sub_category == 'pairs':                       ##Need Pro tier to access API Key
            print('***Need Pro tier to access API Key***')
            #Comma separated list of assets
            asset_pairs = input('Enter hyphenated ditital asset pairs separated by a comma (lower-case): ')

            #Human-readable formatting of JSON responses
            pretty = input('Pretty JSON (Default: true): ')
            if pretty == '':
                pretty = 'true'
            
                param_dict={
                'pairs': asset_pairs,                   #Comma separated list of assets
                'pretty': pretty                        #Human-readable formatting of JSON responses
                }    
    elif sub_category == 'institutions':                ##Need Pro tier to access API Key                  
            print('***Need Pro tier to access API Key***')
            #Comma separated list of institutions
            institutions = input('Enter institutions separated by a comma (lower-case): ')

            #Human-readable formatting of JSON responses
            pretty = input('Pretty JSON (Default: true): ')
            if pretty == '':
                pretty = 'true'
            
                param_dict={
                'institutions': institutions,           #Comma separated list of institutions
                'pretty': pretty                        #Human-readable formatting of JSON responses
                }    
    elif sub_category == 'exchanges':
        #Comma separated exchanges
        exchanges = input('Enter exchanges separated by a comma (lower-case): ')

        #Human-readable formatting of JSON responses
        pretty = input('Pretty JSON (Default: true): ')
        if pretty == '':
            pretty = 'true'
        
            param_dict={
            'exchanges': exchanges,                     #Comma separated exchanges
            'pretty': pretty                            #Human-readable formatting of JSON responses
            }
    elif sub_category == 'markets':
        #Comma separated markets
        markets = input('Enter markets separated by a comma (lower-case): ')
        exchange = input('Enter unique name of an exchange: ')
        type = input('Enter `spot`, `future`, or `option` type: ')
        base = input('Enter base asset of markets: ')
        quote = input('Enter quote asset of markets: ')
        asset = input('Enter any asset of markets: ')
        symbol = input('Enter symbol of derivatives market, full instrument name: ')

        #Human-readable formatting of JSON responses
        pretty = input('Pretty JSON (Default: true): ')
        if pretty == '':
            pretty = 'true'
        
            param_dict={
            'markets': markets,                         #Comma separated markets
            'pretty': pretty,                           #Human-readable formatting of JSON responses
            }
        if exchange:
            param_dict['exchange'] = exchange           #Unique name of an exchange
        if type:
            param_dict['type'] = type                   #Type of markets eg 'spot', 'future', 'option'
        if base:
            param_dict['base'] = base                   #Base asset of markets
        if quote:
            param_dict['quote'] = quote                 #Quote asset of markets
        if asset:
            param_dict['asset'] = asset                 #Any asset of markets
        if symbol:
            param_dict['symbol'] = symbol               #Symbol of derivatives markets, full instrument name
    elif sub_category == 'indexes':
        #Comma separated indexes.
        indexes = input('Enter indexes separated by a comma (eg CMBIBE): ')
        pretty = input('Pretty JSON (Default: true): ')
        if pretty == '':
            pretty = 'true'

        param_dict={
            'indexes': indexes,                         #Comma separated list of indexes. By default all assets are returned.
            'pretty': pretty                            #Human-readable formatting of JSON responses
        }

exec(open('.../CoinMetrics.py').read())
