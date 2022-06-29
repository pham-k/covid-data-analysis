# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from config import path
import os

# %%
def plot_heatmap(df, title):
    row = df.index.to_numpy()
    col = df.columns.to_numpy()

    fig, ax = plt.subplots(figsize=(12, 12))
    im = ax.imshow(df, alpha=0.6, cmap='Greens')

#     plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = True
#     plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = False
    ax.set_xticks(np.arange(len(col)))
    ax.set_yticks(np.arange(len(row)))

    ax.set_xticklabels(col)
    ax.set_yticklabels(row)
#     ax.set_yticklabels(df.index.strftime('%d-%m'))

    plt.setp(
        ax.get_xticklabels(),
        rotation=90,
        ha="right",
        rotation_mode="anchor"
    )

#     Loop over data dimensions and create text annotations.
    for i in range(len(row)):
        for j in range(len(col)):
            text = ax.text(j, i, df.iloc[i, j],
                           ha="center", va="center", color="black")

    ax.set_title(title)
    fig.tight_layout()
    plt.savefig(
        path.interim / 'ct_redcap_awh_image' / (title + '.png'),
        transparent = True)
    plt.close(fig)


# %%
rootdir = path.interim / 'ct_redcap_awh'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        # print(path.interim / 'ct_who_awh' / file)
        df = pd.read_csv(
            os.path.join(subdir, file),
            index_col='date_report')
        plot_heatmap(df, file)