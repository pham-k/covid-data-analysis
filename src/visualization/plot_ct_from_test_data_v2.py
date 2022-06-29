#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 15:00:36 2021

@author: kyo
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

from src.config import path

# %% Import
ct = pd.read_csv(
    path.processed / 'metrics-from-test-data' / 'ct.csv',
    index_col='date',
    parse_dates=True
    )
# ct_by_awh = pd.read_csv(
#     path.processed / 'ct-by-group-from-test-data' / 'ct-by-awh.csv')

# ct_by_adh = pd.read_csv(
#     path.processed / 'metrics-from-test-data' / 'ct-by-adh.csv',
#     index_col='date',
#     parse_dates=True,
#     dtype={'addr_dist_home': 'str'})

# ct_by_ag = pd.read_csv(
#     path.processed / 'ct-by-group-from-test-data' / 'ct-by-ag.csv')

# ct_by_sex = pd.read_csv(
#     path.processed / 'ct-by-group-from-test-data' / 'ct-by-sex.csv')

addiv = pd.read_csv(
    path.reference / 'addiv.csv',
    usecols=['id_addiv', 'name_addiv'],
    dtype={'id_addiv': 'str'})

# %%
ct['ct'] = ct['ct'].fillna(1).astype('int')

# ct_by_adh['ct'] = ct_by_adh['ct'].fillna(1).astype('int')
# ct_by_adh = (
#     ct_by_adh
#     .reset_index()
#     .merge(addiv, how='left',
#             left_on='addr_dist_home', right_on='id_addiv')
#     .drop(columns=['addr_dist_home', 'id_addiv'])
#     .rename(columns={'name_addiv': 'addr_dist_home'})
#     .set_index('date'))
# %% Declare function
def plot_heatmap(df, title, prefix, name,
                 start_date, end_date,
                 width=8, height=20):
    row = df.index.to_numpy()
    col = df.columns.to_numpy()
    # col = df.index.to_numpy()
    # row = df.columns.to_numpy()

    fig, ax = plt.subplots(figsize=(width, height))
    im = ax.imshow(df, alpha=0.6, cmap='Greens')
    ax.set_aspect('auto')

#     plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = True
#     plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = False
    ax.set_xticks(np.arange(len(col)))
    ax.set_yticks(np.arange(len(row)))

    ax.set_xticklabels(col)
    ax.set_yticklabels(row)
#     ax.set_yticklabels(df.index.strftime('%d-%m'))

    plt.setp(
        ax.get_xticklabels(),
        rotation=90,
        ha="right",
        rotation_mode="anchor"
    )

#     Loop over data dimensions and create text annotations.
    for i in range(len(row)):
        for j in range(len(col)):
            text = ax.text(j, i, df.iloc[i, j],
                           ha="center", va="center", color="black")
    
    filename = (
        prefix + '-'
        + name.lower().replace(' ', '').strip()
        # + '-' 
        # + start_date + '-' 
        # + end_date 
        + '.png')
    output_path = path.processed / 'metrics-from-test-data' / 'image' / filename
    
    ax.set_title(title)
#     fig.tight_layout()
    plt.savefig(
        output_path,
        transparent = True,
        bbox_inches='tight')
    plt.close(fig)
    
# %% Plot heatmap ct
# adh = list(ct_by_adh['addr_dist_home'].unique())

start_date = '2021-08-01'
end_date = '2021-09-28'
prefix = 'ct-by'

# df_adh = (
#     ct_by_adh[
#         (ct_by_adh.index >= start_date)
#         & (ct_by_adh.index <= end_date)]
#     [['addr_dist_home', 'ct']]
#     .reset_index()
# )

df_aph = (
    ct[
        (ct.index >= start_date)
        & (ct.index <= end_date)]
    [['ct']]
    .reset_index()
)

# df_adh['date'] = df_adh['date'].dt.strftime('%Y-%m-%d')
df_aph['date'] = df_aph['date'].dt.strftime('%Y-%m-%d')

df_aph['addr_dist_home'] = 'THANH PHO HO CHI MINH'

# df = (
#     df_adh
#     .append(df_aph)
#     .pivot(
#         # index='addr_dist_home',
#         # columns='date_sample',
#         columns='addr_dist_home',
#         index='date',
#         values='ct'
#     )
# )

df = (
    df_aph
    .pivot(
        # index='addr_dist_home',
        # columns='date_sample',
        columns='date',
        index='addr_dist_home',
        values='ct'
    )
)

plot_heatmap(df, title='CT theo quan huyen', prefix=prefix, name='adh',
              start_date=start_date, end_date=end_date,
              width=20, height=1)    
# %% Plot heatmap ct by awh
# dist = list(ct_by_adh.addr_dist_home.unique())
# # dist = dist[0:3] # to test

# start_date = '2021-08-01'
# end_date = '2021-09-27'
# prefix = 'ct-by-awh'

# ct_by_awh['ct'] = ct_by_awh['ct'].fillna(0).replace(0, 4)
# ct_by_awh['ct'] = ct_by_awh['ct'].astype('int')

# for d in dist:
#     df_awh = (
#         ct_by_awh[
#             (ct_by_awh.addr_dist_home == d) 
#             & (ct_by_awh.date_sample >= start_date)
#             & (ct_by_awh.date_sample <= end_date)]
#         [['date_sample', 'addr_ward_home', 'ct']]
#         .pivot(
#             # index='addr_ward_home',
#             # columns='date_sample',
#             columns='addr_ward_home',
#             index='date_sample',
#             values='ct'
#         )
#     )
    
#     df_adh = (
#         ct_by_adh[
#             (ct_by_adh.addr_dist_home == d) 
#             & (ct_by_awh.date_sample >= start_date)
#             & (ct_by_awh.date_sample <= end_date)]
#         [['date_sample', 'addr_dist_home', 'ct']]
#         .pivot(
#             # index='addr_dist_home',
#             # columns='date_sample',
#             columns='addr_dist_home',
#             index='date_sample',
#             values='ct'
#         )
#     )
    
#     df = df_awh.join(df_adh)
#     plot_heatmap(df, title=d, prefix=prefix, name=d,
#                  start_date=start_date, end_date=end_date,
#                  width=8, height=17)

# %% Plot heatmap ct by ag
# ag = list(ct_by_ag.age_group.unique())

# start_date = '2021-08-01'
# end_date = '2021-09-27'
# prefix = 'ct-by'

# df = (
#     ct_by_ag[
#         (ct_by_ag.date_sample >= start_date)
#         & (ct_by_ag.date_sample <= end_date)]
#     .pivot(
#         index='age_group',
#         columns='date_sample',
#         # columns='age_group',
#         # index='date_sample',
#         values='ct'
#     )
# )
# plot_heatmap(df, title='CT theo nhom tuoi', prefix=prefix, name='ag',
#              start_date=start_date, end_date=end_date,
#              width=20, height=4)

# %% Plot heatmap ct by sex
# sex = list(ct_by_sex.sex.unique())

# start_date = '2021-08-01'
# end_date = '2021-09-27'
# prefix = 'ct-by'

# df = (
#     ct_by_sex[
#         (ct_by_sex.date_sample >= start_date)
#         & (ct_by_sex.date_sample <= end_date)]
#     .pivot(
#         index='sex',
#         columns='date_sample',
#         # columns='sex',
#         # index='date_sample',
#         values='ct'
#     )
# )
# plot_heatmap(df, title='CT theo gioi tinh', prefix=prefix, name='sex',
#              start_date=start_date, end_date=end_date,
#              width=20, height=2)

# %%
