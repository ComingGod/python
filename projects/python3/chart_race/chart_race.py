# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:     chart_race
   Description: 
   Author:        nxa28190
   Date:          10/12/2020
-------------------------------------------------
   Change Activity:
                  10/12/2020:
-------------------------------------------------
"""
__author__ = 'Richard Xiong'

import bar_chart_race as bcr
import pandas as pd


data = r'D:\Git_Hub\python\projects\python3\chart_race\data\house_sales.csv'
# df = bcr.load_dataset('baseball')
# bcr.bar_chart_race(
#         df=df,
#         filename='2.gif')

# df = pd.read_csv(data, encoding='utf-8')
# print(df)
# df_result = pd.pivot_table(df)
# bcr.bar_chart_race(df, '2.gif', title='test 2')

# index_dict = {'covid19_tutorial': 'date',
#               'covid19': 'date',
#               'urban_pop': 'year',
#               'baseball': None}
# index_col = index_dict['covid19_tutorial']
# parse_dates = [index_col] if index_col else None
# # return pd.read_csv(url, index_col=index_col, parse_dates=parse_dates)
#
# print('index_col:{} \n'.format(index_col))
# print('parse_data: \n {} \n'.format(parse_dates))
#
# df = pd.read_csv(data,  index_col=index_col, parse_dates=parse_dates)
# bcr.bar_chart_race(df, '2.gif', title='test 2')

# parse the data from CSV file
df = pd.read_csv(data,  index_col='date', encoding='utf-8')
print(df)
# generate the chart race gif
bcr.bar_chart_race(df, 'House_sales.gif', title='Duhui House Sales', orientation='v')
