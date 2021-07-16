#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 09:16:26 2021

@author: kyo
"""

import re


def clean_name_full(row):
    name_full = row.upper()
    # pattern = r'(^|[^\(])([\w\s]+)'
    pattern = r'([^\(=]+)'
    s = re.search(pattern, name_full)
    if s == None:
        return ''
    else:
        return s.group().strip()


print(clean_name_full('Nguyễn A => Nguyễn A'))
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
    
    
def encode_addr_dist(row):
    d = str(row).upper().strip()
    if d in ['QA01', '1', '01', 'QUẬN 1', 'BẾN NGHÉ', 'TÂN ĐỊNH', 'NGUYỄN CƯ TRINH']:
        return 'QA01'
    elif d in ['QA02', '2', '02', 'QUẬN 2']:
        return 'QA02'
    elif d in ['QA03', '3', '03']:
        return 'QA03'
    elif d in ['QA04', '4', '04']:
        return 'QA04'
    elif d in ['QA05', '5', '05']:
        return 'QA05'
    elif d in ['QA06', '6', '06', 'QUẬN 6']:
        return 'QA06'
    elif d in ['QA07', '7', '07']:
        return 'QA07'
    elif d in ['QA08', '8', '08', 'QUẬN 8']:
        return 'QA08'
    elif d in ['QA09', '9', '09', 'QUẬN 9']:
        return 'QA09'
    elif d in ['QA10', '10', 'QUẬN 10']:
        return 'QA10'
    elif d in ['QA11', '11', 'QUẬN 11']:
        return 'QA11'
    elif d in ['QA12', '12', 'Q12', 'TÂN THỚI NHẤT']:
        return 'QA12'
    elif d in ['QGVP', 'GÒ VẤP', 'GO VAP']:
        return 'QGVP'
    elif d in ['QHMN', 'HÓC MÔN', 'HOC MON', 'THÁI TAM THÂN', 'XUÂN THỚI THƯỢNG']:
        return 'QHMN'
    elif d in ['QCGI', 'CẦN GIỜ', 'CAN GIO']:
        return 'QCGI'
    elif d in ['QCCH', 'CỦ CHI', 'CU CHI', 'PHƯỚC VĨNH AN']:
        return 'QCCH'
    elif d in ['QBTH', 'BINH THANH', 'BÌNH THẠNH']:
        return 'QBTH'
    elif d in ['QPNH', 'PHÚ NHUẬN', 'PHU NHUAN']:
        return 'QPNH'
    elif d in ['QTBH', 'TAN BINH', 'TÂN BÌNH']:
        return 'QTBH'
    elif d in ['QTDC', 'THỦ ĐỨC', 'THU DUC', 'BÌNH CHIỂU', 'LINH ĐÔNG', 'HIỆP BÌNH PHƯỚC', 'LONG TRƯỜNG', 
               'LONG PHƯỚC', 'HIỆP BÌNH CHÁNH']:
        return 'QTDC'
    elif d in ['QTPH', 'TAN PHU', 'TÂN PHÚ', 'SƠN KỲ', 'PHÚ TRUNG', 'PHÚ THẠNH', 'TÂN THÀNH']:
        return 'QTPH'
    elif d in ['QBTN', 'BÌNH TÂN', 'BINH TAN', 'AN LẠC', 'BÌNH HƯNG HÒA A', 'BÌNH HƯNG HÒA A', 'BÌNH TRỊ ĐÔNG']:
        return 'QBTN'
    elif d in ['QNBE', 'NHA BE', 'NHÀ BÈ', 'PHƯỚC KIẾN']:
        return 'QNBE'
    elif d in ['QBCH', 'BÌNH CHÁNH', 'BINH CHANH', 'PHONG PHÚ', 'VĨNH LỘC A', 'TÂN QUÝ TÂY', 'TT TÂN TÚC']:
        return 'QBCH'
    else:
        return 'UNKN'