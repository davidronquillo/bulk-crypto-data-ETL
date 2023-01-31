import requests
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

import json
import pandas as pd

import requests

# importing 'config.py' to access its variables
import config

#Patch to avoid 'ValueError: Value is too big' message when applying 'pd.read_json'
pd.io.json._json.loads = lambda s, *a, **kw: json.loads(s)

# Obtain Glassnode API key from 'config.py' file and assign to local variable 
GLASSNODE_TOKEN = config.GLASSNODE_KEY

# add necessary 'api_key' parameter to 'param_dict' dictionary
param_dict['api_key'] = GLASSNODE_TOKEN

# make API request for OHLC
res = requests.get('https://api.glassnode.com/v1/metrics/market/price_usd_close',
    params=param_dict
    )

# convert to pandas dataframe
glassnode_df = pd.read_json(res.text, convert_dates=['t'])

# renames columns
glassnode_df.columns = ['time', 'close']
# reset index to time series
glassnode_df.set_index('time', inplace=True)

# create working copy of 'glassnode_df'
append_df = glassnode_df
# function gathers given 'tier_endpoints', creates respective df and appends latter to 'glassnode_df'
def tier_df(category_count, crypto_df):    
    # make API request for Price Drawdown from ATH
    res = requests.get('https://api.glassnode.com/v1/metrics/' + data_categories[category_count] + '/' + metric_ids[category_count],
        params=param_dict
        )

    # convert to pandas dataframe
    df = pd.read_json(res.text, convert_dates=['t'])
    
    # rename column
    df.columns=['time',metric_ids[category_count]]

    # reset index to time series
    df.set_index('time', inplace=True)
    
    # concatenate dataframes
    result = pd.concat([crypto_df,df], join='outer',axis=1)
    return result


# executes 'tier_df' function for desired 'tier_endpoints'
for n in list(range(len(metric_ids))):
    append_df = tier_df(n, append_df)

# remove OHLC columns from 'append_df'
append_df = append_df.drop(['close'], axis=1)

# identify columns consisting of a series of dictionaries
dictionary_columns = [n for n in append_df.columns if isinstance(append_df[n][str(append_df[n].first_valid_index())], dict)]

# function transforms 'dictionary' columns into seperate columns consisting of its separate constituent elements and
# renames said columns using original dictionary metric name as a prefix to constituent element column names.
def dictionary_column_split(count, og_glassnode_df):
    
    # convert series of dictionaries into dataframe while ignoring NaNs in dictionary columns
    seperate_columns_df = og_glassnode_df[dictionary_columns[count]].apply(pd.Series)
    # seperate_columns_df = og_glassnode_df[dictionary_columns[count]].apply(pd.Series).drop(0, axis=1)

    # rename columns by adding original column name as prefix
    seperate_columns_df = seperate_columns_df.add_prefix(dictionary_columns[count] + '_')
        
    # concatenate dataframes
    result = pd.concat([og_glassnode_df.drop(columns=[dictionary_columns[count]]), seperate_columns_df], join='outer', axis=1)
    return result

# execute 'dictionary_column_split' function for each, separate, dictionary column
for n in list(range(len(dictionary_columns))):
    append_df = dictionary_column_split(n, append_df)

# concatonate original 'glassnode_df' with added columns from 'append_df'
glassnode_df = pd.concat([glassnode_df,append_df], join='outer',axis=1)

csv_name = '.../Data/' + key_name + '.csv'

glassnode_df.to_csv(csv_name)
