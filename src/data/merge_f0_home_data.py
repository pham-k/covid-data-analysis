#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 11:52:17 2021

@author: kyo
"""

import pandas as pd
import os

from src.config import path

# %%
rootdir = path.external / 'f0-home-data'
current_date = '2021-10-09'

# %% Read yesterday data
df = pd.read_csv(path.raw / 'f0-home-data' / 'merge-2021-10-08.csv')

# %% Read today data
df_today = pd.read_excel(
    path.external / 'f0-home-data' / (current_date + '.xlsx'),
    sheet_name='F0 tại nhà',
    skiprows=9,
    usecols=range(19),
    header=None
)

with open(path.reference.joinpath('col-name-f0-home.txt'), 'r') as file:
    df_today.columns = file.read().split('\n')

df_today['date_report'] = pd.to_datetime(current_date)

df = df.append(df_today)
df['date_report'] = pd.to_datetime(df['date_report'])
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
df.to_csv(
    path.raw / 'f0-home-data' / ('merge-' + current_date + '.csv' ),
    index=False,
    sep=',')