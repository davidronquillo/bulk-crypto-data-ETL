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
data_category = input('Enter Data Category:\n********************\n blockchain \n Trading Signals \
(tradingsignals/intotheblock) \n Social Data (social/coin) \n News (v2) \n Order Book \
(ob/l1, v2/ob/l2) \n index \n: ')

# list of sought after endpoint parameters

## Blockchain Data
if data_category == 'blockchain':
        sub_category = input('Enter Data Subcategory (latest, staking/latest): ') 
        if sub_category == 'latest':    
                digital_asset = input('Base Digital Asset: ')
                param_dict={
                        'fsym': digital_asset,                          #Base cryptocurrency symbol of interest
                }
                csv_name = '.../Data/' + \
                'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
                digital_asset[-35:].replace('/','_') + '.csv'

        elif sub_category == 'staking/latest':      
                digital_asset = input('Base Digital Asset: ')
                if digital_asset == '':
                        digital_asset = 'ETH'
                provider = input('Data provider for staking rate: ')
                if provider == '':
                        provider = 'attestant'                          #The data provider for the staking rate.
                param_dict={
                        'fsym': digital_asset,                          #Base cryptocurrency symbol of interest
                }
                csv_name = '.../Data/' + \
                'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
                digital_asset[-35:].replace('/','_') + '.csv'

## Trading Signals
elif data_category == 'tradingsignals/intotheblock': 
        sub_category = input('Enter Data Subcategory (latest): ') 
        digital_asset = input('Base Digital Asset: ')
        param_dict={
                'fsym': digital_asset,                          #Base cryptocurrency symbol of interest
        }
        csv_name = '.../Data/' + \
        'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
        digital_asset[-35:].replace('/','_') + '.csv'

## Social Data
elif data_category == 'social/coin':
        sub_category = input('Enter Data Subcategory (latest): ') 
        coin_id = input('Coin ID:')
        if coin_id == '':
                coin_id = 1182
                param_dict={
                        'coinId': coin_id                       #The id of the coin you want data for
                }
                csv_name = '.../Data/' + \
                'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '.csv'

        else:
                coin_id = int(coin_id)
                param_dict={
                        'coinId': coin_id                       #The id of the coin you want data for
                }
                csv_name = '.../Data/' + \
                'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '.csv'

## News
elif data_category == 'v2':
        sub_category = input('Enter Data Subcategory (news/): ') 
        feeds = input('News feeds (eg cryptocompare, cointelegraph, coindesk): ')
        if feeds == '':
                feeds = 'ALL_NEWS_FEEDS'
        categories = input('News categories (eg BTC, ETH, Technology, Blockchain): ')
        if categories == '':
                categories = 'ALL_NEWS_CATEGORIES'
        excludeCategories = input('Excluded news categories (eg Sponsored): ')
        if excludeCategories == '':
                excludeCategories = 'NO_EXCLUDED_NEWS_CATEGORIES'
        lang = input('Preferred language (eg English EN, Portuguese PT): ')      
        if lang == '':
                lang = 'EN'
        sortOrder = input('Order (eg latest or popular): ')
        if sortOrder == '':
                sortOrder = 'latest'
        param_dict={
                'feeds': feeds,                                 #Specific news feeds to retrieve news from
                'categories': categories,                       #Category of news articles to return
                'excludeCategories': excludeCategories,         #News article categories to exclude from results 
                'lang': lang,                                   #Preferred language
                'sortOrder': sortOrder,                         #Order (eg latest or popular)
        }
        csv_name = '.../Data/' + \
        'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
        feeds[-35:].replace('/','_') + '.csv'

## Order Book
elif data_category == 'ob/l1':
        sub_category = input('Enter Data Subcategory (top): ') 
        digital_asset = input('Base Digital Asset: ')
        conversion_pair = input('Quote Digital Asset: ')
        exchange = input('exchange:')
        param_dict={
                'fsyms': digital_asset,                         #Comma separated cryptocurrency symbols list
                'tsyms': conversion_pair,                       #Comma separated cryptocurrency symbols list to convert into
                'e': exchange,                                  #The exchange to obtain data from
        }
        csv_name = '.../Data/' + \
        'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
        digital_asset[-35:].replace('/','_') + '_' + conversion_pair[-35:].replace('/','_') + '.csv'

elif data_category == 'v2/ob/l2':
        sub_category = input('Enter Data Subcategory (snapshot): ') 
        digital_asset = input('Base Digital Asset: ')
        conversion_pair = input('Quote Digital Asset (use USDT iso USD): ')
        exchange = input('exchange: ')
        if exchange == '':
                exchange = 'Binance'
        limit = input('limit:')
        if limit == '':
                limit = 30
        else:
                limit = int(limit)
        param_dict={
                'fsym': digital_asset,                          #Base cryptocurrency symbol of interest
                'tsym': conversion_pair,                        #Quote cryptocurrency symbol of interest
                'e': exchange,                                  #The exchange to obtain data from
                'limit': limit
        }
        csv_name = '.../Data/' + \
        'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
        digital_asset[-35:].replace('/','_') + '_' + conversion_pair[-35:].replace('/','_') + '.csv'

## Index
elif data_category == 'index':
        sub_category = input('Enter Data Subcategory (value, underlying/value): ') 
        if sub_category == 'value':
                indexName = input('Index: ')  
                if indexName == '':
                        indexName = 'MVDA'                           
                param_dict={
                        'indexName': indexName                          #The index you want to get the latest value for.
                }
                csv_name = '.../Data/' + \
                'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
                indexName[-35:].replace('/','_') + '.csv'

        elif sub_category == 'underlying/value':
                digital_asset = input('Base Digital Asset: ')
                conversion_pair = input('Quote Digital Asset: ')
                market = input('Enter Index Market (Default - CCMVDA): ')
                if market == '':
                        market = 'CCMVDA'
                param_dict={
                        'base': digital_asset,                          #Base cryptocurrency symbol of interest
                        'quote': conversion_pair,                       #Quote cryptocurrency symbol of interest
                        'market': market                                #The Index Market
                }
                csv_name = '.../Data/' + \
                'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
                digital_asset[-35:].replace('/','_') + '_' + conversion_pair[-35:].replace('/','_') + '.csv'



exec(open('.../CryptoCompare/CryptoCompare_Latest.py').read())
