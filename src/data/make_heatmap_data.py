# -*- coding: utf-8 -*-
# %%
import pandas as pd
from config import path

# %%
df = (pd.read_csv(
    path.interim / 'public.csv',
    sep=',',
    dtype={'addr_dist_home': 'str', 'addr_ward_home': 'str'})
      [['date_report', 'name_full',
        'addr_dist_home', 'addr_ward_home']]
     )

pop = (
    pd.read_csv(path.reference / 'pop_1.csv', sep=',', dtype={'id_addiv': 'str'})
    [['id_addiv', 'pop']]
)
addiv = (
    pd.read_csv(path.reference / 'addiv.csv', sep=',', dtype={'id_addiv': 'str', 'of_addiv': 'str'})
    [['id_addiv', 'of_addiv']]
)

addiv_1 = (
    pd.read_csv(path.reference / 'addiv.csv', sep=',', dtype={'id_addiv': 'str', 'of_addiv': 'str'})
)
# %%
df = df.assign(
    date_report = pd.to_datetime(df.date_report, errors='coerce', format='%Y-%m-%d')
)

# %%
inc_adh = (df[['date_report', 'addr_dist_home']]
                      .groupby(['date_report', 'addr_dist_home'])
                      .apply(lambda x: len(x))
                      .to_frame(name='case')
                      .unstack(fill_value=0)
                      .asfreq('D', fill_value=0)
                      .stack()
                      .sort_index(level=0)
                      .reset_index(1)
                     )

inc_adh['case_rmean'] = (
    inc_adh
    .groupby('addr_dist_home')['case']
    .transform(lambda x: x.rolling(7).mean())
)
inc_adh['case_rsum'] = (
    inc_adh
    .groupby('addr_dist_home')['case']
    .transform(lambda x: x.rolling(7).sum())
)

inc_adh = inc_adh.reset_index()

# %%
inc_adh = inc_adh.merge(
    pop,
    how='left',
    left_on='addr_dist_home',
    right_on = 'id_addiv'
)

inc_adh.drop(columns=['addr_dist_home'], inplace=True)

inc_adh['poprisk'] = inc_adh['pop'] - inc_adh.case_rsum
inc_adh['risk'] = inc_adh.case_rsum / inc_adh.poprisk * 100000
inc_adh['ct_who'] = (
        pd.cut(
            x = inc_adh.risk,
            bins = [0, 20, 50, 150, 5000],
            labels= [1, 2, 3, 4],
            right=False
        )
        .astype('float')
        .fillna(0)
        .astype('int')
)

inc_adh['ct_redcap'] = (
    pd.cut(
        x = inc_adh.risk,
        bins = [0, 50, 5000],
        labels= [2, 3],
        right=False
    )
    .astype('float')
    .fillna(0)
    .astype('int')
)

# %%
inc_awh = (
    df[['date_report', 'addr_ward_home']]
    .groupby(['date_report', 'addr_ward_home'])
    .apply(lambda x: len(x))
    .to_frame(name='case')
    # .unstack(fill_value=0)
    # .asfreq('D', fill_value=0)
    # .stack()
    .sort_index(level=0)
    .reset_index()
)

wide = inc_awh.pivot(
    index='date_report',
    columns='addr_ward_home',
    values='case'
).fillna(0).reset_index()

inc_awh = pd.melt(
    wide,
    id_vars = ['date_report'],
    value_vars=wide.columns[1:]
).rename(columns={'value': 'case'})

inc_awh['case_rmean'] = (
    inc_awh
    .groupby('addr_ward_home')['case']
    .transform(lambda x: x.rolling(7).mean())
)
inc_awh['case_rsum'] = (
    inc_awh
    .groupby('addr_ward_home')['case']
    .transform(lambda x: x.rolling(7).sum())
)



# %%
inc_awh = inc_awh.merge(
    pop,
    how='left',
    left_on='addr_ward_home',
    right_on = 'id_addiv'
)

inc_awh = inc_awh.merge(
    addiv,
    how='left',
    left_on='addr_ward_home',
    right_on = 'id_addiv'
)

inc_awh.drop(columns=['id_addiv_x', 'id_addiv_y'], inplace=True)

inc_awh['poprisk'] = inc_awh['pop'] - inc_awh.case_rsum
inc_awh['risk'] = inc_awh.case_rsum / inc_awh.poprisk * 100000
inc_awh['ct_who'] = (
        pd.cut(
            x = inc_awh.risk,
            bins = [0, 20, 50, 150, 5000],
            labels= [1, 2, 3, 4],
            right=False
        )
        .astype('float')
        .fillna(0)
        .astype('int')
)

inc_awh['ct_redcap'] = (
    pd.cut(
        x = inc_awh.risk,
        bins = [0, 50, 5000],
        labels= [2, 3],
        right=False
    )
    .astype('float')
    .fillna(0)
    .astype('int')
)
# %%
inc = (
    df[['date_report']]
    .groupby(['date_report'])
    .apply(lambda x: len(x))
    .to_frame(name='case')
    # .reindex(pd.date_range(start=df.date_report.min(), end=df.date_report.max(), freq='D'))
    .fillna(0)
)

inc = inc.assign(
    case_rmean = inc.case.rolling(7).mean(),
    case_rsum = inc.case.rolling(7).sum(),
    id_addiv = '79'
)

inc = inc.reset_index().rename(columns={'index': 'date_report'})

inc = inc.merge(
    pop,
    how = 'left',
    left_on = 'id_addiv',
    right_on = 'id_addiv'
)

inc['poprisk'] = inc['pop'] - inc.case_rsum
inc['risk'] = inc.case_rsum / inc.poprisk * 100000

inc['ct_who'] = pd.cut(
    x = inc.risk,
    bins = [0, 20, 50, 150, 5000],
    labels= [1, 2, 3, 4],
    right=False
)
inc['ct_redcap'] = pd.cut(
    x = inc.risk,
    bins = [0, 50, 5000],
    labels= [2, 3],
    right=False
)

# %%
ct_who_1 = (
    inc_adh[['date_report', 'id_addiv', 'ct_who']]
    .append(inc[['date_report', 'id_addiv', 'ct_who']])
    .merge(
        addiv_1[['id_addiv', 'name_addiv']],
        how = 'left',
        left_on = 'id_addiv',
        right_on = 'id_addiv')
    .drop(columns=['id_addiv'])
    .pivot(index='date_report', columns='name_addiv', values='ct_who')
    .loc['2021-06-02': '2021-06-16',:]
)

ct_who_2 = (
    inc_adh[['date_report', 'id_addiv', 'ct_who']]
    .append(inc[['date_report', 'id_addiv', 'ct_who']])
    .merge(
        addiv_1[['id_addiv', 'name_addiv']],
        how = 'left',
        left_on = 'id_addiv',
        right_on = 'id_addiv')
    .drop(columns=['id_addiv'])
    .pivot(index='date_report', columns='name_addiv', values='ct_who')
    .loc['2021-06-17':,:]
)


ct_redcap = (
    inc_adh[['date_report', 'id_addiv', 'ct_redcap']]
    .append(inc[['date_report', 'id_addiv', 'ct_redcap']])
    .merge(
        addiv_1[['id_addiv', 'name_addiv']],
        how = 'left',
        left_on = 'id_addiv',
        right_on = 'id_addiv')
    .drop(columns=['id_addiv'])
    .pivot(index='date_report', columns='name_addiv', values='ct_redcap')
    .loc['2021-06-24':,:]
)

# %%
def export_ct_awh(df, ct):
    dist = df.of_addiv.unique().tolist()
    for d in dist:
        filename = addiv_1[addiv_1.id_addiv == d]['name_addiv'].values[0].replace(' ', '_')
        foo = (
            df
            [(df.of_addiv == d)
             & (df.date_report >= '2021-07-01')]
            [['date_report', 'addr_ward_home', ct]]
            .merge(
                addiv_1[['id_addiv', 'name_addiv']],
                how = 'left',
                left_on = 'addr_ward_home',
                right_on = 'id_addiv')
            .drop(columns=['id_addiv', 'addr_ward_home'])
            .pivot(
                index = 'date_report',
                columns = 'name_addiv',
                values = ct)
        )
        foo.to_csv(path.interim / (ct + '_awh') / (filename + '.csv'))

# %%
export_ct_awh(inc_awh, ct = 'ct_who')
export_ct_awh(inc_awh, ct = 'ct_redcap')
# %%
ct_who_1.to_csv(path.interim.joinpath('ct_who_1.csv'))
ct_who_2.to_csv(path.interim.joinpath('ct_who_2.csv'))
ct_redcap.to_csv(path.interim.joinpath('ct_redcap.csv'))