#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 13:53:16 2021

@author: kyo
"""

import pandas as pd
from src.config import path
from data import util
from datetime import date

# %% Import
raw = pd.read_csv(path.raw / 'f0-home-data' / 'merge-2021-10-09.csv')
pop = pd.read_csv(path.reference / 'pop_1.csv', sep=',', dtype={'id_addiv': 'str'})

# %% Rename
    
df = raw.assign(
    addr_dist_home = raw.addr_dist_home.astype('str').apply(util.preprocess_string),    
)

df['addr_dist_home'] = df['addr_dist_home'].apply(util.encode_addr_dist)
df = (df
      .drop(columns=['no'])
      .set_index('date_report'))
# %% Export
df.to_csv(path.interim.joinpath('f0-home-data.csv'), sep=',')