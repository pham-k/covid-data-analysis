# -*- coding: utf-8 -*-
import pandas as pd
from datetime import date

from src.config import path
from src.data import util_test as ut


# %% Import
usecols = ['id', 'id_patient', 'date_sample', 'sex', 'yob', 'reason', 'result',
         'addr_prov_home', 'addr_dist_home', 'addr_ward_home',
         'ct_e', 'ct_n', 'ct_rdrp', 'sample_type']
raw = pd.read_csv(
    path.raw / 'pcr-data' / 'merge-2021-09-28.csv',
    usecols = usecols)

# %% Rename columns
# with open(path.reference.joinpath('col-name-test.txt'), 'r') as file:
#     raw.columns = file.read().split('\n')
    
# raw = raw[['id', 'date_sample', 'sex', 'yob', 'reason', 'result',
#          'addr_prov_home', 'addr_dist_home', 'addr_ward_home',
#          'ct_e', 'ct_n', 'ct_rdrp', 'sample_type']]
# %% Dedup
raw = raw.drop_duplicates(['id', 'id_patient'])
# dup = raw[raw.duplicated(['id', 'id_patient'])]
# raw.drop(columns=['id', 'id_patient'], inplace=True)
# %% Preprocess
df = raw.assign(
    sex = raw.sex.astype('str').apply(ut.preprocess_string),
    reason = raw.reason.astype('str').apply(ut.preprocess_string),
    result = raw.result.astype('str').apply(ut.preprocess_string),
    addr_ward_home = raw.addr_ward_home.astype('str').apply(ut.preprocess_string),
    addr_dist_home = raw.addr_dist_home.astype('str').apply(ut.preprocess_string),
    addr_prov_home = raw.addr_prov_home.astype('str').apply(ut.preprocess_string),
    date_sample = raw.date_sample.astype('str').apply(lambda x: x[0:10]),
    age = date.today().year - raw.yob,
    sample_type = raw.sample_type.astype('str').apply(ut.preprocess_string)
)

# Create age_group
df['age_group'] = pd.cut(
    df.age,
    bins = [0, 17, 45, 65, 200],
    labels = ['0 - 16', '17 - 44', '45 - 64', '> 65'],
    right = False
)

# Create positive (binary var used for counting) 
df.date_sample = pd.to_datetime(
    df.date_sample, 
    format='%d/%m/%Y',
    errors='coerce')

df['positive'] = df.result == 'DUONG TINH'
df['positive_group_sample'] = ((df.result == 'DUONG TINH') 
                               & (df.sample_type == 'MAU GOP'))
# %% Fix addr_dist_home = 'THANH PHO THU DUC'
# Create temporary col adh = addr_dist_home
df['adh'] = df.addr_dist_home

# Some addr_dist_home = 'THANH PHO THU DUC'
# Fix district by mapping addr_ward_home to valid district
df.loc[df.addr_ward_home.isin([
    'PHUONG THAO DIEN', 'PHUONG THU THIEM', 'PHUONG THANH MY LOI', 'PHUONG CAT LAI', 'PHUONG BINH TRUNG TAY',
    'PHUONG BINH TRUNG DONG', 'PHUONG BINH KHANH', 'PHUONG BINH AN', 'PHUONG AN PHU', 'PHUONG AN LOI DONG',
    'PHUONG AN KHANH'
]), 'adh'] = 'QUAN 02'

df.loc[df.addr_ward_home.isin([
    'PHUONG BINH CHIEU', 'PHUONG BINH THO', 'PHUONG HIEP BINH CHANH', 'PHUONG HIEP BINH PHUOC',
    'PHUONG LINH CHIEU', 'PHUONG LINH DONG', 'PHUONG LINH TAY', 'PHUONG LINH TRUNG', 'PHUONG LINH XUAN',
    'PHUONG TAM BINH', 'PHUONG TAM PHU', 'PHUONG TRUONG THO'
]), 'adh'] = 'QUAN THU DUC'

df.loc[df.addr_ward_home.isin([
    'PHUONG HIEP PHU', 'PHUONG LONG BINH', 'PHUONG LONG PHUOC', 'PHUONG LONG THANH MY', 'PHUONG LONG TRUONG',
    'PHUONG PHU HUU', 'PHUONG PHUOC BINH', 'PHUONG PHUOC LONG A', 'PHUONG PHUOC LONG B', 'PHUONG TAN PHU',
    'PHUONG TANG NHON PHU A', 'PHUONG TANG NHON PHU B', 'PHUONG TRUONG THANH'
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

# %% !DEPRECATED ct
# data_in_get_no_test = (
#     df[(~df.reason.str.startswith('KIEM DICH'))
#        &(~df.reason.str.contains('THEO DOI'))] # remove reason KIEM DICH
#     [['date_sample', 'id']]
# )

# data_in_get_no_positive = (
#     df[(~df.reason.str.startswith('KIEM DICH'))
#        &(~df.reason.str.contains('THEO DOI'))] # remove reason KIEM DICH
#     [['date_sample', 'positive']]
# )

# data_in_get_no_positive_group_sample = (
#     df[(~df.reason.str.startswith('KIEM DICH'))
#        &(~df.reason.str.contains('THEO DOI'))] # remove reason KIEM DICH
#     [['date_sample', 'positive_group_sample']]
# )

# no_test = ut.get_no_test(data_in_get_no_test)
# no_positive = ut.get_no_positive(data_in_get_no_positive)
# no_positive_group_sample = (
#     ut.get_no_positive_group_sample(
#         data_in_get_no_positive_group_sample))
# ct = ut.get_ct_from_test_data(no_test, no_positive, no_positive_group_sample)
# ct = (
#     ct.reset_index()
#     .rename(columns={'index': 'date_sample'})
# )

# %% Get ct by addr_ward_home
data_in_get_no_test_by_group_awh = (
    df[(~df.reason.str.startswith('KIEM DICH'))
       &(~df.reason.str.contains('THEO DOI'))] # remove reason KIEM DICH
    .query('addr_prov_home == "THANH PHO HO CHI MINH"')
    [['date_sample', 'addr_dist_home', 'addr_ward_home']]
    [(df.addr_dist_home  != 'NAN') & (df.addr_prov_home  != 'NAN') & (df.addr_ward_home  != 'NAN')]
)

# Number of test by date_sample and addr_ward_home
no_test_by_awh = ut.get_no_test_by_group(data_in_get_no_test_by_group_awh,
                                       group = ['addr_dist_home', 'addr_ward_home'])

data_in_get_no_positive_by_group_awh = (
    df[(~df.reason.str.startswith('KIEM DICH'))
       &(~df.reason.str.contains('THEO DOI'))] # remove reason KIEM DICH
    .query('addr_prov_home == "THANH PHO HO CHI MINH"')
    [['date_sample', 'addr_dist_home', 'addr_ward_home', 'positive']]
    [(df.addr_dist_home  != 'NAN') & (df.addr_prov_home  != 'NAN') & (df.addr_ward_home  != 'NAN')]
)

# Number of positive result by date_sample and addr_ward_home
no_positive_by_awh = ut.get_no_positive_by_group(data_in_get_no_positive_by_group_awh,
                                               group = ['addr_dist_home', 'addr_ward_home'])

data_in_get_no_positive_group_sample_by_group_awh = (
    df[(~df.reason.str.startswith('KIEM DICH'))
       &(~df.reason.str.contains('THEO DOI'))] # remove reason KIEM DICH
    .query('addr_prov_home == "THANH PHO HO CHI MINH"')
    [['date_sample', 'addr_dist_home', 'addr_ward_home', 'positive_group_sample']]
    [(df.addr_dist_home  != 'NAN') & (df.addr_prov_home  != 'NAN') & (df.addr_ward_home  != 'NAN')]
)

no_positive_group_sample_by_awh = (
    ut.get_no_positive_group_sample_by_group(
        data_in_get_no_positive_group_sample_by_group_awh,
        group = ['addr_dist_home', 'addr_ward_home']))

# CT by percentage of positive per 7d by addr_ward_home
ct_by_awh = ut.get_ct_by_group_from_test_data(
    no_test_by_awh, no_positive_by_awh, no_positive_group_sample_by_awh,
    group = ['addr_dist_home', 'addr_ward_home'])

# %% !DEPRECATED Get ct by addr_dist_home

data_in_get_no_test_by_group_adh = (
    df[(~df.reason.str.startswith('KIEM DICH'))
        &(~df.reason.str.contains('THEO DOI'))] # remove reason KIEM DICH
    .query('addr_prov_home == "THANH PHO HO CHI MINH"')
    [['date_sample', 'addr_dist_home']]
    [(df.addr_dist_home  != 'NAN') & (df.addr_dist_home  != 'THANH PHO THU DUC') & (df.addr_prov_home  != 'NAN')]
)

# Number of test by date_sample and addr_dist_home
no_test_by_adh = ut.get_no_test_by_group(data_in_get_no_test_by_group_adh,
                                        group = ['addr_dist_home'])

data_in_get_no_positive_by_group_adh = (
    df[(~df.reason.str.startswith('KIEM DICH'))
        &(~df.reason.str.contains('THEO DOI'))] # remove reason KIEM DICH
    .query('addr_prov_home == "THANH PHO HO CHI MINH"')
    [['date_sample', 'addr_dist_home', 'positive']]
    [(df.addr_dist_home  != 'NAN') & (df.addr_dist_home  != 'THANH PHO THU DUC') & (df.addr_prov_home  != 'NAN')]
)

# Number of positive result by date_sample and addr_dist_home
no_positive_by_adh = ut.get_no_positive_by_group(data_in_get_no_positive_by_group_adh,
                                                group = ['addr_dist_home'])

data_in_get_no_positive_group_sample_by_group_adh = (
    df[(~df.reason.str.startswith('KIEM DICH'))
        &(~df.reason.str.contains('THEO DOI'))] # remove reason KIEM DICH
    .query('addr_prov_home == "THANH PHO HO CHI MINH"')
    [['date_sample', 'addr_dist_home', 'positive_group_sample']]
    [(df.addr_dist_home  != 'NAN') & (df.addr_dist_home  != 'THANH PHO THU DUC') & (df.addr_prov_home  != 'NAN')]
)

no_positive_group_sample_by_adh = (
    ut.get_no_positive_group_sample_by_group(
        data_in_get_no_positive_group_sample_by_group_adh,
        group = ['addr_dist_home']))

# CT by percentage of positive per 7d by addr_dist_home
ct_by_adh = (
    ut.get_ct_by_group_from_test_data(
        no_test_by_adh, no_positive_by_adh, no_positive_group_sample_by_adh,
        group = ['addr_dist_home']))

# %% Get ct by age_group
data_in_get_no_test_by_group_ag = (
    df[(~df.reason.str.startswith('KIEM DICH'))
       &(~df.reason.str.contains('THEO DOI'))] # remove reason KIEM DICH
    .query('addr_prov_home == "THANH PHO HO CHI MINH"')
    [['date_sample', 'age_group']]
    [(df.age_group  != 'NAN')]
)

# Number of test by date_sample and age_group
no_test_by_ag = ut.get_no_test_by_group(data_in_get_no_test_by_group_ag,
                                       group = ['age_group'])

data_in_get_no_positive_by_group_ag = (
    df[(~df.reason.str.startswith('KIEM DICH'))
       &(~df.reason.str.contains('THEO DOI'))] # remove reason KIEM DICH
    .query('addr_prov_home == "THANH PHO HO CHI MINH"')
    [['date_sample', 'age_group', 'positive']]
    [(df.age_group  != 'NAN')]
)

# Number of positive result by date_sample and age_group
no_positive_by_ag = (
    ut.get_no_positive_by_group(
        data_in_get_no_positive_by_group_ag,
        group = ['age_group'])
)

data_in_get_no_positive_group_sample_by_group_ag = (
    df[(~df.reason.str.startswith('KIEM DICH'))
       &(~df.reason.str.contains('THEO DOI'))] # remove reason KIEM DICH
    .query('addr_prov_home == "THANH PHO HO CHI MINH"')
    [['date_sample', 'age_group', 'positive_group_sample']]
    [(df.age_group  != 'NAN')]
)

# Number of positive result by date_sample and age_group
no_positive_group_sample_by_ag = (
    ut.get_no_positive_group_sample_by_group(
        data_in_get_no_positive_group_sample_by_group_ag,
        group = ['age_group']))

# CT by percentage of positive per 7d by age_group
ct_by_ag = (
    ut.get_ct_by_group_from_test_data(
        no_test_by_ag, no_positive_by_ag, no_positive_group_sample_by_ag,
        group = ['age_group']))

# %% Get ct by sex
data_in_get_no_test_by_group_sex = (
    df[(~df.reason.str.startswith('KIEM DICH'))
       &(~df.reason.str.contains('THEO DOI'))] # remove reason KIEM DICH
#     .query('addr_prov_home == "THANH PHO HO CHI MINH"')
    [['date_sample', 'sex']]
    [(df.sex  != 'NAN')]
)

# Number of test by date_sample and sex
no_test_by_sex = ut.get_no_test_by_group(data_in_get_no_test_by_group_sex,
                                       group = ['sex'])

data_in_get_no_positive_by_group_sex = (
    df[(~df.reason.str.startswith('KIEM DICH'))
       &(~df.reason.str.contains('THEO DOI'))] # remove reason KIEM DICH
#     .query('addr_prov_home == "THANH PHO HO CHI MINH"')
    [['date_sample', 'sex', 'positive']]
    [(df.sex  != 'NAN')]
)

# Number of positive result by date_sample and sex
no_positive_by_sex = ut.get_no_positive_by_group(data_in_get_no_positive_by_group_sex,
                                               group = ['sex'])

data_in_get_no_positive_group_sample_by_group_sex = (
    df[(~df.reason.str.startswith('KIEM DICH'))
       &(~df.reason.str.contains('THEO DOI'))] # remove reason KIEM DICH
#     .query('addr_prov_home == "THANH PHO HO CHI MINH"')
    [['date_sample', 'sex', 'positive_group_sample']]
    [(df.sex  != 'NAN')]
)

# Number of positive result by date_sample and sex
no_positive_group_sample_by_sex = (
    ut.get_no_positive_group_sample_by_group(
        data_in_get_no_positive_group_sample_by_group_sex,
        group = ['sex'])
)

# CT by percentage of positive per 7d by sex
ct_by_sex = (
    ut.get_ct_by_group_from_test_data(
        no_test_by_sex, no_positive_by_sex, no_positive_group_sample_by_sex,
        group = ['sex'])
    )

# %% Summary ct
ct_summary_by_sex = (
    df[['sex', 'ct_e', 'ct_n', 'ct_rdrp']]
    .groupby('sex')
    .describe()
    .transpose()
    .reset_index()
    .rename(columns={
        'level_0': 'var',
        'level_1': 'statistics'
    })
)
# %% Export
# ct.to_csv(path.processed / 'ct-from-test-data' / 'ct.csv', index=False)
ct_by_awh.to_csv(path.processed / 'ct-by-group-from-pcr-data' / 'ct-by-awh.csv', index=False)
ct_by_adh.to_csv(path.processed / 'ct-by-group-from-pcr-data' / 'ct-by-adh.csv', index=False)
ct_by_ag.to_csv(path.processed / 'ct-by-group-from-pcr-data' / 'ct-by-ag.csv', index=False)
ct_by_sex.to_csv(path.processed / 'ct-by-group-from-pcr-data' / 'ct-by-sex.csv', index=False)
ct_summary_by_sex.to_csv(path.processed / 'ct-by-group-from-pcr-data' / 'ct-summary-by-sex.csv', index=False)

