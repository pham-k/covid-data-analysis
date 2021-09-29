#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 14:20:15 2021

@author: kyo
"""

import pandas as pd
from config import path
import util

# %% Import
df = pd.read_csv(
    path.interim / 'treatment-data.csv',
    sep=','
)

pop = pd.read_csv(
    path.reference / 'pop_1.csv',
    sep=',',
    dtype={'id_addiv': 'str'}
)
# %% Get no death
pop_total = int(pop[pop.id_addiv == '79']['pop'][0])
df['date_report'] = pd.to_datetime(df['date_report'])
no_in = df.groupby('date_report')[['no_in']].apply(sum)
no_in['no_in_rollmean7d'] = (
    no_in.no_in.rolling(7).mean()
)
no_in['no_in_cumsum'] = no_in.no_in.cumsum()
no_in['no_in_ppop'] = (
    no_in.no_in / pop_total * 100000
)
no_in['no_in_ppop_rollmean7d'] = (
    no_in.no_in_ppop.rolling(7).mean()
)
no_in['no_in_ppop_cumsum'] = (
    no_in.no_in_ppop.cumsum()
)
no_in['ct'] = pd.cut(
    no_in.no_in_ppop_rollmean7d,
    bins = [0, 1, 2, 5, 200],
    labels = ['1', '2', '3', '4'],
    right = False
)

no_in['diff'] = no_in.no_in.diff(1)
no_in['pct_change'] = no_in.no_in.pct_change(1)
no_in['diff7'] = no_in.no_in_cumsum.diff(7)
# %% Export
no_in.to_csv(
    path.processed / 'no-in-from-treatment-data'/ 'no-in.csv',
    sep=','
)



