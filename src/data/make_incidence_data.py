# -*- coding: utf-8 -*-
# %%
import pandas as pd
from config import path

# %%
def calculate_incidence(df, group_col, roll_mean=False, pivot=True, roll_sum=False):
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

    if roll_sum:
        inc['case_rs'] = (
            inc.groupby(group_col)['case']
            .transform(lambda x: x.rolling(14).sum())
        )
        
    inc = inc.reset_index(0)
    
    if pivot:
        inc = inc.pivot(index='date_report', columns=group_col, values=['case'])
#         col = inc[group_col].unique()
#         inc.columns = col
        
    return inc

def export_inc_awh(df):
    dist = df.addr_dist_home.unique()
    for d in dist:
        filename = 'inc_awh_' + d + '.csv'
        data = (
            df[df.addr_dist_home == d]
            .drop(columns='addr_dist_home')
        )
        
        data_pivot = data.pivot(
            index = 'date_report',
            columns= 'addr_ward_home',
            values = 'case'
        ).fillna(0)
        data_pivot.to_csv(path.interim / 'inc_awh_heatmap' / filename)
        
# %%
df = (pd.read_csv(path.interim / 'public.csv', sep=',')
      [['date_report', 'sex', 'yob', 'addr_dist_home', 'addr_ward_home', 'name_full']]
     )

population = pd.read_csv(path.reference / 'population.csv', sep=',')

addiv_1 = (
    pd.read_csv(path.reference / 'addiv.csv', sep=',', dtype={'id_addiv': 'str', 'of_addiv': 'str'})
)

pop = (
    pd.read_csv(path.reference / 'pop_1.csv', sep=',', dtype={'id_addiv': 'str'})
    [['id_addiv', 'pop']]
)
# %%
df = df.assign(
    date_report = pd.to_datetime(df.date_report, errors='coerce', format='%Y/%m/%d'),
    age = 2021 - df.yob.astype('float'),
    adult = (2021 - df.yob.astype('float')) > 18
)

df['age_group'] = (
    pd.cut(
        df.age,
        [-1, 16, 44, 65, 200],
        right = True,
    )
)
df_sex = df[(df.sex == 'NAM') | (df.sex == 'NU')]
# df_sex = df.replace(['NAM', 'NỮ'], ['MALE', 'FEMALE'])
population.rename(columns={'addr_dist': 'addr_dist_home'}, inplace=True)
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
inc['pop'] = population[population.addr_dist_home == 'TPHCM']['pop'].values[0]
inc['case_ppop'] = round(inc['case'] / inc['pop'] * 100000, 2)

# %%
inc_adh_rollmean = (
    calculate_incidence(df, 'addr_dist_home', roll_mean=True, pivot=False)
    .merge(
        addiv_1[['id_addiv', 'name_addiv']],
        how = 'left',
        left_on = 'addr_dist_home',
        right_on = 'id_addiv'
    )
    .drop(columns=['id_addiv', 'addr_dist_home'])
    .rename(columns={'name_addiv': 'addr_dist_home'})
)
inc_adh_rollsum = (
    calculate_incidence(df, 'addr_dist_home', roll_sum=True, pivot=False)
    .merge(
        addiv_1[['id_addiv', 'name_addiv']],
        how = 'left',
        left_on = 'addr_dist_home',
        right_on = 'id_addiv'
    )
    .drop(columns=['id_addiv', 'addr_dist_home'])
    .rename(columns={'name_addiv': 'addr_dist_home'})
)
inc_adh_cumsum = (
    calculate_incidence(df, 'addr_dist_home', roll_mean=False, pivot=False)
    .groupby(['addr_dist_home', 'date_report'])
    .sum()
    .groupby(level=0)
    .cumsum()
    .reset_index()
    .rename(columns={'case': 'case_cumsum'})
)
inc_adh_cumsum = (
    inc_adh_cumsum.merge(
        pop,
        how='left',
        left_on='addr_dist_home',
        right_on = 'id_addiv')
)
inc_adh_cumsum['case_cumsum_perpop'] = inc_adh_cumsum.case_cumsum / inc_adh_cumsum['pop'] * 100000
inc_adh_cumsum = (
    inc_adh_cumsum.merge(
        addiv_1[['id_addiv', 'name_addiv']],
        how = 'left',
        left_on = 'addr_dist_home',
        right_on = 'id_addiv'
    )
    .drop(columns=['id_addiv_x', 'id_addiv_y', 'addr_dist_home'])
    .rename(columns={'name_addiv': 'addr_dist_home'})
)
# TODO fix missing sex
inc_sex = calculate_incidence(df_sex, 'sex', roll_mean=False, pivot=True)
inc_sex.columns = ['female', 'male']
inc_sex['case_rmean_female'] = inc_sex.female.rolling(7).mean()
inc_sex['case_rmean_male'] = inc_sex.male.rolling(7).mean()

inc_adult = calculate_incidence(df, 'adult', roll_mean=False, pivot=True)
inc_adult.columns = ['lte18', 'gt18']

inc_ag = calculate_incidence(df, 'age_group', roll_mean=False, pivot=True)
inc_ag.columns = ['inf_e16', '16_e44', '44_e65','65_inf']
inc_ag['case_rmean_inf_e16'] = inc_ag['inf_e16'].rolling(7).mean()
inc_ag['case_rmean_16_e44'] = inc_ag['16_e44'].rolling(7).mean()
inc_ag['case_rmean_44_e65'] = inc_ag['44_e65'].rolling(7).mean()
inc_ag['case_rmean_65_inf'] = inc_ag['65_inf'].rolling(7).mean()

inc_awh = (
    df[['date_report', 'addr_dist_home', 'addr_ward_home']]
    .groupby(['date_report', 'addr_dist_home', 'addr_ward_home'])
    .apply(lambda x: len(x))
    .to_frame(name='case')
    # .unstack(fill_value=0)
    # .asfreq('D', fill_value=0)
    # .stack()
    .sort_index(level=0)
    .reset_index()
    .merge(
        addiv_1[['id_addiv', 'name_addiv']],
        how = 'left',
        left_on = 'addr_dist_home',
        right_on = 'id_addiv'
    )
    .drop(columns=['id_addiv', 'addr_dist_home'])
    .rename(columns={'name_addiv': 'addr_dist_home'})
)

inc_awh['addr_ward_home'] = inc_awh['addr_ward_home'].astype('str').str.replace('\.0', '')
inc_awh = (
    inc_awh.merge(
        addiv_1[['id_addiv', 'name_addiv']],
        how = 'left',
        left_on = 'addr_ward_home',
        right_on = 'id_addiv'
    )
    .drop(columns=['id_addiv', 'addr_ward_home'])
    .rename(columns={'name_addiv': 'addr_ward_home'})
)
#%%
inc.to_csv(path.interim.joinpath('inc.csv'))
inc_sex.to_csv(path.interim.joinpath('inc_sex.csv'))
inc_adult.to_csv(path.interim.joinpath('inc_adult.csv'))
inc_ag.to_csv(path.interim.joinpath('inc_ag.csv'))
inc_adh_rollmean.to_csv(path.interim.joinpath('inc_adh_rollmean.csv'))
inc_adh_rollsum.to_csv(path.interim.joinpath('inc_adh_rollsum.csv'))
inc_adh_cumsum.to_csv(path.interim.joinpath('inc_adh_cumsum.csv'))
export_inc_awh(inc_awh)



