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

import requests
import json
import pandas as pd

import requests

# importing 'config.py' to access its variables

#Patch to avoid 'ValueError: Value is too big' message when applying 'pd.read_json'
pd.io.json._json.loads = lambda s, *a, **kw: json.loads(s)

# # Obtain CryptoCompare API key from 'config.py' file and assign to local variable 
# COINMETRICS_TOKEN = config.COINMETRICS_KEY

# # add necessary 'api_key' parameter to 'param_dict' dictionary
# param_dict['api_key'] = COINMETRICS_TOKEN

get_url = 'https://community-api.coinmetrics.io/v4/' + data_category + '/' + sub_category

# make API request for OHLC
res = requests.get(get_url,
    params=param_dict
    )

#Creates digital asset dataframe
doc = res.json()

#convert to pandas dataframe
df = pd.DataFrame(doc['data'])

if data_category == 'timeseries':
    #convert 'time' column entries into 'datetime' 
    df['time'] = pd.to_datetime(df['time'])

    #set 'time' column as df index 
    df.set_index('time', inplace=True)
    

csv_name = '.../Data/coinmetrics.csv'

df.to_csv(csv_name)