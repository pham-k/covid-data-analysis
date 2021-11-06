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
    index_col='date_report',
    parse_dates=True
)

no_test_pos = pd.read_csv(
    path.processed / 'no-test' / 'no-test-pos.csv',
    index_col='date_report',
    parse_dates=True
)

no_test_by_adh = pd.read_csv(
    path.processed / 'no-test' / 'no-test-by-adh.csv',
    index_col='date_report',
    parse_dates=True,
    dtype={'addr_dist_home': str,}
)

no_test_pos_by_adh = pd.read_csv(
    path.processed / 'no-test' / 'no-test-pos-by-adh.csv',
    index_col='date_report',
    parse_dates=True,
    dtype={'addr_dist_home': str,}
)

no_test_by_adwh = pd.read_csv(
    path.processed / 'no-test' / 'no-test-by-adwh.csv',
    index_col='date_report',
    parse_dates=True,
    dtype={'addr_dist_home': str, 'addr_ward_home': str}
)

no_test_pos_by_adwh = pd.read_csv(
    path.processed / 'no-test' / 'no-test-pos-by-adwh.csv',
    index_col='date_report',
    parse_dates=True,
    dtype={'addr_dist_home': str, 'addr_ward_home': str}
)

addiv = pd.read_csv(
    path.reference / 'addiv.csv',
    usecols=['id_addiv', 'name_addiv'],
    dtype={'id_addiv': str, 'name_addiv': str})

pop = pd.read_csv(
    path.reference / 'pop_1.csv',
    usecols=['id_addiv', 'pop'],
    dtype={'id_addiv': str, 'pop': int})
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

ct['pop'] = 8993082
ct['pop_risk'] = ct['pop'] - ct['no_test_pos']
ct['inc_per7d'] = (
    ct['no_test_pos_rollingsum7d']
    * 100000
    / ct['pop_risk']).fillna(0)
ct['ct_inc'] = pd.cut(
        ct['inc_per7d'],
        bins = [0, 20, 50, 150, 100000],
        labels = [1, 2, 3, 4],
        right = False)

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

ct['no_test_perpop_per7d'] = (
    ct['no_test_rollingsum7d']
    / 8993082
    * 1000).fillna(0)

ct['public_health_response_capacity'] = pd.cut(
        ct['no_test_perpop_per7d'],
        bins = [0, 1, 4, 1000],
        labels = ['limited', 'moderate', 'adequate'],
        right = False)
# %% ct theo quan huyen
df1 = (
        no_test_by_adh.groupby(['addr_dist_home'])
        ['no_test']
        .rolling(7).sum()
        .to_frame('no_test_rollingsum7d')
        .reset_index()
        .set_index('date_report')
        )

df2 = (
        no_test_pos_by_adh.groupby(['addr_dist_home'])
        ['no_test_pos']
        .rolling(7).sum()
        .to_frame('no_test_pos_rollingsum7d')
        .reset_index()
        .set_index('date_report')
        )

df3 = (
        no_test_by_adh.groupby(['addr_dist_home'])
        ['no_test']
        .rolling(7).mean()
        .to_frame('no_test_rollingmean7d')
        .reset_index()
        .set_index('date_report')
        )

df4 = (
        no_test_pos_by_adh.groupby(['addr_dist_home'])
        ['no_test_pos']
        .rolling(7).sum()
        .to_frame('no_test_pos_rollingmean7d')
        .reset_index()
        .set_index('date_report')
        )

ct_by_adh = (
      no_test_by_adh
      .merge(
          no_test_pos_by_adh,
          how='left',
          on=['date_report', 'addr_dist_home'])
      .merge(
          df1,
          how='left',
          on=['date_report', 'addr_dist_home'])
      .merge(
          df2,
          how='left',
          on=['date_report', 'addr_dist_home'])
      .merge(
          df3,
          how='left',
          on=['date_report', 'addr_dist_home'])
      .merge(
          df4,
          how='left',
          on=['date_report', 'addr_dist_home'])
      )

ct_by_adh = (
    ct_by_adh
    .reset_index()
    .merge(
        pop,
        how='left',
        left_on='addr_dist_home',
        right_on='id_addiv')
    .set_index('date_report'))

ct_by_adh['pop_risk'] = ct_by_adh['pop'] - ct_by_adh['no_test_pos']
ct_by_adh['inc_per7d'] = (
    ct_by_adh['no_test_pos_rollingsum7d']
    * 100000
    / ct_by_adh['pop_risk']).fillna(0)

ct_by_adh['ct_inc'] = pd.cut(
        ct_by_adh['inc_per7d'],
        bins = [0, 20, 50, 150, 100000],
        labels = [1, 2, 3, 4],
        right = False)

ct_by_adh['pct_test_pos_per7d'] = (
    ct_by_adh['no_test_pos_rollingsum7d']
    / ct_by_adh['no_test_rollingsum7d'])

ct_by_adh['pct_test_pos_per7d'] = ct_by_adh['pct_test_pos_per7d'].fillna(0)

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

ct_by_adh['no_test_perpop_per7d'] = (
    ct_by_adh['no_test_rollingsum7d']
    / ct_by_adh['pop']
    * 1000).fillna(0)

ct_by_adh['public_health_response_capacity'] = pd.cut(
        ct_by_adh['no_test_perpop_per7d'],
        bins = [0, 1, 4, 1000],
        labels = ['limited', 'moderate', 'adequate'],
        right = False)

ct_by_adh = (
    ct_by_adh
    .reset_index()
    .merge(
        addiv,
        how='left',
        left_on='addr_dist_home',
        right_on='id_addiv')
    .drop(columns=['addr_dist_home',
                    'id_addiv_y',
                    'id_addiv_x',])
    .rename(columns={'name_addiv': 'addr_dist_home',})
    .set_index('date_report'))

# %% ct theo quan huyen, phuong xa
df1 = (
        no_test_by_adwh.groupby(['addr_dist_home', 'addr_ward_home'])
        ['no_test']
        .rolling(7).sum()
        .to_frame('no_test_rollingsum7d')
        .reset_index()
        .set_index('date_report')
        )

df2 = (
        no_test_pos_by_adwh.groupby(['addr_dist_home', 'addr_ward_home'])
        ['no_test_pos']
        .rolling(7).sum()
        .to_frame('no_test_pos_rollingsum7d')
        .reset_index()
        .set_index('date_report')
        )

df3 = (
        no_test_by_adwh.groupby(['addr_dist_home', 'addr_ward_home'])
        ['no_test']
        .rolling(7).mean()
        .to_frame('no_test_rollingmean7d')
        .reset_index()
        .set_index('date_report')
        )

df4 = (
        no_test_pos_by_adwh.groupby(['addr_dist_home', 'addr_ward_home'])
        ['no_test_pos']
        .rolling(7).sum()
        .to_frame('no_test_pos_rollingmean7d')
        .reset_index()
        .set_index('date_report')
        )

ct_by_adwh = (
      no_test_by_adwh
      .merge(
          no_test_pos_by_adwh,
          how='left',
          on=['date_report', 'addr_dist_home', 'addr_ward_home'])
      .merge(
          df1,
          how='left',
          on=['date_report', 'addr_dist_home', 'addr_ward_home'])
      .merge(
          df2,
          how='left',
          on=['date_report', 'addr_dist_home', 'addr_ward_home'])
      .merge(
          df3,
          how='left',
          on=['date_report', 'addr_dist_home', 'addr_ward_home'])
      .merge(
          df4,
          how='left',
          on=['date_report', 'addr_dist_home', 'addr_ward_home'])
      )

ct_by_adwh = (
    ct_by_adwh
    .reset_index()
    .merge(
        pop,
        how='left',
        left_on='addr_ward_home',
        right_on='id_addiv')
    .set_index('date_report'))

ct_by_adwh['pop_risk'] = ct_by_adwh['pop'] - ct_by_adwh['no_test_pos']
ct_by_adwh['inc_per7d'] = (
    ct_by_adwh['no_test_pos_rollingsum7d']
    * 100000
    / ct_by_adwh['pop_risk']).fillna(0)

ct_by_adwh['ct_inc'] = pd.cut(
        ct_by_adwh['inc_per7d'],
        bins = [0, 20, 50, 150, 100000],
        labels = [1, 2, 3, 4],
        right = False)

ct_by_adwh['pct_test_pos_per7d'] = (
    ct_by_adwh['no_test_pos_rollingsum7d']
    / ct_by_adwh['no_test_rollingsum7d'])

ct_by_adwh['pct_test_pos_per7d'] = ct_by_adwh['pct_test_pos_per7d'].fillna(0)

ct_by_adwh['ct'] = pd.cut(
        ct_by_adwh['pct_test_pos_per7d'],
        bins = [0, 0.02, 0.05, 0.20, 1.01],
        labels = [1, 2, 3, 4],
        right = False)

ct_by_adwh['situational_level'] = pd.cut(
        ct_by_adwh['pct_test_pos_per7d'],
        bins = [0, 0.05, 1.01],
        labels = [2, 3],
        right = False)

ct_by_adwh['no_test_perpop_per7d'] = (
    ct_by_adwh['no_test_rollingsum7d']
    / ct_by_adwh['pop']
    * 1000).fillna(0)

ct_by_adwh['public_health_response_capacity'] = pd.cut(
        ct_by_adwh['no_test_perpop_per7d'],
        bins = [0, 1, 4, 1000],
        labels = ['limited', 'moderate', 'adequate'],
        right = False)

ct_by_adwh = (
    ct_by_adwh
    .reset_index()
    .merge(
        addiv,
        how='left',
        left_on='addr_dist_home',
        right_on='id_addiv')
    .merge(
        addiv,
        how='left',
        left_on='addr_ward_home',
        right_on='id_addiv')
    .drop(columns=['addr_dist_home', 'addr_ward_home',
                    'id_addiv', 'id_addiv_y', 'id_addiv_x'])
    .rename(columns={
        'name_addiv_x': 'addr_dist_home',
        'name_addiv_y': 'addr_ward_home'})
    .set_index('date_report'))

# %%
ct.to_csv(
    path.processed / 'metrics-from-test-data' / 'ct.csv')

ct_by_adh.to_csv(
    path.processed / 'metrics-from-test-data' / 'ct-by-adh.csv')

ct_by_adwh.to_csv(
    path.processed / 'metrics-from-test-data' / 'ct-by-adwh.csv')
