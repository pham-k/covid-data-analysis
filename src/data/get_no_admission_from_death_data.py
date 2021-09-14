#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 15:33:39 2021

@author: kyo
"""

# -*- coding: utf-8 -*-

import pandas as pd
from config import path

# %% Import
df = (pd.read_csv(
    path.interim / 'death-data.csv',
    sep=',',
    dtype={'addr_dist_home': 'str', 'addr_ward_home': 'str'})
)

pop = pd.read_csv(path.reference / 'pop_1.csv', sep=',', dtype={'id_addiv': 'str'})
addiv = pd.read_csv(path.reference / 'addiv.csv', sep=',', dtype={'id_addiv': 'str', 'of_addiv': 'str'})


# %% Process
# Get age group
df = df.assign(
    date_report = pd.to_datetime(df.date_report),
    date_admit = pd.to_datetime(
        pd.to_datetime(df.date_admit).dt.date),
    age = 2021 - df.yob.astype('float')
)

df['age_group'] = pd.cut(
    df.age,
    bins = [0, 17, 45, 65, 200],
    labels = ['0 - 16', '17 - 44', '45 - 64', '> 65'],
    right = False
)


# %%
def get_no_event(data, date_col='date_report', no_col='no_test', pop=10000000, rolling=7):
    """
    Count number of (no) event by date
    
    Args:
        data: Data frame, input data frame
        date_col: String, name of date column, default 'date_report'
        no_col: String, name of event count column, default 'no_case'
        rolling: Int, rolling window, default 7
        pop: Int, population, default 10000000
    
    Return:
        A data frame
    """
    # number of events by date, reindex to fill missing date entry with 0
    df = (
        data[[date_col]]
        .groupby(date_col)
        .apply(lambda x: len(x))
        .to_frame(name=no_col)
        .reindex(pd.date_range(start=data[date_col].min(), end=data[date_col].max(), freq='D'))
        .fillna(0)
    )
    # population column
    df['pop'] = pop
    # name of columns to be created
    col_per_pop = no_col + '_ppop'
    col_rollmean = no_col + '_rollmean' + str(rolling) + 'd'
    col_per_pop_rollmean = no_col + '_ppop_rollmean' + str(rolling) + 'd'
    col_cumsum = no_col + '_cumsum'
    col_per_pop_cumsum = no_col + '_ppop_cumsum'
    # number of events per population by date
    df[col_per_pop] = round(df[no_col] /df['pop'] * 100000, 3)
    # rolling mean number of events by date
    df[col_rollmean] = df[no_col].rolling(rolling).mean()
    # rolling mean number of events per population by date
    df[col_per_pop_rollmean] = df[col_per_pop].rolling(7).mean()
    # cumulative sum number of events by date
    df[col_cumsum] = df[no_col].cumsum()
    # cumulative sum number of events per population by date
    df[col_per_pop_cumsum] = df[col_per_pop].cumsum()
    df = df.drop(columns='pop')
    return df

def get_no_event_by_group(data,
                         group_col,
                         date_col='date_report',
                         no_col='no_test',
                         available_pop=False,
                         getname=False, rolling=7):
    """
    Count number of (no) event by group and date
    
    Args:
        data: Data frame, input data frame
        date_col: String, name of date column, default date_col
        no_col: String, name of event count column, default no_col
        rolling: Int, rolling window, default 7
        available_pop: Boolean, if population data frame by group is available, default False
        getname: Boolean, to get group label if it exists, default False
    
    Return:
        A data frame
    """
    unique = data[group_col].unique()
    # number of events by group and date
    df_1 = (
        data[[date_col, group_col]]
        .groupby([date_col, group_col])
        .apply(lambda x: len(x))
        .to_frame(name=no_col)
        .unstack(fill_value=0)
        .asfreq('D', fill_value=0)
        .stack()
        .sort_index(level=0)
        .reset_index()
    )
    # pivot table to fill missing group with 0
    df_pv = (
        df_1[[date_col, group_col, no_col]]
        .pivot(index=date_col, columns=group_col, values=no_col)
    ).fillna(0)
    # fill missing date with 0
    df_2 = (
        df_pv.reindex(pd.date_range(
            start=df_pv.index.min(),
            end=df_pv.index.max(),
            freq='D'))
        .fillna(0)
        .stack(list(range(0, 1)))
        .reset_index()
        .rename(columns={
            'level_0': date_col,
            0: no_col
        })
#         .set_index([date_col] + group)
    )
    
    # name of columns to be created
    col_per_pop = no_col + '_ppop'
    col_rollmean = no_col + '_rollmean' + str(rolling) + 'd'
    col_per_pop_rollmean = no_col + '_ppop_rollmean' + str(rolling) + 'd'
    col_cumsum = no_col + '_cumsum'
    col_per_pop_cumsum = no_col + '_ppop_cumsum'
    
    # get no_case_rollmean
    df_3 = df_2
    df_3[col_rollmean] = (
        df_3.groupby(group_col)[no_col]
        .transform(lambda x: x.rolling(rolling).mean())
    )
    # get no_case cumsum
    df_3[col_cumsum] = (
        df_3[[date_col, group_col, no_col]]
        .groupby([date_col, group_col]).sum()
        .groupby(level=1).cumsum().reset_index()
        [no_col]
    )
    
    # Get number of events per population
    if available_pop:
        df_pop = pop[['id_addiv', 'pop']]
        # merge with population
        df_3 = (
            df_3.merge(
                df_pop,
                how= 'left',
                left_on=group_col,
                right_on= 'id_addiv')
            .drop(columns=['id_addiv'])
        )
        # number of events per population by group
        df_3[col_per_pop] = round(df_3[no_col] / df_3['pop'] * 100000, 3)
        df_3 = df_3.drop(columns='pop')
        # rolling mean number of events per population by group
        df_3[col_per_pop_rollmean] = (
            df_3.groupby(group_col)[col_per_pop]
            .transform(lambda x: x.rolling(rolling).mean())
        )
        # cumulative sum number of events per population by group
        df_3[col_per_pop_cumsum] = (
            df_3[[date_col, group_col, col_per_pop]]
            .groupby([date_col, group_col]).sum()
            .groupby(level=1).cumsum().reset_index()
            [col_per_pop]
        )

    # Get district name (optional)
    if getname:
        df_3 = (
            df_3.merge(
                addiv[['id_addiv', 'name_addiv_2']],
                how = 'left',
                left_on = group_col,
                right_on = 'id_addiv'
            )
            .drop(columns=[group_col, 'id_addiv'])
            .rename(columns={'name_addiv_2': group_col})
        )
    return df_3


# %% Get no admission
pop_total = int(pop[pop.id_addiv == '79']['pop'][0])
data_in_get_no_admission = df[(df.status == 'TU VONG')
                          & (df.date_admit >= '2021-05-27')
                          & (df.date_admit <= '2021-08-21')]

no_admission = get_no_event(
    data_in_get_no_admission,
    pop=pop_total,
    date_col='date_admit',
    no_col='no_admission',
    rolling=7)


# %% export
no_admission.to_csv(path.processed / 'no-admission' / 'no-admission.csv')
# no_death_by_adh.to_csv(
#     path.processed / 'no-death-by-group' / 'no-death-by-adh.csv',
#     index=False)
# no_death_by_ag.to_csv(
#     path.processed / 'no-death-by-group' / 'no-death-by-ag.csv',
#     index=False)
# no_death_by_sex.to_csv(
#     path.processed / 'no-death-by-group' / 'no-death-by-sex.csv',
#     index=False)

