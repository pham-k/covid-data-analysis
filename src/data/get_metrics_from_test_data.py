#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 11:23:40 2021

@author: kyo
"""

import pandas as pd
from src.config import path

# %%
no_test = pd.read_csv(
    path.processed / 'no-test' / 'no-test.csv',
    index_col='date',
    parse_dates=True
)

no_test_pos = pd.read_csv(
    path.processed / 'no-test' / 'no-test-pos.csv',
    index_col='date',
    parse_dates=True
)

no_test_by_adh = pd.read_csv(
    path.processed / 'no-test' / 'no-test-by-adh.csv',
    index_col='date',
    parse_dates=True
)

no_test_pos_by_adh = pd.read_csv(
    path.processed / 'no-test' / 'no-test-pos-by-adh.csv',
    index_col='date',
    parse_dates=True
)

# %% ct toan tp
ct = (
      no_test
      .join(no_test_pos, how='left'))

ct['no_test_rollingsum7d'] = (
    ct['no_test'].rolling(7).sum())
ct['no_test_rollingmean7d'] = (
    ct['no_test'].rolling(7).mean())
ct['no_test_pos_rollingsum7d'] = (
    ct['no_test_pos'].rolling(7).sum())
ct['no_test_pos_rollingmean7d'] = (
    ct['no_test_pos'].rolling(7).mean())
ct['pct_test_pos_per7d'] = (
    ct['no_test_pos_rollingsum7d']
    / ct['no_test_rollingsum7d'])
ct['ct'] = pd.cut(
        ct['pct_test_pos_per7d'],
        bins = [0, 0.02, 0.05, 0.20, 1.01],
        labels = [1, 2, 3, 4],
        right = False)

ct['situational_level'] = pd.cut(
        ct['pct_test_pos_per7d'],
        bins = [0, 0.05, 1.01],
        labels = [2, 3],
        right = False)

# %% ct theo quan huyen
df1 = (
       no_test_by_adh.groupby(['addr_dist_home'])
       ['no_test']
       .rolling(7).sum()
       .to_frame('no_test_rollingsum7d')
       .reset_index()
       .set_index('date')
       )

df2 = (
       no_test_pos_by_adh.groupby(['addr_dist_home'])
       ['no_test_pos']
       .rolling(7).sum()
       .to_frame('no_test_pos_rollingsum7d')
       .reset_index()
       .set_index('date')
       )

df3 = (
       no_test_by_adh.groupby(['addr_dist_home'])
       ['no_test']
       .rolling(7).mean()
       .to_frame('no_test_rollingmean7d')
       .reset_index()
       .set_index('date')
       )

df4 = (
       no_test_pos_by_adh.groupby(['addr_dist_home'])
       ['no_test_pos']
       .rolling(7).sum()
       .to_frame('no_test_pos_rollingmean7d')
       .reset_index()
       .set_index('date')
       )

ct_by_adh = (
      no_test_by_adh
      .merge(no_test_pos_by_adh, how='left', on=['date', 'addr_dist_home'])
      .merge(df1, how='left', on=['date', 'addr_dist_home'])
      .merge(df2, how='left', on=['date', 'addr_dist_home'])
      .merge(df3, how='left', on=['date', 'addr_dist_home'])
      .merge(df4, how='left', on=['date', 'addr_dist_home'])
      )

ct_by_adh['pct_test_pos_per7d'] = (
    ct_by_adh['no_test_pos_rollingsum7d']
    / ct_by_adh['no_test_rollingsum7d'])

ct_by_adh['ct'] = pd.cut(
        ct_by_adh['pct_test_pos_per7d'],
        bins = [0, 0.02, 0.05, 0.20, 1.01],
        labels = [1, 2, 3, 4],
        right = False)

ct_by_adh['situational_level'] = pd.cut(
        ct_by_adh['pct_test_pos_per7d'],
        bins = [0, 0.05, 1.01],
        labels = [2, 3],
        right = False)
# %%
ct.to_csv(
    path.processed / 'metrics-from-test-data' / 'ct.csv')

ct_by_adh.to_csv(
    path.processed / 'metrics-from-test-data' / 'ct-by-adh.csv')
