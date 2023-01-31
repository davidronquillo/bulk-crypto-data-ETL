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

#Input desired tier 1 `metric_id` metrics
input_metric_ids = input('Enter Metric ID separated by a comma: ')
metric_ids = input_metric_ids.split(',')

key_name = 'glassnode'

#Obtains 'data_categories' metrics from list of 'metric_id' inputs
exec(open('.../glassnode_data_cat_from_sub_cat.py').read())

#Input Optional currency denomination
currency = input('Optional currency denomination (eg USD): ')

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
