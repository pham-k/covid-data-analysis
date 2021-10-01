#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 14:17:15 2021

@author: kyo
"""

import pandas as pd
import numpy as np
from src.config import path
import util

# %%
df = pd.read_csv(
    path.interim / 'vaccine-data.csv')
pop = pd.read_csv(path.reference / 'pop_1.csv', sep=',', dtype={'id_addiv': 'str'})
pop_total = int(pop[pop.id_addiv == '79']['pop'][0])
# %%
df['date_report'] = pd.to_datetime(df['date_report'])
idx = pd.date_range(df['date_report'].min(), df['date_report'].max())

shot_1 = (
    df.groupby('date_report')['shot_1_cs']
    .apply(lambda x: sum(x))
    .to_frame('shot_1_cs')
    .reindex(idx)
    .fillna(method='ffill')
)

shot_1['shot_1_coverage'] = shot_1['shot_1_cs'] / pop_total

shot_2 = (
    df.groupby('date_report')['shot_2_cs']
    .apply(lambda x: sum(x))
    .to_frame('shot_2_cs')
    .reindex(idx)
    .fillna(method='ffill')
)

shot_2['shot_2_coverage'] = shot_2['shot_2_cs'] / pop_total

shot_1 = (
    shot_1.reset_index()
    .rename(columns={'index': 'date_report'})
    )
shot_2 = (
    shot_2.reset_index()
    .rename(columns={'index': 'date_report'})
    )
# %%
shot_1.to_csv(
    path.processed / 'from-vaccine-data' / 'shot-1.csv',
    index=False)

shot_2.to_csv(
    path.processed / 'from-vaccine-data' / 'shot-2.csv',
    index=False)


