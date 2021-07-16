# -*- coding: utf-8 -*-
# %%
import pandas as pd
from config import path

# %%
df = (pd.read_csv(path.interim / 'public-test.csv', sep=';')
      [['date_report', 'addr_dist_home', 'name_full']]
     )

population = pd.read_csv(path.reference / 'population.csv', sep=',')

# %%
df = df.assign(
    date_report = pd.to_datetime(df.date_report, errors='coerce', format='%d/%m/%Y')
)

# %%
inc_addr_dist_home = (df[['date_report', 'addr_dist_home']]
                      .groupby(['date_report', 'addr_dist_home'])
                      .apply(lambda x: len(x))
                      .to_frame(name='case')
                      .unstack(fill_value=0)
                      .asfreq('D', fill_value=0)
                      .stack()
                      .sort_index(level=0)
                      .reset_index(1)
                     )

inc_addr_dist_home['case_rmean'] = (inc_addr_dist_home
                                 .groupby('addr_dist_home')['case']
                                 .transform(lambda x: x.rolling(7).mean())
                                )
inc_addr_dist_home['case_rsum'] = (inc_addr_dist_home
                                 .groupby('addr_dist_home')['case']
                                 .transform(lambda x: x.rolling(7).sum())
                                )

inc_addr_dist_home = inc_addr_dist_home.reset_index()
inc_addr_dist_home.rename(columns={'addr_dist_home': 'addr_dist'}, inplace=True)
inc_addr_dist_home = inc_addr_dist_home.merge(population, how='left', on='addr_dist')
inc_addr_dist_home['poprisk'] = inc_addr_dist_home['pop'] - inc_addr_dist_home.case_rsum
inc_addr_dist_home['risk'] = inc_addr_dist_home.case_rsum / inc_addr_dist_home.poprisk * 100000
inc_addr_dist_home['ct_who'] = (
        pd.cut(
            x = inc_addr_dist_home.risk,
            bins = [0, 20, 50, 150, 1000],
            labels= [1, 2, 3, 4],
            right=False
        )
        .astype('float')
        .fillna(0)
        .astype('int')
)

inc_addr_dist_home['ct_redcap'] = (
    pd.cut(
        x = inc_addr_dist_home.risk,
        bins = [0, 50, 1000],
        labels= [2, 3],
        right=False
    )
    .astype('float')
    .fillna(0)
    .astype('int')
)

ct_who_1 = (
    inc_addr_dist_home[['date_report', 'addr_dist', 'ct_who']]
    .pivot(index='date_report', columns='addr_dist', values='ct_who')
    .loc['2021-06-02': '2021-06-16',:]
)

ct_who_2 = (
    inc_addr_dist_home[['date_report', 'addr_dist', 'ct_who']]
    .pivot(index='date_report', columns='addr_dist', values='ct_who')
    .loc['2021-06-17':,:]
)


ct_redcap = (
    inc_addr_dist_home[['date_report', 'addr_dist', 'ct_redcap']]
    .pivot(index='date_report', columns='addr_dist', values='ct_redcap')
    .loc['2021-06-24':,:]
)

# %%
# inc = (df[['date_report']]
#        .groupby(['date_report'])
#        .apply(lambda x: len(x))
#        .to_frame(name='case')
#       )

# inc = inc.assign(
#     case_rmean = inc.case.rolling(7).mean(),
#     case_rsum = inc.case.rolling(7).sum(),
#     addr_dist = 'TPHCM'
# )

# inc = inc.merge(
#     population,
#     how = 'left',
#     on = 'addr_dist'
# )

# inc['poprisk'] = 9038566 - inc.case_rsum
# inc['risk'] = inc.case_rsum / inc.poprisk * 100000
# inc['ct'] = pd.cut(
#     x = inc.risk,
#     bins = [0, 20, 50, 150, 1000],
#     labels= [1, 2, 3, 4],
#     right=False
# )

# %%
ct_who_1.to_csv(path.interim.joinpath('ct_who_1.csv'))
ct_who_2.to_csv(path.interim.joinpath('ct_who_2.csv'))
ct_redcap.to_csv(path.interim.joinpath('ct_redcap.csv'))