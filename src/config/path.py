#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 10:39:50 2021

@author: kyo
"""

import pathlib

path = pathlib.Path('/home/kyo/Documents/script/covid-data-analysis/')

reference = path.joinpath('reference')

raw = path.joinpath('data', 'raw')

interim = path.joinpath('data', 'interim')

external = path.joinpath('data', 'external')

processed = path.joinpath('data', 'processed')