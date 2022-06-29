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
# pop_total = int(pop[pop.id_addiv == '79']['pop'][0])
df['date_report'] = pd.to_datetime(df['date_report'])
no_ecmo_total = df.groupby('date_report')[['no_ecmo_total']].apply(sum)
# no_ecmo_total['no_ecmo_total_rollmean7d'] = (
#     no_ecmo_total.no_ecmo_total.rolling(7).mean()
# )
# no_ecmo_total['no_ecmo_total_cumsum'] = no_ecmo_total.no_ecmo_total.cumsum()
# no_ecmo_total['no_ecmo_total_ppop'] = (
#     no_ecmo_total.no_ecmo_total / pop_total * 100000
# )
# no_ecmo_total['no_ecmo_total_ppop_rollmean7d'] = (
#     no_ecmo_total.no_ecmo_total_ppop.rolling(7).mean()
# )
# no_ecmo_total['no_ecmo_total_ppop_cumsum'] = (
#     no_ecmo_total.no_ecmo_total_ppop.cumsum()
# )
# no_ecmo_total['ct'] = pd.cut(
#     no_ecmo_total.no_ecmo_total_ppop_rollmean7d,
#     bins = [0, 1, 2, 5, 200],
#     labels = ['1', '2', '3', '4'],
#     right = False
# )

# no_ecmo_total['diff'] = no_ecmo_total.no_ecmo_total.diff(1)
# no_ecmo_total['pct_change'] = no_ecmo_total.no_ecmo_total.pct_change(1)
# no_ecmo_total['diff7'] = no_ecmo_total.no_ecmo_total_cumsum.diff(7)
# %% Export
no_ecmo_total.to_csv(
    path.processed / 'metrics-from-treatment-data'/ 'no-ecmo-total.csv',
    sep=','
)



