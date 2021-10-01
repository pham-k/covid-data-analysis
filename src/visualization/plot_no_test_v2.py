#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 10:03:49 2021

@author: kyo
"""

import pandas as pd
import matplotlib.pyplot as plt

from src.config import path

# %% Import
ct = pd.read_csv(
    path.processed / 'metrics-from-test-data' / 'ct.csv',
    index_col='date',
    parse_dates=True
    )
# ct_by_awh = pd.read_csv(
#     path.processed / 'ct-by-group-from-test-data' / 'ct-by-awh.csv')

ct_by_adh = pd.read_csv(
    path.processed / 'metrics-from-test-data' / 'ct-by-adh.csv',
    index_col='date',
    parse_dates=True,
    dtype={'addr_dist_home': 'str'})

# ct_by_ag = pd.read_csv(
#     path.processed / 'ct-by-group-from-test-data' / 'ct-by-ag.csv')

# ct_by_sex = pd.read_csv(
#     path.processed / 'ct-by-group-from-test-data' / 'ct-by-sex.csv')

addiv = pd.read_csv(
    path.reference / 'addiv.csv',
    usecols=['id_addiv', 'name_addiv'],
    dtype={'id_addiv': 'str'})
# %%
ct_by_adh = (
    ct_by_adh
    .reset_index()
    .merge(addiv, how='left',
           left_on='addr_dist_home', right_on='id_addiv')
    .drop(columns=['addr_dist_home', 'id_addiv'])
    .rename(columns={'name_addiv': 'addr_dist_home'})
    .set_index('date'))
# %% Plot no_test, no_test_pos by toan tp <= 16/09
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(x[i], y[i] + 4000, y[i].astype('int'), ha='center', va='top', rotation=90)
        
df = (
    ct[
       (ct.index >= '2021-05-27')
        & (ct.index <= '2021-09-16')
       ]
)
fig, ax = plt.subplots(figsize=(16,8))
# [bar] So test theo ngay
ax.bar(
    df.index, df.no_test,
    label='Số test (hc) theo ngày', linewidth=3, alpha=0.5, color='gray')
# [line] BDTB so test theo ngay
ax.plot(
    df.index, df.no_test_rollingmean7d, 
    label='Biến động trung bình 7 ngày', linewidth=3, color='black')
# [bar] So test duong theo ngay
ax.bar(
    df.index, df.no_test_pos,
    label='Số test dương theo ngày', linewidth=3, alpha=0.5, color='red')
# [line] BDTB so test duong theo ngay
ax.plot(
    df.index, df.no_test_pos_rollingmean7d,
    label='Biến động trung bình 7 ngày', linewidth=3, color='red')
ax.set_ylabel('Số test (hc)')
ax.set_ylim([0, 40000])
ax.set_xlabel('Ngày')
ax.set_xticks(df.index)
ax.tick_params(axis='x', labelrotation=90)
ax.set_title('Số test (hc) theo ngày và biến động trung bình 7 ngày')
ax.legend(loc='upper left')
ax.locator_params(axis='x', tight=True, nbins=30)
addlabels(df.index, df.no_test)
filename = 'no-test-2021-09-16.png'
output_path = path.processed / 'metrics-from-test-data' / 'image' / filename
plt.savefig(
        output_path,
        transparent = True)
plt.close(fig)

# %% Plot no_test, no_test_pos by toan tp > 16/09
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(x[i], y[i] + 50000, y[i].astype('int'), ha='center', va='top', rotation=90)
        
df = (
    ct[
       (ct.index >= '2021-09-16')
        # & (ct.index <= '2021-09-16')
       ]
)
fig, ax = plt.subplots(figsize=(16,8))
# [bar] So test theo ngay
ax.bar(
    df.index, df.no_test,
    label='Số test (hc) theo ngày', linewidth=3, alpha=0.5, color='gray')
# [line] BDTB so test theo ngay
ax.plot(
    df.index, df.no_test_rollingmean7d, 
    label='Biến động trung bình 7 ngày', linewidth=3, color='black')
# [bar] So test duong theo ngay
ax.bar(
    df.index, df.no_test_pos,
    label='Số test dương theo ngày', linewidth=3, alpha=0.5, color='red')
# [line] BDTB so test duong theo ngay
ax.plot(
    df.index, df.no_test_pos_rollingmean7d,
    label='Biến động trung bình 7 ngày', linewidth=3, color='red')
ax.set_ylabel('Số test (hc)')
# ax.set_ylim([0, 40000])
ax.set_xlabel('Ngày')
ax.set_xticks(df.index)
ax.tick_params(axis='x', labelrotation=90)
ax.set_title('Số test (hc) theo ngày và biến động trung bình 7 ngày')
ax.legend(loc='upper left')
ax.locator_params(axis='x', tight=True, nbins=30)
addlabels(df.index, df.no_test)
filename = 'no-test-latest.png'
output_path = path.processed / 'metrics-from-test-data' / 'image' / filename
plt.savefig(
        output_path,
        transparent = True)
plt.close(fig)
# %% Plot no_test cumsum by district
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(y[i], x[i], y[i].astype('int'), ha='left', va='center')
        
df = (
    ct_by_adh[['addr_dist_home', 'no_test', 'no_test_pos']]
#     .query('date_sample == "2021-08-05"')
    .groupby('addr_dist_home')[['no_test', 'no_test_pos']]
    .sum()
#     .to_frame(name='no_test_cumsum')
    .reset_index()
    .sort_values('no_test')
    .set_index('addr_dist_home')
)
df.index = df.index.astype('str')
# df
# ct_by_adh.loc[ct_by_adh.addr_dist_home == 'HUYEN BINH CHANH', 'no_positive'].sum()
fig, ax = plt.subplots(figsize=(16,8))
ax.barh(df.index, df.no_test, color='grey', alpha=0.4, label='Số test cộng dồn (hc)')
ax.barh(df.index, df.no_test_pos, color='red', alpha=0.4, label='Số dương tính cộng dồn')
ax.set_ylabel('Quận huyện')
ax.set_xlabel('Số test (hc) cộng dồn')
ax.set_xlim([0, 1.8*1e6])
ax.set_title('Số test (hc) và số test dương cộng dồn theo quận huyện')
ax.legend(loc='lower right')
addlabels(df.index, df.no_test)
filename = 'no-test-cumsum-by-adh.png'
output_path = path.processed / 'metrics-from-test-data' / 'image' / filename
plt.savefig(
        output_path,
        transparent = True)
plt.close(fig)

# %% Plot no_test, no_positive by sex
# def addlabels(x,y):
#     offset = y.max() / 10
#     for i in range(len(x)):
#         plt.text(i, y[i] + offset, y[i].astype('int'), ha='center', va='top', rotation=90)

# unique = ct_by_sex.sex.unique()
# start_date = '2021-05-27'

# for u in unique:
#     df = (
#         ct_by_sex[(ct_by_sex.date_sample >= start_date)
#                   & (ct_by_sex.sex == u)]
#         .set_index('date_sample')
#     )
            
#     fig, ax = plt.subplots(figsize=(16,8))
    
#     # [bar] So test theo ngay
#     ax.bar(
#         df.index, df.no_test_corrected, 
#         label='Số test (hc) theo ngày', linewidth=3, alpha=0.5, color='grey')
#     # [line] BDTB so test theo ngay
#     ax.plot(
#         df.index, df.no_test_rollsum / 7, 
#         label='Biến động trung bình 7 ngày', linewidth=3, color='black')
    
#     # [bar] So test duong theo ngay
#     ax.bar(df.index, df.no_positive,
#            label='Số test dương theo ngày', linewidth=3, alpha=0.5, color='red')
    
#     # [line] BDTB so test duong theo ngay
#     ax.plot(df.index, df.no_positive_rollsum / 7,
#             label='Biến động trung bình 7 ngày', linewidth=3, color='red')
    
#     ax.set_ylabel('Số test (hc)')
#     ax.set_ylim([0, df.no_test_corrected.max() * 1.2])
#     ax.set_xlabel('Ngày')
#     ax.set_xticks(df.index)
#     ax.tick_params(axis='x', labelrotation=90)
#     ax.set_title('Số test (hc) theo ngày và biến động trung bình 7 ngày của ' + str(u))
#     ax.legend(loc='upper left')
#     addlabels(df.index, df.no_test_corrected)
#     filename = 'no-test-no-postsitive-' + str(u).strip().lower().replace(' ', '') + '.png'
#     output_path = path.processed / 'no-test-no-positive' / 'image' / filename
#     plt.savefig(
#             output_path,
#             transparent = True)
#     plt.close(fig)

# %% Plot no_test district <= 16/09
def addlabels(x,y):
    offset = y.max() / 10
    for i in range(len(x)):
        plt.text(x[i], y[i] + offset, y[i].astype('int'), ha='center', va='top', rotation=90)

unique = ct_by_adh['addr_dist_home'].unique()
start_date = '2021-05-27'
end_date = '2021-09-16'

for u in unique:
    df = (
        ct_by_adh[(ct_by_adh.index >= start_date)
                  & (ct_by_adh.index <= end_date)
                  & (ct_by_adh['addr_dist_home'] == u)]
        # .set_index('date_sample')
    )
            
    fig, ax = plt.subplots(figsize=(16,8))
    
    # [bar] So test theo ngay
    ax.bar(
        df.index, df.no_test, 
        label='Số test (hc) theo ngày', linewidth=3, alpha=0.5, color='grey')
    # [line] BDTB so test theo ngay
    ax.plot(
        df.index, df.no_test_rollingmean7d, 
        label='Biến động trung bình 7 ngày', linewidth=3, color='black')
    
    # [bar] So test duong theo ngay
    ax.bar(df.index, df.no_test_pos,
           label='Số test dương theo ngày', linewidth=3, alpha=0.5, color='red')
    
    # [line] BDTB so test duong theo ngay
    ax.plot(df.index, df.no_test_pos_rollingmean7d / 7,
            label='Biến động trung bình 7 ngày', linewidth=3, color='red')
    
    ax.set_ylabel('Số test (hc)')
    ax.set_ylim([0, df.no_test.max() * 1.2])
    ax.set_xlabel('Ngày')
    ax.set_xticks(df.index)
    ax.tick_params(axis='x', labelrotation=90)
    ax.set_title('Số test (hc) theo ngày và biến động trung bình 7 ngày của ' + str(u))
    ax.legend(loc='upper left')
    addlabels(df.index, df.no_test)
    filename = (
        'no-test-'
        + str(u).strip().lower().replace(' ', '')
        + '-' + end_date
        + '.png')
    output_path = path.processed / 'metrics-from-test-data' / 'image' / filename
    plt.savefig(
            output_path,
            transparent = True)
    plt.close(fig)

# %% Plot no_test district > 16/09
def addlabels(x,y):
    offset = y.max() / 10
    for i in range(len(x)):
        plt.text(x[i], y[i] + offset, y[i].astype('int'), ha='center', va='top', rotation=90)

unique = ct_by_adh['addr_dist_home'].unique()
start_date = '2021-09-17'
# end_date = '2021-09-28'

for u in unique:
    df = (
        ct_by_adh[(ct_by_adh.index >= start_date)
                  # & (ct_by_adh.index <= end_date)
                  & (ct_by_adh['addr_dist_home'] == u)]
        # .set_index('date_sample')
    )
            
    fig, ax = plt.subplots(figsize=(16,8))
    
    # [bar] So test theo ngay
    ax.bar(
        df.index, df.no_test, 
        label='Số test (hc) theo ngày', linewidth=3, alpha=0.5, color='grey')
    # [line] BDTB so test theo ngay
    ax.plot(
        df.index, df.no_test_rollingmean7d, 
        label='Biến động trung bình 7 ngày', linewidth=3, color='black')
    
    # [bar] So test duong theo ngay
    ax.bar(df.index, df.no_test_pos,
           label='Số test dương theo ngày', linewidth=3, alpha=0.5, color='red')
    
    # [line] BDTB so test duong theo ngay
    ax.plot(df.index, df.no_test_pos_rollingmean7d / 7,
            label='Biến động trung bình 7 ngày', linewidth=3, color='red')
    
    ax.set_ylabel('Số test (hc)')
    ax.set_ylim([0, df.no_test.max() * 1.2])
    ax.set_xlabel('Ngày')
    ax.set_xticks(df.index)
    ax.tick_params(axis='x', labelrotation=90)
    ax.set_title('Số test (hc) theo ngày và biến động trung bình 7 ngày của ' + str(u))
    ax.legend(loc='upper left')
    addlabels(df.index, df.no_test)
    filename = (
        'no-test-'
        + str(u).strip().lower().replace(' ', '')
        + '-latest'
        + '.png')
    output_path = path.processed / 'metrics-from-test-data' / 'image' / filename
    plt.savefig(
            output_path,
            transparent = True)
    plt.close(fig)
# %% Plot no_test, no_positive by age group
# def addlabels(x,y):
#     offset = y.max() / 10
#     for i in range(len(x)):
#         plt.text(i, y[i] + offset, y[i].astype('int'), ha='center', va='top', rotation=90)

# unique = ct_by_ag.age_group.unique()
# start_date = '2021-05-27'

# for u in unique:
#     df = (
#         ct_by_ag[(ct_by_ag.date_sample >= start_date)
#                   & (ct_by_ag.age_group == u)]
#         .set_index('date_sample')
#     )
            
#     fig, ax = plt.subplots(figsize=(16,8))
    
#     # [bar] So test theo ngay
#     ax.bar(
#         df.index, df.no_test_corrected, 
#         label='Số test (hc) theo ngày', linewidth=3, alpha=0.5, color='grey')
#     # [line] BDTB so test theo ngay
#     ax.plot(
#         df.index, df.no_test_rollsum / 7, 
#         label='Biến động trung bình 7 ngày', linewidth=3, color='black')
    
#     # [bar] So test duong theo ngay
#     ax.bar(df.index, df.no_positive,
#            label='Số test dương theo ngày', linewidth=3, alpha=0.5, color='red')
    
#     # [line] BDTB so test duong theo ngay
#     ax.plot(df.index, df.no_positive_rollsum / 7,
#             label='Biến động trung bình 7 ngày', linewidth=3, color='red')
    
#     ax.set_ylabel('Số test (hc)')
#     ax.set_ylim([0, df.no_test_corrected.max() * 1.2])
#     ax.set_xlabel('Ngày')
#     ax.set_xticks(df.index)
#     ax.tick_params(axis='x', labelrotation=90)
#     ax.set_title('Số test (hc) theo ngày và biến động trung bình 7 ngày của ' + str(u))
#     ax.legend(loc='upper left')
#     addlabels(df.index, df.no_test_corrected)
#     filename = 'no-test-no-positive-' + str(u).strip().lower().replace(' ', '') + '.png'
#     output_path = path.processed / 'no-test-no-positive' / 'image' / filename
#     plt.savefig(
#             output_path,
#             transparent = True)
#     plt.close(fig)