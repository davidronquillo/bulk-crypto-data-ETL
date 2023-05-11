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

import pandas as pd
import requests


from functools import reduce

# importing 'config.py' to access its variables
# import config

# Obtain CryptoCompare API key from 'config.py' file and assign to local variable 
# CRYPTOCOMPARE_TOKEN = config.CRYPTOCOMPARE_KEY

# add necessary 'api_key' parameter to 'param_dict' dictionary
param_dict['api_key'] = CRYPTOCOMPARE_TOKEN

#CryptoCompare API
#Download initial batch of data (CryptoCompare: 2000 data unit limit per query)

get_url = 'https://min-api.cryptocompare.com/data/' + data_category + '/' + sub_category

resp = requests.get(get_url,          
    params=param_dict
)

#Creates digital asset dataframe
doc = resp.json()

#convert to pandas dataframe
if data_category == 'v2' or data_category == 'blockchain':
    df = pd.DataFrame(doc['Data']['Data'])
else:
    df = pd.DataFrame(doc['Data'])

#convert 'time' column entries into 'datetime' 
df['time'] = pd.to_datetime(df['time'], unit='s')

#set 'time' column as df index     
df.set_index('time', inplace=True)

#function to download additional 2000 unit batches (beyond initial 2000 data unit limit) and append
#these to earlier downloaded batches
def concat_data(asset_df):
    
    param_dict['toTs'] = int(asset_df.index.min().timestamp()),  #Returns historical data before earliest timestamp received
    
    resp = requests.get(
    get_url,
    params=param_dict
    )
    
    doc = resp.json()
    
    if data_category == 'v2' or data_category == 'blockchain':
        new_df = pd.DataFrame(doc['Data']['Data'])
    else:
        new_df = pd.DataFrame(doc['Data'])
    
    new_df['time'] = pd.to_datetime(new_df['time'], unit='s')
    
    new_df.set_index('time', inplace=True)
    new_df = new_df[:-1].append(asset_df)
    return new_df

# Applies function 'f' to its own output 'n' times'
def repeated(f, n):
     def rfun(p):
        return reduce(lambda x, _: f(x), range(n), p)
     return rfun

# Applies 'repeated' to 'concat_data' generating complete digital asset dataframe
df = repeated(concat_data, num)(df)

# drops irrelevant columns from df
if 'conversionSymbol' in df:
    df = df.drop(columns=['conversionSymbol','conversionType'])

# drops rows in df with all zeros
df = df[(df.T != 0).any()]

df.to_csv(csv_name)
