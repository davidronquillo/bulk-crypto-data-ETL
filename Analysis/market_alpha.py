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

import talib

global df

# Takes 'data' df and accomponying 'short', 'medium', and 'long' numerical values to calculate traditional 
# TA market alphas
# Requires 'data' df to contain 'ohlc' columns 'open', 'high', 'low', and 'close'.
def market(data, short, medium, long):

    df = data.copy()

    # Simple Moving Average (SMA)
    for t in [short, medium, long]:
        df[f'SMA_{t}'] = talib.SMA(df.close,
                                timeperiod=t)
    # for t in [short, medium, long]:

    #Mayer Multiple
    df['mayer_mult'] = df.close/df.SMA_200
    # Exponential Moving Average (EMA)
    for t in [short, medium, long]:
        df[f'EMA_{t}'] = talib.EMA(df.close,
                                timeperiod=t)
    # for t in [short, medium, long]:

    # Weighted Moving Average (WMA)
    for t in [short, medium, long]:
        df[f'WMA_{t}'] = talib.WMA(df.close,
                                timeperiod=t)
    # for t in [short, medium, long]:

    # Double Exponential Moving Average (DEMA)
    for t in [short, medium, long]:
        df[f'DEMA_{t}'] = talib.DEMA(df.close,
                                    timeperiod=t)
    # for t in [short, medium, long]:

    # Triple Exponential Moving Average (TEMA)
    for t in [short, medium, long]:
        df[f'TEMA_{t}'] = talib.TEMA(df.close,
                                    timeperiod=t)
    # for t in [short, medium, long]:

    # Triangular Moving Average (TRIMA)
    for t in [short, medium, long]:
        df[f'TRIMA_{t}'] = talib.TRIMA(df.close,
                                    timeperiod=t)
    # for t in [short, medium, long]:

    # Kaufman Adaptive Moving Average (KAMA)
    for t in [short, medium, long]:
        df[f'KAMA_{t}'] = talib.KAMA(df.close,
                                    timeperiod=t)
    # for t in [short, medium, long]:

    # MESA Adaptive Moving Average (MAMA)
    mama, fama = talib.MAMA(df.close,
                            fastlimit=.5,
                            slowlimit=.05)
    df['mama'] = mama
    df['fama'] = fama


    # Bollinger Bands
    s = talib.BBANDS(df.close,   # Number of periods (2 to 100000)
                    timeperiod=20,
                    nbdevup=2,    # Deviation multiplier for lower band
                    nbdevdn=2,    # Deviation multiplier for upper band
                    matype=1      # default: SMA
                    )
    bb_bands = ['upper', 'middle', 'lower']
    df = df.assign(**dict(zip(bb_bands, s)))
    # Normalized squeeze & mean reversion indicators
    df['bb_up'] = df.upper.div(df.close)
    df['bb_low'] = df.lower.div(df.close)
    df['bb_squeeze'] = df.upper.div(df.lower)
    # Hilbert Transform - Instantaneous Trendline
    df['HT_TRENDLINE'] = talib.HT_TRENDLINE(df.close)
    # Parabolic SAR
    df['SAR'] = talib.SAR(df.high, df.low, 
                        acceleration=0.02, # common value
                        maximum=0.2)
    # Plus/Minus Directional Movement (PLUS_DM/MINUS_DM)
    df['PLUS_DM'] = talib.PLUS_DM(df.high, df.low, timeperiod=10)
    df['MINUS_DM'] = talib.MINUS_DM(df.high, df.low, timeperiod=10)
    # Plus/Minus Directional Index (PLUS_DI/MINUS_DI)
    df['PLUS_DI'] = talib.PLUS_DI(df.high, df.low, df.close, timeperiod=14)
    df['MINUS_DI'] = talib.MINUS_DI(df.high, df.low, df.close, timeperiod=14)
    # Average directional movement index (ADX)
    df['ADX'] = talib.ADX(df.high, 
                        df.low, 
                        df.close, 
                        timeperiod=14)
    # Average Directional Movement Index Rating
    df['ADXR'] = talib.ADXR(df.high,
                            df.low,
                            df.close,
                            timeperiod=14)
    # Absolute Price Oscillator (APO)
    df['APO'] = talib.APO(df.close,
                        fastperiod=12,
                        slowperiod=26,
                        matype=0)
    # Percentage Price Oscillator (PPO)
    df['PPO'] = talib.PPO(df.close,
                        fastperiod=12,
                        slowperiod=26,
                        matype=0)
    # Aroon Up/Down Indicator
    aroonup, aroondwn = talib.AROON(high=df.high,
                                    low=df.low,
                                    timeperiod=14)
    df['AROON_UP'] = aroonup
    df['AROON_DWN'] = aroondwn
    # Aroon Oscillator
    df['AROONOSC'] = talib.AROONOSC(high=df.high,
                                    low=df.low,
                                    timeperiod=14)
    # Balance Of Power (BOP)
    df['BOP'] = talib.BOP(open=df.open,
                        high=df.high,
                        low=df.low,
                        close=df.close)
    # Commodity Channel Index (CCI)
    df['CCI'] = talib.CCI(high=df.high,
                        low=df.low,
                        close=df.close,
                        timeperiod=14)
    # Moving Average Convergence/Divergence (MACD)
    macd, macdsignal, macdhist = talib.MACD(df.close,
                                            fastperiod=12,
                                            slowperiod=26,
                                            signalperiod=9)
    df['MACD'] = macd
    df['MACDSIG'] = macdsignal
    df['MACDHIST'] = macdhist
    # Chande Momentum Oscillator (CMO)
    df['CMO'] = talib.CMO(df.close, timeperiod=14)
    # Relative Strength Index 14
    df['RSI14'] = talib.RSI(df.close, timeperiod=14)
    # Relative Strength Index 90
    df['RSI90'] = talib.RSI(df.close, timeperiod=90)
    # Stochastic RSI (STOCHRSI)
    fastk, fastd = talib.STOCHRSI(df.close,
                                timeperiod=14, 
                                fastk_period=14, 
                                fastd_period=3, 
                                fastd_matype=0)
    df['fastk'] = fastk
    df['fastd'] = fastd
    # Stochastic (STOCH)
    slowk, slowd = talib.STOCH(df.high,
                            df.low,
                            df.close,
                            fastk_period=14,
                            slowk_period=3,
                            slowk_matype=0,
                            slowd_period=3,
                            slowd_matype=0)
    df['STOCH'] = slowd / slowk
    # Ultimate Oscillator (ULTOSC)
    df['ULTOSC'] = talib.ULTOSC(df.high,
                                df.low,
                                df.close,
                                timeperiod1=7,
                                timeperiod2=14,
                                timeperiod3=28)
    # Williams' %R (WILLR)
    df['WILLR'] = talib.WILLR(df.high,
                            df.low,
                            df.close,
                            timeperiod=14)
    # Volume Indicators
    # Money Flow Index
    if 'volumefrom' in df:
        df['MFI'] = talib.MFI(df.high, 
                        df.low, 
                        df.close, 
                        df.volumeto, 
                        timeperiod=14)
    # Chaikin A/D Line
        df['AD'] = talib.AD(df.high,
                            df.low,
                            df.close,
                            df.volumeto)
        # Chaikin A/D Oscillator (ADOSC)
        df['ADOSC'] = talib.ADOSC(df.high,
                                df.low,
                                df.close,
                                df.volumeto,
                                fastperiod=3,
                                slowperiod=10)
        # On Balance Volume (OBV)
        df['OBV'] = talib.OBV(df.close,
                            df.volumeto)
    # Average True Range indicator (ATR)
    df['ATR'] = talib.ATR(df.high,
                        df.low,
                        df.close,
                        timeperiod=14)
    # Normalized Average True Range (NATR)
    df['NATR'] = talib.NATR(df.high,
                            df.low,
                            df.close,
                            timeperiod=14)

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


    # return df








