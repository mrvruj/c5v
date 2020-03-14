#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scipy.stats import gamma
import numpy as np
import pandas as pd

#################   GAMMA CALCS   #################   

MIDAS = [2.00262E-07,2.01307E-07,1.8657E-07,1.78572E-07,1.76163E-07,1.78642E-07,1.8515E-07,1.93002E-07,2.02005E-07,2.14533E-07,2.31185E-07,2.51936E-07,2.76916E-07,3.05671E-07,3.34833E-07,3.65117E-07,4.03235E-07,4.51265E-07,5.09361E-07,5.77455E-07,6.57932E-07,7.37232E-07,8.14176E-07,9.05858E-07,1.02469E-06,1.16867E-06,1.34511E-06,1.5474E-06,1.75134E-06,1.96423E-06,2.24551E-06,2.53249E-06,2.89278E-06,3.29931E-06,3.8412E-06,4.3324E-06,4.85465E-06,5.47179E-06,6.16445E-06,7.07428E-06,8.27131E-06,9.49378E-06,1.09156E-05,1.21438E-05,1.37283E-05,1.57208E-05,1.79789E-05,2.06963E-05,2.36651E-05,2.69076E-05,3.00761E-05,3.41172E-05,3.89155E-05,4.51412E-05,4.85552E-05,5.92189E-05,6.86491E-05,7.60414E-05,8.62128E-05,9.31567E-05,0.000117215,0.00012144,0.000145461,0.000163928,0.000182725,0.000204256,0.000228848,0.000260567,0.000288344,0.000326988,0.000381135,0.000424963,0.000445799,0.000507271,0.000564386,0.00065757,0.000743688,0.000897775,0.001010098,0.001118681,0.001208534,0.001418268,0.001594266,0.001843767,0.002071218,0.002307429,0.002607086,0.002952581,0.00322516,0.003635776,0.004065966,0.004617907,0.004917045,0.005458708,0.00601502,0.006323044,0.0071665,0.007836093,0.008356697,0.008859337,0.00942685,0.010224811,0.011010594,0.011533369,0.012438796,0.013020524,0.013675804,0.014095047,0.014624532,0.015359524,0.015838443,0.016352469,0.016948469,0.017226132,0.017292033,0.017960385,0.018238306,0.018444877,0.018935103,0.019052603,0.019048883,0.018891817,0.018858088,0.019046816,0.019036994,0.018912131,0.01873734,0.018426829,0.018176861,0.01820602,0.017971113,0.017672604,0.017304309,0.016853865,0.016515483,0.01592707,0.015568839,0.015126821,0.014614909,0.014369084,0.01365471,0.013275443,0.012489638,0.012048597,0.011416639,0.011202709,0.010528467,0.010029517,0.009493479,0.008936816,0.008487525,0.00818117,0.007700167,0.007197222,0.006777008,0.006374689,0.006059472,0.005594732,0.00540245,0.00499034,0.004703479,0.004498828,0.004178178,0.003912983,0.003707334,0.003462947,0.003221098,0.003053193,0.002792653,0.002621862,0.002507767,0.00237217,0.002105541,0.002006419,0.001840493,0.001750993,0.001602003,0.001553716,0.001506319,0.001329662,0.001204771,0.001131417,0.001123594,0.001023513,0.000987072,0.000882027,0.00080783,0.000829178,0.000715048,0.000611818,0.000597251,0.00057765,0.00058059,0.000499776,0.000483223,0.000436522,0.000381591,0.000368463,0.000366268,0.000336125,0.000299607,0.000268451,0.00026761,0.00024692,0.000234073,0.00020744,0.000196445,0.000183481,0.0001799,0.000161993,0.000156156,0.000128567,0.000123872,0.000128539,0.000114981,0.000114034,8.70696E-05,0.000102518,8.84324E-05,7.44127E-05,7.28161E-05,6.90667E-05,6.55987E-05,5.80623E-05,5.34003E-05,4.94455E-05,4.76328E-05,5.07176E-05,4.31379E-05,3.57816E-05,3.96226E-05,3.58411E-05,3.96907E-05,2.97795E-05,3.07381E-05,2.94846E-05,2.36271E-05,2.32098E-05,2.17029E-05,2.02604E-05,1.88659E-05,1.75698E-05,1.64648E-05,1.5444E-05,1.43903E-05,1.32665E-05,1.23585E-05,1.16092E-05,1.06966E-05,9.88014E-06,9.20536E-06,8.66783E-06,8.19904E-06,7.66667E-06,7.21236E-06,6.66697E-06,6.15502E-06,5.70826E-06,5.38479E-06,5.02943E-06,4.6886E-06,4.37191E-06,4.07835E-06,3.80595E-06,3.55287E-06,3.31712E-06,3.09542E-06,2.88696E-06,2.69291E-06,2.51234E-06,2.34456E-06,2.18868E-06,2.0435E-06,1.90698E-06,1.77863E-06,1.65922E-06,1.54835E-06,1.44507E-06,1.34902E-06,1.25956E-06]
#values of the MIDAS model

def gamma_pdf(a,b):
    """
    Takes in the paramters of the gamma probability density function, 
    shape [alpha (a)] and scale [beta (b)] and returns a list with values 
    of the pdf for days 0-180. 
    
    Parameters:
        a: alpha
        b: beta
        
    Output:
        an array with 180 elements representing a gamma pdf for days 1-180
    """
    output = []
    for day in range(181):
        output.append(gamma.pdf(day,a,0,b))
    return output


def epi_curve(max, peakedness):
    """
    Takes the input variables of which day the maximum cases will be [max] and how 
    peaked the user wants the epidemic curve to be [peakedness] represented as:
    Flat --------------> 0
    Not peaked --------> 1
    A bit peaked ------> 2
    Very peaked -------> 3
    Extremely peaked --> 4
    MIDAS -------------> 5 (280 day model)
    
    These two inputs are converted to values of alpha and beta and used as 
    inputs for the gamma_pdf function. 
    
    However, if the user indicated the peakedness as MIDAS, a preinputted 
    array will be used. 
    """
    
    if peakedness != 5:
        alpha_beta = [(7,5),(13,2.5),(21,1.5),(31,1),(68,0.45),(7,10),(13,5),(21,3),(31,2),(68,0.9),(7,15),(13,7.5),(21,4.5),(31,3),(68,1.35)]
        if max == 30:
            i = peakedness
        elif max == 60:
            i = peakedness + 5
        elif max == 90:
            i = peakedness + 10
        alpha = float(alpha_beta[i][0])
        beta = float(alpha_beta[i][1])
        return gamma_pdf(alpha,beta)
    elif peakedness == 5:
        return MIDAS
    
def ageDist(totalPop, popCOM):
    """
    Parameters:
        totalPop = total number of people
        popCOM = a qualitative assessment of the shape of the population
                    pyramid; has the following options:
                        1. Old
                        2. Middle-Aged
                        3. Adults
                        4. Teenagers
                        5. Children
                    
    Output: 
        ageDist = a dataframe with 5 elements representing the number of people 
                    in each age class
    """
    ad = pd.DataFrame(columns=['proportions'])
    if popCOM == 1:
        ad = ad.append({'proportions': .1}, ignore_index=True)
        ad = ad.append({'proportions': .1}, ignore_index=True)
        ad = ad.append({'proportions': .1}, ignore_index=True)
        ad = ad.append({'proportions': .1}, ignore_index=True)
        ad = ad.append({'proportions': .6}, ignore_index=True)
    elif popCOM == 2:
        ad = ad.append({'proportions': 535068/8398748}, ignore_index=True)
        ad = ad.append({'proportions': 1204188/8398748}, ignore_index=True)
        ad = ad.append({'proportions': 3886398/8398748}, ignore_index=True)
        ad = ad.append({'proportions': 1527614/8398748}, ignore_index=True)
        ad = ad.append({'proportions': 1245480/8398748}, ignore_index=True)
    elif popCOM == 3:
        ad = ad.append({'proportions': .1}, ignore_index=True)
        ad = ad.append({'proportions': .1}, ignore_index=True)
        ad = ad.append({'proportions': .6}, ignore_index=True)
        ad = ad.append({'proportions': .1}, ignore_index=True)
        ad = ad.append({'proportions': .1}, ignore_index=True)
    elif popCOM == 4:
        ad = ad.append({'Ages': '0 to 4',    'proportions': .1}, ignore_index=True)
        ad = ad.append({'Ages': '5 to 17',   'proportions': .6}, ignore_index=True)
        ad = ad.append({'Ages': '18 to 49',  'proportions': .1}, ignore_index=True)
        ad = ad.append({'Ages': '50 to 64',  'proportions': .1}, ignore_index=True)
        ad = ad.append({'Ages': '65+',       'proportions': .1}, ignore_index=True)
    elif popCOM == 5:
        ad = ad.append({'proportions': .6}, ignore_index=True)
        ad = ad.append({'proportions': .1}, ignore_index=True)
        ad = ad.append({'proportions': .1}, ignore_index=True)
        ad = ad.append({'proportions': .1}, ignore_index=True)
        ad = ad.append({'proportions': .1}, ignore_index=True)

    ad['proportions'] = ad['proportions'].apply(lambda x:x*totalPop)
    return ad

def CHR():
    CHR = pd.DataFrame(columns = ['Mild','Severe'])
    CHR = CHR.append({'Mild': 0.0125, 'Severe': 0.05}, ignore_index=True)
    CHR = CHR.append({'Mild': 0.0050, 'Severe': 0.02}, ignore_index=True)
    CHR = CHR.append({'Mild': 0.0125, 'Severe': 0.05}, ignore_index=True)
    CHR = CHR.append({'Mild': 0.0175, 'Severe': 0.07}, ignore_index=True)
    CHR = CHR.append({'Mild': 0.1600, 'Severe': 0.60}, ignore_index=True)
    
    return CHR

def CCHR():
    CCHR = pd.DataFrame(columns = ['Mild','Severe'])
    CCHR = CCHR.append({'Mild': 0.15, 'Severe': 0.15}, ignore_index=True)
    CCHR = CCHR.append({'Mild': 0.20, 'Severe': 0.20}, ignore_index=True)
    CCHR = CCHR.append({'Mild': 0.15, 'Severe': 0.15}, ignore_index=True)
    CCHR = CCHR.append({'Mild': 0.20, 'Severe': 0.20}, ignore_index=True)
    CCHR = CCHR.append({'Mild': 0.15, 'Severe': 0.15}, ignore_index=True)
    
    return CCHR
    
def totalHosp(attackRate, symp, ad, CHR):
    tH = CHR.copy()
    
    tH['Mild'] =   tH['Mild'].apply(lambda x: x*attackRate*symp)
    tH['Severe'] = tH['Severe'].apply(lambda x: x*attackRate*symp)
    
    tH['Mild'] =   tH['Mild'] *   ad['proportions']
    tH['Severe'] = tH['Severe'] * ad['proportions']
    
    return tH

def ICUs(attackRate, symp, ad, CHR, CCHR):
    tH = totalHosp(attackRate, symp, ad, CHR)
    tICU = pd.DataFrame(columns = ['Mild','Severe'])
    
    tICU['Mild'] =   tH['Mild']   * CCHR['Mild']
    tICU['Severe'] = tH['Severe'] * CCHR['Severe']
    
    return tICU
        
def wardCases(attackRate, symp, ad, CHR, CCHR):
    tH = totalHosp(attackRate, symp, ad, CHR)
    tICU = ICUs(attackRate, symp, ad, CHR, CCHR)
    wards = pd.DataFrame(columns = ['Mild', 'Severe'])
    
    wards['Mild'] =   tH['Mild'] -   tICU['Mild']
    wards['Severe'] = tH['Severe'] - tICU['Severe']
    
    return wards
