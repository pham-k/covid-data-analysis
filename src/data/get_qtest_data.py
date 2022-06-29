# -*- coding: utf-8 -*-
import pandas as pd
import sys
sys.path.append('/home/kyo/Documents/script/covid-data-analysis/')
from src.config import path
import util
from datetime import date

# %% Import
usecols = ['id', 'date_sample', 'sex', 'yob', 'reason', 'result',
         'addr_prov_home', 'addr_dist_home', 'addr_ward_home', 'vaccinated']
raw = pd.read_csv(
    path.raw / 'qtest-data' / 'merge-2022-06-06.csv',
    usecols=usecols,
    dtype={
        # 'yob': int,
        'id': str,
        'sex': str,
        'reason': str,
        'result': str,
        'addr_prov_home': str,
        'addr_ward_home': str,
        'addr_dist_home': str,
        'vaccinated': str,
        'date_sample': str
    },
    # index_col='date_sample',
    # parse_dates=['date_sample']
)
pop = pd.read_csv(path.reference / 'pop_1.csv', sep=',', dtype={'id_addiv': 'str'})
addiv = pd.read_csv(path.reference / 'addiv.csv', sep=',', dtype={'id_addiv': 'str', 'of_addiv': 'str'})
# %% Rename columns
# with open(path.reference.joinpath('col-name-test.txt'), 'r') as file:
#     raw.columns = file.read().split('\n')
    
# raw = raw[['id', 'id_patient', 'date_sample', 'sex', 'yob', 'reason', 'result',
#          'addr_prov_home', 'addr_dist_home', 'addr_ward_home',
#          'ct_e', 'ct_n', 'ct_rdrp', 'diag_proc', 'sample_type']]
# %% Dedup
raw = raw.drop_duplicates(['id'])
# dup = raw[raw.duplicated(['id'])]
# %% Preprocess
raw.loc[raw.yob == ' ', 'yob'] = None
raw['yob'] = raw.yob.str[-4:]
raw['yob'] = raw['yob'].astype('float')
df = raw.assign(
    sex = raw.sex.astype('str').apply(util.preprocess_string),
    reason = raw.reason.astype('str').apply(util.preprocess_string),
    vaccinated = raw.vaccinated.astype('str').apply(util.preprocess_string),
    result = raw.result.astype('str').apply(util.preprocess_string),
    addr_ward_home = raw.addr_ward_home.astype('str').apply(util.preprocess_addr_ward),
    addr_dist_home = raw.addr_dist_home.astype('str').apply(util.preprocess_string),
    addr_prov_home = raw.addr_prov_home.astype('str').apply(util.preprocess_string),
    date_sample = raw.date_sample.astype('str').apply(lambda x: x[0:10]),
    age = date.today().year - raw.yob,
)
# %% Fix addr_dist_home = 'THANH PHO THU DUC'
# Create temporary col adh = addr_dist_home
df['adh'] = df.addr_dist_home

# Some addr_dist_home = 'THANH PHO THU DUC'
# Fix district by mapping addr_ward_home to valid district
df.loc[df.addr_ward_home.isin([
    'THAO DIEN', 'THU THIEM', 'THANH MY LOI', 'CAT LAI', 'BINH TRUNG TAY',
    'BINH TRUNG DONG', 'BINH KHANH', 'BINH AN', 'AN PHU', 'AN LOI DONG',
    'AN KHANH'
]), 'adh'] = 'QUAN 02'

df.loc[df.addr_ward_home.isin([
    'BINH CHIEU', 'BINH THO', 'HIEP BINH CHANH', 'HIEP BINH PHUOC',
    'LINH CHIEU', 'LINH DONG', 'LINH TAY', 'LINH TRUNG', 'LINH XUAN',
    'TAM BINH', 'TAM PHU', 'TRUONG THO'
]), 'adh'] = 'QUAN THU DUC'

df.loc[df.addr_ward_home.isin([
    'HIEP PHU', 'LONG BINH', 'LONG PHUOC', 'LONG THANH MY', 'LONG TRUONG',
    'PHU HUU', 'PHUOC BINH', 'PHUOC LONG A', 'PHUOC LONG B', 'TAN PHU',
    'TANG NHON PHU A', 'TANG NHON PHU B', 'TRUONG THANH'
]), 'adh'] = 'QUAN 09'

# fix district name
df.loc[df.addr_dist_home == 'QUAN 1', 'adh'] = 'QUAN 01'
df.loc[df.addr_dist_home == 'QUAN 2', 'adh'] = 'QUAN 02'
df.loc[df.addr_dist_home == 'QUAN 3', 'adh'] = 'QUAN 03'
df.loc[df.addr_dist_home == 'QUAN 4', 'adh'] = 'QUAN 04'
df.loc[df.addr_dist_home == 'QUAN 5', 'adh'] = 'QUAN 05'
df.loc[df.addr_dist_home == 'QUAN 6', 'adh'] = 'QUAN 06'
df.loc[df.addr_dist_home == 'QUAN 7', 'adh'] = 'QUAN 07'
df.loc[df.addr_dist_home == 'QUAN 8', 'adh'] = 'QUAN 08'
df.loc[df.addr_dist_home == 'QUAN 9', 'adh'] = 'QUAN 09'

# Drop old col and replace by fixed col
df = df.drop(columns=['addr_dist_home'])
df = df.rename(columns={'adh': 'addr_dist_home'})

# Change all province, district 
# with addr_prov_home != TPHCM to "KHAC", 
mask_addr = (
    (df.addr_prov_home != 'THANH PHO HO CHI MINH')
    | (df.addr_dist_home == 'THANH PHO DI AN')
    | (df.addr_dist_home == 'THANH PHO THUAN AN')
    | (df.addr_dist_home == 'THANH PHO THANH HOA')
)

df.loc[mask_addr, 'addr_prov_home'] = 'KHAC'
df.loc[mask_addr, 'addr_dist_home'] = 'KHAC'

# %% Encode province, district, ward
# df1 = df
df['addr_dist_home'] = df['addr_dist_home'].apply(util.encode_addr_dist)
df['addr_prov_home'] = df['addr_prov_home'].apply(util.encode_addr_prov)

# combine name of dist and ward
df['dw'] = df.addr_dist_home + ' ' + df.addr_ward_home

# merge with addiv
df = df.merge(addiv[['dw', 'id_addiv']], how = 'left', on= 'dw' )
df['addr_ward_home'] = df.id_addiv
df = df.drop(columns=['id_addiv', 'dw'])

# %% Export
df.to_csv(path.interim.joinpath('qtest-data.csv'), index=False, sep=',')



