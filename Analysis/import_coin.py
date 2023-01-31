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

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd

from os import listdir
from os.path import isfile, join

import talib

global df

# Main function called by 'coin_data.py' that takes stated 'data_source' (eg glassnode, cryptocompare) and
# 'coin_pair' inputs and searches for, and gathers, respective data and appends complementary data from
# non-specified sources to create main coin df
def coin(data_source, coin_pair):
    def create_df(data_provider):

        df = pd.read_csv('.../Data/' + coin_pair + '/' + data_provider + '.csv')

        # #drops rows containing NaN's above threshold value.
    #     df = df.dropna()

        #Identify 'time' column in df and assign it to variable 'time_column' to use as input in next step
        time_column = df.columns[df.columns.get_loc('time' or 'Time' or 'TIME' or 't' or 'T')]

        #Convert from 'string' characters into 'datetime' format
        df[time_column] = pd.to_datetime(df[time_column])

        #set 'time' column as df index 
        df.set_index(time_column, inplace=True)
        
        return df

    # data_source = input('Enter OHLC source/provider (eg glassnode, cryptocompare): ')
    # coin_pair = input('Enter choise of coin pair (eg BTCUSD): ')

    # Identifies files contained in 'Data/' + coin_pair folder
    onlyfiles = [f for f in listdir('.../Data/' + coin_pair + '/') \
                if isfile(join('.../Data/' + coin_pair + '/', f))]

    # Picks out 'Coinmetrics' only files
    coinmetrics_files = [n for n in onlyfiles if n.startswith('coin')]

    # Picks out 'Glassnode' only files
    glassnode_files = [n for n in onlyfiles if n.startswith('glass')]


    if data_source == 'glassnode':
            
        # Checks if any 'glassnode.csv' files exist in the 'Data' folder
        if len(glassnode_files) > 0:
            # Imports data from 'glassnode_files' using 'create_df' to generate list of Glassnode df's
            glassnode_df_list = list(map(lambda n: create_df(glassnode_files[n][:-4]), list(range(len(glassnode_files)))))

            if len(glassnode_files) > 1:
                # Creates 'glassnode_df' by joining various Glassnode dfs
                glassnode_df = pd.concat(glassnode_df_list, axis=1, join='outer')
                # Removes duplicate columns (mainly ohlc)
                glassnode_df = glassnode_df.loc[:,~glassnode_df.columns.duplicated()]
            elif len(glassnode_files) == 1:
                glassnode_df = glassnode_df_list[0]

        # Checks if any 'coinmetrics.csv' files exist in the 'Data' folder
        if len(coinmetrics_files) > 0:
            # Imports data from 'coinmetrics_files' using 'create_df' to generate list of Coinmetrics df's
            coinmetrics_df_list = list(map(lambda n: create_df(coinmetrics_files[n][:-4]), list(range(len(coinmetrics_files)))))

            if len(coinmetrics_files) > 1:
                # Creates 'coinmetrics_df' by joining various Coinmetrics dfs
                coinmetrics_df = pd.concat(coinmetrics_df_list, axis=1, how='outer')
            elif len(coinmetrics_files) == 1:
                coinmetrics_df = coinmetrics_df_list[0]

            #Remove UTC from datetime64[ns, UTC] dtype to make consistent with glassnode_df.index
            coinmetrics_df.index = coinmetrics_df.index.tz_convert(None)

        # Picks out 'CryptoCompare' only files (except OHLC files)
        cryptocompare_files = [n for n in onlyfiles if n.startswith('cc_') and not n.startswith('cc_v2')]

        # Checks if there are any cryptocompare csv files in 'Data' folder
        if len(cryptocompare_files) > 0:
            # Imports data from 'cryptocompare_files' using 'create_df' to generate list of CryptoCompare df's
            cryptocompare_df_list = list(map(lambda n: create_df(cryptocompare_files[n][:-4]), list(range(len(cryptocompare_files)))))

            if len(cryptocompare_df_list) > 1:
                # Creates 'cryptocompare_df' by joining various CryptoCompare dfs
                df = pd.concat(cryptocompare_df_list, axis=1, join='outer')

                df = df.drop(['comments', 'posts', 'followers', 'points', 'overview_page_views', 'analysis_page_views', 'markets_page_views', \
    'charts_page_views', 'trades_page_views', 'forum_page_views', 'influence_page_views', 'total_page_views', 'fb_likes', \
    'fb_talking_about', 'twitter_followers', 'twitter_following', 'twitter_lists', 'twitter_favourites', 'twitter_statuses', \
    'code_repo_stars', 'code_repo_forks', 'code_repo_subscribers', 'code_repo_open_pull_issues', 'code_repo_closed_pull_issues', \
    'code_repo_open_issues', 'code_repo_closed_issues', 'code_repo_contributors'], axis=1)
            else:
                df = cryptocompare_df_list[0]

        if len(coinmetrics_files) > 0 and len(cryptocompare_files) > 0:
            #Join cryptocompare & coinmetrics dataframes
            cp_cm_df = df.join(coinmetrics_df, how='outer')
            #Join glassnode df with cryptocompare & coinmetrics df
            df = glassnode_df.join(cp_cm_df, how='outer')
        elif len(coinmetrics_files) > 0 and len(cryptocompare_files) == 0:
            df = glassnode_df.join(coinmetrics_df, how='outer')
        elif len(coinmetrics_files) == 0 and len(cryptocompare_files) > 0:
            df = glassnode_df.join(df, how='outer')
        else:
            df = glassnode_df
        
    else:

        # Picks out 'CryptoCompare' only files
        cryptocompare_files = [n for n in onlyfiles if n.startswith('cc_')]

        # Imports data from 'cryptocompare_files' using 'create_df' to generate list of CryptoCompare df's
        cryptocompare_df_list = list(map(lambda n: create_df(cryptocompare_files[n][:-4]), list(range(len(cryptocompare_files)))))

        if len(cryptocompare_df_list) > 1:
            # Creates 'cryptocompare_df' by joining various CryptoCompare dfs
            df = pd.concat(cryptocompare_df_list, axis=1, join='outer')

            df = df.drop(['comments', 'posts', 'followers', 'points', 'overview_page_views', 'analysis_page_views', 'markets_page_views', \
    'charts_page_views', 'trades_page_views', 'forum_page_views', 'influence_page_views', 'total_page_views', 'fb_likes', \
    'fb_talking_about', 'twitter_followers', 'twitter_following', 'twitter_lists', 'twitter_favourites', 'twitter_statuses', \
    'code_repo_stars', 'code_repo_forks', 'code_repo_subscribers', 'code_repo_open_pull_issues', 'code_repo_closed_pull_issues', \
    'code_repo_open_issues', 'code_repo_closed_issues', 'code_repo_contributors'], axis=1)
        else:
            df = cryptocompare_df_list[0]

        # Checks if any 'glassnode.csv' files exist in the 'Data' folder
        if len(glassnode_files) > 0:
            # Imports data from 'glassnode_files' using 'create_df' to generate list of Glassnode df's
            glassnode_df_list = list(map(lambda n: create_df(glassnode_files[n][:-4]), list(range(len(glassnode_files)))))

            if len(glassnode_files) > 1:
                # Creates 'glassnode_df' by joining various Glassnode dfs
                glassnode_df = pd.concat(glassnode_df_list, axis=1, join='outer')
                # Removes duplicate columns (mainly ohlc)
                glassnode_df = glassnode_df.loc[:,~glassnode_df.columns.duplicated()]
            elif len(glassnode_files) == 1:
                glassnode_df = glassnode_df_list[0]
            
            # Drop OHLC columns from 'glassnode_df'
            glassnode_df = glassnode_df.drop(['close', 'open', 'low', 'high'], axis=1)

        # Checks if any 'coinmetrics.csv' files exist in the 'Data' folder
        if len(coinmetrics_files) > 0:
            # Imports data from 'coinmetrics_files' using 'create_df' to generate list of Coinmetrics df's
            coinmetrics_df_list = list(map(lambda n: create_df(coinmetrics_files[n][:-4]), list(range(len(coinmetrics_files)))))

            if len(coinmetrics_files) > 1:
                # Creates 'coinmetrics_df' by joining various Coinmetrics dfs
                coinmetrics_df = pd.concat(coinmetrics_df_list, axis=1, join='outer')
            elif len(coinmetrics_files) == 1:
                coinmetrics_df = coinmetrics_df_list[0]

            #Remove UTC from datetime64[ns, UTC] dtype to make consistent with glassnode_df.index
            coinmetrics_df.index = coinmetrics_df.index.tz_convert(None)

        if len(glassnode_files) > 0 and len(coinmetrics_files) > 0:
            #Join glassnode & coinmetrics dataframes
            gn_cm_df = glassnode_df.join(coinmetrics_df, how='outer')
            #Join cryptocompare df with glassnode & coinmetrics df
            df = df.join(gn_cm_df, how='outer')
        elif len(glassnode_files) > 0 and len(coinmetrics_files) == 0:
            df = glassnode_df.join(df, how='outer')
        elif len(glassnode_files) == 0 and len(coinmetrics_files) > 0:
            df = df.join(coinmetrics_df, how='outer')
        else:
            df = df

    function_groups = ['Overlap Studies',
                    'Momentum Indicators',
                    'Volume Indicators',
                    'Volatility Indicators',
                    'Price Transform',
                    'Cycle Indicators',
                    'Pattern Recognition',
                    'Statistic Functions',
                    'Math Transform',
                    'Math Operators']

    talib_grps = talib.get_function_groups()

    return df








