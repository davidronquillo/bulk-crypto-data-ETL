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

import numpy as np
import pandas as pd

global data

# takes inputs 'data_source' (eg 'glassnode', 'cryptocompare') and 'coin_pair' (eg 'BTCUSD', 'ETHUSD')
# and returns 'data' dataframe which is cleaned and processed. 

# def process(data_source, coin_pair, returns_dependant):
def process(data_source, coin_pair):

    import import_coin as cn
    df = cn.coin(data_source, coin_pair)

    # Create copy of df
    working_df = df.copy()

    # Obtains date of last 'close' value entry
    last_valid_date = working_df.close.index.get_loc(working_df.close.last_valid_index()) + 1
    data = working_df.copy()[:last_valid_date]

    # Construct pd showing length non-NaN elements of each column in 'data' df
    meta_data = pd.DataFrame(list(map(lambda x: [x,len(data[[x]].dropna())], data.columns.values)))

    # Creates column whose elements consist of the length of a given column's non-NaN elements divided by the length of the longest column's non-NaN elements
    meta_data[[2]]=pd.DataFrame(meta_data[1]/meta_data[1].max())

    meta_data = meta_data.rename(columns={0: 'column_name', 1: 'non-NaN_column_length', 2: 'non-NaN/Max_non-NaN'})

    # Set 'column_name' as index
    meta_data = meta_data.set_index('column_name')

    # Removes from 'meta_data' & 'data_spearman' rows containing 'return' data
    meta_data = meta_data[~meta_data.index.str.startswith('ret_')]

    # Identifies factors having less than 75% length of non-NaN timeseries values
    small_factors = meta_data[meta_data[['non-NaN/Max_non-NaN']]<0.75].drop('non-NaN_column_length', axis=1).dropna()

    # Removes all factors whose 'non-NaN/Max_non-NaN' < 0.75 (ie that do not have sufficient history)
    meta_data=meta_data[meta_data[['non-NaN/Max_non-NaN']]>0.75].drop('non-NaN_column_length', axis=1).dropna()

    # Removes all factors whose 'non-NaN/Max_non-NaN' < 0.75 (ie that do not have sufficient history)
    data = data.drop(data[small_factors.index],axis=1,inplace=False)

    if 'asset' in data:
        data = data.drop('asset', axis=1, inplace=False)

    # Remove rows containing '1-nan_thresh' NaN's from data set 
    nan_thresh=0.75
    data = data.dropna(thresh=round(len(data.columns)*nan_thresh))

    # Generates 'factors.txt' text file listing names of all factors obtained
    column_names = data.columns.values
    np.savetxt('factors.txt',column_names,fmt='%s')

    return data

    # # Creates csv file of 'data' df
    # csv_name = '.../Analysis/data.csv'
    # data.to_csv(csv_name)
    # data.to_csv('data.csv')