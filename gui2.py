# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 08:34:15 2020

@author: Vruj
"""
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import calc

app = tk.Tk()
entry_value = tk.IntVar()

labelpop=tk.StringVar()
labelpop.set("Enter total population size: ")
labelpopS=tk.Label(app, textvariable=labelpop, height=4)
labelpopS.grid(row=1,column=0)

popS=tk.StringVar(None)
popSize=tk.Entry(app,textvariable=popS,width=15)
popSize.grid(row=1,column=1)
        
labelText=tk.StringVar()
labelText.set("Choose population distribution: ")
labelpopS=tk.Label(app, textvariable=labelText, height=4)
labelpopS.grid(row=2,column=0)

popD = tk.Listbox(app, selectmode='SINGLE', height=5, width=25) #resize box later
popD.insert(1,'Young (Niger)')
popD.insert(2,'Young adults (xx)')
popD.insert(3,'Adults (xx)')
popD.insert(4,'Middle-Aged (New York)')
popD.insert(5,'Old (Japan)')
popD.grid(row=2, column=1) # how do i center on this row?
#popD.place(relx = 0.5, rely = 0.5, anchor=tk.CENTER)

attack = tk.Scale(app, from_=0, to=entry_value.get(), orient='horizontal', label='Attack Rate')
attack.configure(to=100)
attack.grid(row=3, column = 0)

symp = tk.Scale(app, from_=0, to=entry_value.get(), orient='horizontal', label='%Symptomatic')
symp.configure(to=100)
symp.grid(row=3, column = 1)

#input for CHR

labelCHR=tk.StringVar()
labelCHR.set("Case Hospitalization Ratios")
labelCHR=tk.Label(app, textvariable=labelCHR, height=1)
labelCHR.grid(row=4,column=1)

labelCHR0=tk.StringVar()
labelCHR0.set("0 to 4")
labelCHR0=tk.Label(app, textvariable=labelCHR0, height=1)
labelCHR0.grid(row=5,column=0)
CHR0=tk.StringVar(None)
CHR0=tk.Entry(app,textvariable=CHR0,width=15)
CHR0.grid(row=5,column=1)


labelCHR1=tk.StringVar()
labelCHR1.set("5 to 17")
labelCHR1=tk.Label(app, textvariable=labelCHR1, height=1)
labelCHR1.grid(row=6,column=0)
CHR1=tk.StringVar(None)
CHR1=tk.Entry(app,textvariable=CHR1,width=15)
CHR1.grid(row=6,column=1)

labelCHR2=tk.StringVar()
labelCHR2.set("18 to 49")
labelCHR2=tk.Label(app, textvariable=labelCHR2, height=1)
labelCHR2.grid(row=7,column=0)
CHR2=tk.StringVar(None)
CHR2=tk.Entry(app,textvariable=CHR2,width=15)
CHR2.grid(row=7,column=1)

labelCHR3=tk.StringVar()
labelCHR3.set("50 to 64")
labelCHR3=tk.Label(app, textvariable=labelCHR3, height=1)
labelCHR3.grid(row=8,column=0)
CHR3=tk.StringVar(None)
CHR3=tk.Entry(app,textvariable=CHR3,width=15)
CHR3.grid(row=8,column=1)

labelCHR4=tk.StringVar()
labelCHR4.set("65+")
labelCHR4=tk.Label(app, textvariable=labelCHR4, height=1)
labelCHR4.grid(row=9,column=0)
CHR4=tk.StringVar(None)
CHR4=tk.Entry(app,textvariable=CHR4,width=15)
CHR4.grid(row=9,column=1)

#input for CCHR

labelCHR=tk.StringVar()
labelCHR.set("Critical Case Hospitalization Ratios")
labelCHR=tk.Label(app, textvariable=labelCHR, height=1)
labelCHR.grid(row=10,column=1)

labelCHR0=tk.StringVar()
labelCHR0.set("0 to 4")
labelCHR0=tk.Label(app, textvariable=labelCHR0, height=1)
labelCHR0.grid(row=11,column=0)
CHR0=tk.StringVar(None)
CHR0=tk.Entry(app,textvariable=CHR0,width=15)
CHR0.grid(row=11,column=1)


labelCHR1=tk.StringVar()
labelCHR1.set("5 to 17")
labelCHR1=tk.Label(app, textvariable=labelCHR1, height=1)
labelCHR1.grid(row=12,column=0)
CHR1=tk.StringVar(None)
CHR1=tk.Entry(app,textvariable=CHR1,width=15)
CHR1.grid(row=12,column=1)

labelCHR2=tk.StringVar()
labelCHR2.set("18 to 49")
labelCHR2=tk.Label(app, textvariable=labelCHR2, height=1)
labelCHR2.grid(row=13,column=0)
CHR2=tk.StringVar(None)
CHR2=tk.Entry(app,textvariable=CHR2,width=15)
CHR2.grid(row=13,column=1)

labelCHR3=tk.StringVar()
labelCHR3.set("50 to 64")
labelCHR3=tk.Label(app, textvariable=labelCHR3, height=1)
labelCHR3.grid(row=14,column=0)
CHR3=tk.StringVar(None)
CHR3=tk.Entry(app,textvariable=CHR3,width=15)
CHR3.grid(row=14,column=1)

labelCHR4=tk.StringVar()
labelCHR4.set("65+")
labelCHR4=tk.Label(app, textvariable=labelCHR4, height=1)
labelCHR4.grid(row=15,column=0)
CHR4=tk.StringVar(None)
CHR4=tk.Entry(app,textvariable=CHR4,width=15)
CHR4.grid(row=15,column=1)

dayPeak = tk.Scale(app, from_=30, to=entry_value.get(), resolution=30, orient='horizontal', label='Day of Peak')
dayPeak.configure(to=90)
dayPeak.grid(row=17, column=0)

labelpkN=tk.StringVar()
labelpkN.set("Peakedness")
labelpkN=tk.Label(app, textvariable=labelpkN, height=1)
labelpkN.grid(row=16,column=1)

pkN = tk.Listbox(app, selectmode='SINGLE', height=6, width=17)
pkN.insert(0,'Flat')
pkN.insert(1,'Not Peaked')
pkN.insert(2,'A Bit Peaked')
pkN.insert(3,'Very Peaked')
pkN.insert(4,'Extremely Peaked')
pkN.insert(5,'MIDAS')
pkN.grid(row=17, column=1)
        
day = tk.Scale(app, from_=1, to=entry_value.get(), orient='horizontal', label='Day')
day.configure(to=180)
day.grid(row=18, column=0)

button = tk.Button(app, text='Run simulation.', command=calc.epi_curve(30, 2))
button.grid(row=18, column=1)
#button.place(anchor=tk.CENTER)

app.mainloop()
