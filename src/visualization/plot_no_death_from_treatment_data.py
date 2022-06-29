# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

from src.config import path

# %%
df = pd.read_csv(
    path.processed / 'no-death-from-treatment-data' / 'no-death.csv'
)

# %%
df['date_report'] = pd.to_datetime(df['date_report'])

# %%
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(x[i], y[i] + 30, y[i].astype('int'), ha='center', va='top', rotation=90)

        
fig, ax = plt.subplots(figsize=(16,8))

ax.bar(df.date_report, df.no_death, label='So tu vong theo ngay', linewidth=3, alpha=0.5, color='gray')
ax.plot(df.date_report, df.no_death_rollmean7d, label='Bien dong trung binh', linewidth=3, color='black')

ax.set_ylabel('So tu vong')
ax.set_ylim([0, 500])
ax.set_xlabel('Ngay')
ax.set_xticks(df.date_report)
ax.tick_params(axis='x', labelrotation=90)
ax.set_title('So tu vong va bien dong trung binh 7 ngay')
ax.legend(loc='upper left')
addlabels(df.date_report, df.no_death)

filename = 'no-death.png'
output_path = path.processed / 'no-death-from-treatment-data' / 'image' / filename
plt.savefig(
        output_path,
        transparent = True)
plt.close(fig)
