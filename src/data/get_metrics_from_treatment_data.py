#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 10:19:28 2021

@author: kyo
"""

import pandas as pd
from config import path

# %%
no_ecmo_total = pd.read_csv(
    path.processed / 'metrics-from-treatment-data' / 'no-ecmo-total.csv',
    sep=',',
    index_col='date_report'
)

no_ecmo_in_use = pd.read_csv(
    path.processed / 'metrics-from-treatment-data' / 'no-ecmo-in-use.csv',
    sep=',',
    index_col='date_report'
)

no_dialysis_total = pd.read_csv(
    path.processed / 'metrics-from-treatment-data' / 'no-dialysis-total.csv',
    sep=',',
    index_col='date_report'
)

no_dialysis_in_use = pd.read_csv(
    path.processed / 'metrics-from-treatment-data' / 'no-dialysis-in-use.csv',
    sep=',',
    index_col='date_report'
)

no_ivent_total = pd.read_csv(
    path.processed / 'metrics-from-treatment-data' / 'no-ivent-total.csv',
    sep=',',
    index_col='date_report'
)

no_ivent_in_use = pd.read_csv(
    path.processed / 'metrics-from-treatment-data' / 'no-ivent-in-use.csv',
    sep=',',
    index_col='date_report'
)

no_bed_total = pd.read_csv(
    path.processed / 'metrics-from-treatment-data' / 'no-bed.csv',
    sep=',',
    index_col='date_report'
)

no_bed_in_use = pd.read_csv(
    path.processed / 'metrics-from-treatment-data' / 'no-bed-in-use.csv',
    sep=',',
    index_col='date_report'
)

no_oxy_total = pd.read_csv(
    path.processed / 'metrics-from-treatment-data' / 'no-oxy-total.csv',
    sep=',',
    index_col='date_report'
)

no_oxy_in_use = pd.read_csv(
    path.processed / 'metrics-from-treatment-data' / 'no-oxy-in-use.csv',
    sep=',',
    index_col='date_report'
)

no_death = pd.read_csv(
    path.processed / 'no-death-from-treatment-data' / 'no-death.csv',
    sep=',',
    index_col='date_report'
)

no_in = pd.read_csv(
    path.processed / 'no-in-from-treatment-data' / 'no-in.csv',
    sep=',',
    index_col='date_report'
)

no_test = pd.read_csv(
    path.processed / 'no-test' / 'no-test.csv',
    sep=',',
    index_col='date_report'
)

no_positive = pd.read_csv(
    path.processed / 'no-positive' / 'no-positive.csv',
    sep=',',
    index_col='date_report'
)

pop = pd.read_csv(path.reference / 'pop_1.csv', sep=',', dtype={'id_addiv': 'str'})


# %%
epi_metrics = (
    no_ecmo_total
    .join(no_dialysis_total)
    .join(no_ivent_total)
    .join(no_ecmo_in_use)
    .join(no_dialysis_in_use)
    .join(no_ivent_in_use)
)

epi_metrics['icu_total'] = (
    epi_metrics['no_ecmo_total']
    + epi_metrics['no_dialysis_total']
    + epi_metrics['no_ivent_total']
)

epi_metrics['icu_in_use'] = (
    epi_metrics['no_ecmo_in_use']
    + epi_metrics['no_dialysis_in_use']
    + epi_metrics['no_ivent_in_use']
)

epi_metrics['icu_proportional_occupancy'] = (
    epi_metrics['icu_in_use']
    / epi_metrics['icu_total']
)

# %%
pop_total = int(pop[pop.id_addiv == '79']['pop'][0])

public_health_metrics = (
    no_bed_total
    .join(no_bed_in_use)
    .join(no_death['no_death'])
    .join(no_in['no_in'])
    .join(no_test['no_test'])
)

public_health_metrics['clinical_care_capacity'] = (
    public_health_metrics['no_bed_in_use']
    / public_health_metrics['no_bed']
)

public_health_metrics['clinical_care_capacity_response_capacity'] = pd.cut(
    public_health_metrics['clinical_care_capacity'],
    bins = [0, 0.75, 0.9, 10000],
    labels = ['adequate', 'moderate', 'limited'],
    right = False)

public_health_metrics['clinical_performance'] = (
    public_health_metrics['no_death']
    / public_health_metrics['no_in']
)

public_health_metrics['no_test_per1000pop_sum7d'] = (
    (public_health_metrics['no_test'] / pop_total * 1000)
    .rolling(7).sum()
)

public_health_metrics['no_test_per1000pop_sum7d_response_capacity'] = pd.cut(
    public_health_metrics['no_test_per1000pop_sum7d'],
    bins = [0, 1, 4, 10000],
    labels = ['limited', 'moderate', 'adequate'],
    right = False)

public_health_metrics['no_test_per1000pop_mean14d'] = (
    (public_health_metrics['no_test'] / pop_total * 1000)
    .rolling(14).mean()
)

public_health_metrics['no_test_per1000pop_mean14d_response_capacity'] = pd.cut(
    public_health_metrics['no_test_per1000pop_mean14d'],
    bins = [0, 1, 4, 10000],
    labels = ['limited', 'moderate', 'adequate'],
    right = False)

# %%
health_system_metrics = (
    no_oxy_total
    .join(no_oxy_in_use)
    .join(no_death['no_death'])
    .join(no_positive['no_positive'])
)

health_system_metrics['proportion_of_occupied_bed_with_oxy'] = (
    health_system_metrics['no_oxy_in_use']
    / health_system_metrics['no_oxy_total']
)

health_system_metrics['crude_fatality_rate'] = (
    health_system_metrics['no_death']
    / health_system_metrics['no_positive']
)

# %%
epi_metrics.to_csv(
    path.processed / 'metrics-from-treatment-data'/ 'epi-metrics.csv',
    sep=','
)

public_health_metrics.to_csv(
    path.processed / 'metrics-from-treatment-data'/ 'public-health-metrics.csv',
    sep=','
)

health_system_metrics.to_csv(
    path.processed / 'metrics-from-treatment-data'/ 'health-system-metrics.csv',
    sep=','
)
