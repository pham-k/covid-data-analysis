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
rootdir = path.external / 'treatment-data'
current_date = '2021-10-09'

# %% Read yesterday data
df = pd.read_csv(path.raw / 'treatment-data' / 'merge-2021-10-08.csv')
with open(path.reference.joinpath('col-name-treatment.txt'), 'r') as file:
    df.columns = file.read().split('\n')

df.loc[:,df.columns.str.startswith('no')] = (
    df.loc[:,df.columns.str.startswith('no')].fillna(0))
    
# %% Read today data
df_today = pd.read_excel(
    rootdir / (current_date + '.xlsx'),
    skiprows=3,
    header=0,
    sheet_name=2,
    usecols=range(49)
)

# exclude summary row
# df_today = df_today.iloc[:-5,:]

df_today['date_report'] = pd.to_datetime(current_date)
with open(path.reference.joinpath('col-name-treatment.txt'), 'r') as file:
    df_today.columns = file.read().split('\n')

df_today.loc[:,df_today.columns.str.startswith('no')] = (
    df_today.loc[:,df_today.columns.str.startswith('no')].fillna(0))

    
# df_today['no_out'] = (
#     df_today['no_out_children']
#     + df_today['no_out_pregnant']
#     + df_today['no_out_else']
# )

# df_today['no_out_cs'] = (
#     df_today['no_out_children_cs']
#     + df_today['no_out_pregnant_cs']
#     + df_today['no_out_else_cs']
# )

# df_today['no_death'] = (
#     df_today['no_death_children']
#     + df_today['no_death_pregnant']
#     + df_today['no_death_else']
# )

# df_today['no_death_cs'] = (
#     df_today['no_death_children_cs']
#     + df_today['no_death_pregnant_cs']
#     + df_today['no_death_else_cs']
# )

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
    path.raw / 'treatment-data' / ('merge-' + current_date + '.csv' ),
    index=False,
    sep=',')