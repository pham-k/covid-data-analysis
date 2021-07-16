# -*- coding: utf-8 -*-
# %%
import pandas as pd
from config import path

# %%
def calculate_incidence(df, group_col, roll_mean=False, pivot=True):
    inc = (
        df[['date_report', group_col]]
        .groupby(['date_report', group_col])
        .apply(lambda x: len(x))
        .to_frame(name='case')
        .unstack(fill_value=0)
        .asfreq('D', fill_value=0)
        .stack()
        .sort_index(level=0)
        .reset_index(1)
    )
    
    if roll_mean:
        inc['case_rm'] = (
            inc.groupby(group_col)['case']
            .transform(lambda x: x.rolling(7).mean())
        )

    inc = inc.reset_index(0)
    
    if pivot:
        inc = inc.pivot(index='date_report', columns=group_col, values=['case'])
#         col = inc[group_col].unique()
#         inc.columns = col
        
    return inc

# %%
df = (pd.read_csv(path.interim / 'public-test.csv', sep=';')
      [['date_report', 'sex', 'yob', 'addr_dist_home', 'name_full']]
     )

# %%
df = df.assign(
    date_report = pd.to_datetime(df.date_report, errors='coerce', format='%d/%m/%Y'),
    adult = (2021 - df.yob.astype('float')) > 18
)

df = df[(df.sex == 'NAM') | (df.sex == 'NỮ')]
df = df.replace(['NAM', 'NỮ'], ['MALE', 'FEMALE'])

# %%
inc = (
    df[['date_report']]
    .groupby(['date_report'])
    .apply(lambda x: len(x))
    .to_frame(name='case')
    .reindex(pd.date_range(start=df.date_report.min(), end=df.date_report.max(), freq='D'))
    .fillna(0)
      )
inc['case_rm'] = inc.case.rolling(7).mean()

# %%
inc_adh_rollmean = calculate_incidence(df, 'addr_dist_home', roll_mean=True, pivot=False)
inc_adh_cumsum = (
    calculate_incidence(df, 'addr_dist_home', roll_mean=False, pivot=False)
    .groupby(['addr_dist_home', 'date_report'])
    .sum()
    .groupby(level=0)
    .cumsum()
    .reset_index()
    .rename(columns={'case': 'case_cumsum'})
)
inc_sex = calculate_incidence(df, 'sex', roll_mean=False, pivot=True)
inc_sex.columns = ['female', 'male']
inc_adult = calculate_incidence(df, 'adult', roll_mean=False, pivot=True)
inc_adult.columns = ['lte18', 'gt18']

#%%
inc.to_csv(path.interim.joinpath('inc.csv'))
inc_sex.to_csv(path.interim.joinpath('inc_sex.csv'))
inc_adult.to_csv(path.interim.joinpath('inc_adult.csv'))
inc_adh_rollmean.to_csv(path.interim.joinpath('inc_adh_rollmean.csv'))
inc_adh_cumsum.to_csv(path.interim.joinpath('inc_adh_cumsum.csv'))