#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 15:33:39 2021

@author: kyo
"""

# -*- coding: utf-8 -*-

import pandas as pd
from config import path
import data.util as util

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
    date_admit = pd.to_datetime(df.date_admit),
    age = 2021 - df.yob.astype('float')
)

df['age_group'] = pd.cut(
    df.age,
    bins = [0, 17, 45, 65, 200],
    labels = ['0 - 16', '17 - 44', '45 - 64', '> 65'],
    right = False
)


# %%

# %% Get no death
pop_total = int(pop[pop.id_addiv == '79']['pop'][0])
data_in_get_no_death = df[(df.status == 'TU VONG')
                          & (df.date_report >= '2021-05-27')
                          & (df.date_report <= '2021-08-21')]
no_death = util.get_no_event(
    data=data_in_get_no_death,
    pop=pop_total,
    date_col='date_report',
    no_col='no_death',
    rolling=7)


# %% Get no death by age group
data_in_get_no_death_by_group_ag = (
    df[(df.age.notna())
       & (df.status == 'TU VONG')
       & (df.date_report >= '2021-05-27')
       & (df.date_report <= '2021-08-21')]
)
no_death_by_ag = util.get_no_event_by_group(
    data_in_get_no_death_by_group_ag,
    group_col='age_group',
    date_col='date_report',
    no_col='no_death',
    rolling=7,
    available_pop=False,
    getname=False,
    pop=pop,
    addiv=addiv)

# no_death_by_ag['date_report'] = no_death_by_ag['date_report'].astype('str')
# no_death_by_ag['age_group'] = no_death_by_ag['age_group'].astype('str')

# %% Get no death by sex
data_in_get_no_death_by_group_sex = (
    df[(df.sex != 'NAN')
       & (df.status == 'TU VONG')
       & (df.date_report >= '2021-05-27')
       & (df.date_report <= '2021-08-21')]
)
no_death_by_sex = util.get_no_event_by_group(
    data_in_get_no_death_by_group_sex,
    group_col='sex',
    date_col='date_report',
    no_col='no_death',
    rolling=7,
    available_pop=False,
    getname=False,
    pop=pop,
    addiv=addiv)

# no_death_by_sex['date_report'] = no_death_by_sex['date_report'].astype('str')
# no_death_by_sex['sex'] = no_death_by_sex['sex'].astype('str')

# %% Get no death by district
data_in_get_no_death_by_group_adh = (
    df[(df.addr_dist_home != 'UNKN')
       & (df.status == 'TU VONG')
       & (df.date_report >= '2021-05-27')
       & (df.date_report <= '2021-08-21')]
)
no_death_by_adh = util.get_no_event_by_group(
    data_in_get_no_death_by_group_adh,
    pop = pop,
    addiv = addiv,
    group_col='addr_dist_home',
    date_col='date_report',
    no_col='no_death',
    rolling=7,
    available_pop=True,
    getname=True)

# %% Export
no_death.to_csv(path.processed / 'no-death' / 'no-death.csv')
no_death_by_adh.to_csv(
    path.processed / 'no-death-by-group' / 'no-death-by-adh.csv',
    index=False)
no_death_by_ag.to_csv(
    path.processed / 'no-death-by-group' / 'no-death-by-ag.csv',
    index=False)
no_death_by_sex.to_csv(
    path.processed / 'no-death-by-group' / 'no-death-by-sex.csv',
    index=False)
