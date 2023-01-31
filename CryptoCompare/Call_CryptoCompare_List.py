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
data_category = input('Enter Data Category:\n********************\n blockchain\n Pair Mapping (v2/pair/mapping)\n \
Top Lists (top, exchange/top)\n news\n Order Book (ob)\n General Info (v4, all, \
v2/cccagg, cccagg/pairs, cccagg/coins, exchanges, gambling, wa llets, cards, mining/contracts, \
mining/companies, mining/equipment, mining/pools)\n index \n: ')


# list of sought after endpoint parameters

## Blockchain Data
if data_category == 'blockchain':
        sub_category = input('Enter Data Subcategory (list, mining/calculator): ')
        if sub_category == 'list':
                param_dict={
                }
                csv_name = '.../Data/' + \
                'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '.csv'
        elif sub_category == 'mining/calculator':
                digital_asset = input('Base Digital Asset: ')
                conversion_pair = input('Quote Digital Asset: ')
                param_dict={
                        'fsyms': digital_asset,                         #Comma separated cryptocurrency symbols list
                        'tsyms': conversion_pair,                       #Comma separated cryptocurrency symbols list to convert into
                }
                csv_name = '.../Data/' + \
                'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
                digital_asset[-35:].replace('/','_') + '_' + conversion_pair[-35:].replace('/','_') + '.csv'

## Pair Mapping
elif data_category == 'v2/pair/mapping':
        sub_category = input('Enter Data Subcategory (fsym, exchange, exchange/fsym): ')
        if sub_category == 'fsym':
                digital_asset = input('Base Digital Asset: ')
                if digital_asset == '':
                        digital_asset = 'BTC'
                param_dict={
                        'fsym': digital_asset,                          #Base cryptocurrency symbol of interest
                }
                csv_name = '.../Data/' + \
                'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
                digital_asset[-35:].replace('/','_') + '.csv'

        elif sub_category == 'exchange':
                exchange = input('exchange: ')
                param_dict={
                        'e': exchange,                                  #The exchange to obtain data from
                }
                csv_name = '.../Data/' + \
                'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
                exchange[-35:].replace('/','_') + '.csv'

        elif sub_category == 'exchange/fsym':
                digital_asset = input('Base Digital Asset: ')
                if digital_asset == '':
                        digital_asset = 'BTC'
                param_dict={
                        'exchangeFsym': digital_asset,                  #The exchange to obtain data from
                }
                csv_name = '.../Data/' + \
                'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
                digital_asset[-35:].replace('/','_') + '.csv'

## Top Lists
elif data_category == 'top':
        sub_category = input('Enter Data Subcategory (totalvolfull, \
totaltoptiervolfull, mktcapfull, volumes, \
pairs, exchanges, exchanges/full): ')
        if sub_category == 'totalvolfull' or \
                sub_category == 'totaltoptiervolfull' or \
                sub_category == 'mktcapfull' or \
                sub_category == 'volumes':
                        conversion_pair = input('Quote Digital Asset: ')
                        asset_Class = input('asset class (DeFi or All)): ')
                        limit = int(input('Number of coins:'))
                        if limit == '':
                                limit = 10                  
                        param_dict={
                                'tsym': conversion_pair,                        #Quote cryptocurrency symbol of interest
                                'assetClass': asset_Class,                      #The asset class of a set of coins to filter the toplist by. Options are DEFI and ALL.
                                'limit': limit                                  #Number of coins to return in toplist
                        }
                        csv_name = '.../Data/' + \
                        'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
                        conversion_pair[-35:].replace('/','_') + '_' + asset_Class[-35:].replace('/','_') + '.csv'

        elif sub_category == 'pairs':
                        digital_asset = input('Base Digital Asset: ')
                        limit = int(input('Number of coins: '))                  
                        param_dict={
                                'fsym': digital_asset,                          #Base cryptocurrency symbol of interest
                                'limit': limit                                  #Number of coins to return in toplist
                        }
                        csv_name = '.../Data/' + \
                        'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
                        digital_asset[-35:].replace('/','_') + '.csv'

        elif sub_category == 'exchanges' or \
                sub_category == 'exchanges/full':
                        digital_asset = input('Base Digital Asset: ')
                        conversion_pair = input('Quote Digital Asset: ')
                        limit = int(input('Number of coins: '))                  
                        param_dict={
                                'fsym': digital_asset,                          #Base cryptocurrency symbol of interest
                                'tsym': conversion_pair,                        #Quote cryptocurrency symbol of interest
                                'limit': limit                                  #Number of coins to return in toplist
                        }
                        csv_name = '.../Data/' + \
                        'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
                        digital_asset[-35:].replace('/','_') + '_' + conversion_pair[-35:].replace('/','_') + '.csv'

elif data_category == 'exchange/top':
        sub_category = input('Enter Data Subcategory (volume): ')
        exchange = input('exchange: ')
        limit = int(input('Number of coins: '))                 
        param_dict={
                'e': exchange,                                  #The exchange to obtain data from
                'limit': limit
        }
        csv_name = '.../Data/' + \
        'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
        exchange[-35:].replace('/','_') + '.csv'

## News
elif data_category == 'news':
        sub_category = input('Enter Data Subcategory (feeds, categories, \
feedsandcategories): ')
        param_dict={
        }
        csv_name = '.../Data/' + \
        'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '.csv'

## Order Book
elif data_category == 'ob':
        sub_category = input('Enter Data Subcategory (exchanges): ')
        param_dict={
        }
        csv_name = '.../Data/' + \
        'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '.csv'
     
## General Info
elif data_category == 'v4':
        sub_category = input('Enter Data Subcategory (all/exchanges): ')
        digital_asset = input('Base Digital Asset: ')
        exchange = input('exchange:')
        topTier = input('Set `true` for top tier exchanges: ')
        if topTier == '':
                topTier = 'false'
        param_dict={
                'fsym': digital_asset,                          #Base cryptocurrency symbol of interest
                'e': exchange,                                  #The exchange to obtain data from
                'topTier': topTier                              #Set to true if you just want to return the top tier exchanges
        }
        csv_name = '.../Data/' + \
        'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
        digital_asset[-35:].replace('/','_') + '_' + exchange[-35:].replace('/','_') + '.csv'

elif data_category == 'all':
        sub_category = input('Enter Data Subcategory (includedexchanges, coinlist): ')
        if sub_category == 'includedexchanges':
                instrument = input('Type of average instrument (default: CCCAGG):')
                if instrument == '':
                        instrument = 'CCCAGG'                           
                param_dict={
                        'instrument': instrument                        #The type of average instrument. Will return the exchanges and pairs included in this average.
                }      
                csv_name = '.../Data/' + \
                'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
                instrument[-35:].replace('/','_') + '.csv'

        elif sub_category == 'coinlist':
                builtOn = input('Platform token is built on: ')
                summary = input('return id, ImageUrl, Symbol, FullName if `true`: ')
                if summary == '':
                        summary = 'false'
                param_dict={
                        'builtOn': builtOn,                             #The platform that the token is built on
                        'summary': summary                              #If set to true it will only return Id, ImageUrl, Symbol, FullName for each coin. Only works with the full list of coins.
                }
                csv_name = '.../Data/' + \
                'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
                builtOn[-35:].replace('/','_') + '.csv'

elif data_category == 'v2/cccagg':
        sub_category = input('Enter Data Subcategory (pairs): ')               
        digital_asset = input('Base Digital Asset: ')
        param_dict={
                'fsym': digital_asset,                          #Base cryptocurrency symbol of interest
        }    
        csv_name = '.../Data/' + \
        'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
        digital_asset[-35:].replace('/','_') + '.csv'
   
elif data_category == 'cccagg/pairs':
        sub_category = input('Enter Data Subcategory (excluded, absent): ')               
        digital_asset = input('Base Digital Asset: ')
        param_dict={
                'fsym': digital_asset,                          #Base cryptocurrency symbol of interest
        }       
        csv_name = '.../Data/' + \
        'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
        digital_asset[-35:].replace('/','_') + '.csv'

elif data_category == 'cccagg/coins':         #*********
        sub_category = input('Enter Data Subcategory (absent): ')               
        digital_asset = input('Base Digital Asset: ')
        param_dict={
                'fsym': digital_asset,                          #Base cryptocurrency symbol of interest
        }       
        csv_name = '.../Data/' + \
        'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
        digital_asset[-35:].replace('/','_') + '.csv'

elif data_category == 'exchanges':
        sub_category = input('Enter Data Subcategory (general): ')               
        conversion_pair = input('Quote Digital Asset: ')
        param_dict={
                'tsym': conversion_pair,                        #Quote cryptocurrency symbol of interest
        }
        csv_name = '.../Data/' + \
        'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '_' + \
        conversion_pair[-35:].replace('/','_') + '.csv'

elif data_category == 'gambling' or \
        data_category == 'wallets' or \
        data_category == 'cards' or \
        data_category == 'mining/contracts' or \
        data_category == 'mining/companies' or \
        data_category == 'mining/equipment' or \
        data_category == 'mining/pools':
        sub_category = input('Enter Data Subcategory (general): ')               
        param_dict={
        }    
        csv_name = '.../Data/' + \
        'cc_' + data_category[-35:].replace('/','_') + '.csv'
                                                   ## `sub_category` = general
## Index
elif data_category == 'index':
        sub_category = input('Enter Data Subcategory (list, underlying/list): ')               
        param_dict={
        }
        csv_name = '.../Data/' + \
        'cc_' + data_category[-35:].replace('/','_') + '_' + sub_category[-35:].replace('/','_') + '.csv'

exec(open('.../CryptoCompare/CryptoCompare_List.py').read())
