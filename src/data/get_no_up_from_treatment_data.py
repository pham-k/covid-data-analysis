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
no_up = df.groupby('date_report')[['no_up']].apply(sum)
no_up['no_up_rollmean7d'] = (
    no_up.no_up.rolling(7).mean()
)
no_up['no_up_cumsum'] = no_up.no_up.cumsum()
# no_up['no_up_ppop'] = (
#     no_up.no_up / pop_total * 100000
# )
# no_up['no_up_ppop_rollmean7d'] = (
#     no_up.no_up_ppop.rolling(7).mean()
# )
# no_up['no_up_ppop_cumsum'] = (
#     no_up.no_up_ppop.cumsum()
# )
# no_up['ct'] = pd.cut(
#     no_up.no_up_ppop_rollmean7d,
#     bins = [0, 1, 2, 5, 200],
#     labels = ['1', '2', '3', '4'],
#     right = False
# )

no_up['diff'] = no_up.no_up.diff(1)
no_up['pct_change'] = no_up.no_up.pct_change(1)
no_up['diff7'] = no_up.no_up_cumsum.diff(7)
# %% Export
no_up.to_csv(
    path.processed / 'no-up-from-treatment-data'/ 'no-up.csv',
    sep=','
)



