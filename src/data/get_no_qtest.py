#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 09:49:20 2021

@author: kyo
"""

import pandas as pd
from datetime import date

from src.config import path
import src.data.util as util

# %%
usecols = ['date_sample', 'reason', 'result', 'addr_dist_home',
           'addr_ward_home']

df = pd.read_csv(
    path.interim / 'qtest-data.csv',
    usecols=usecols,
    dtype={
        'reason': str,
        'result': str,
        'addr_dist_home': str,
    },
    parse_dates=['date_sample']
)


# %% tong test nhanh

data_in_get_no_qtest = (
    df[(~df.reason.str.startswith('KIEM DICH'))
       &(~df.reason.str.contains('XET NGHIEM THEO DOI F0'))]
)

no_qtest = util.get_no(
    data=data_in_get_no_qtest,
    date_col='date_sample',
    no_col='no_qtest'
)

# %% tong test nhanh duong
data_in_get_no_qtest_pos = (
    df[(~df.reason.str.startswith('KIEM DICH')) # remove reason KIEM DICH
       & (~df.reason.str.contains('XET NGHIEM THEO DOI F0'))
       & (df.result == 'DUONG TINH')] 
)
no_qtest_pos = util.get_no(
    data=data_in_get_no_qtest_pos,
    date_col='date_sample',
    no_col='no_qtest_pos')

# %% tong test nhanh theo quan
data_in_get_no_qtest_by_adh = (
    df[(~df.reason.str.startswith('KIEM DICH'))
        & (~df.reason.str.contains('XET NGHIEM THEO DOI F0'))
        & (df.addr_dist_home != 'UNKN')]
)

no_qtest_by_adh = util.get_no_by_group(
    data=data_in_get_no_qtest_by_adh,
    group_col=['addr_dist_home'],
    date_col='date_sample',
    no_col='no_qtest'
)

# %% tong test nhanh duong theo quan
data_in_get_no_qtest_pos_by_adh = (
    df[(~df.reason.str.startswith('KIEM DICH')) # remove reason KIEM DICH
        & (~df.reason.str.contains('XET NGHIEM THEO DOI F0'))
        & (df.result == 'DUONG TINH')
        & (df.addr_dist_home != 'UNKN')] 
)

no_qtest_pos_by_adh = util.get_no_by_group(
    data=data_in_get_no_qtest_pos_by_adh,
    group_col=['addr_dist_home'],
    date_col='date_sample',
    no_col='no_qtest_pos')

# %% tong test nhanh theo quan, phuong
data_in_get_no_qtest_by_adwh = (
    df[(~df.reason.str.startswith('KIEM DICH'))
        & (~df.reason.str.contains('XET NGHIEM THEO DOI F0'))
        & (df.addr_dist_home != 'UNKN')]
)

no_qtest_by_adwh = util.get_no_by_group(
    data=data_in_get_no_qtest_by_adwh,
    group_col=['addr_dist_home', 'addr_ward_home'],
    date_col='date_sample',
    no_col='no_qtest'
)

# %% tong test nhanh duong theo quan, phuong
data_in_get_no_qtest_pos_by_adwh = (
    df[(~df.reason.str.startswith('KIEM DICH')) # remove reason KIEM DICH
        & (~df.reason.str.contains('XET NGHIEM THEO DOI F0'))
        & (df.result == 'DUONG TINH')
        & (df.addr_dist_home != 'UNKN')] 
)

no_qtest_pos_by_adwh = util.get_no_by_group(
    data=data_in_get_no_qtest_pos_by_adwh,
    group_col=['addr_dist_home', 'addr_ward_home'],
    date_col='date_sample',
    no_col='no_qtest_pos')
# %% qtest theo quan huyen
# df2 = df2.set_index('date')

# df2['addr_dist_home'] = df2['addr_dist_home'].apply(util.preprocess_string)
# df2['addr_dist_home'] = df2['addr_dist_home'].apply(util.encode_addr_dist)

# no_qtest_by_adh = df2[['addr_dist_home', 'no_qtest']]
# no_qtest_pos_by_adh = df2[['addr_dist_home', 'no_qtest_pos']]
# %%
no_qtest.to_csv(
    path.processed / 'no-qtest' / 'no-qtest.csv'
)

no_qtest_pos.to_csv(
    path.processed / 'no-qtest' / 'no-qtest-pos.csv'
)

no_qtest_by_adh.to_csv(
    path.processed / 'no-qtest' / 'no-qtest-by-adh.csv'
)

no_qtest_pos_by_adh.to_csv(
    path.processed / 'no-qtest' / 'no-qtest-pos-by-adh.csv'
)

no_qtest_by_adwh.to_csv(
    path.processed / 'no-qtest' / 'no-qtest-by-adwh.csv'
)

no_qtest_pos_by_adwh.to_csv(
    path.processed / 'no-qtest' / 'no-qtest-pos-by-adwh.csv'
)

