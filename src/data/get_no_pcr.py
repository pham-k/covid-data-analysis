#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 15:33:39 2021

@author: kyo
"""

# -*- coding: utf-8 -*-

import pandas as pd
from config import path
import util

# %% Import
df = (pd.read_csv(
    path.interim / 'pcr-data.csv',
    sep=',',
    dtype={'addr_dist_home': 'str', 'addr_ward_home': 'str'})
      # [['date_sample', 'yob', 'sex', 'addr_dist_home']]
)

pop = pd.read_csv(path.reference / 'pop_1.csv', sep=',', dtype={'id_addiv': 'str'})
addiv = pd.read_csv(path.reference / 'addiv.csv', sep=',', dtype={'id_addiv': 'str', 'of_addiv': 'str'})


# %% Process
# Get age group
df = df.assign(
    date_sample = pd.to_datetime(df.date_sample),
    age = 2021 - df.yob.astype('float')
)

df['age_group'] = pd.cut(
    df.age,
    bins = [0, 17, 45, 65, 200],
    labels = ['0 - 16', '17 - 44', '45 - 64', '> 65'],
    right = False
)

df['age_group_children'] = pd.cut(
    df.age,
    bins = [0, 6, 12, 17, 200],
    labels = ['0 - 5', '6 - 11', '12 - 16', '> 16'],
    right = False
)

df = df[(df.date_sample >= '2021-05-27')]
df = df.rename(columns={'date_sample': 'date_report'})

# duong tinh mau gop
# loai ra vi mau gop (+) duoc lam pcr nen se bi tinh 2 lan
df['positive_group_sample'] = ((df.result == 'DUONG TINH') 
                                & (df.sample_type == 'MAU GOP'))
# %%
# baz = df[(df.result == 'DUONG TINH')]
# foo = df[(df.result == 'DUONG TINH') 
#          & (df.sample_type != 'MAU GOP')]
# %% tong pcr

data_in_get_no_pcr = (
    df[(~df.reason.str.startswith('KIEM DICH'))
       &(~df.reason.str.contains('THEO DOI'))  # loai li do theo doi
       & (df.positive_group_sample == False)] 
)

no_pcr = util.get_no(
    data=data_in_get_no_pcr,
    date_col='date_report',
    no_col='no_pcr'
)
# %% 
# data_in_1 = df[
#     df.reason.str.contains('TEST NHANH')
# ]

# no_test_1 = util.get_no_event(
#     data=data_in_1,
#     pop=pop_total,
#     date_col='date_report',
#     no_col='no_test',
#     rolling=7)

# %% Get no_test: tong test nhanh duong co PCR duong
# pop_total = int(pop[pop.id_addiv == '79']['pop'][0])
# data_in_2 = df[
#     df.reason.str.contains('TEST NHANH')
#     & df.diag_proc.str.contains('PCR')
#     & df.result.str.contains('DUONG TINH')
# ]

# no_test_2 = util.get_no_event(
#     data=data_in_2,
#     pop=pop_total,
#     date_col='date_report',
#     no_col='no_test',
#     rolling=7)

# %% Tinh ty le PCR duong trong test nhanh duong
# no_test_3 = no_test_1.join(
#     no_test_2,
#     how = 'left',
#     lsuffix = '_1',
#     rsuffix = '_2'
# )

# no_test_3['pct'] = no_test_3.no_test_2 / no_test_3.no_test_1

# %% tong pcr duong
data_in_get_no_pcr_pos = (
    df[(~df.reason.str.startswith('KIEM DICH')) # remove reason KIEM DICH
       & (~df.reason.str.contains('THEO DOI'))
       & (df.result == 'DUONG TINH')] 
)
no_pcr_pos = util.get_no(
    data=data_in_get_no_pcr_pos,
    date_col='date_report',
    no_col='no_pcr_pos')

# %% Get no test by ward
# data_in_get_no_test_by_group_awh = (
#     df[(~df.reason.str.startswith('KIEM DICH'))
#        & (~df.reason.str.contains('THEO DOI'))] # remove reason KIEM DICH
#     .query('addr_prov_home == "79"')
#     [df.addr_ward_home.notna()]
# )

# no_test_by_awh = util.get_no_event_by_group(
#     data_in_get_no_test_by_group_awh,
#     date_col = 'date_report',
#     no_col = 'no_test',
#     rolling = 7,
#     getname = False,
#     pop=pop,
#     addiv=addiv,
#     group_col = 'addr_ward_home')

# %% Get no positive by ward
# data_in_get_no_positive_by_group_awh = (
#     df[(~df.reason.str.startswith('KIEM DICH')) # remove reason KIEM DICH
#        & (~df.reason.str.contains('THEO DOI'))
#        & (df.result == 'DUONG TINH')]
#     .query('addr_prov_home == "79"')
#     [df.addr_ward_home.notna()]
# )

# no_positive_by_awh = get_no_event_by_group(
#     data_in_get_no_positive_by_group_awh,
#     date_col = 'date_report',
#     no_col = 'no_positive',
#     rolling = 7,
#     getname = False,
#     available_pop = True,
#     group_col = 'addr_ward_home')

# %% tong pcr theo quan huyen
data_in_get_no_pcr_by_adh = (
    df[(~df.reason.str.startswith('KIEM DICH'))
       & (~df.reason.str.contains('THEO DOI')) # remove reason KIEM DICH
       & (df.addr_prov_home == '79')
       & (df.addr_dist_home != 'UNKN')
       & (df.positive_group_sample == False)]
)

no_pcr_by_adh = util.get_no_by_group(
    data_in_get_no_pcr_by_adh,
    group_col = ['addr_dist_home'],
    date_col = 'date_report',
    no_col = 'no_pcr',
)

# %% tong pcr duong theo quan huyen
data_in_get_no_pcr_pos_by_adh = (
    df[(~df.reason.str.startswith('KIEM DICH')) # remove reason KIEM DICH
       & (~df.reason.str.contains('THEO DOI'))
       & (df.result == 'DUONG TINH')
       & (df.addr_prov_home == '79')
       & (df.addr_dist_home != 'UNKN')]
    # [df.addr_dist_home.notna()]
)

no_pcr_pos_by_adh = util.get_no_by_group(
    data_in_get_no_pcr_pos_by_adh,
    group_col = ['addr_dist_home'],
    date_col = 'date_report',
    no_col = 'no_pcr_pos',
)

# %% tong pcr theo nhom tuoi tre em
data_in_get_no_test_by_group_agc = (
    df[(~df.reason.str.startswith('KIEM DICH'))
        & (~df.reason.str.contains('THEO DOI'))
        & (df.addr_prov_home == '79')
        & (df.age_group_children != '> 16')
        & (df.age_group_children.notna())] 
)

no_pcr_by_agc = util.get_no_by_group(
    data_in_get_no_test_by_group_agc,
    group_col =['age_group_children'],
    date_col = 'date_report',
    no_col = 'no_pcr',
)

# %% tong pcr duong theo nhom tuoi tre em
data_in_get_no_test_by_group_agc = (
    df[(~df.reason.str.startswith('KIEM DICH'))
        & (~df.reason.str.contains('THEO DOI'))
        & (df.result == 'DUONG TINH')
        & (df.addr_prov_home == '79')
        & (df.age_group_children != '> 16')
        & (df.age_group_children.notna())] 
)

no_pcr_pos_by_agc = util.get_no_by_group(
    data_in_get_no_test_by_group_agc,
    group_col =['age_group_children'],
    date_col = 'date_report',
    no_col = 'no_pcr_pos',
)
# %% Get no test by age group
# data_in_get_no_test_by_group_ag = (
#     df[(~df.reason.str.startswith('KIEM DICH'))
#        & (~df.reason.str.contains('THEO DOI'))] # remove reason KIEM DICH
#     .query('addr_prov_home == "79"')
#     [df.age_group.notna()]
# )

# no_test_by_ag = get_no_event_by_group(
#     data_in_get_no_test_by_group_ag,
#     date_col = 'date_report',
#     no_col = 'no_test',
#     rolling = 7,
#     getname = False,
#     available_pop = False,
#     group_col = 'age_group')

# %% Get no positive by age_group
# data_in_get_no_positive_by_group_ag = (
#     df[(~df.reason.str.startswith('KIEM DICH')) # remove reason KIEM DICH
#        & (~df.reason.str.contains('THEO DOI'))
#        & (df.result == 'DUONG TINH')]
#     .query('addr_prov_home == "79"')
#     [df.age_group.notna()]
# )

# no_positive_by_ag = get_no_event_by_group(
#     data_in_get_no_positive_by_group_ag,
#     date_col = 'date_report',
#     no_col = 'no_positive',
#     rolling = 7,
#     getname = False,
#     available_pop = False,
#     group_col = 'age_group')

# %% Get no test by sex
# data_in_get_no_test_by_group_sex = (
#     df[(~df.reason.str.startswith('KIEM DICH'))
#        & (~df.reason.str.contains('THEO DOI'))] # remove reason KIEM DICH
#     .query('addr_prov_home == "79"')
#     [df.sex != 'NAN']
# )

# no_test_by_sex = get_no_event_by_group(
#     data_in_get_no_test_by_group_sex,
#     date_col = 'date_report',
#     no_col = 'no_test',
#     rolling = 7,
#     getname = False,
#     available_pop = False,
#     group_col = 'sex')

# %% Get no positive by age_group
# data_in_get_no_positive_by_group_sex = (
#     df[(~df.reason.str.startswith('KIEM DICH')) # remove reason KIEM DICH
#        & (~df.reason.str.contains('THEO DOI'))
#        & (df.result == 'DUONG TINH')]
#     .query('addr_prov_home == "79"')
#     [df.sex != 'NAN']
# )

# no_positive_by_sex = get_no_event_by_group(
#     data_in_get_no_positive_by_group_sex,
#     date_col = 'date_report',
#     no_col = 'no_positive',
#     rolling = 7,
#     getname = False,
#     available_pop = False,
#     group_col = 'sex')

# %% Export
no_pcr.to_csv(
    path.processed / 'no-pcr' / 'no-pcr.csv',
)

# no_test_3.to_csv(path.processed / 'no-test' / 'no-test-3.csv')

no_pcr_by_adh.to_csv(
    path.processed / 'no-pcr' / 'no-pcr-by-adh.csv',
)

no_pcr_by_agc.to_csv(
    path.processed / 'no-pcr' / 'no-pcr-by-agc.csv',
)

# no_test_by_awh.to_csv(
#     path.processed / 'no-test-by-group' / 'no-test-by-awh.csv',
#     index=False)

# no_test_by_ag.to_csv(
#     path.processed / 'no-test-by-group' / 'no-test-by-ag.csv',
#     index=False)

# no_test_by_sex.to_csv(
#     path.processed / 'no-test-by-group' / 'no-test-by-sex.csv',
#     index=False)

no_pcr_pos.to_csv(
    path.processed / 'no-pcr' / 'no-pcr-pos.csv'
)

no_pcr_pos_by_adh.to_csv(
    path.processed / 'no-pcr' / 'no-pcr-pos-by-adh.csv',
)

no_pcr_pos_by_agc.to_csv(
    path.processed / 'no-pcr' / 'no-pcr-pos-by-agc.csv',
)

# no_positive_by_awh.to_csv(
#     path.processed / 'no-positive-by-group' / 'no-positive-by-awh.csv',
#     index=False)

# no_positive_by_ag.to_csv(
#     path.processed / 'no-positive-by-group' / 'no-positive-by-ag.csv',
#     index=False)

# no_positive_by_sex.to_csv(
#     path.processed / 'no-positive-by-group' / 'no-positive-by-sex.csv',
#     index=False)

