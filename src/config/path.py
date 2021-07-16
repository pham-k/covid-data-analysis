#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 10:39:50 2021

@author: kyo
"""

import pathlib

path = pathlib.Path('/home/kyo/Documents/script/covid/')

reference = path.joinpath('reference')

raw = path.joinpath('data', 'raw')

interim = path.joinpath('data', 'interim')