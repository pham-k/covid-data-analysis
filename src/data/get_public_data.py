# %%
import pandas as pd
import pathlib
# from config import path
import config.path as path
from data import util

# %% Import
df = pd.read_csv(
    path.external.joinpath('public-data', 'data-covid-2021-09-30.csv')
)
# df = pd.read_excel(
#     path.external / 'public-data' / 'data-covid-2021-09-12.xlsx'
# )
pop = pd.read_csv(path.reference / 'pop_1.csv', sep=',', dtype={'id_addiv': 'str'})
addiv = pd.read_csv(path.reference / 'addiv.csv', sep=',', dtype={'id_addiv': 'str', 'of_addiv': 'str'})
# %% Rename col
with open(path.reference.joinpath('col-name-public-3.txt'), 'r') as file:
    df.columns = file.read().split('\n')
    
    
# df = df[['name_full', 'sex', 'yob',
#          'addr_prov_home', 'addr_dist_home', 'addr_ward_home', 'addr_home',
#          'date_report', 'date_positive']]

# %% Preprocess
df = df.assign(
    date_report = pd.to_datetime(
        df['date_report'].astype('str').apply(util.compute_date_report),
        errors='coerce',
        format='%d/%m/%Y'
        ),
    # date_report = df.date_report.dt.date,
    name_full = df['name_full'].astype('str').apply(util.clean_name_full),
    sex = df['sex'].astype('str').apply(util.clean_sex),
    addr_dist_home = df['addr_dist_home'].apply(util.encode_addr_dist),
    date_positive = pd.to_datetime(
        df['date_positive'].astype('str'),
        errors='coerce',
        format='%d/%m/%Y'
    ),
    # date_positive = df.date_positive.dt.date,
    addr_home = df.addr_home.astype('str').apply(util.compute_addr_x),
    addr_ward_home = df.addr_ward_home.astype('str').apply(util.preprocess_addr_ward),
    addr_prov_home = '79',
    # place_recognize = df.place_recognize.astype('str').apply(util.clean_place_recognize)
)

# %% Encode district and ward
df.loc[(df.addr_ward_home == 'THI TRAN') & (df.addr_dist_home == '786'), 'addr_ward_home'] = 'THI TRAN NHA BE'
df.loc[(df.addr_ward_home == 'THI TRAN') & (df.addr_dist_home == '784'), 'addr_ward_home'] = 'THI TRAN HOC MON'
df.loc[(df.addr_ward_home == 'THI TRAN') & (df.addr_dist_home == '783'), 'addr_ward_home'] = 'THI TRAN CU CHI'
df.loc[(df.addr_ward_home == 'THI TRAN') & (df.addr_dist_home == '785'), 'addr_ward_home'] = 'THI TRAN TAN TUC'
df.loc[(df.addr_ward_home == 'THI TRAN') & (df.addr_dist_home == '787'), 'addr_ward_home'] = 'THI TRAN CAN THANH'

# combine name of dist and ward
df['dw'] = df.addr_dist_home + ' ' + df.addr_ward_home

df = df.merge(addiv[['dw', 'id_addiv']], how = 'left', on= 'dw' )
df['addr_ward_home'] = df.id_addiv


# df['addr_comb_home'] = (df.addr_home.str.cat(df.addr_ward_home)
#                                     .str.cat(df.addr_dist_home)
#                                     .str.cat(df.addr_prov_home)
#                           )

# df.addr_comb_home = df.addr_comb_home.str.replace(' ', '')

# select valid data
# df = df[(df.date_report >= pd.to_datetime('2021-05-01')) & 
#             (df.date_report <= pd.to_datetime('2021-07-12'))]

df = df.drop_duplicates(
    subset=['name_full', 'sex', 'yob',
            'addr_dist_home', 'addr_ward_home', 'addr_home',
            'date_report']
)

df = df.drop(columns=['id_addiv', 'dw'])

# test auto id
# df['pidp1'] = df.date_report.dt.strftime('%y%m%d').astype('str')
# df['pidp2'] = df.index.astype('str').str.zfill(6).astype('str')
# df['pid'] = df['pidp1'] + df['pidp2']

# df.drop(columns=['pidp1', 'pidp2'], inplace=True)

# %% Export
df.to_csv(path.interim.joinpath('public-data.csv'), index=False, sep=',')
    