# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 10:58:01 2020

@author: Vruj
"""

import tkinter
from matplotlib.widgets import Slider, Button, RadioButtons
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import calc as calc

def makeGT(df, title):
    copy = df.copy()
    dfa = copy.to_numpy()
    
    zero4m = dfa[0][0]
    zero4s = dfa[0][1]
    
    five17m = dfa[1][0]
    five17s = dfa[1][1]
    
    eighteen49m = dfa[2][0]
    eighteen49s = dfa[2][1]
    
    fifty64m = dfa[3][0]
    fifty64s = dfa[3][1]
    
    sixty5plusm = dfa[4][0]
    sixty5pluss = dfa[4][1]
    
    sumSev = zero4s + five17s + eighteen49s + fifty64s + sixty5pluss
    sumMild = zero4m + five17m + eighteen49m + fifty64m + sixty5plusm
    
    data = [[ zero4m,       zero4s],
            [ five17m,      five17s],
            [ eighteen49m,  eighteen49s],
            [ fifty64m,     fifty64s],
            [ sixty5plusm,  sixty5pluss]]
    
    columns = ('MILD', 'SEVERE')
    rows = ['0 to 4', '5 to 17', '18 to 49', '50 to 64', '65+']
    if sumSev<10000:
        values = np.arange(0, sumSev + 1000, 1000)
    else:
        values = np.arange(0, sumSev + 5000, 5000)
    value_increment = 1
    
    colors = plt.cm.OrRd(np.linspace(0, 1, len(rows)))
    n_rows = len(data)
    
    index = np.arange(len(columns)) 
    bar_width = 0.5
    
    # Initialize the vertical-offset for the stacked bar chart.
    y_offset = np.zeros(len(columns))
    
    # Plot bars and create text labels for the table
    cell_text = []
    for row in range(n_rows):
        plt.bar(index, data[row], bar_width, bottom=y_offset, color=colors[row])
        y_offset = y_offset + data[row]
        cell_text.append(['%d' %x for x in data[row]])
        
        
    # Add a table at the bottom of the axes
    plt.table(cellText=cell_text,
              rowLabels=rows,
              rowColours=colors,
              colLabels=columns,
              cellLoc = 'center',
              loc='bottom')
    
    # Adjust layout to make room for the table:
    plt.subplots_adjust(left=0.2, bottom=0.2)
    
    plt.ylabel("TOTAL Predicted Cases".format(value_increment))
    plt.yticks(values * value_increment, ['%d' % val for val in values])
    plt.xticks([])
    plt.title(title)
    
    return plt

