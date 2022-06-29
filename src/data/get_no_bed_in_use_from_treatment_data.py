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
# %% Get no bed_in_use
pop_total = int(pop[pop.id_addiv == '79']['pop'][0])
df['date_report'] = pd.to_datetime(df['date_report'])
no_bed_in_use = (
    df.groupby('date_report')[['no_positive']]
    .apply(sum)
    .rename(columns={'no_positive': 'no_bed_in_use'})
)
# no_bed_in_use['no_bed_in_use_rollmean7d'] = (
#     no_bed_in_use.no_bed_in_use.rolling(7).mean()
# )
# no_bed_in_use['no_bed_in_use_cumsum'] = no_bed_in_use.no_bed_in_use.cumsum()
# no_bed_in_use['no_bed_in_use_ppop'] = (
#     no_bed_in_use.no_bed_in_use / pop_total * 100000
# )
# no_bed_in_use['no_bed_in_use_ppop_rollmean7d'] = (
#     no_bed_in_use.no_bed_in_use_ppop.rolling(7).mean()
# )
# no_bed_in_use['no_bed_in_use_ppop_cumsum'] = (
#     no_bed_in_use.no_bed_in_use_ppop.cumsum()
# )
# no_bed_in_use['ct'] = pd.cut(
#     no_bed_in_use.no_bed_in_use_ppop_rollmean7d,
#     bins = [0, 1, 2, 5, 200],
#     labels = ['1', '2', '3', '4'],
#     right = False
# )

# no_bed_in_use['diff'] = no_bed_in_use.no_bed_in_use.diff(1)
# no_bed_in_use['pct_change'] = no_bed_in_use.no_bed_in_use.pct_change(1)
# no_bed_in_use['diff7'] = no_bed_in_use.no_bed_in_use_cumsum.diff(7)
# %% Export
no_bed_in_use.to_csv(
    path.processed / 'metrics-from-treatment-data'/ 'no-bed-in-use.csv',
    sep=','
)



