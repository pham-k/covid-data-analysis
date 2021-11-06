# %%
import pandas as pd
import os

from src.config import path
# %%
rootdir = path.external / 'pcr-data'
current_date = '2021-11-02'

# %% Read yesterday data
usecols = ['id', 'id_patient', 'date_sample', 'sex', 'yob', 'reason', 'result',
         'addr_prov_home', 'addr_dist_home', 'addr_ward_home',
         'ct_e', 'ct_n', 'ct_rdrp', 'diag_proc', 'sample_type']
df = pd.read_csv(
    path.raw / 'pcr-data' / 'merge-2021-11-01.csv',
    usecols=usecols)

# %% Read today data
# test data from xuat ket qua xn tong
# df_today = pd.read_excel(
#     rootdir / (current_date + '.xlsx'),
#     header=1,
#     skiprows=4
# )

# test data from xuat ket qua chi tiet, since 17/09/2021
df_today_1 = pd.read_excel(
    rootdir / (current_date + '.xlsx')
)

df_today = df_today_1[[
    # 'Stt',
    # 'Họ và tên',
    # 'SDT',
    'Năm sinh',
    'CMND_CCCD_Passport',
    'Giới tính',
    'Phường/ Xã',
    'Quận / Huyện',
    'Tỉnh thành',
    'Kết quả',
    'CT-E',
    'CT-N',
    'CT-RdRp',
    'Kỹ thuật XN',
    'Lý do XN',
    'Loại mẫu XN',
    'Thời gian lấy mẫu',
    'Mã Xét Nghiệm', # rename to Ma XN
    # 'Đơn vị lấy mẫu',
    # 'Thời gian chuyển \n "phiên chuyển mẫu"', # rename to Da gui
    # 'Cơ sở được \n chuyển mẫu', # rename to gui toi don vi
    # 'Thời gian \n nhận mẫu', # rename to da nhan
    # 'Cơ sở \n xét nghiệm', # rename to don vi xet nghiem  
    # 'Thời gian có kết quả \n theo Hệ thống', # rename to thoi gian ket qua
]]

df_today.columns = df.columns
# %% Merge with today data
df = df.append(df_today)
# with open(path.reference.joinpath('col-name-test.txt'), 'r') as file:
#     df.columns = file.read().split('\n')
# %% Merge all
# !Do not uncomment unless you want to merge ALL FILES
 
# df = None
#
# for subdir, dirs, files in os.walk(rootdir):
#     for file in files:
#         data = pd.read_excel(
#             rootdir / file,
#             header=1,
#             skiprows=4
#         )
#         if df is None:
#             df = data
#         else:
#             df = df.append(data)

# %%
df.to_csv(
    path.raw / 'pcr-data' / ('merge-' + current_date + '.csv' ),
    index=False,
    sep=',')