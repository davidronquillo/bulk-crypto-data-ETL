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



# importing 'config.py' to access its variables
import config

# Obtain CryptoCompare API key from 'config.py' file and assign to local variable 
CRYPTOCOMPARE_TOKEN = config.CRYPTOCOMPARE_KEY

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
if data_category == 'blockchain' and (sub_category == 'latest' or \
                                        sub_category == 'staking/latest'):
    df = pd.DataFrame(doc)
elif data_category == 'social/coin' or (data_category == 'news' or \
                                            data_category == 'index'):
    df = pd.DataFrame(doc) 
elif data_category == 'v2':
    df = pd.DataFrame(doc['Data']) 
else:
    df = pd.DataFrame(doc['Data'])

df.to_csv(csv_name)
