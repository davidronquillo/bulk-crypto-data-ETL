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

# Data category
data_category = input('Enter Data Category: \n********************\n Historical Data (v2, symbol, \
exchange/symbol, exchange) \n blockchain \n social/coin \n index \n: ')

# The number of data points to return. If limit * aggregate > 2000 we reduce the limit param on our side. So a limit of 1000 and an aggerate of 4 would only return 2000 (max points) / 4 (aggregation size) = 500 total points + current one so 501.
limit = 2000

# Number of 2000 sets requested
num = int(input('Number of 2000 sets requested: '))


# list of sought after endpoint parameters

## Historical Data
if data_category == 'v2' or \
                data_category == 'symbol' or \
                data_category == 'exchange/symbol':
        sub_category = input('Enter Data Subcategory (histoday, histohour, histominute): ')
        digital_asset = input('Base Digital Asset: ')
        conversion_pair = input('Quote Digital Asset: ')
        exchange = input('exchange (default: CCCAGG): ')
        if exchange == '':
                exchange = 'CCCAGG'                             #CCCAGG = CryptoCompare's real-time aggregate index
        param_dict={
                'fsym': digital_asset,                          #Base cryptocurrency symbol of interest
                'tsym': conversion_pair,                        #Quote cryptocurrency symbol of interest
                'e': exchange,                                  #The exchange to obtain data from
                'limit': limit
        }
        csv_name = '.../Data/' + \
        'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
        digital_asset[-35:].replace('/','_') + '_' + conversion_pair[-35:].replace('/','_') + '.csv'
elif data_category == 'exchange':
        sub_category = input('Enter Data Subcategory (histoday, histohour): ')
        conversion_pair = input('Quote Digital Asset: ')
        exchange = input('exchange (default: CCCAGG): ')
        if exchange == '':
                exchange = 'CCCAGG'                             #CCCAGG = CryptoCompare's real-time aggregate index
        param_dict={
                'tsym': conversion_pair,                        #Comma separated cryptocurrency symbols list to convert into
                'e': exchange,                                  #The exchange to obtain data from
                'limit': limit
        }
        csv_name = '.../Data/' + \
        'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
        conversion_pair[-35:].replace('/','_') + '_' + exchange[-35:].replace('/','_') + '.csv'
        
## Blockchain Data
elif data_category == 'blockchain':
        sub_category = input('Enter Data Subcategory (histo/day, staking/histoday): ')  #********** `staking/histoday`
        digital_asset = input('Base Digital Asset: ')
        exchange = input('exchange (default: CCCAGG): ')
        if exchange == '':
                exchange = 'CCCAGG'                             #CCCAGG = CryptoCompare's real-time aggregate index
        param_dict={
                'fsym': digital_asset,                          #Base cryptocurrency symbol of interest
                'e': exchange,                                  #The exchange to obtain data from
                'limit': limit
        }        
        csv_name = '.../Data/' + \
        'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
        digital_asset[-35:].replace('/','_') + '_' + exchange[-35:].replace('/','_') + '.csv'

## Social Data    
elif data_category == 'social/coin':   
        sub_category = input('Enter Data Subcategory (histo/day, histo/hour): ')
        coin_id = input('Coin ID (default BTC: 1182): ')
        if coin_id == '':
                coin_id = 1182
        else:
                coin_id = int(coin_id)
        param_dict={
                'coinId': coin_id,                               #The id of the coin you want data for
                'limit': limit
        }
        csv_name = '.../Data/' + \
        'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '.csv'

## Index (excluding CCCAGG)
elif data_category == 'index':
        sub_category = input('Enter Data Subcategory (histo/day, histo/hour, histo/minute, \
histo/underlying/day, histo/underlying/hour, histo/underlying/minute): ')      
        if sub_category == 'histo/day' or sub_category == 'histo/hour' or sub_category == 'histo/minute':
                index_name = input('Index Name (default: MVDA): ')
                if index_name == '':
                        index_name = 'MVDA'
                param_dict={
                        'indexName': index_name                         #The index you want to get the latest value for. 
                }
                csv_name = '.../Data/' + \
                'cc_' + data_category[-35:].replace('/','_') + '_' + index_name[-35:].replace('/','_') + '.csv'
        # ***************** Special permissions required for below metrics ****************
        elif sub_category == 'histo/underlying/day' or sub_category == 'histo/underlying/hour' or \
                                sub_category == 'histo/underlying/minute':
                base_asset = input('Base Digital Asset: ')
                quote_asset = input('Quote Digital Asset: ')
                index_market = input('Market (default: CCMVDA): ')
                if index_market == '':
                        index_market = 'CCMVDA'
                param_dict={
                        'base': base_asset,                             #Base cryptocurrency symbol of interest
                        'quote': quote_asset,                           #Quote cryptocurrency symbol of interest
                        'market': index_market,                         #The index market
                        'limit': limit
                }
                csv_name = '.../Data/' + \
                'cc_' + data_category[-35:].replace('/','_') + '_' + base_asset[-35:].replace('/','_') + '_' + \
                quote_asset[-35:].replace('/','_') + '_' + index_market[-35:].replace('/','_') + '.csv'

exec(open('.../CryptoCompare/CryptoCompare_Time_Series.py').read())
