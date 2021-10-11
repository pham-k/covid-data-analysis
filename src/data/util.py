#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 09:16:26 2021

@author: kyo
"""

import re
import unidecode
import pandas as pd

def preprocess_string(row):
    s = unidecode.unidecode(row).upper().strip()
    return s

def clean_place_recognize(row):
    s = row.upper().strip()
    return unidecode.unidecode(s)

def clean_sex(row):
    s = row.upper().strip()
    return unidecode.unidecode(s)

def clean_name_full(row):
    name_full = row.upper()
    # pattern = r'(^|[^\(])([\w\s]+)'
    pattern = r'([^\(=]+)'
    s = re.search(pattern, name_full)
    if s == None:
        return ''
    else:
        return s.group().strip()

# print(clean_name_full('Nguyễn A => Nguyễn A'))
# clean_name_full('')


def compute_date_report(row):
    pattern = r'[\d]{1,2}(?:/|-)[\d]{1,2}'
    s = re.search(pattern, row)
    if s != None:
        return s.group().replace('-', '/').replace('/6', '/06') + '/2021'
    else:
        return ""
    

def compute_date_positive(row):
    if row.result_1 == 'D':
        return str(row.date_test_1)[0:11]
    elif row.result_2 == 'D':
        return str(row.date_test_2)[0:11]
    elif row.result_3 == 'D':
        return str(row.date_test_3)[0:11]
    elif row.result_4 == 'D':
        return str(row.date_test_4)[0:11]
    elif row.result_5 == 'D':
        return str(row.date_test_5)[0:11]
    

def preprocess_addr_ward(row):
    s = row.strip().upper();
    s = unidecode.unidecode(s)
    s = (s.replace('(', '')
          .replace(')', '')
          # .replace(',', '')
          .replace('.', '')
          .replace(';', '')
          .replace('PHUONG', '')
          .replace('XA', '')
          .strip()
        )
    if s in ['1', '01']:
        s = '1'
    elif s in ['2', '02']:
        s = '2'
    elif s in ['3', '03']:
        s = '3' 
    elif s in ['4', '04']:
        s = '4'
    elif s in ['5', '05']:
        s = '5'
    elif s in ['6', '06']:
        s = '6' 
    elif s in ['7', '07']:
        s = '7'
    elif s in ['8', '08']:
        s = '8'
    elif s in ['9', '09']:
        s = '9'
    return s


def compute_addr_x(row):
    s = row.strip().upper();
    s = (s.replace('(', '')
          .replace(')', '')
          # .replace(',', '')
          .replace('.', '')
          .replace(';', '')
        )
    return unidecode.unidecode(s)
    
    
def encode_addr_dist(row):
    d = str(row).upper().strip()
    if d in ['760', 'QA01', '1', '01', 'QUẬN 1', 'QUAN 01',
             'BẾN NGHÉ', 'TÂN ĐỊNH', 'NGUYỄN CƯ TRINH']:
        return '760'
    elif d in ['769', 'QA02', '2', '02', 'QUẬN 2', 'QUAN 02']:
        return '769'
    elif d in ['770', 'QA03', '3', '03', 'QUAN 03']:
        return '770'
    elif d in ['773', 'QA04', '4', '04', 'QUAN 04']:
        return '773'
    elif d in ['774', 'QA05', '5', '05', 'QUAN 05']:
        return '774'
    elif d in ['775', 'QA06', '6', '06', 'QUẬN 6', 'QUAN 06']:
        return '775'
    elif d in ['778', 'QA07', '7', '07', 'QUAN 07']:
        return '778'
    elif d in ['776', 'QA08', '8', '08', 'QUẬN 8', 'QUAN 08']:
        return '776'
    elif d in ['763', 'QA09', '9', '09', 'QUẬN 9', 'QUAN 09']:
        return '763'
    elif d in ['771', 'QA10', '10', 'QUẬN 10', 'QUAN 10']:
        return '771'
    elif d in ['772', 'QA11', '11', 'QUẬN 11', 'QUAN 11']:
        return '772'
    elif d in ['761', 'QA12', '12', 'Q12', 'TÂN THỚI NHẤT', 'QUAN 12']:
        return '761'
    elif d in ['764', 'QGVP', 'GÒ VẤP', 'GO VAP', 'QUAN GO VAP']:
        return '764'
    elif d in ['QHMN', 'HÓC MÔN', 'HOC MON', 'THÁI TAM THÂN',
               'XUÂN THỚI THƯỢNG', 'HUYEN HOC MON']:
        return '784'
    elif d in ['787', 'QCGI', 'CẦN GIỜ', 'CAN GIO', 'HUYEN CAN GIO']:
        return '787'
    elif d in ['783', 'QCCH', 'CỦ CHI', 'CU CHI', 'PHƯỚC VĨNH AN', 'HUYEN CU CHI']:
        return '783'
    elif d in ['765', 'QBTH', 'BINH THANH', 'BÌNH THẠNH', 'QUAN BINH THANH']:
        return '765'
    elif d in ['768', 'QPNH', 'PHÚ NHUẬN', 'PHU NHUAN', 'QUAN PHU NHUAN']:
        return '768'
    elif d in ['766', 'QTBH', 'TAN BINH', 'TÂN BÌNH', 'QUAN TAN BINH']:
        return '766'
    elif d in ['762', 'QTDC', 'THỦ ĐỨC', 'THU DUC', 'BÌNH CHIỂU', 'LINH ĐÔNG', 'HIỆP BÌNH PHƯỚC', 'LONG TRƯỜNG', 
               'LONG PHƯỚC', 'HIỆP BÌNH CHÁNH', 'QUAN THU DUC']:
        return '762'
    elif d in ['767', 'QTPH', 'TAN PHU', 'TÂN PHÚ', 'SƠN KỲ',
               'PHÚ TRUNG', 'PHÚ THẠNH', 'TÂN THÀNH', 'QUAN TAN PHU']:
        return '767'
    elif d in ['777', 'QBTN', 'BÌNH TÂN', 'BINH TAN', 'AN LẠC',
               'BÌNH HƯNG HÒA A', 'BÌNH HƯNG HÒA A', 'BÌNH TRỊ ĐÔNG',
               'QUAN BINH TAN']:
        return '777'
    elif d in ['786', 'QNBE', 'NHA BE', 'NHÀ BÈ', 'PHƯỚC KIẾN', 
               'HUYEN NHA BE']:
        return '786'
    elif d in ['785', 'QBCH', 'BÌNH CHÁNH', 'BINH CHANH', 'PHONG PHÚ',
               'VĨNH LỘC A', 'TÂN QUÝ TÂY', 'TT TÂN TÚC',
               'HUYEN BINH CHANH', 'QUAN BINH CHANH']:
        return '785'
    elif d in ['999', 'THANH PHO THU DUC', 'TP THU DUC', 'TPTD']:
        return '999'
    else:
        return 'UNKN'
    
def encode_addr_prov(row):
    d = str(row).upper().strip()
    if d in ['THANH PHO HO CHI MINH', 'TP HCM', 'TPHCM']:
        return '79'
    else:
        return 'UNKN'

def get_no_event(data, date_col='date_report', no_col='no_test', pop=10000000, rolling=7):
    """
    Count number of (no) event by date
    
    Args:
        data: Data frame, input data frame
        date_col: String, name of date column, default 'date_report'
        no_col: String, name of event count column, default 'no_case'
        rolling: Int, rolling window, default 7
        pop: Int, population, default 10000000
    
    Return:
        A data frame
    """
    # number of events by date, reindex to fill missing date entry with 0
    df = (
        data[[date_col]]
        .groupby(date_col)
        .apply(lambda x: len(x))
        .to_frame(name=no_col)
        .reindex(pd.date_range(start=data[date_col].min(), end=data[date_col].max(), freq='D'))
        .fillna(0)
    )
    # population column
    df['pop'] = pop
    # name of columns to be created
    col_per_pop = no_col + '_ppop'
    col_rollmean = no_col + '_rollmean' + str(rolling) + 'd'
    col_per_pop_rollmean = no_col + '_ppop_rollmean' + str(rolling) + 'd'
    col_cumsum = no_col + '_cumsum'
    col_per_pop_cumsum = no_col + '_ppop_cumsum'
    # number of events per population by date
    df[col_per_pop] = round(df[no_col] /df['pop'] * 100000, 3)
    # rolling mean number of events by date
    df[col_rollmean] = df[no_col].rolling(rolling).mean()
    # rolling mean number of events per population by date
    df[col_per_pop_rollmean] = df[col_per_pop].rolling(7).mean()
    # cumulative sum number of events by date
    df[col_cumsum] = df[no_col].cumsum()
    # cumulative sum number of events per population by date
    df[col_per_pop_cumsum] = df[col_per_pop].cumsum()
    df = df.drop(columns='pop')
    return df

def get_no_event_by_group(data, pop, addiv,
                         group_col,
                         date_col='date_report',
                         no_col='no_test',
                         available_pop=False,
                         getname=False, rolling=7):
    """
    Count number of (no) event by group and date
    
    Args:
        data: Data frame, input data frame
        pop: Data frame, population data frame
        addiv: Data frame, adminstrative division data frame
        date_col: String, name of date column, default date_col
        no_col: String, name of event count column, default no_col
        rolling: Int, rolling window, default 7
        available_pop: Boolean, if population data frame by group is available, default False
        getname: Boolean, to get group label if it exists, default False
    
    Return:
        A data frame
    """
    unique = data[group_col].unique()
    # number of events by group and date
    df_1 = (
        data[[date_col, group_col]]
        .groupby([date_col, group_col])
        .apply(lambda x: len(x))
        .to_frame(name=no_col)
        .unstack(fill_value=0)
        .asfreq('D', fill_value=0)
        .stack()
        .sort_index(level=0)
        .reset_index()
    )
    # pivot table to fill missing group with 0
    df_pv = (
        df_1[[date_col, group_col, no_col]]
        .pivot(index=date_col, columns=group_col, values=no_col)
    ).fillna(0)
    # fill missing date with 0
    df_2 = (
        df_pv.reindex(pd.date_range(
            start=df_pv.index.min(),
            end=df_pv.index.max(),
            freq='D'))
        .fillna(0)
        .stack(list(range(0, 1)))
        .reset_index()
        .rename(columns={
            'level_0': date_col,
            0: no_col
        })
#         .set_index([date_col] + group)
    )
    
    # name of columns to be created
    col_per_pop = no_col + '_ppop'
    col_rollmean = no_col + '_rollmean' + str(rolling) + 'd'
    col_per_pop_rollmean = no_col + '_ppop_rollmean' + str(rolling) + 'd'
    col_cumsum = no_col + '_cumsum'
    col_per_pop_cumsum = no_col + '_ppop_cumsum'
    
    # get no_case_rollmean
    df_3 = df_2
    df_3[col_rollmean] = (
        df_3.groupby(group_col)[no_col]
        .transform(lambda x: x.rolling(rolling).mean())
    )
    # get no_case cumsum
    df_3[col_cumsum] = (
        df_3[[date_col, group_col, no_col]]
        .groupby([date_col, group_col]).sum()
        .groupby(level=1).cumsum().reset_index()
        [no_col]
    )
    
    # Get number of events per population
    if available_pop:
        df_pop = pop[['id_addiv', 'pop']]
        # merge with population
        df_3 = (
            df_3.merge(
                df_pop,
                how= 'left',
                left_on=group_col,
                right_on= 'id_addiv')
            .drop(columns=['id_addiv'])
        )
        # number of events per population by group
        df_3[col_per_pop] = round(df_3[no_col] / df_3['pop'] * 100000, 3)
        df_3 = df_3.drop(columns='pop')
        # rolling mean number of events per population by group
        df_3[col_per_pop_rollmean] = (
            df_3.groupby(group_col)[col_per_pop]
            .transform(lambda x: x.rolling(rolling).mean())
        )
        # cumulative sum number of events per population by group
        df_3[col_per_pop_cumsum] = (
            df_3[[date_col, group_col, col_per_pop]]
            .groupby([date_col, group_col]).sum()
            .groupby(level=1).cumsum().reset_index()
            [col_per_pop]
        )

    # Get district name (optional)
    if getname:
        df_3 = (
            df_3.merge(
                addiv[['id_addiv', 'name_addiv_2']],
                how = 'left',
                left_on = group_col,
                right_on = 'id_addiv'
            )
            .drop(columns=[group_col, 'id_addiv'])
            .rename(columns={'name_addiv_2': group_col})
        )
    return df_3


def get_no(data, date_col='date_report', no_col='no_case'):
    """
    Count number of (no) event by date
    
    Args:
        data: Data frame, input data frame
        date_col: String, name of date column, default 'date_report'
        no_col: String, name of event count column, default 'no_case'
        
    Return:
        A data frame
    """
    # number of events by date, reindex to fill missing date entry with 0
    idx = pd.date_range(start=data[date_col].min(), end=data[date_col].max(), freq='D')
    df = (
        data[[date_col]]
        .groupby(date_col)
        .apply(lambda x: len(x))
        .to_frame(name=no_col)
        .reindex(idx)
        .fillna(0)
        .rename_axis('date_report')
    )
    
    return df

def get_no_by_group(data, group_col = [], date_col='date_report', no_col='no_case'):
    """
    Count number of (no) event by group and date
    
    Args:
        data: Data frame, input data frame
        group_col: list of group columns
        date_col: String, name of date column, default date_col
        no_col: String, name of event count column, default no_col
    
    Return:
        A data frame
    """
    df = (
        data.groupby(group_col + [date_col])
        .apply(lambda x: len(x)).to_frame(name=no_col)
        .reset_index()
        .set_index(date_col)
        .groupby(group_col)
        [no_col]
        .resample('D').sum()
        .reset_index()
        .pivot(index=date_col, columns=group_col, values=no_col)
        .fillna(0)
        .stack(list(range(len(group_col))))
        .reset_index()
        .rename(columns={0: no_col, date_col: 'date_report'})
        .set_index('date_report')
    )
    return df