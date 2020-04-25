#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 20:46:41 2020

@author: liorshtayer
"""

from pandas import DataFrame
import calc

LOS_data_df = DataFrame(columns=['W_A','ICU_A','W_P','ICU_P'], 
                        index=['Survivor_min','Survivor_max','Survivor_share','Victim_min','Victim_max','Victim_share'])

LOS_Admissions_df = DataFrame(columns=['Day','mW_A','sW_A','mICU_A','sICU_A','mW_P','sW_P','mICU_P','sICU_P'])

LOS_Occupancy_df = DataFrame(columns=['Day','mW_A','sW_A','mICU_A','sICU_A','mW_P','sW_P','mICU_P','sICU_P'])

LOS_Deaths_df = DataFrame(columns=['Day','mW_A','sW_A','mICU_A','sICU_A','mW_P','sW_P','mICU_P','sICU_P'])

LOS_Discharges_df = DataFrame(columns=['Day','mW_A','sW_A','mICU_A','sICU_A','mW_P','sW_P','mICU_P','sICU_P'])

def calc_LOS_Admissions(df, tICU_p, tICU_a, tWard_p, tWard_a):
    """
    Takes input DataFrame from epi_curve and populates LOS_Admissions_df with the 
    corresponding values based on mild/severe ward/ICU adult/peds parameters.
    
    """
    mW_A = tWard_a.loc[0][0]
    sW_A = tWard_a.loc[0][1]
    mICU_A = tICU_a.loc[0][0]
    sICU_A = tICU_a.loc[0][1]
    mW_P = tWard_p.loc[0][0]
    sW_P = tWard_p.loc[0][1]
    mICU_P = tICU_p.loc[0][0]
    sICU_P = tICU_p.loc[0][1]
    
    LOS_Admissions_df['Day'] = df['Day']
    d = {'mW_A':mW_A, 'sW_A':sW_A, 'mICU_A':mICU_A, 'sICU_A':sICU_A, 'mW_P':mW_P, 'sW_P':sW_P, 'mICU_P':mICU_P, 'sICU_P':sICU_P}
    for key,value in d.items():
        LOS_Admissions_df[key] = df['Gamma_Values'].apply(lambda x: x*value)
    LOS_Admissions_df.index += 1
    #To correct for C4-AnalyticOutput starting at 1

def calc_LOS_data(LOS):
    """
    Takes in the data from the LOS table in the inputs and converts it to the proper form to 
    be used during the LOS Dynamics calculations.
    
    Here, both mild and severe scenarios have the same LOS.
    """
    W_A_min = LOS.loc[0][0]
    W_A_max = LOS.loc[0][1]
    W_A_FR = LOS.loc[0][2]
    W_A_adj = LOS.loc[0][3]
    ICU_A_min = LOS.loc[1][0]
    ICU_A_max = LOS.loc[1][1]
    ICU_A_FR = LOS.loc[1][2]
    ICU_A_adj = LOS.loc[1][3]
    W_P_min = LOS.loc[2][0]
    W_P_max = LOS.loc[2][1]
    W_P_FR = LOS.loc[2][2]
    W_P_adj = LOS.loc[2][3]
    ICU_P_min = LOS.loc[3][0]
    ICU_P_max = LOS.loc[3][1]
    ICU_P_FR = LOS.loc[3][2]
    ICU_P_adj = LOS.loc[3][3]
    
    LOS_data_df.loc['Survivor_min']['W_A'] = W_A_min
    LOS_data_df.loc['Survivor_min']['ICU_A'] = ICU_A_min
    LOS_data_df.loc['Survivor_min']['W_P'] = W_P_min
    LOS_data_df.loc['Survivor_min']['ICU_P'] = ICU_P_min
    
    LOS_data_df.loc['Survivor_max']['W_A'] = W_A_max
    LOS_data_df.loc['Survivor_max']['ICU_A'] = ICU_A_max
    LOS_data_df.loc['Survivor_max']['W_P'] = W_P_max
    LOS_data_df.loc['Survivor_max']['ICU_P'] = ICU_P_max
    
    LOS_data_df.loc['Survivor_share']['W_A'] = 100-W_A_FR
    LOS_data_df.loc['Survivor_share']['ICU_A'] = 100-ICU_A_FR
    LOS_data_df.loc['Survivor_share']['W_P'] = 100-W_P_FR
    LOS_data_df.loc['Survivor_share']['ICU_P'] = 100-ICU_P_FR
    
    LOS_data_df.loc['Victim_min']['W_A'] = round(W_A_min*W_A_adj/100)
    LOS_data_df.loc['Victim_min']['ICU_A'] = round(ICU_A_min*ICU_A_adj/100)
    LOS_data_df.loc['Victim_min']['W_P'] = round(W_P_min*W_P_adj/100)
    LOS_data_df.loc['Victim_min']['ICU_P'] = round(ICU_P_min*ICU_P_adj/100)
    
    LOS_data_df.loc['Victim_max']['W_A'] = round(W_A_max*W_A_adj/100)
    LOS_data_df.loc['Victim_max']['ICU_A'] = round(ICU_A_max*ICU_A_adj/100)
    LOS_data_df.loc['Victim_max']['W_P'] = round(W_P_max*W_P_adj/100)
    LOS_data_df.loc['Victim_max']['ICU_P'] = round(ICU_P_max*ICU_P_adj/100)
    
    LOS_data_df.loc['Victim_share']['W_A'] = W_A_FR
    LOS_data_df.loc['Victim_share']['ICU_A'] = ICU_A_FR
    LOS_data_df.loc['Victim_share']['W_P'] = W_P_FR
    LOS_data_df.loc['Victim_share']['ICU_P'] = ICU_P_FR
    
def DepartureOnDay(LOS_Admissions,Share,Day,MinDay,MaxDay):
    """
    LOS_Admissions ==> LOS_Admissions_df['mW_A'] for example. Selects corresponding column. 
    This is the function that is used to fill in the cells of LOS Deaths and Discharges
    """
    if MinDay < MaxDay:
        departureRate = 1/(MaxDay-MinDay)
    else:
        departureRate = 1
    departures = 0
    startDay = Day-MaxDay
    if startDay < 1:
        startDay=1
    for i in range(1,Day+1):
        arrivals = LOS_Admissions[i]*(Share/100)
        if Day <= i+MaxDay and Day > i+MinDay:
            departures = departures + arrivals*departureRate
    return departures

def calc_LOS_Deaths():
    """
    Based off LOS_data Victims....takes in the Min LOS, Max LOS, Share of arrivals, and
    reiterates the DepartureOnDay function for each cell for a given Day and Admissions count. 
    """
    LOS_Deaths_df['Day'] = LOS_Admissions_df['Day']
    #To start at Day 1
    for day in range(1,181):
        for col in ['mW_A','sW_A','mICU_A','sICU_A','mW_P','sW_P','mICU_P','sICU_P']:            
            LOS_Deaths_df.at[day,col] = DepartureOnDay(LOS_Admissions_df[col],LOS_data_df.loc['Victim_share'][col[1:]],
                             day,LOS_data_df.loc['Victim_min'][col[1:]],LOS_data_df.loc['Victim_max'][col[1:]])
    
def calc_LOS_Discharges():
    """
    Based off LOS_data Survivors....takes in the Min LOS, Max LOS, Share of arrivals, and
    reiterates the DepartureOnDay function for each cell for a given Day and Admissions count. 
    """
    LOS_Discharges_df['Day'] = LOS_Admissions_df['Day']
    #To start at Day 1
    for day in range(1,181):
        for col in ['mW_A','sW_A','mICU_A','sICU_A','mW_P','sW_P','mICU_P','sICU_P']:            
            LOS_Discharges_df.at[day,col] = DepartureOnDay(LOS_Admissions_df[col],LOS_data_df.loc['Survivor_share'][col[1:]],
                             day,LOS_data_df.loc['Survivor_min'][col[1:]],LOS_data_df.loc['Survivor_max'][col[1:]])

def calc_LOS_Occupancy():
    """
    Takes the occupancy the day prior, adds any new admissions and subtracts discharges and deaths.
    """
    LOS_Occupancy_df['Day'] = LOS_Admissions_df['Day']
    for day in range(1,181):
        for col in ['mW_A','sW_A','mICU_A','sICU_A','mW_P','sW_P','mICU_P','sICU_P']:
            if day == 1:
                LOS_Occupancy_df.at[day,col] = 0
            else:
                LOS_Occupancy_df.at[day,col] = LOS_Occupancy_df.loc[day-1][col] + LOS_Admissions_df.loc[day][col] - LOS_Deaths_df.loc[day-1][col] - LOS_Discharges_df.loc[day-1][col]
    LOS_Occupancy_df['Day'] += 1
    LOS_Occupancy_df.drop([181],inplace=True)
    LOS_Occupancy_df.reset_index(drop=True, inplace=True)

