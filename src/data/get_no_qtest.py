#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 09:49:20 2021

@author: kyo
"""

import pandas as pd
from datetime import date

from src.config import path
import util

# %%
df1 = pd.read_excel(
    path.external / 'qtest-data' / 'qtest.xlsx',
)

# df2 = pd.read_excel(
#     path.external / 'qtest-data' / 'qtest-by-adh.xlsx',
# )

# %%
df1 = df1.set_index('date_report')

no_qtest = df1['no_qtest']
no_qtest_pos = df1['no_qtest_pos']

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

# no_qtest_by_adh.to_csv(
#     path.processed / 'no-qtest' / 'no-qtest-by-adh.csv'
# )

# no_qtest_pos_by_adh.to_csv(
#     path.processed / 'no-qtest' / 'no-qtest-pos-by-adh.csv'
# )

