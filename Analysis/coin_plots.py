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
from pylab import mpl, plt
plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'

import warnings
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')
idx = pd.IndexSlice

import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots

today = pd.to_datetime("today")

def single_axis(data, metric, start_date=[], end_date=today, window=1, span=1):
    ''' 
        Plots 'metric1' and 'metric2' on same axis
    '''
    #Obtains respective metrics & transforms y2 to SMA or EMA if desired
    if start_date !=[]:
        y1 = data[metric][start_date:end_date].rolling(window=window).mean()
    else:
        y1 = data[metric][:end_date].rolling(window=window).mean()
    y1 = y1.ewm(span=span).mean()

    #Setup data for 'single_axis' plot function in 'Plotting.ipynb'
    if start_date !=[]:
        plot_data = go.Scatter(x=data[start_date:end_date].index, y=y1, name=metric)
    else:
        plot_data = go.Scatter(x=data[:end_date].index, y=y1, name=metric)

    plot_df = plot_data

    #Place menu to toggle between linear and log scale plot
    updatemenus = [
        dict(
            type="buttons",
            direction="right",
            active=0,
            x=1,
            y=1.08,
            buttons=list([
                dict(
                    args=[{'yaxis.type': 'linear'}],
                    label="Linear Scale",
                    method="relayout",
                ),
                dict(
                    args=[{'yaxis.type': 'log'}],
                    label="Log Scale",
                    method="relayout",
                )
            ])
        ),
    ]

    #Plot layout parameters
    layout = go.Layout(
        autosize=False,
        width=1000,
        height=750,
        yaxis=dict(type='log'),
        legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    fig = go.Figure(data=plot_df, layout=layout)

    fig.update_layout(
            updatemenus=updatemenus
        )
    
    # fig.update_xaxes(rangeslider_visible=True)
    fig.show()

def single_axis2(data, metric1, metric2, start_date=[], end_date=today, window2=1, span2=1):
    ''' 
        Plots 'metric1' and 'metric2' on same axis
    '''
    #Obtains respective metrics & transforms y2 to SMA or EMA if desired
    if start_date !=[]:
        y1 = data[metric1][start_date:end_date]
        y2 = data[metric2][start_date:end_date].rolling(window=window2).mean()
    else:
        y1 = data[metric1][:end_date]
        y2 = data[metric2][:end_date].rolling(window=window2).mean()

    y2 = y2.ewm(span=span2).mean()

    #Setup data for 'single_axis' plot function in 'Plotting.ipynb'
    if start_date !=[]:
        plot_data = go.Scatter(x=data[start_date:end_date].index, y=y1, name=metric1)
        plot_data2 = go.Scatter(x=data[start_date:end_date].index, y=y2 , name=metric2)
    else:
        plot_data = go.Scatter(x=data[:end_date].index, y=y1, name=metric1)
        plot_data2 = go.Scatter(x=data[:end_date].index, y=y2 , name=metric2)

    plot_df = [plot_data, plot_data2]

    #Place menu to toggle between linear and log scale plot
    updatemenus = [
        dict(
            type="buttons",
            direction="right",
            active=0,
            x=1,
            y=1.08,
            buttons=list([
                dict(
                    args=[{'yaxis.type': 'linear'}],
                    label="Linear Scale",
                    method="relayout",
                ),
                dict(
                    args=[{'yaxis.type': 'log'}],
                    label="Log Scale",
                    method="relayout",
                )
            ])
        ),
    ]

    #Plot layout parameters
    layout = go.Layout(
        autosize=False,
        width=1000,
        height=750,
        yaxis=dict(type='log'),
        legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    fig = go.Figure(data=plot_df, layout=layout)

    fig.update_layout(
            updatemenus=updatemenus
        )
    
    # fig.update_xaxes(rangeslider_visible=True)
    fig.show()

def secondary_axis(data, metric1, metric2, start_date=[], end_date=today, metric3=1, window2=1, span2=1):
    ''' 
        Plots 'metric1' and 'metric2' on separate axes as well as
        'metric1' on one axis and 'metric2 / metric3' on a second axis
    '''
    #Obtains respective metrics & transforms y2 to SMA or EMA if desired
    if start_date !=[]:
        y1 = data[metric1][start_date:end_date]
        y2 = data[metric2][start_date:end_date].rolling(window=window2).mean()
    else:
        y1 = data[metric1][:end_date]
        y2 = data[metric2][:end_date].rolling(window=window2).mean()
    y2 = y2.ewm(span=span2).mean()
    if metric3 != 1:
        if start_date !=[]:
            y2 = y2 / data[metric3][start_date:end_date]
        else:
            y2 = y2 / data[metric3][:end_date]


    #Place menu to toggle between linear and log scale plot
    updatemenus = [
        dict(
            type="buttons",
            direction="right",
            active=0,
            x=0.93,
            y=1.08,
            buttons=list([
                dict(
                    args=[{'yaxis.type': 'linear'}],
                    label="Linear Scale",
                    method="relayout",
                ),
                dict(
                    args=[{'yaxis.type': 'log'}],
                    label="Log Scale",
                    method="relayout",
                )
            ])
        ),
        dict(
            type="buttons",
            direction="right",
            active=0,
            x=0.22,
            y=1.08,
            buttons=list([
                dict(
                    args=[{'yaxis2.type': 'linear'}],
                    label="Linear Scale",
                    method="relayout",
                ),
                dict(
                    args=[{'yaxis2.type': 'log'}],
                    label="Log Scale",
                    method="relayout",
                )
            ])
        ),
    ]

    # fig = go.Figure(data=data, layout=layout)

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    if start_date !=[]:
        fig.add_trace(
            go.Scatter(x=data[start_date:end_date].index, y=y1, name=metric1),
            secondary_y=False,
        )
    else:
        fig.add_trace(
            go.Scatter(x=data[:end_date].index, y=y1, name=metric1),
            secondary_y=False,
        )

    if metric3 != 1:
        if start_date !=[]:
            fig.add_trace(
                go.Scatter(x=data[start_date:end_date].index, y=y2, name=metric2 + ' / ' + metric3),
                secondary_y=True,
            )
        else:
            fig.add_trace(
                go.Scatter(x=data[:end_date].index, y=y2, name=metric2 + ' / ' + metric3),
                secondary_y=True,
            )
    else:
        if start_date !=[]:
            fig.add_trace(
                go.Scatter(x=data[start_date:end_date].index, y=y2, name=metric2),
                secondary_y=True,
            )
        else:
            fig.add_trace(
                go.Scatter(x=data[:end_date].index, y=y2, name=metric2),
                secondary_y=True,
            )

    #Plot layout parameters
    fig.update_layout(
            updatemenus=updatemenus,
            autosize=True,
            width=1060,
            height=750,
            yaxis=dict(type='log'),
            yaxis2=dict(type='log'),
            legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
            )
        )
    
#   fig.update_xaxes(rangeslider_visible=True)

    fig.show()

def factor_plot(data, factors, start_date=[], end_date=today, log_yn='y', look=[]):
    ''' 
        Plots 'factors' on same axis
    '''
    if start_date != []:
        ax = data[factors][start_date:end_date].plot(figsize=(16, 8), style=look, rot=0)
    else:ax = data[factors][:end_date].plot(figsize=(16, 8), style=look, rot=0)
        
    ax.set_xlabel('');
        
    if log_yn == 'y':
        ax.set_yscale('log')

def two_rows(data, factors1, factors2, start_date=[], end_date=today, log_yn='y'):
    ''' 
        Plots 'factors1' and 'factors2' on different charts
    '''
    fig, axes= plt.subplots(nrows=2, figsize=(15, 8))
    if start_date != []:
        data[factors1][start_date:end_date].plot(ax=axes[0])
        data[factors2][start_date:end_date].plot(ax=axes[1])
    else:
        data[factors1][:end_date].plot(ax=axes[0])
        data[factors2][:end_date].plot(ax=axes[1])
    fig.tight_layout()
    if log_yn == 'y':
        axes[0].set_yscale('log') 

def three_rows(data, factors1, factors2, factors3, start_date=[], end_date=today, log_yn='y'):
    ''' 
        Plots 'factors1', 'factors2', and 'factors3' on different charts
    '''
    fig, axes= plt.subplots(nrows=3, figsize=(15, 10))
    if start_date != []:
        data[factors1][start_date:end_date].plot(ax=axes[0])
        data[factors2][start_date:end_date].plot(ax=axes[1])
        data[factors3][start_date:end_date].plot(ax=axes[2])
    else:
        data[factors1][:end_date].plot(ax=axes[0])
        data[factors2][:end_date].plot(ax=axes[1])
        data[factors3][:end_date].plot(ax=axes[2])
    fig.tight_layout()
    if log_yn == 'y':
        axes[0].set_yscale('log')

def distribution_plots(data, factors, start_date=[], end_date=today):
    ''' 
        Plots distribution plots for list of 'factors'
    '''
    q = .005
    with sns.axes_style('white'):
        fig, axes = plt.subplots(ncols=len(factors), figsize=(14, 4))
        if start_date != []:
            df_ = data[factors][start_date:end_date]
        else:
            df_ = data[factors][:end_date]
        df_ = df_.clip(df_.quantile(q), df_.quantile(1-q), axis=1)
        if len(factors)>1:
            for i, indicator in enumerate(factors):
                    sns.distplot(df_[indicator], ax=axes[i])
        else:
            sns.distplot(df_[factors])
        fig.tight_layout();

def multi_scale(data, factors1, factors2, start_date=[], end_date=today, log_yn='y', look=[]):
    ''' 
        Plots 'factors' and 'factors2' on separate axes
    '''
    factors = factors1 + factors2
    if start_date != []:
        ax = data[factors][start_date:end_date].plot(figsize=(14, 7),
                                            secondary_y=factors2,
                                            style=look,
                                            rot=0)
    else:
        ax = data[factors][:end_date].plot(figsize=(14, 7),
                                            secondary_y=factors2,
                                            style=look,
                                            rot=0)
    ax.set_xlabel('')
    if log_yn == 'y':
        ax.set_yscale('log')
    plt.tight_layout()

def ratio_plot(data, factors, ratio, start_date=[], end_date=today, log_yn='y', look=[]):
    ''' 
        Plots ratio of 'factors' on same axis
    '''
    fig, ax1 = plt.subplots(figsize=(14, 7))

    color = 'tab:blue'
    # ax1.set_xlabel('time (s)')
    ax1.set_ylabel(factors)
    if start_date != []:
        ax1.plot(data[factors][start_date:end_date], color=color)
        # ax1.tick_params(axis='y')
    else:
        ax1.plot(data[factors][:end_date], color=color)
        # ax1.tick_params(axis='y')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:orange'
    ax2.set_ylabel(ratio[0] + ' / ' + ratio[1])  # we already handled the x-label with ax1
    if start_date != []:
        ax2.plot(data[ratio[0]][start_date:end_date]/data[ratio[1]][start_date:end_date], \
                color=color)
        # ax2.tick_params(axis='y')
    else:
        ax2.plot(data[ratio[0]][:end_date]/data[ratio[1]][start_date:end_date], \
                color=color)
        # ax2.tick_params(axis='y')

    if log_yn == 'y':
        ax1.set_yscale('log')

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.show
    
    
    # ax = (data[factors[0]][start_date:end_date]/data[factors[1]][start_date:end_date]) \
    #         .plot(figsize=(16, 8), style=look, rot=0)
    # ax.set_xlabel('');
    # if log_yn == 'y':
    #     ax.set_yscale('log')
