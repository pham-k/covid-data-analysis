#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 10:06:57 2021

@author: kyo
"""

import pandas as pd

from src.config import path
# %%
no_pcr = pd.read_csv(
    path.processed / 'no-pcr' / 'no-pcr.csv',
    index_col='date_report',
    parse_dates=True
)

no_pcr_pos = pd.read_csv(
    path.processed / 'no-pcr' / 'no-pcr-pos.csv',
    index_col='date_report',
    parse_dates=True
)

no_qtest = pd.read_csv(
    path.processed / 'no-qtest' / 'no-qtest.csv',
    index_col='date_report',
    parse_dates=True
)

no_qtest_pos = pd.read_csv(
    path.processed / 'no-qtest' / 'no-qtest-pos.csv',
    index_col='date_report',
    parse_dates=True
)

# no_pcr_by_adh = pd.read_csv(
#     path.processed / 'no-pcr' / 'no-pcr-by-adh.csv',
#     index_col='date_report',
#     parse_dates=True
# )

# no_pcr_pos_by_adh = pd.read_csv(
#     path.processed / 'no-pcr' / 'no-pcr-pos-by-adh.csv',
#     index_col='date_report',
#     parse_dates=True
# )

# no_qtest_by_adh = pd.read_csv(
#     path.processed / 'no-qtest' / 'no-qtest-by-adh.csv',
#     index_col='date_report',
#     parse_dates=True
# )

# no_qtest_pos_by_adh = pd.read_csv(
#     path.processed / 'no-qtest' / 'no-qtest-pos-by-adh.csv',
#     index_col='date_report',
#     parse_dates=True
# )

# %% tong test
no_test = (
    no_pcr
    .join(no_qtest, how='left')
    .fillna(0)
)

no_test['no_test'] = (
    no_test['no_pcr']
    + no_test['no_qtest'])

no_test.drop(columns=['no_pcr', 'no_qtest'], inplace=True)

# %% tong test duong
no_test_pos = (
    no_pcr_pos
    .join(no_qtest_pos, how='left')
    .fillna(0)
)

no_test_pos['no_test_pos'] = (
    no_test_pos['no_pcr_pos']
    + no_test_pos['no_qtest_pos'])

no_test_pos.drop(columns=['no_pcr_pos', 'no_qtest_pos'], inplace=True)
# %% tong test theo quan huyen
# no_test_by_adh = (
#     no_pcr_by_adh
#     .merge(no_qtest_by_adh, how='left', on=['date', 'addr_dist_home'])
#     .fillna(0)
#     )

# no_test_by_adh['no_test'] = (
#     no_test_by_adh['no_pcr']
#     + no_test_by_adh['no_qtest']
#     )

# no_test_by_adh.drop(columns=['no_pcr', 'no_qtest'], inplace=True)

# %% tong test duong theo quan huyen
# no_test_pos_by_adh = (
#     no_pcr_pos_by_adh
#     .merge(no_qtest_pos_by_adh, how='left', on=['date', 'addr_dist_home'])
#     .fillna(0)
#     )

# no_test_pos_by_adh['no_test_pos'] = (
#     no_test_pos_by_adh['no_pcr_pos']
#     + no_test_pos_by_adh['no_qtest_pos']
#     )

# no_test_pos_by_adh.drop(columns=['no_pcr_pos', 'no_qtest_pos'], inplace=True)
# %%
no_test.to_csv(
    path.processed / 'no-test' / 'no-test.csv')

no_test_pos.to_csv(
    path.processed / 'no-test' / 'no-test-pos.csv')

# no_test_by_adh.to_csv(
#     path.processed / 'no-test' / 'no-test-by-adh.csv')

# no_test_pos_by_adh.to_csv(
#     path.processed / 'no-test' / 'no-test-pos-by-adh.csv')