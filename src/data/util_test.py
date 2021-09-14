# -*- coding: utf-8 -*-

import re
import unidecode
import pandas as pd

# Preprocess data

def preprocess_string(row):
    s = unidecode.unidecode(row).upper().strip()
    return s

def preprocess_addr(row):
    p = row.addr_prov_home
    d = row.addr_dist_home
    w = row.addr_ward_home
    
# get ct from test data

def get_no_test(data):
    df = (
        data.groupby(['date_sample'])
        .size()
        .to_frame(name='no_test')
        .reindex(pd.date_range(start=data.date_sample.min(), end=data.date_sample.max(), freq='D'))
        .fillna(0)
    )
    return df

def get_no_positive(data):
    df = (
        data.groupby(['date_sample', 'positive'])
        .apply(lambda x: len(x))
        .to_frame(name='no_positive')
        .reset_index()
        .query('positive == True')
        .set_index('date_sample')
        [['no_positive']]
        .reindex(pd.date_range(start=data.date_sample.min(), end=data.date_sample.max(), freq='D'))
        .fillna(0)
    )
    return df

def get_no_positive_group_sample(data):
    df = (
        data.groupby(['date_sample', 'positive_group_sample'])
        .apply(lambda x: len(x))
        .to_frame(name='no_positive_group_sample')
        .reset_index()
        .query('positive_group_sample == True')
        .set_index('date_sample')
        [['no_positive_group_sample']]
        .reindex(pd.date_range(start=data.date_sample.min(), end=data.date_sample.max(), freq='D'))
        .fillna(0)
    )
    return df

def get_ct_from_test_data(data_no_test, data_no_positive, data_no_positive_group_sample,
                          bins = [0, 0.02, 0.05, 0.20, 1.01], labels = [1, 2, 3, 4], right = False,
                          rolling = 7):
    df = data_no_test.join(data_no_positive, how='left')
    df = df.join(data_no_positive_group_sample, how='left')
    df['no_test_corrected'] = df.no_test - df.no_positive_group_sample
    df['pct_positive'] = df.no_positive / df.no_test_corrected
    df['pct_positive'] = df.pct_positive.fillna(0)
    df['no_test_rollsum'] = df.no_test_corrected.rolling(rolling).sum()
    df['no_positive_rollsum'] = df.no_positive.rolling(rolling).sum()
    df[('pct_positive_per' + str(rolling) + 'd')] = df.no_positive_rollsum / df.no_test_rollsum
    df[('pct_positive_per' + str(rolling) + 'd')] = df[('pct_positive_per' + str(rolling) + 'd')].fillna(0)

    # calculate ct
    df['ct'] = pd.cut(
        df[('pct_positive_per' + str(rolling) + 'd')],
        bins = bins,
        labels = labels,
        right = right)
    
    return df

# get ct by group from test data
    
def get_no_test_by_group(data, group=[]):
    df_1 = (
        data.groupby(['date_sample'] + group)
        .size()
        .to_frame(name='no_test')
        .reset_index()
    )
    
    df_pv = df_1.pivot(
        index = 'date_sample',
        columns = group,
        values = 'no_test'
    ).fillna(0)
    
    df_2 = (
        df_pv.reindex(pd.date_range(
            start=df_pv.index.min(),
            end=df_pv.index.max(),
            freq='D'))
        .fillna(0)
        .stack(list(range(0, len(group))))
        .reset_index()
        .rename(columns={
            'level_0': 'date_sample',
            0: 'no_test'
        })
        .set_index(['date_sample'] + group)
    )
    
    return df_2

def get_no_positive_by_group(data, group=[]):
    df_1 = (
        data.groupby(['date_sample', 'positive'] + group)
        .apply(lambda x: len(x))
        .to_frame(name='no_positive')
        .reset_index()
        .query('positive == True')
        .drop(columns=['positive'])
    )
    
    df_pv = df_1.pivot(
        index = 'date_sample',
        columns = group,
        values = 'no_positive'
    ).fillna(0)
    
    df_2 = (
        df_pv
        .reindex(pd.date_range(
            start=df_pv.index.min(),
            end=df_pv.index.max(),
            freq='D'))
        .fillna(0)
        .stack(list(range(0, len(group))))
        .reset_index()
        .rename(columns={
            'level_0': 'date_sample',
            0: 'no_positive'
        })
        .set_index(['date_sample'] + group)
    )
    
    return df_2

def get_no_positive_group_sample_by_group(data, group=[]):
    df_1 = (
        data.groupby(['date_sample', 'positive_group_sample'] + group)
        .apply(lambda x: len(x))
        .to_frame(name='no_positive_group_sample')
        .reset_index()
        .query('positive_group_sample == True')
        .drop(columns=['positive_group_sample'])
    )
    
    df_pv = df_1.pivot(
        index = 'date_sample',
        columns = group,
        values = 'no_positive_group_sample'
    ).fillna(0)
    
    df_2 = (
        df_pv
        .reindex(pd.date_range(
            start=df_pv.index.min(),
            end=df_pv.index.max(),
            freq='D'))
        .fillna(0)
        .stack(list(range(0, len(group))))
        .reset_index()
        .rename(columns={
            'level_0': 'date_sample',
            0: 'no_positive_group_sample'
        })
        .set_index(['date_sample'] + group)
    )
    
    return df_2

def get_ct_by_group_from_test_data(data_no_test, data_no_positive, data_no_positive_group_sample,
                          bins = [0, 0.02, 0.05, 0.20, 1.01], labels = [1, 2, 3, 4], right = False,
                          rolling = 7, group = []):
    df = data_no_test.join(data_no_positive, how = 'left')
    df = (
        df.join(data_no_positive_group_sample, how = 'left')
        .fillna(0).reset_index()
    )
    df['no_test_corrected'] = df['no_test'] - df['no_positive_group_sample']
    df['pct_positive'] = df.no_positive / df.no_test_corrected
    df['pct_positive'] = df['pct_positive'].fillna(0)

    df['no_test_rollsum'] = (
        df[['date_sample', 'no_test_corrected'] + group]
        .groupby(group)['no_test_corrected']
        .transform(lambda x: x.rolling(rolling).sum())
    )

    df['no_positive_rollsum'] = (
        df[['date_sample', 'no_positive'] + group]
        .groupby(group)['no_positive']
        .transform(lambda x: x.rolling(rolling).sum())
    )

    df[('pct_positive_per' +str(rolling) + 'd')] = df.no_positive_rollsum / df.no_test_rollsum
    df[('pct_positive_per' +str(rolling) + 'd')] = df[('pct_positive_per' +str(rolling) + 'd')].fillna(0)

    df['ct'] = pd.cut(
        df[('pct_positive_per' +str(rolling) + 'd')],
        bins = bins,
        labels = labels,
        right = right)
    
    return df