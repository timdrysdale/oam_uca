#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 15:54:00 2019

@author: tim
"""

from uca import *


frequency = 150e9 #D band https://www.etsi.org/images/files/ETSIWhitePapers/etsi_wp25_mwt_and_5g_FINAL.pdf

config = {
    'frequency': frequency
}

uca(config)