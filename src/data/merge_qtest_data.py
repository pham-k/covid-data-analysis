#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 11:52:17 2021

@author: kyo
"""

import pandas as pd
import sys
sys.path.append('/home/kyo/Documents/script/covid-data-analysis/')

from src.config import path

# %%
# rootdir = path.external / 'f0-home-data'
current_date = '2022-06-06'

# %% Read yesterday data
df = pd.read_csv(path.raw / 'qtest-data' / 'merge-2022-05-30.csv')
df['date_sample'] = pd.to_datetime(df.date_sample)
# %% Read today data
df_today = pd.read_excel(
    path.external / 'qtest-data' / 'theo-ngay-lay-mau' / (current_date + '.xlsx'),
    skiprows=3,
    # usecols=range(19),
)

with open(path.reference.joinpath('col-name-qtest.txt'), 'r') as file:
    df_today.columns = file.read().split('\n')

df_today['date_sample'] = pd.to_datetime(df_today.date_sample, format='%H:%M %d-%m-%Y')
df = df.append(df_today)
# %% Merge all
# !Do not uncomment unless you want to merge ALL FILES
 
# df = None

# for subdir, dirs, files in os.walk(rootdir):
#     for file in files:
#         # print(file.replace('.xlsx', ''))
#         date_str = file.replace('.xlsx', '')
#         data = pd.read_excel(
#             rootdir / file,
#             skiprows=3,
#             header=0
#         )
#         data = data.iloc[:-5,:]
#         data['date_report'] = pd.to_datetime(date_str)
#         if df is None:
#             df = data
#         else:
#             df = df.append(data)

# %% Export
# df.to_csv(
#     path.raw / 'qtest-data' / ('merge-' + current_date + '.csv' ),
#     index=False,
#     sep=',')

df.to_csv(
    path.raw / 'qtest-data' / ('merge-' + current_date + '.csv' ),
    index=False,
    sep=',')