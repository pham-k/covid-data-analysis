# -*- coding: utf-8 -*-

import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
import pandas as pd
import pathlib
from config import path
import data.util as util
import networkx as nx
import re

# %%
df = pd.read_csv(
    path.interim.joinpath('public.csv')
    # sep=';'
    )

# %%
def foo(row):
    pattern = r'[\d]{1,5}'
    s = re.search(pattern, row)
    if s != None:
        return s.group()
    else:
        return ""

# %%
df = df.assign(
    id_patient = df.id_patient.apply(foo),
    cntt_case_2 = df.cntt_case_2.astype('str').apply(foo)
    )

# df1 = df.iloc[0:50,:]
# %%
nodes = df1.id_patient.to_numpy()
edges = list(df1[['cntt_case_2', 'id_patient']].itertuples(index=False, name=None))

# %%
# print(df1.value_counts('id_patient'))

# %%
g = nx.Graph()

g.add_nodes_from(nodes)

g.add_edges_from(edges)

nx.draw(g)

# %%

fig = go.Figure(data=[edges, nodes],
              layout=go.Layout(
                title='<br>Network graph made with Python',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
fig.show()
