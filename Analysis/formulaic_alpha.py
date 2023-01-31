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

from sklearn.feature_selection import mutual_info_regression

# Takes 'data' df and calculates formulaic alphas based on '101 Formulaic Alphas' by Zura Kakushadze's
# https://arxiv.org/ftp/arxiv/papers/1601/1601.00991.pdf via Stefan Jansen's 'Machine Learning for Algorithmic Trading' book. 
# https://github.com/stefan-jansen/machine-learning-for-trading/blob/main/24_alpha_factor_library/03_101_formulaic_alphas.ipynb

# Requires 'data' df to contain 'ohlc' columns 'open', 'high', 'low', and 'close', and 'volumeto' column.

# Optional 'returns_dependent' argument will include returns dependent formulaic alpha factors.
# Default: returns_dependent='N'
def formulaic(data, returns_dependent='N'):

    df = data.copy()

    today = pd.to_datetime("today")

    # Operators
    def log(df):
        return np.log1p(df)

    def sign(df):
        return np.sign(df)

    def power(df, exp):
        return df.pow(exp)

    # Time Series Functions
    def ts_lag(df: pd.DataFrame, t: int = 1) -> pd.DataFrame:
        """Return the lagged values t periods ago.

        Args:
            :param df: tickers in columns, sorted dates in rows.
            :param t: lag

        Returns:
            pd.DataFrame: the lagged values
        """
        return df.shift(t)

    def ts_delta(df, period=1):
        """
        Wrapper function to estimate difference.
        :param df: a pandas DataFrame.
        :param period: the difference grade.
        :return: a pandas DataFrame with today’s value minus the value 'period' days ago.
        """
        return df.diff(period)

    def ts_sum(df: pd.DataFrame, window: int = 10) -> pd.DataFrame:
        """Computes the rolling ts_sum for the given window size.

        Args:
            df (pd.DataFrame): tickers in columns, dates in rows.
            window      (int): size of rolling window.

        Returns:
            pd.DataFrame: the ts_sum over the last 'window' days.
        """
        return df.rolling(window).sum()

    def ts_mean(df, window=10):
        """Computes the rolling mean for the given window size.

        Args:
            df (pd.DataFrame): tickers in columns, dates in rows.
            window      (int): size of rolling window.

        Returns:
            pd.DataFrame: the mean over the last 'window' days.
        """
        return df.rolling(window).mean()

    def ts_weighted_mean(df, period=10):
        """
        Linear weighted moving average implementation.
        :param df: a pandas DataFrame.
        :param period: the LWMA period
        :return: a pandas DataFrame with the LWMA.
        """
        return (df.apply(lambda x: WMA(x, timeperiod=period)))

    def ts_std(df, window=10):
        """
        Wrapper function to estimate rolling standard deviation.
        :param df: a pandas DataFrame.
        :param window: the rolling window.
        :return: a pandas DataFrame with the time-series min over the past 'window' days.
        """
        return (df
                .rolling(window)
                .std())

    def ts_rank(df, window=10):
        """
        Wrapper function to estimate rolling rank.
        :param df: a pandas DataFrame.
        :param window: the rolling window.
        :return: a pandas DataFrame with the time-series rank over the past window days.
        """
        return (df
                .rolling(window)
                .apply(lambda x: x.rank().iloc[-1]))

    def ts_product(df, window=10):
        """
        Wrapper function to estimate rolling ts_product.
        :param df: a pandas DataFrame.
        :param window: the rolling window.
        :return: a pandas DataFrame with the time-series ts_product over the past 'window' days.
        """
        return (df
                .rolling(window)
                .apply(np.prod))

    def ts_min(df, window=10):
        """
        Wrapper function to estimate rolling min.
        :param df: a pandas DataFrame.
        :param window: the rolling window.
        :return: a pandas DataFrame with the time-series min over the past 'window' days.
        """
        return df.rolling(window).min()

    def ts_max(df, window=10):
        """
        Wrapper function to estimate rolling min.
        :param df: a pandas DataFrame.
        :param window: the rolling window.
        :return: a pandas DataFrame with the time-series max over the past 'window' days.
        """
        return df.rolling(window).max()

    def ts_argmax(df, window=10):
        """
        Wrapper function to estimate which day ts_max(df, window) occurred on
        :param df: a pandas DataFrame.
        :param window: the rolling window.
        :return: well.. that :)
        """
        return df.rolling(window).apply(np.argmax).add(1)

    def ts_argmin(df, window=10):
        """
        Wrapper function to estimate which day ts_min(df, window) occurred on
        :param df: a pandas DataFrame.
        :param window: the rolling window.
        :return: well.. that :)
        """
        return (df.rolling(window)
                .apply(np.argmin)
                .add(1))

    def ts_corr(x, y, window=10):
        """
        Wrapper function to estimate rolling correlations.
        :param x, y: pandas DataFrames.
        :param window: the rolling window.
        :return: a pandas DataFrame with the time-series min over the past 'window' days.
        """
        return x.rolling(window).corr(y)

    def ts_cov(x, y, window=10):
        """
        Wrapper function to estimate rolling covariance.
        :param df: a pandas DataFrame.
        :param window: the rolling window.
        :return: a pandas DataFrame with the time-series min over the past 'window' days.
        """
        return x.rolling(window).cov(y)

    # Calculate mutual information between alpha & forward returns (using 55% sample size)
    def get_mutual_info_score(returns, alpha):
        df = pd.DataFrame({'y': returns, 'alpha': alpha}).dropna().sample(n=int(len(alpha)*0.55))
        return mutual_info_regression(y=df.y, X=df[['alpha']])[0]

    ohlcv = ['open', 'high', 'low', 'close', 'volumeto']

    adv20 = df.rolling(20).volumeto.mean().reset_index(0, drop=True)
    data = df.assign(adv20=adv20)
    # data.info(null_counts=True)

    o = df.open.copy()
    h = df.high.copy()
    l = df.low.copy()
    c = df.close.copy()
    v = df.volumeto.copy()
    vwap = o.add(h).add(l).add(c).div(4)
    adv20 = v.rolling(20).mean()

    # alpha_no = {}
    # formulaic_alpha_dict = {}

    # returns_dependent = input('Include "returns dependent" formulaic alpha? (Y/N): ')

    if returns_dependent == 'Y' or returns_dependent == 'N':

        # Formulaic Alphas returns independent

        def alpha002(o, c, v):
            """(-1 * ts_corr(rank(ts_delta(log(volume), 2)), rank(((close - open) / open)), 6))"""
            s1 = ts_delta(log(v), 2)
            s2 = (c / o) - 1
            alpha = -ts_corr(s1, s2, 6)
            return alpha.replace([-np.inf, np.inf], np.nan)

        alpha_str = '002'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha002(o, c, v)

        def alpha003(o, v):
            """(-1 * ts_corr(rank(open), rank(volume), 10))"""

            return (-ts_corr(o, v, 10).replace([-np.inf, np.inf], np.nan))

        alpha_str = '003'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha003(o, v)

        def alpha004(l):
            """(-1 * Ts_Rank(rank(low), 9))"""
            return (-ts_rank(l, 9))

        alpha_str = '004'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha004(l)

        def alpha005(o, vwap, c):
            """(rank((open - ts_mean(vwap, 10))) * (-1 * abs(rank((close - vwap)))))"""
            return o.sub(ts_mean(vwap, 10)).mul(c.sub(vwap).mul(-1).abs())

        alpha_str = '005'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha005(o, vwap, c)

        def alpha006(o, v):
            """(-ts_corr(open, volume, 10))"""
            return (-ts_corr(o, v, 10))

        alpha_str = '006'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha006(o, v)

        def alpha007(c, v, adv20):
            """(adv20 < volume) 
                ? ((-ts_rank(abs(ts_delta(close, 7)), 60)) * sign(ts_delta(close, 7))) 
                : -1
            """
            
            delta7 = ts_delta(c, 7)
            return (-ts_rank(abs(delta7), 60)
                    .mul(sign(delta7))
                    .where(adv20<v, -1))

        alpha_str = '007'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha007(c, v, adv20)

        def alpha009(c):
            """(0 < ts_min(ts_delta(close, 1), 5)) ? ts_delta(close, 1) 
            : ((ts_max(ts_delta(close, 1), 5) < 0) 
            ? ts_delta(close, 1) : (-1 * ts_delta(close, 1)))
            """
            close_diff = ts_delta(c, 1)
            alpha = close_diff.where(ts_min(close_diff, 5) > 0,
                                    close_diff.where(ts_max(close_diff, 5) < 0,
                                                    -close_diff))
            return alpha

        alpha_str = '009'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha009(c)

        def alpha010(c):
            """rank(((0 < ts_min(ts_delta(close, 1), 4)) 
                ? ts_delta(close, 1) 
                : ((ts_max(ts_delta(close, 1), 4) < 0)
                    ? ts_delta(close, 1) 
                    : (-1 * ts_delta(close, 1)))))
            """
            close_diff = ts_delta(c, 1)
            alpha = close_diff.where(ts_min(close_diff, 4) > 0,
                                    close_diff.where(ts_min(close_diff, 4) > 0,
                                                    -close_diff))

            return alpha

        alpha_str = '010'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha010(c)

        def alpha011(c, vwap, v):
            """(rank(ts_max((vwap - close), 3)) + 
                rank(ts_min(vwap - close), 3)) * 
                rank(ts_delta(volume, 3))
                """
            return ts_max(vwap.sub(c), 3).add(ts_min(vwap.sub(c), 3)).mul(ts_delta(v, 3))

        alpha_str = '011'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha011(c, vwap, v)

        def alpha012(v, c):
            """(sign(ts_delta(volume, 1)) * 
                    (-1 * ts_delta(close, 1)))
                """
            return sign(ts_delta(v, 1)).mul(-ts_delta(c, 1))
                    
        alpha_str = '012'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha012(v, c)

        def alpha013(c, v):
            """-rank(ts_cov(rank(close), rank(volume), 5))"""
            return -ts_cov(c, v, 5)
                    
        alpha_str = '013'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha013(c, v)

        def alpha015(h, v):
            """(-1 * ts_sum(rank(ts_corr(rank(high), rank(volume), 3)), 3))"""
            alpha = (-ts_sum(ts_corr(h, v, 3).replace([-np.inf, np.inf], np.nan), 3))
            return alpha

        alpha_str = '015'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha015(h, v)

        def alpha016(h, v):
            """(-1 * rank(ts_cov(rank(high), rank(volume), 5)))"""
            return -ts_cov(h, v, 5)

        alpha_str = '016'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha016(h, v)

        def alpha017(c, v):
            """(((-1 * rank(ts_rank(close, 10))) * rank(ts_delta(ts_delta(close, 1), 1))) *rank(ts_rank((volume / adv20), 5)))
                """
            adv20 = ts_mean(v, 20)
            return -ts_rank(c, 10).mul(ts_delta(ts_delta(c, 1), 1)).mul(ts_rank(v.div(adv20), 5))

        alpha_str = '017'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha017(c, v)

        def alpha018(o, c):
            """-rank((ts_std(abs((close - open)), 5) + (close - open)) +
                    ts_corr(close, open,10))
            """
            return -ts_std(c.sub(o).abs(), 5).add(c.sub(o)).add(ts_corr(c, o, 10).replace([-np.inf,np.inf],np.nan))
                    
        alpha_str = '018'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha018(o, c)

        def alpha020(o, h, l, c):
            """-rank(open - ts_lag(high, 1)) * 
                rank(open - ts_lag(close, 1)) * 
                rank(open -ts_lag(low, 1))"""
            return -(o - ts_lag(h, 1)).mul(o - ts_lag(c, 1)).mul(o - ts_lag(l, 1)).mul(-1)

        alpha_str = '020'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha020(o, h, l, c)

        def alpha021(c, v):
            """ts_mean(close, 8) + ts_std(close, 8) < ts_mean(close, 2)
                ? -1
                : (ts_mean(close,2) < ts_mean(close, 8) - ts_std(close, 8)
                    ? 1
                    : (volume / adv20 < 1
                        ? -1
                        : 1))
            """
            sma2 = ts_mean(c, 2)
            sma8 = ts_mean(c, 8)
            std8 = ts_std(c, 8)

            cond_1 = sma8.add(std8) < sma2
            cond_2 = sma8.add(std8) > sma2
            cond_3 = v.div(ts_mean(v, 20)) < 1

            val = np.ones_like(c)
            alpha = pd.DataFrame(np.select(condlist=[cond_1, cond_2, cond_3],choicelist=[-1, 1, -1], default=1),index=c.index)

            return alpha

        alpha_str = '021'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha021(c, v)

        def alpha022(h, c, v):
            """-(ts_delta(ts_corr(high, volume, 5), 5) * 
                rank(ts_std(close, 20)))
            """

            return ts_delta(ts_corr(h, v, 5).replace([-np.inf,np.inf],np.nan), 5).mul(ts_std(c, 20)).mul(-1)

        alpha_str = '022'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha022(h, c, v)

        def alpha023(h, c):
            """((ts_mean(high, 20) < high)
                    ? (-1 * ts_delta(high, 2))
                    : 0
                """

            return ts_delta(h, 2).mul(-1).where(ts_mean(h, 20) < h, 0)

        alpha_str = '023'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha023(h, c)

        def alpha024(c):
            """((((ts_delta((ts_mean(close, 100)), 100) / ts_lag(close, 100)) <= 0.05)  
                ? (-1 * (close - ts_min(close, 100))) 
                : (-1 * ts_delta(close, 3)))
            """
            cond = ts_delta(ts_mean(c, 100), 100) / ts_lag(c, 100) <= 0.05

            return c.sub(ts_min(c, 100)).mul(-1).where(cond, -ts_delta(c, 3))

        alpha_str = '024'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha024(c)

        def alpha026(h, v):
            """(-1 * ts_max(ts_corr(ts_rank(volume, 5), ts_rank(high, 5), 5), 3))"""
            return ts_max(ts_corr(ts_rank(v, 5), ts_rank(h, 5), 5).replace([-np.inf, np.inf], np.nan), 3).mul(-1)
                    
        alpha_str = '026'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha026(h, v)

        def alpha027(v, vwap):
            """((0.5 < rank(ts_mean(ts_corr(rank(volume), rank(vwap), 6), 2))) 
                    ? -1
                    : 1)"""
            cond = ts_mean(ts_corr(v,vwap, 6), 2)
            alpha = cond.notnull().astype(float)
            return alpha.where(cond <= 0.5, -alpha)

        alpha_str = '027'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha027(v, vwap)

        def alpha028(h, l, c, v, adv20):
            """scale(((ts_corr(adv20, low, 5) + (high + low) / 2) - close))"""
            return ts_corr(adv20, l, 5).replace([-np.inf, np.inf], 0).add(h.add(l).div(2).sub(c))

        alpha_str = '028'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha028(h, l, c, v, adv20)

        def alpha030(c, v):
            """(((1.0 - rank(((sign((close - ts_lag(close, 1))) +
                    sign((ts_lag(close, 1) - ts_lag(close, 2)))) +
                    sign((ts_lag(close, 2) - ts_lag(close, 3)))))) *
                    ts_sum(volume, 5)) / ts_sum(volume, 20))"""
            close_diff = ts_delta(c, 1)
            return sign(close_diff).add(sign(ts_lag(close_diff, 1))).add(sign(ts_lag(close_diff, 2))).mul(-1).add(1).mul(ts_sum(v, 5)).div(ts_sum(v, 20))

        alpha_str = '030'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha030(c, v)

        def alpha032(c, vwap):
            """scale(ts_mean(close, 7) - close) + 
                (20 * scale(ts_corr(vwap, ts_lag(close, 5),230)))"""
            return (ts_mean(c, 7).sub(c)).add(20 * ts_corr(vwap,ts_lag(c, 5), 230))

        alpha_str = '032'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha032(c, vwap)

        def alpha033(o, c):
            """rank(-(1 - (open / close)))"""
            return o.div(c).mul(-1).add(1).mul(-1)

        alpha_str = '033'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha033(o, c)

        def alpha037(o, c):
            """(rank(ts_corr(ts_lag((open - close), 1), close, 200)) + rank((open - close)))"""
            return ts_corr(ts_lag(o.sub(c), 1), c, 200).add(o.sub(c))

        alpha_str = '037'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha037(o, c)

        def alpha038(o, c):
            """"-1 * rank(ts_rank(close, 10)) * rank(close / open)"""
            return ts_rank(o, 10).mul(c.div(o).replace([-np.inf, np.inf], np.nan)).mul(-1)

        alpha_str = '038'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha038(o, c)

        def alpha040(h, v):
            """((-1 * rank(ts_std(high, 10))) * ts_corr(high, volume, 10))
            """
            return ts_std(h, 10).mul(ts_corr(h, v, 10)).mul(-1)

        alpha_str = '040'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha040(h, v)

        def alpha041(h, l, vwap):
            """power(high * low, 0.5 - vwap"""
            return power(h.mul(l), 0.5).sub(vwap)

        alpha_str = '041'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha041(h, l, vwap)

        def alpha042(c, vwap):
            """rank(vwap - close) / rank(vwap + close)"""
            return vwap.sub(c).div(vwap.add(c))

        alpha_str = '042'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha042(c, vwap)

        def alpha043(c, adv20):
            """(ts_rank((volume / adv20), 20) * ts_rank((-1 * ts_delta(close, 7)), 8))"""

            return ts_rank(v.div(adv20), 20).mul(ts_rank(ts_delta(c, 7).mul(-1), 8))

        alpha_str = '043'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha043(c, adv20)

        def alpha044(h, v):
            """-ts_corr(high, rank(volume), 5)"""

            return ts_corr(h, v, 5).replace([-np.inf, np.inf], np.nan).mul(-1)

        alpha_str = '044'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha044(h, v)

        def alpha045(c, v):
            """-(rank((ts_mean(ts_lag(close, 5), 20)) * 
                ts_corr(close, volume, 2)) *
                rank(ts_corr(ts_sum(close, 5), ts_sum(close, 20), 2)))"""

            return ts_mean(ts_lag(c, 5), 20).mul(ts_corr(c, v, 2).replace([-np.inf, np.inf], np.nan)).mul(ts_corr(ts_sum(c, 5),ts_sum(c, 20), 2)).mul(-1)

        alpha_str = '045'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha045(c, v)

        def alpha047(h, c, v, vwap, adv20):
            """((((rank((1 / close)) * volume) / adv20) * ((high * rank((high - close))) / 
                (ts_sum(high, 5) /5))) - rank((vwap - ts_lag(vwap, 5))))"""

            return c.pow(-1).mul(v).div(adv20).mul(h.mul(h.sub(c).div(ts_mean(h, 5))).sub(ts_delta(vwap, 5)))

        alpha_str = '047'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha047(h, c, v, vwap, adv20)

        def alpha049(c):
            """ts_delta(ts_lag(close, 10), 10).div(10).sub(ts_delta(close, 10).div(10)) < -0.1 * c
                ? 1 
                : -ts_delta(close, 1)"""
            cond = (ts_delta(ts_lag(c, 10), 10).div(10).sub(ts_delta(c, 10).div(10)) >= -0.1 * c)
            return -ts_delta(c, 1).where(cond, 1)

        alpha_str = '049'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha049(c)

        def alpha050(v, vwap):
            """-ts_max(rank(ts_corr(rank(volume), rank(vwap), 5)), 5)"""
            return ts_max(ts_corr(v,vwap, 5), 5).mul(-1)

        alpha_str = '050'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha050(v, vwap)

        def alpha051(c):
            """ts_delta(ts_lag(close, 10), 10).div(10).sub(ts_delta(close, 10).div(10)) < -0.05 * c
                ? 1 
                : -ts_delta(close, 1)"""
            cond = (ts_delta(ts_lag(c, 10), 10).div(10).sub(ts_delta(c, 10).div(10)) >= -0.05 * c)
            return -ts_delta(c, 1).where(cond, 1)

        alpha_str = '051'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha051(c)

        def alpha053(h, l, c):
            """-1 * ts_delta(1 - (high - close) / (close - low), 9)"""
            inner = (c.sub(l)).add(1e-6)
            return ts_delta(h.sub(c).mul(-1).add(1).div(c.sub(l).add(1e-6)), 9).mul(-1)

        alpha_str = '053'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha053(h, l, c)

        def alpha054(o, h, l, c):
            """-(low - close) * power(open, 5) / ((low - high) * power(close, 5))"""
            return l.sub(c).mul(o.pow(5)).mul(-1).div(l.sub(h).replace(0, -0.0001).mul(c ** 5))

        alpha_str = '054'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha054(o, h, l, c)

        def alpha055(h, l, c):
            """(-1 * ts_corr(rank(((close - ts_min(low, 12)) / 
                                    (ts_max(high, 12) - ts_min(low,12)))), 
                            rank(volume), 6))"""

            return ts_corr(c.sub(ts_min(l, 12)).div(ts_max(h, 12).sub(ts_min(l, 12)).replace(0, 1e-6)),v, 6).replace([-np.inf, np.inf], np.nan).mul(-1)

        alpha_str = '055'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha055(h, l, c)

        def alpha060(l, h, c, v):
            """-((2 * scale(rank(((((close - low) - (high - close)) / (high - low)) * volume)))) -scale(rank(ts_argmax(close, 10))))"""
            return c.mul(2).sub(l).sub(h).div(h.sub(l).replace(0, 1e-5)).mul(v).mul(2).sub(ts_argmax(c, 10)).mul(-1)

        alpha_str = '060'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha060(l, h, c, v)

        def alpha061(v, vwap):
            """rank((vwap - ts_min(vwap, 16))) < rank(ts_corr(vwap, adv180, 17))"""

            return vwap.sub(ts_min(vwap, 16)).lt(ts_corr(vwap, ts_mean(v, 180), 18)).astype(int)

        alpha_str = '061'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha061(v, vwap)

        def alpha062(o, h, l, vwap, adv20):
            """((rank(ts_corr(vwap, ts_sum(adv20, 22.4101), 9.91009)) < 
            rank(((rank(open) + rank(open)) < (rank(((high + low) / 2)) + rank(high))))) * -1)"""
            return ts_corr(vwap, ts_sum(adv20, 22), 9).lt(o.mul(2).lt(h.add(l).div(2).add(h))).mul(-1)

        alpha_str = '062'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha062(o, h, l, vwap, adv20)

        def alpha064(o, h, l, v, vwap):
            """((rank(ts_corr(ts_sum(((open * 0.178404) + (low * (1 - 0.178404))), 12.7054),ts_sum(adv120, 12.7054), 16.6208)) <
                rank(ts_delta(((((high + low) / 2) * 0.178404) + (vwap * (1 -0.178404))), 3.69741))) * -1)"""
            w = 0.178404
            return ts_corr(ts_sum(o.mul(w).add(l.mul(1 - w)), 12),ts_sum(ts_mean(v, 120), 12), 16).lt(ts_delta(h.add(l).div(2).mul(w).add(vwap.mul(1 - w)), 3)).mul(-1)

        alpha_str = '064'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha064(o, h, l, v, vwap)

        def alpha065(o, v, vwap):
            """((rank(ts_corr(((open * 0.00817205) + (vwap * (1 - 0.00817205))), 
                                ts_sum(adv60,8.6911), 6.40374)) < 
                rank((open - ts_min(open, 13.635)))) * -1)
            """
            w = 0.00817205
            return ts_corr(o.mul(w).add(vwap.mul(1 - w)),ts_mean(ts_mean(v, 60), 9), 6).lt(o.sub(ts_min(o, 13))).mul(-1)

        alpha_str = '065'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha065(o, v, vwap)

        def alpha068(h, c, v):
            """((ts_rank(ts_corr(rank(high), rank(adv15), 8.91644), 13.9333) <
                rank(ts_delta(((close * 0.518371) + (low * (1 - 0.518371))), 1.06157))) * -1)
            """
            w = 0.518371
            return ts_rank(ts_corr(h, ts_mean(v, 15), 9), 14).lt(ts_delta(c.mul(w).add(l.mul(1 - w)), 1)).mul(-1)

        alpha_str = '068'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha068(l, h, vwap)

        def alpha074(v, vwap):
            """((rank(ts_corr(close, ts_sum(adv30, 37.4843), 15.1365)) <
                rank(ts_corr(rank(((high * 0.0261661) + (vwap * (1 - 0.0261661)))), rank(volume), 11.4791)))* -1)"""

            w = 0.0261661
            return ts_corr(c, ts_mean(ts_mean(v, 30), 37), 15).lt(ts_corr(h.mul(w).add(vwap.mul(1 - w)), v, 11)).mul(-1)

        alpha_str = '074'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha074(v, vwap)

        def alpha075(l, v, vwap):
            """(rank(ts_corr(vwap, volume, 4.24304)) < 
                rank(ts_corr(rank(low), rank(adv50),12.4413)))
            """

            return ts_corr(vwap, v, 4).lt(ts_corr(l, ts_mean(v, 50), 12)).astype(int)

        alpha_str = '075'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha075(l, v, vwap)

        def alpha078(l, v, vwap):
            """(rank(ts_corr(ts_sum(((low * 0.352233) + (vwap * (1 - 0.352233))), 19.7428),
                ts_sum(adv40, 19.7428), 6.83313))^rank(ts_corr(rank(vwap), rank(volume), 5.77492)))"""

            w = 0.352233
            return ts_corr(ts_sum((l.mul(w).add(vwap.mul(1 - w))), 19),ts_sum(ts_mean(v, 40), 19), 6).pow(ts_corr(vwap, v, 5))

        alpha_str = '078'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha078(l, v, vwap)

        def alpha081(v, vwap):
            """-(rank(log(ts_product(rank((rank(ts_corr(vwap, ts_sum(adv10, 49.6054),8.47743))^4)), 14.9655))) <
                rank(ts_corr(rank(vwap), rank(volume), 5.07914)))"""

            return log(ts_product(ts_corr(vwap,ts_sum(ts_mean(v, 10), 50), 8).pow(4), 15)).lt(ts_corr(vwap, v, 5)).mul(-1)

        alpha_str = '081'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha081(v, vwap)

        def alpha083(h, l, c):
            """(rank(ts_lag((high - low) / ts_mean(close, 5), 2)) * rank(rank(volume)) / 
                    (((high - low) / ts_mean(close, 5) / (vwap - close)))
            """
            s = h.sub(l).div(ts_mean(c, 5))

            return ts_lag(s, 2).mul(v).div(s).div(vwap.sub(c).add(1e-3)).replace((np.inf, -np.inf), np.nan)

        alpha_str = '083'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha083(h, l, c)

        def alpha085(l, v):
            """power(rank(ts_corr(((high * 0.876703) + (close * (1 - 0.876703))), adv30,9.61331)),
                rank(ts_corr(ts_rank(((high + low) / 2), 3.70596), 
                            ts_rank(volume, 10.1595),7.11408)))
                            """
            w = 0.876703
            return ts_corr(h.mul(w).add(c.mul(1 - w)), ts_mean(v, 30), 10).pow(ts_corr(ts_rank(h.add(l).div(2), 4),ts_rank(v, 10), 7))

        alpha_str = '085'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha085(l, v)

        def alpha086(c, v, vwap):
            """((ts_rank(ts_corr(close, ts_sum(adv20, 14.7444), 6.00049), 20.4195) < 
                rank(((open + close) - (vwap + open)))) * -1)
            """
            return ts_rank(ts_corr(c, ts_mean(ts_mean(v, 20), 15), 6), 20).lt(c.sub(vwap)).mul(-1)

        alpha_str = '086'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha086(c, v, vwap)

        def alpha094(v, vwap):
            """((rank((vwap - ts_min(vwap, 11.5783)))^ts_rank(ts_corr(ts_rank(vwap,19.6462), 
                ts_rank(adv60, 4.02992), 18.0926), 2.70756)) * -1)
            """

            return vwap.sub(ts_min(vwap, 11)).pow(ts_rank(ts_corr(ts_rank(vwap, 20),ts_rank(ts_mean(v, 60), 4), 18), 2)).mul(-1)

        alpha_str = '094'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha094(v, vwap)

        def alpha095(o, l, v):
            """(rank((open - ts_min(open, 12.4105))) < 
                ts_rank((rank(ts_corr(ts_sum(((high + low)/ 2), 19.1351), ts_sum(adv40, 19.1351), 12.8742))^5), 11.7584))
            """
            
            return o.sub(ts_min(o, 12)).lt(ts_rank(ts_corr(ts_mean(h.add(l).div(2), 19),ts_sum(ts_mean(v, 40), 19), 13).pow(5), 12)).astype(int)

        alpha_str = '095'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha095(o, l, v)

        def alpha099(l, v):
            """((rank(ts_corr(ts_sum(((high + low) / 2), 19.8975), 
                            ts_sum(adv60, 19.8975), 8.8136)) <
                            rank(ts_corr(low, volume, 6.28259))) * -1)"""

            return ts_corr(ts_sum((h.add(l).div(2)), 19),ts_sum(ts_mean(v, 60), 19), 8).mul(-1)

        alpha_str = '099'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha099(l, v)

        def alpha101(o, h, l, c):
            """((close - open) / ((high - low) + .001))"""
            return c.sub(o).div(h.sub(l).add(1e-3))

        alpha_str = '101'
        alpha = int(alpha_str)

        df[f'{alpha:03}'] = alpha101(o, h, l, c)

    if returns_dependent == 'Y':

        data = df[ohlcv].copy()

        adv20 = data.rolling(20).volumeto.mean().reset_index(0, drop=True)
        data = data.assign(adv20=adv20)
        # data.info(null_counts=True)

        o = data.open.copy()
        h = data.high.copy()
        l = data.low.copy()
        c = data.close.copy()
        v = data.volumeto.copy()
        vwap = o.add(h).add(l).add(c).div(4)
        adv20 = v.rolling(20).mean()

        alpha_no = {}
        formulaic_alpha_dict = {}

        # Historical returns
        T = [1, 2, 3, 4, 5, 6, 7, 10, 15, 21, 30, 42, 63, 126, 183, 252, 365]

        for t in T:

            data[f'ret_{t:02}'] = data.close.pct_change(t)

            # returns = input('Enter historical returns window: ')

            # Forward returns
            data['ret_fwd'] = data[[f'ret_{t:02}']].shift(-t)
            # data = data.dropna(subset=['ret_fwd'])

            # # Rename 'ret_XXX' as 'returns'
            # data = data.rename(columns={returns: 'returns'})

            # Determine data inputs
            r = data[f'ret_{t:02}'].copy()

            # Evaluate Alphas
            alphas = data[[f'ret_{t:02}', 'ret_fwd']][:today].dropna().copy()

            # Formulaic Alphas returns dependent
            def alpha001(c, r):
                """(rank(ts_argmax(power(((returns < 0)
                    ? ts_std(returns, 20)
                    : close), 2.), 5)) -0.5)"""
                c[r < 0] = ts_std(r, 20)
                return ts_argmax(power(c, 2), 5).mul(-.5)

            alpha_str = '001'
            alpha = int(alpha_str)

            alphas[f'{alpha:03}'] = alpha001(c, r)

            formulaic_alpha_dict[f'ret_{t:02}'] = alphas

            def alpha008(o, r):
                """-rank(((ts_sum(open, 5) * ts_sum(returns, 5)) - 
                    ts_lag((ts_sum(open, 5) * ts_sum(returns, 5)),10)))
                """
                return (-((ts_sum(o, 5) * ts_sum(r, 5)) -
                                ts_lag((ts_sum(o, 5) * ts_sum(r, 5)), 10)))

            alpha_str = '008'
            alpha = int(alpha_str)

            alphas[f'{alpha:03}'] = alpha008(o, r)

            def alpha014(o, v, r):
                """
                (-rank(ts_delta(returns, 3))) * ts_corr(open, volume, 10))
                """

                alpha = -ts_delta(r, 3).mul(ts_corr(o, v, 10)
                                                .replace([-np.inf,
                                                            np.inf],
                                                        np.nan))
                return alpha

            alpha_str = '014'
            alpha = int(alpha_str)

            alphas[f'{alpha:03}'] = alpha014(o, v, r)

            def alpha019(c, r):
                """((-1 * sign(((close - ts_lag(close, 7)) + ts_delta(close, 7)))) * 
                (1 + rank((1 + ts_sum(returns,250)))))
                """
                return -sign(ts_delta(c, 7) + ts_delta(c, 7)).mul(1 + 1 + ts_sum(r, 250))

            alpha_str = '019'
            alpha = int(alpha_str)

            alphas[f'{alpha:03}'] = alpha019(c, r)

            def alpha025(h, c, r, vwap, adv20):
                """rank((-1 * returns) * adv20 * vwap * (high - close))"""
                return -r.mul(adv20).mul(vwap).mul(h.sub(c))

            alpha_str = '025'
            alpha = int(alpha_str)

            alphas[f'{alpha:03}'] = alpha025(h, c, r, vwap, adv20)

            def alpha029(c, r):
                """(ts_min(ts_product(rank(rank(scale(log(ts_sum(ts_min(rank(rank((-1 * 
                        rank(ts_delta((close - 1),5))))), 2), 1))))), 1), 5)
                    + ts_rank(ts_lag((-1 * returns), 6), 5))
                """
                return ts_min(log(ts_sum(-ts_delta((c - 1), 5), 2)), 5).add(ts_rank(ts_lag((-1 * r), 6), 5))

            alpha_str = '029'
            alpha = int(alpha_str)

            alphas[f'{alpha:03}'] = alpha029(c, r)

            def alpha034(c, r):
                """rank(((1 - rank((ts_std(returns, 2) / ts_std(returns, 5)))) + (1 - rank(ts_delta(close, 1)))))"""

                return (ts_std(r, 2).div(ts_std(r, 5)).replace([-np.inf, np.inf],np.nan).mul(-1).sub(ts_delta(c, 1)).add(2))

            alpha_str = '034'
            alpha = int(alpha_str)

            alphas[f'{alpha:03}'] = alpha034(c, r)

            def alpha035(h, l, c, v, r):
                """((ts_Rank(volume, 32) *
                    (1 - ts_Rank(((close + high) - low), 16))) *
                    (1 -ts_Rank(returns, 32)))
                """
                return ts_rank(v, 32).mul(1 - ts_rank(c.add(h).sub(l), 16)).mul(1 - ts_rank(r, 32))

            alpha_str = '035'
            alpha = int(alpha_str)

            alphas[f'{alpha:03}'] = alpha035(h, l, c, v, r)

            def alpha052(l, v, r):
                """(ts_lag(ts_min(low, 5), 5) - ts_min(low, 5)) * 
                    rank((ts_sum(returns, 240) - ts_sum(returns, 20)) / 220) * 
                    ts_rank(volume, 5)
                """
                return ts_delta(ts_min(l, 5), 5).mul(ts_sum(r, 240).sub(ts_sum(r, 20)).div(220)).mul(ts_rank(v, 5))

            alpha_str = '052'
            alpha = int(alpha_str)

            alphas[f'{alpha:03}'] = alpha052(l, v, r)

    return df