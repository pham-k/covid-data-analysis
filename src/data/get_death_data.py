#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 13:23:50 2021

@author: kyo
"""

import pandas as pd
import pathlib
# from config import path
import config.path as path
from data import util

# %%
df = pd.read_excel(
    path.external / 'death-data' / 'death-data-2021-08-21.xlsx',
    skiprows=2
    # sep=';'
)
pop = pd.read_csv(path.reference / 'pop_1.csv', sep=',', dtype={'id_addiv': 'str'})
addiv = pd.read_csv(path.reference / 'addiv.csv', sep=',', dtype={'id_addiv': 'str', 'of_addiv': 'str'})
# %%
with open(path.reference.joinpath('col-name-death-data.txt'), 'r') as file:
    df.columns = file.read().split('\n')


# %%
df['yob'] = pd.to_numeric(df.yob, errors='coerce')
df['sex'] = df.sex.astype('str').apply(util.preprocess_string)
df['addr_dist_home'] = df.addr_dist_home.astype('str').apply(util.preprocess_string)
df['addr_ward_home'] = df.addr_ward_home.astype('str').apply(util.preprocess_string)
df['addr_ward_home'] = df.addr_ward_home.astype('str').apply(util.preprocess_addr_ward)
df['status'] = df.status.astype('str').apply(util.preprocess_string)
df['level'] = df.level.astype('str').apply(util.preprocess_string)
df['hospital'] = df.hospital.astype('str').apply(util.preprocess_string)
df['diagnosis'] = df.diagnosis.astype('str').apply(util.preprocess_string)
df['from'] = df['from'].astype('str').apply(util.preprocess_string)
df['test_result'] = df.test_result.astype('str').apply(util.preprocess_string)
df['date_report'] = pd.to_datetime(df.date_report.dt.date)

# fix district name
df['adh'] = df['addr_dist_home']
df.loc[df.addr_dist_home == 'QUAN 1', 'adh'] = 'QUAN 01'
df.loc[df.addr_dist_home == 'QUAN 2', 'adh'] = 'QUAN 02'
df.loc[df.addr_dist_home == 'QUAN 3', 'adh'] = 'QUAN 03'
df.loc[df.addr_dist_home == 'QUAN 4', 'adh'] = 'QUAN 04'
df.loc[df.addr_dist_home == 'QUAN 5', 'adh'] = 'QUAN 05'
df.loc[df.addr_dist_home == 'QUAN 6', 'adh'] = 'QUAN 06'
df.loc[df.addr_dist_home == 'QUAN 7', 'adh'] = 'QUAN 07'
df.loc[df.addr_dist_home == 'QUAN 8', 'adh'] = 'QUAN 08'
df.loc[df.addr_dist_home == 'QUAN 9', 'adh'] = 'QUAN 09'

# Drop old col and replace by fixed col
df = df.drop(columns=['addr_dist_home'])
df = df.rename(columns={'adh': 'addr_dist_home'})

df['addr_dist_home'] = df['addr_dist_home'].apply(util.encode_addr_dist)


# combine name of dist and ward
df['dw'] = df.addr_dist_home + ' ' + df.addr_ward_home

df = df.merge(addiv[['dw', 'id_addiv']], how = 'left', on= 'dw' )
df['addr_ward_home'] = df.id_addiv
df = df.drop(columns=['id_addiv', 'dw'])
# %%
df.to_csv(path.interim.joinpath('death-data.csv'), index=False, sep=',')




