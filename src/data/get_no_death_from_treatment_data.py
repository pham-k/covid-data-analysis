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
no_death = df.groupby('date_report')[['no_death']].apply(sum)
no_death['no_death_rollmean7d'] = (
    no_death.no_death.rolling(7).mean()
)
no_death['no_death_cumsum'] = no_death.no_death.cumsum()
no_death['no_death_ppop'] = (
    no_death.no_death / pop_total * 100000
)
no_death['no_death_ppop_rollmean7d'] = (
    no_death.no_death_ppop.rolling(7).mean()
)
no_death['no_death_ppop_cumsum'] = (
    no_death.no_death_ppop.cumsum()
)
no_death['ct'] = pd.cut(
    no_death.no_death_ppop_rollmean7d,
    bins = [0, 1, 2, 5, 200],
    labels = ['1', '2', '3', '4'],
    right = False
)

no_death['diff'] = no_death.no_death.diff(1)
no_death['pct_change'] = no_death.no_death.pct_change(1)
no_death['diff7'] = no_death.no_death_cumsum.diff(7)
# %% Export
no_death.to_csv(
    path.processed / 'no-death-from-treatment-data'/ 'no-death.csv',
    sep=','
)



