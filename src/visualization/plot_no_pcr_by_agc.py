#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 10:57:10 2021

@author: kyo
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

from src.config import path

# %% Import
no_pcr_by_agc = pd.read_csv(
    path.processed / 'no-pcr' / 'no-pcr-by-agc.csv',
    index_col='date',
    parse_dates=True)

no_pcr_pos_by_agc = pd.read_csv(
    path.processed / 'no-pcr' / 'no-pcr-pos-by-agc.csv',
    index_col='date',
    parse_dates=True)

# %% Calculate
df = (
   no_pcr_by_agc.reset_index()
   .merge(
       no_pcr_pos_by_agc.reset_index(),
       how='left',
       left_on=['date', 'age_group_children'],
       right_on=['date', 'age_group_children'])
   .set_index('date')    
   )

# %% Plot 0 - 5
data = df[df.age_group_children == '0 - 5']
data['no_pcr_rollingmean7d'] = (
    data['no_pcr']
    .rolling(7)
    .mean())
data['no_pcr_pos_rollingmean7d'] = (
    data['no_pcr_pos']
    .rolling(7)
    .mean())

fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(data.index, data.no_pcr,
       label='PCR', 
       alpha=0.5, color='gray')
ax.plot(data.index, data.no_pcr_rollingmean7d,
       label='PCR - BDTB 7 ngay', 
       linewidth=3, color='black')
ax.bar(data.index, data.no_pcr_pos,
       label='PCR duong', 
       alpha=0.5, color='red')
ax.plot(data.index, data.no_pcr_pos_rollingmean7d,
       label='PCR duong - BDTB 7 ngay', 
       linewidth=3, color='red')
ax.set_ylabel('')
ax.set_xlabel('Ngay')
ax.set_xticks(data.index)
ax.locator_params(axis='x', nbins=60)
ax.tick_params(axis='x', labelrotation=90)
ax.set_title('So PCR, PCR duong o tre 0 - 5 tuoi')
ax.legend(loc='upper left')
plt.savefig(
    path.processed / 'no-pcr' / 'image' / 'no-pcr-by-agc-0-5.png',
    transparent = True)
plt.close(fig)

# %% Plot 6 - 11
data = df[df.age_group_children == '6 - 11']
data['no_pcr_rollingmean7d'] = (
    data['no_pcr']
    .rolling(7)
    .mean())
data['no_pcr_pos_rollingmean7d'] = (
    data['no_pcr_pos']
    .rolling(7)
    .mean())

fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(data.index, data.no_pcr,
       label='PCR', 
       alpha=0.5, color='gray')
ax.plot(data.index, data.no_pcr_rollingmean7d,
       label='PCR - BDTB 7 ngay', 
       linewidth=3, color='black')
ax.bar(data.index, data.no_pcr_pos,
       label='PCR duong', 
       alpha=0.5, color='red')
ax.plot(data.index, data.no_pcr_pos_rollingmean7d,
       label='PCR duong - BDTB 7 ngay', 
       linewidth=3, color='red')
ax.set_ylabel('')
ax.set_xlabel('Ngay')
ax.set_xticks(data.index)
ax.locator_params(axis='x', nbins=60)
ax.tick_params(axis='x', labelrotation=90)
ax.set_title('So PCR, PCR duong o tre 6 - 11 tuoi')
ax.legend(loc='upper left')
plt.savefig(
    path.processed / 'no-pcr' / 'image' / 'no-pcr-by-agc-6-11.png',
    transparent = True)
plt.close(fig)

# %% Plot 12 - 16
data = df[df.age_group_children == '12 - 16']
data['no_pcr_rollingmean7d'] = (
    data['no_pcr']
    .rolling(7)
    .mean())
data['no_pcr_pos_rollingmean7d'] = (
    data['no_pcr_pos']
    .rolling(7)
    .mean())

fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(data.index, data.no_pcr,
       label='PCR', 
       alpha=0.5, color='gray')
ax.plot(data.index, data.no_pcr_rollingmean7d,
       label='PCR - BDTB 7 ngay', 
       linewidth=3, color='black')
ax.bar(data.index, data.no_pcr_pos,
       label='PCR duong', 
       alpha=0.5, color='red')
ax.plot(data.index, data.no_pcr_pos_rollingmean7d,
       label='PCR duong - BDTB 7 ngay', 
       linewidth=3, color='red')
ax.set_ylabel('')
ax.set_xlabel('Ngay')
ax.set_xticks(data.index)
ax.locator_params(axis='x', nbins=60)
ax.tick_params(axis='x', labelrotation=90)
ax.set_title('So PCR, PCR duong o tre 12 - 16 tuoi')
ax.legend(loc='upper left')
plt.savefig(
    path.processed / 'no-pcr' / 'image' / 'no-pcr-by-agc-12-16.png',
    transparent = True)
plt.close(fig)