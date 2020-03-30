#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 20:46:41 2020

@author: liorshtayer
"""

import pandas as pd

Gamma_df = pd.DatFrame(columns=['Day','Gamma_Adult_Med/Surg_mild','Gamma_Adult_ICU_mild','Gamma_Peds_Med/Surg_mild',
                              'Gamma_Peds_ICU_mild','Gamma_Adult_Med/Surg_severe','Gamma_Adult_ICU_severe','Gamma_Peds_Med/Surg_severe',
                              'Gamma_Peds_ICU_severe'])

LOS_Occupancy_df = pd.DataFrame(columns=['Day','Adult_Med/Surg_mild','Adult_ICU_mild','Peds_Med/Surg_mild','Peds_ICU_mild',
                               'Adult_Med/Surg_severe','Adult_ICU_severe','Peds_Med/Surg_severe','Peds_ICU_severe'])

LOS_Deaths_df = pd.DataFrame(columns=['Day','Adult_Med/Surg_mild','Adult_ICU_mild','Peds_Med/Surg_mild','Peds_ICU_mild',
                               'Adult_Med/Surg_severe','Adult_ICU_severe','Peds_Med/Surg_severe','Peds_ICU_severe'])

LOS_Discharges_df = pd.DataFrame(columns=['Day','Adult_Med/Surg_mild','Adult_ICU_mild','Peds_Med/Surg_mild','Peds_ICU_mild',
                               'Adult_Med/Surg_severe','Adult_ICU_severe','Peds_Med/Surg_severe','Peds_ICU_severe'])

#TODO: Define LOS variables, multiplication factors

#TODO: Carry out functions to pouplate the DFs

#TODO: Map everything back to LOS outputs