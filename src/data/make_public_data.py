# %%
import pandas as pd
import pathlib
from config import path
import data.util as util

# %%
# import data
shdf = pd.read_csv(
    path.raw.joinpath('shift', 'shift-2021-07-01.csv'),
    sep=';'
    ).iloc[:,0:20]

# %%
pbdf = pd.read_csv(
    path.raw.joinpath('public', 'public-2021-07-11.csv')
    # sep=';'
    )
# %% Shift

# * fix input

# fix report 22/06
shdf.iloc[1663:1704,0] = '22/06'
shdf.iloc[826,0] = '16/06'
shdf.iloc[1777:1779,0] = '23/06'

# fix yob
shdf[shdf.iloc[:,4] == '978'] = 1978
shdf[shdf.iloc[:,4] == '19678'] = 1978

# rename
with open(path.reference.joinpath('col-name-shift.txt'), 'r') as file:
    shdf.columns = file.read().split('\n')

# wrangle
shdf = shdf.assign(
    date_report = shdf['report'].astype('str').apply(util.compute_date_report),
    name_full = shdf['name_full'].astype('str').apply(util.clean_name_full),
    addr_dist_home = shdf['addr_dist_home'].apply(util.encode_addr_dist),
    yob = shdf['yob'].str[-4:],
    sex = shdf['sex'].str.upper().str.strip(),
    result_1 = shdf['result_1'].str.upper().str.strip().str.extract(r'(^[ÂD])'),
    result_2 = shdf['result_2'].str.upper().str.strip().str.extract(r'(^[ÂD])'),
    result_3 = shdf['result_3'].str.upper().str.strip().str.extract(r'(^[ÂD])'),
    result_4 = shdf['result_4'].str.upper().str.strip().str.extract(r'(^[ÂD])'),
    result_5 = shdf['result_5'].str.upper().str.strip().str.extract(r'(^[ÂD])')
)

shdf['date_positive'] = shdf.apply(util.compute_date_positive, axis=1)

# remove dup
shdf = shdf.drop_duplicates(
    subset=['name_full', 'sex', 'yob', 'addr_dist_home', 'date_report']
)

# remove uneccessary col
shdf.drop(
    columns=['report', 'tel', 'addr_home', 'addr_ward_home', 'no',
             'date_test_1', 'result_1', 'date_test_2', 'result_2',
             'date_test_3', 'result_3', 'date_test_4', 'result_4',
             'date_test_5', 'result_5', 'addr_work'],
    inplace=True
)

# export to csv
shdf.to_csv(path.interim.joinpath('shift.csv'), index=False)

# %%
with open(path.reference.joinpath('col-name-public.txt'), 'r') as file:
    pbdf.columns = file.read().split('\n')
    
# pbdf = pbdf[['name_full', 'sex', 'yob', 'addr_dist_home',
#              'date_report', 'date_positive']]

pbdf = pbdf.assign(
    date_report = pd.to_datetime(
        pbdf['date_report'].astype('str').apply(util.compute_date_report),
        errors='coerce',
        format='%d/%m/%Y'
        ),
    name_full = pbdf['name_full'].astype('str').apply(util.clean_name_full),
    sex = pbdf['sex'].str.upper().str.strip(),
    addr_dist_home = pbdf['addr_dist_home'].apply(util.encode_addr_dist),
    date_positive = pd.to_datetime(
        pbdf['date_positive'].astype('str'),
        errors='coerce',
        format='%d/%m/%Y'
        )
    )

# select valid data
# pbdf = pbdf[(pbdf.date_report >= pd.to_datetime('2021-05-01')) & 
#             (pbdf.date_report <= pd.to_datetime('2021-07-12'))]

pbdf = pbdf.drop_duplicates(
    subset=['name_full', 'sex', 'yob', 'addr_dist_home', 'date_report']
)

# create increment id
# pbdf.insert(0, 'id_patient_new', range(len(pbdf)))

# export to csv
pbdf.to_csv(path.interim.joinpath('public.csv'), index=False)