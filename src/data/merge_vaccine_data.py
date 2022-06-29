#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 13:38:32 2021

@author: kyo
"""

# %%
import pandas as pd
import os

from src.config import path
# %%
rootdir = path.external / 'vaccine-data'
current_date = '2021-10-04'

# %%
df = pd.read_csv(
    path.raw / 'vaccine-data' / 'merge-2021-10-03.csv'
)

df['date_report'] = pd.to_datetime(df['date_report'])

# with open(path.reference.joinpath('col-name-vaccine.txt'), 'r') as file:
#     df.columns = file.read().split('\n')

# %%
df_today = pd.read_excel(
    path.external / 'vaccine-data' / (current_date + '.xlsx'),
    sheet_name='vaccine'
)

with open(path.reference.joinpath('col-name-vaccine.txt'), 'r') as file:
    df_today.columns = file.read().split('\n')

df_today['date_report'] = pd.to_datetime(current_date)


df = df.append(df_today)
# %%
df.to_csv(
    path.raw / 'vaccine-data' / ('merge-' + current_date + '.csv' ),
    index=False,
    sep=',')
    
    
    
    
    