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

#Link to 'Glassnode_Metrics.xlsx' info excel file
excel_link = '.../Glassnode_Metrics.xlsx'

#create df's from sheets 'T1' & 'T2' of 'Glassnode_Metrics.xlsx' file
glassnode_T1 = pd.read_excel(excel_link, sheet_name='T1')
glassnode_T2 = pd.read_excel(excel_link, sheet_name='T2')

#concatenate df's
df = pd.concat([glassnode_T1, glassnode_T2])

#get 'data_category' names for given 'metric_id' values
data_categories = list(map(lambda x: df[df.metric_id==x].data_category.values[0], metric_ids))