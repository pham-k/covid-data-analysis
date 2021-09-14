# -*- coding: utf-8 -*-
# %%
import pandas as pd
from config import path
import data.util as util

# %%
df = (
    pd.read_csv(path.interim / 'public.csv', sep=';')
    [['date_report','addr_home', 'addr_dist_home', 'addr_ward_home', 'addr_prov_home']]     
    )

# %%
df = df[(df.date_report >= '2021-06-25') & (df.date_report <= '2021-07-01')]
# df = df[(df.date_report >= '2021-07-02') & (df.date_report <= '2021-07-08')]
# df = df[(df.date_report >= '2021-07-09') & (df.date_report <= '2021-07-15')]
# df = df[(df.date_report >= '2021-07-16') & (df.date_report <= '2021-07-22')]
# df = df[(df.date_report >= '2021-07-23') & (df.date_report <= '2021-07-29')]
# %%
# df = df.assign(
#     addr_home = df.addr_home.astype('str').apply(util.compute_addr_x),
#     addr_ward_home = df.addr_ward_home.astype('str').apply(util.compute_addr_x),
#     addr_prov_home = df.addr_prov_home.astype('str').apply(util.compute_addr_x)
# )

# df['addr_comb_home'] = (df.addr_home.str.cat(df.addr_ward_home)
#                                     .str.cat(df.addr_dist_home)
#                                     .str.cat(df.addr_prov_home)
#                          )
# %%
count_adw = (df.groupby(['addr_dist_home', 'addr_ward_home'])
    .apply(lambda x: len(x))
    .to_frame('count')
    .reset_index()
)

count_hh_awh = (df.groupby(['addr_dist_home', 'addr_ward_home', 'addr_home'])
    .apply(lambda x: len(x))
    .to_frame('count')
    .reset_index()
    .drop(columns=['addr_home'])
    .groupby(['addr_dist_home', 'addr_ward_home', 'count'])
    .apply(lambda x: len(x))
    .to_frame('count1')
    .reset_index()
)

count_hh_adh = (df.groupby(['addr_dist_home', 'addr_ward_home', 'addr_home'])
    .apply(lambda x: len(x))
    .to_frame('count')
    .reset_index()
    .drop(columns=['addr_home', 'addr_ward_home'])
    .groupby(['addr_dist_home', 'count'])
    .apply(lambda x: len(x))
    .to_frame('count1')
    .reset_index()
)

# test['adwh'] = test.addr_dist_home + ' ' + test.addr_ward_home
# test1 = test.drop(columns=['addr_dist_home', 'addr_ward_home', 'addr_home'])
# test1 = test.drop(columns=['addr_home'])

# test2 = (test1.groupby(['addr_dist_home', 'addr_ward_home', 'count'])
#          .apply(lambda x: len(x))
#          .to_frame('count1')
#          .reset_index()
#          )

hh_awh = count_hh_awh.pivot(
            index = ['addr_dist_home', 'addr_ward_home'],
            columns='count',
            values='count1'
        ).fillna(0)

hh_awh['total'] = hh_awh.sum(axis=1)
hh_awh['pct_hh1'] = hh_awh[1] / hh_awh.total
hh_awh = hh_awh.reset_index()


hh_adh = count_hh_adh.pivot(
            index = ['addr_dist_home'],
            columns='count',
            values='count1'
        ).fillna(0)

hh_adh['total'] = hh_adh.sum(axis=1)
hh_adh['pct_hh1'] = hh_adh[1] / hh_adh.total
hh_adh = hh_adh.reset_index()
# %%
def foo(data, lst, name_prefix):
    for e in lst:
        df = data[data.addr_dist_home == e]
        name = name_prefix + '_' + e + '.csv'
        df.to_csv(path.interim / 'khu-phong-toa' / '2021-06-25-2021-07-01' / name, index = False, sep=',')

# foo(count_adw, count_adw.addr_dist_home.unique(), 'count')
# count_adw.to_csv(path.interim.joinpath('count_adw.csv'))

# foo(hh_awh, hh_awh.addr_dist_home.unique(), 'hh_awh')
# hh_adh.to_csv(path.interim / 'khu-phong-toa' / '2021-06-25-2021-07-01' / 'hh_adh.csv', index=False, sep=',')
# hh_adh.to_csv(path.interim / 'khu-phong-toa' / '2021-07-02-2021-07-08' / 'hh_adh.csv', index=False, sep=',')
# hh_adh.to_csv(path.interim / 'khu-phong-toa' / '2021-07-09-2021-07-15' / 'hh_adh.csv', index=False, sep=',')
# hh_adh.to_csv(path.interim / 'khu-phong-toa' / '2021-07-16-2021-07-22' / 'hh_adh.csv', index=False, sep=',')
# hh_adh.to_csv(path.interim / 'khu-phong-toa' / '2021-07-23-2021-07-29' / 'hh_adh.csv', index=False, sep=',')




