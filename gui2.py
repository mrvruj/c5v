# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 08:34:15 2020
@author: Vruj
"""
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import calc as calc
import tables as tables

app = tk.Tk()
entry_value = tk.IntVar()

labelpop=tk.StringVar()
labelpop.set("Enter total population size: ")
labelpopS=tk.Label(app, textvariable=labelpop, height=4)
labelpopS.grid(row=1,column=0)

popS=tk.StringVar()
popS.set("8398478")
popSize=tk.Entry(app,textvariable=popS,width=15)
popSize.grid(row=1,column=1)
        
labelText=tk.StringVar()
labelText.set("Choose population distribution: ")
labelpopD=tk.Label(app, textvariable=labelText, height=4)
labelpopD.grid(row=2,column=0)

popD = tk.Listbox(app, height=4, width=25, exportselection=0) #resize box later
popD.insert(0,'Young (Mali)')
popD.insert(1,'Young adults (Bangladesh)')
popD.insert(2,'Middle-Aged (New York)')
popD.insert(3,'Old (Japan)')
popD.grid(row=2, column=1) # how do i center on this row?
popD.select_set(2)

attack = tk.Scale(app, from_=0, to=entry_value.get(), orient='horizontal', label='Attack Rate')
attack.configure(to=100)
attack.grid(row=3, column = 1)
attack.set(30)

symp = tk.Scale(app, from_=0, to=entry_value.get(), orient='horizontal', label='%Symptomatic')
symp.configure(to=100)
symp.grid(row=4, column = 1)
symp.set(50)

#input for CHR

labelCHR=tk.StringVar()
labelCHR.set("Case Hospitalization Ratios")
labelCHR=tk.Label(app, textvariable=labelCHR, height=1)
labelCHR.grid(row=5,column=1)

labelCHRm=tk.StringVar()
labelCHRm.set("Mild")
labelCHRm=tk.Label(app, textvariable=labelCHRm, height=1)
labelCHRm.grid(row=6,column=1)

labelCHRs=tk.StringVar()
labelCHRs.set("Severe")
labelCHRs=tk.Label(app, textvariable=labelCHRs, height=1)
labelCHRs.grid(row=6,column=2, padx=(0, 15))

labelCHR0=tk.StringVar()
labelCHR0.set("0 to 4")
labelCHR0=tk.Label(app, textvariable=labelCHR0, height=1)
labelCHR0.grid(row=7,column=0)

CHR0m=tk.StringVar(app, "1.25")
CHR0m=tk.Entry(app,textvariable=CHR0m,width=15) #mild 0-4
CHR0m.grid(row=7,column=1)

labelCHR1=tk.StringVar()
labelCHR1.set("5 to 17")
labelCHR1=tk.Label(app, textvariable=labelCHR1, height=1)
labelCHR1.grid(row=8,column=0)

CHR1m=tk.StringVar(app, "0.50")
CHR1m=tk.Entry(app,textvariable=CHR1m,width=15) #mild 5-17
CHR1m.grid(row=8,column=1)

labelCHR2=tk.StringVar()
labelCHR2.set("18 to 49")
labelCHR2=tk.Label(app, textvariable=labelCHR2, height=1)
labelCHR2.grid(row=9,column=0)

CHR2m=tk.StringVar(app, "1.25")
CHR2m=tk.Entry(app,textvariable=CHR2m,width=15) #mild 18-49
CHR2m.grid(row=9,column=1)

labelCHR3=tk.StringVar()
labelCHR3.set("50 to 64")
labelCHR3=tk.Label(app, textvariable=labelCHR3, height=1)
labelCHR3.grid(row=10,column=0)

CHR3m=tk.StringVar(app, "1.75")
CHR3m=tk.Entry(app,textvariable=CHR3m,width=15) #mild 50-64
CHR3m.grid(row=10,column=1)

labelCHR4=tk.StringVar()
labelCHR4.set("65+")
labelCHR4=tk.Label(app, textvariable=labelCHR4, height=1)
labelCHR4.grid(row=11,column=0)

CHR4m=tk.StringVar(app, "16.00")
CHR4m=tk.Entry(app,textvariable=CHR4m,width=15) #mild 65+
CHR4m.grid(row=11,column=1)

## severe column
CHR0s=tk.StringVar(app, "5.00")
CHR0s=tk.Entry(app,textvariable=CHR0s,width=15) #severe 0-4
CHR0s.grid(row=7,column=2, padx=(0, 15))

CHR1s=tk.StringVar(app, "2.00")
CHR1s=tk.Entry(app,textvariable=CHR1s,width=15) #severe 5-17
CHR1s.grid(row=8,column=2, padx=(0, 15))

CHR2s=tk.StringVar(app, "5.00")
CHR2s=tk.Entry(app,textvariable=CHR2s,width=15) #severe 18-49
CHR2s.grid(row=9,column=2, padx=(0, 15))

CHR3s=tk.StringVar(app, "7.00")
CHR3s=tk.Entry(app,textvariable=CHR3s,width=15) #severe 50-64
CHR3s.grid(row=10,column=2, padx=(0, 15))

CHR4s=tk.StringVar(app, "60.00")
CHR4s=tk.Entry(app,textvariable=CHR4s,width=15) #severe 65+
CHR4s.grid(row=11,column=2, padx=(0, 15))

#input for CCHR

labelCCHR=tk.StringVar()
labelCCHR.set("Critical Case Hospitalization Ratios")
labelCCHR=tk.Label(app, textvariable=labelCCHR, height=1)
labelCCHR.grid(row=12,column=1)

labelCCHRm=tk.StringVar()
labelCCHRm.set("Mild")
labelCCHRm=tk.Label(app, textvariable=labelCCHRm, height=1)
labelCCHRm.grid(row=13,column=1)

labelCCHRs=tk.StringVar()
labelCCHRs.set("Severe")
labelCCHRs=tk.Label(app, textvariable=labelCCHRs, height=1)
labelCCHRs.grid(row=13,column=2, padx=(0, 15))

labelCCHR0=tk.StringVar()
labelCCHR0.set("0 to 4")
labelCCHR0=tk.Label(app, textvariable=labelCCHR0, height=1) 
labelCCHR0.grid(row=14,column=0)

CCHR0m=tk.StringVar(app, "15.00")
CCHR0m=tk.Entry(app,textvariable=CCHR0m,width=15) #mild 0-4
CCHR0m.grid(row=14,column=1)

CCHR0s=tk.StringVar(app, "15.00")
CCHR0s=tk.Entry(app,textvariable=CCHR0s,width=15) #severe 0-4
CCHR0s.grid(row=14,column=2, padx=(0, 15))

labelCCHR1=tk.StringVar()
labelCCHR1.set("5 to 17")
labelCCHR1=tk.Label(app, textvariable=labelCCHR1, height=1)
labelCCHR1.grid(row=15,column=0)

CCHR1m=tk.StringVar(app, "20.00")
CCHR1m=tk.Entry(app,textvariable=CCHR1m,width=15) #mild 5-17
CCHR1m.grid(row=15,column=1)

CCHR1s=tk.StringVar(app, "20.00")
CCHR1s=tk.Entry(app,textvariable=CCHR1s,width=15) #severe 5-17
CCHR1s.grid(row=15,column=2, padx=(0, 15))

labelCCHR2=tk.StringVar()
labelCCHR2.set("18 to 49")
labelCCHR2=tk.Label(app, textvariable=labelCCHR2, height=1)
labelCCHR2.grid(row=16,column=0)

CCHR2m=tk.StringVar(app, "15.00")
CCHR2m=tk.Entry(app,textvariable=CCHR2m,width=15) #mild 18-49
CCHR2m.grid(row=16,column=1)

CCHR2s=tk.StringVar(app, "15.00")
CCHR2s=tk.Entry(app,textvariable=CCHR2s,width=15) #severe 18-49
CCHR2s.grid(row=16,column=2, padx=(0, 15))

labelCCHR3=tk.StringVar()
labelCCHR3.set("50 to 64")
labelCCHR3=tk.Label(app, textvariable=labelCCHR3, height=1)
labelCCHR3.grid(row=17,column=0)

CCHR3m=tk.StringVar(app, "20.00")
CCHR3m=tk.Entry(app,textvariable=CCHR3m,width=15) #mild 50-64
CCHR3m.grid(row=17,column=1)

CCHR3s=tk.StringVar(app, "20.00")
CCHR3s=tk.Entry(app,textvariable=CCHR3s,width=15) #severe 50-64
CCHR3s.grid(row=17,column=2, padx=(0, 15))

labelCCHR4=tk.StringVar()
labelCCHR4.set("65+")
labelCCHR4=tk.Label(app, textvariable=labelCCHR4, height=1)
labelCCHR4.grid(row=18,column=0)

CCHR4m=tk.StringVar(app, "15.00")
CCHR4m=tk.Entry(app,textvariable=CCHR4m,width=15) #mild 65+
CCHR4m.grid(row=18,column=1)

CCHR4s=tk.StringVar(app, "15.00")
CCHR4s=tk.Entry(app,textvariable=CCHR4s,width=15) #severe 65+
CCHR4s.grid(row=18,column=2, padx=(0, 15))

dayPeak = tk.Scale(app, from_=30, to=entry_value.get(), resolution=30, orient='horizontal', label='Day of Peak', )
dayPeak.configure(to=90)
dayPeak.grid(row=20, column=1)
dayPeak.set(30)

labelpkN=tk.StringVar()
labelpkN.set("Peakedness")
labelpkN=tk.Label(app, textvariable=labelpkN, height=1)
labelpkN.grid(row=19,column=0)

pkN = tk.Listbox(app, height=6, width=17, exportselection=0)
pkN.insert(0,'Flat')
pkN.insert(1,'Not Peaked')
pkN.insert(2,'A Bit Peaked')
pkN.insert(3,'Very Peaked')
pkN.insert(4,'Extremely Peaked')
pkN.insert(5,'MIDAS')
pkN.grid(row=19, column=1, pady=(10,0))
pkN.select_set(3)

day = tk.Scale(app, from_=1, to=entry_value.get(), orient='horizontal', label='Day')
day.configure(to=180)
day.grid(row=21, column=1)
day.set(30)

def simulate():
    attackRate = attack.get() / 100
    symptomatic = symp.get() / 100
    dayOfPeak = dayPeak.get()
    peakedness = int(pkN.curselection()[0])
    dayOf = day.get()
    totalP = int(popS.get())
    populationType = int(popD.curselection()[0])
    
    ad = calc.ageDist(totalP, populationType)
    CHR1 = calc.CHR(CHR0m.get(), CHR0s.get(), CHR1m.get(), CHR1s.get(), CHR2m.get(), CHR2s.get(), CHR3m.get(), CHR3s.get(), CHR4m.get(), CHR4s.get())
    CCHR1 = calc.CCHR(CCHR0m.get(), CCHR0s.get(), CCHR1m.get(), CCHR1s.get(), CCHR2m.get(), CCHR2s.get(), CCHR3m.get(), CCHR3s.get(), CCHR4m.get(), CCHR4s.get())
    THR = calc.totalHosp(attackRate, symptomatic, ad, CHR1)
    numICU = calc.totalICUs(attackRate, symptomatic, ad, CHR1, CCHR1)
    WR = calc.totalWardCases(attackRate, symptomatic, ad, CHR1, CCHR1)
    eC = calc.epi_curve(dayOfPeak,peakedness)
    dICU = calc.dailyICU(numICU, eC, dayOf)
    dWard = calc.dailyWard(WR, eC, dayOf)
    
    #os.mkdir('Outputs_attackRate('+str(attackRate)+')_symptomatic('+str(symptomatic)+')_peakDay('+str(dayOfPeak)+')_peakedness('+str(peakedness)+')day('+str(dayOf)+')_population('+str(totalP)')+_populationType('+str(populationType)')')
    totalWard = calc.getMaxes(WR)
    totalICU = calc.getMaxes(numICU)
    mW = totalWard[0]
    sW = totalWard[1]
    mICU = totalICU[0]
    sICU = totalICU[1]
    calc.plot_gamma(eC, mW, sW, mICU, sICU)
    pTHR = tables.makeGT(THR, 'TOTAL Predicted Cases').show()
    pICU = tables.makeGT(numICU, 'TOTAL Critical Care Cases').show()
    pWR = tables.makeGT(WR, 'TOTAL Med/Surg Ward Cases').show()
    pdICU = tables.makeGT(dICU, 'DAILY ICU Cases - Day '  + str(dayOf)).show()
    pdWard = tables.makeGT(dWard, 'DAILY Ward Cases - Day ' + str(dayOf)).show()


button = tk.Button(app, text='Calculate', command=simulate)
button.grid(row=22, column=1)
#button.place(anchor=tk.CENTER)

#app.grid(padx=20, pady=20)

app.mainloop()
