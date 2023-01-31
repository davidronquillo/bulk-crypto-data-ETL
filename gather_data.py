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

data_provider = input('Enter name of data provider (eg glassnode, coinmetrics, cryptocompare): ')

if data_provider == 'glassnode':
    manual_auto_fill = input('Would you like to auto or manually enter a metric list, or a list of all metrics? (Enter "a/m/all"): ')
    if manual_auto_fill == 'm':
        exec(open('.../Call_Glassnode.py').read())
    elif manual_auto_fill == 'a':
        exec(open('.../Auto_Glassnode.py').read())
    elif manual_auto_fill == 'all':
        exec(open('.../All_Glassnode.py').read())
elif data_provider == 'coinmetrics':
    manual_auto_fill = input('Would you like to auto or manually enter a metric list, or a list of all metrics? (Enter "a/m/all"): ')
    if manual_auto_fill == 'm':
        exec(open('.../Call_CoinMetrics.py').read())
    elif manual_auto_fill == 'a':
        exec(open('.../Auto_CoinMetrics.py').read())
    elif manual_auto_fill == 'all':
        exec(open('.../All_CoinMetrics.py').read())
elif data_provider == 'cryptocompare':
    data_type = input('list, latest, timeseries: ')
    if data_type == 'list':
        exec(open('.../Call_CryptoCompare_List.py').read())
    elif data_type == 'latest':
        exec(open('.../Call_CryptoCompare_Latest.py').read())
    elif data_type == 'timeseries':
        exec(open('.../Call_CryptoCompare_Time_Series.py').read()) 