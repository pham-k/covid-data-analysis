#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 14:01:22 2021

@author: kyo
"""

import pandas as pd
from src.config import path
import util
from datetime import date

# %%
raw = pd.read_csv(
    path.raw / 'vaccine-data' / 'merge-2021-10-04.csv')
addiv = pd.read_csv(path.reference / 'addiv.csv', sep=',', dtype={'id_addiv': 'str', 'of_addiv': 'str'})
# %%
df = raw.assign(
    addiv = raw['addiv'].apply(util.preprocess_string))

# fix district name
df['adh'] = df.addiv
df.loc[df.addiv == 'QUAN 1', 'adh'] = 'QUAN 01'
df.loc[df.addiv == 'QUAN 2', 'adh'] = 'QUAN 02'
df.loc[df.addiv == 'QUAN 3', 'adh'] = 'QUAN 03'
df.loc[df.addiv == 'QUAN 4', 'adh'] = 'QUAN 04'
df.loc[df.addiv == 'QUAN 5', 'adh'] = 'QUAN 05'
df.loc[df.addiv == 'QUAN 6', 'adh'] = 'QUAN 06'
df.loc[df.addiv == 'QUAN 7', 'adh'] = 'QUAN 07'
df.loc[df.addiv == 'QUAN 8', 'adh'] = 'QUAN 08'
df.loc[df.addiv == 'QUAN 9', 'adh'] = 'QUAN 09'

df = df.drop(columns=['addiv'])
df = df.rename(columns={'adh': 'addiv'})

df['addiv'] = df['addiv'].apply(util.encode_addr_dist)

# %%
df.to_csv(
    path.interim / 'vaccine-data.csv', index=False)
