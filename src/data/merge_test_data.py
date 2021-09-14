# %%
import pandas as pd
import os

from src.config import path


# %%
rootdir = path.external / 'test-data'
current_date = '2021-09-11'

# %%
df = pd.read_csv(path.raw / 'test-data' / 'test-merge-2021-09-10.csv')

# %% Read yesterday data
df_today = pd.read_excel(
    rootdir / (current_date + '.xlsx'),
    header=1,
    skiprows=4
)

# %% Merge with today data
df = df.append(df_today)
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
    path.raw / 'test-data' / ('test-merge-' + current_date + '.csv' ),
    index=False,
    sep=',')