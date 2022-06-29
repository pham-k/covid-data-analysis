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
no_death_children = df.groupby('date_report')[['no_death_children']].apply(sum)
no_death_children['no_death_children_rollmean7d'] = (
    no_death_children.no_death_children.rolling(7).mean()
)
no_death_children['no_death_children_cumsum'] = no_death_children.no_death_children.cumsum()
no_death_children['no_death_children_ppop'] = (
    no_death_children.no_death_children / pop_total * 100000
)
no_death_children['no_death_children_ppop_rollmean7d'] = (
    no_death_children.no_death_children_ppop.rolling(7).mean()
)
no_death_children['no_death_children_ppop_cumsum'] = (
    no_death_children.no_death_children_ppop.cumsum()
)
no_death_children['ct'] = pd.cut(
    no_death_children.no_death_children_ppop_rollmean7d,
    bins = [0, 1, 2, 5, 200],
    labels = ['1', '2', '3', '4'],
    right = False
)

no_death_children['diff'] = no_death_children.no_death_children.diff(1)
no_death_children['pct_change'] = no_death_children.no_death_children.pct_change(1)
no_death_children['diff7'] = no_death_children.no_death_children_cumsum.diff(7)
# %% Export
no_death_children.to_csv(
    path.processed / 'no-death-from-treatment-data'/ 'no-death-children.csv',
    sep=','
)



