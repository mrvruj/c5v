# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 10:58:01 2020

@author: Vruj
"""

import tkinter
import calc as calc

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import pandas as pd

totalP = 8 * 10**6

attackRate = 0.6
symp = 0.5

ageSpread = calc.ageDist(totalP, 3)
totalHosp = calc.totalHosp(ageSpread, attackRate, symp, CHR)


zero4m = 334
zero4s = 1338

five17m = 301
five17s = 1204

eighteen49m = 2429
eighteen49s = 9716

fifty64m = 1337
fifty64s = 5347

sixty5plusm = 9964
sixty5pluss = 37364

less18m = 635
less18s = 2542
more18m = 13730
more18s = 52427

##TODO: put total on graph
#TODO: make this a function and call it
#TODO: embed in tkinter

sumSev = zero4s + five17s + eighteen49s + fifty64s + sixty5pluss
sumMild = zero4m + five17m + eighteen49m + fifty64m + sixty5plusm

data = [[ zero4m,       zero4s],
        [ five17m,      five17s],
        [ eighteen49m,  eighteen49s],
        [ fifty64m,     fifty64s],
        [ sixty5plusm,  sixty5pluss],
        #[ less18m,      less18s],
        #[ more18m,      more18s]
        ]

columns = ('MILD', 'SEVERE')
rows = ['0 to 4', '5 to 17', '18 to 49', '50 to 64', '65+']

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
the_table = plt.table(cellText=cell_text,
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
plt.title('Total Predicted Cases by Age and Severity')

plt.show()
