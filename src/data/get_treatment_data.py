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
raw = pd.read_csv(path.raw / 'treatment-data' / 'merge-2021-10-09.csv')
pop = pd.read_csv(path.reference / 'pop_1.csv', sep=',', dtype={'id_addiv': 'str'})

# %% Rename
with open(path.reference.joinpath('col-name-treatment.txt'), 'r') as file:
    raw.columns = file.read().split('\n')
    
df = raw.assign(
    level = raw.level.astype('str').apply(util.preprocess_string),
    hospital = raw.hospital.astype('str').apply(util.preprocess_string)    
)

df = df[~df.level.str.contains('NAN')]

df.loc[:,df.columns.str.startswith('no')] = df.loc[:,df.columns.str.startswith('no')].fillna(0)
# %% Export
df.to_csv(path.interim.joinpath('treatment-data.csv'), index=False, sep=',')