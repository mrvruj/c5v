# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 22:31:59 2020

@author: Vruj
"""

import tkinter

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import calc as calc
from tables import *
#from tables import *


class Window:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry('700x700')

        self.entry_value = tkinter.IntVar()

        self.button = tkinter.Button(master=self.root, text='Run simulation.', command = lambda: self.simulate())

        self.button.pack(pady=10)

        self.pop = tkinter.Scale(master=self.root, from_=1, to=self.entry_value.get(), orient='horizontal', label='Population COM')
        self.pop.pack(pady=10)
        self.pop.configure(to=5)
        
        self.attack = tkinter.Scale(master=self.root, from_=0, to=self.entry_value.get(), resolution = 5, orient='horizontal', label='Attack Rate')
        self.attack.pack(pady=10)
        self.attack.configure(to=100)
        
        self.symp = tkinter.Scale(master=self.root, from_=0, to=self.entry_value.get(), resolution = 5, orient='horizontal', label='%Symptomatic')
        self.symp.pack(pady=10)
        self.symp.configure(to=100)
        
        self.hosp = tkinter.Scale(master=self.root, from_=0, to=self.entry_value.get(), resolution = 5, orient='horizontal', label='%Hospitalized')
        self.hosp.pack(pady=10)
        self.hosp.configure(to=100)
        
        self.icu = tkinter.Scale(master=self.root, from_=0, to=self.entry_value.get(), resolution = 5, orient='horizontal', label='%ICU')
        self.icu.pack(pady=10)
        self.icu.configure(to=100)
        
        self.dayPeak = tkinter.Scale(master=self.root, from_=30, to=self.entry_value.get(), resolution=30, orient='horizontal', label='Day of Peak')
        self.dayPeak.pack(pady=10)
        self.dayPeak.configure(to=90)

        #self.pkN = tkinter.Scale(master=self.root, from_=0, to=self.entry_value.get(), orient='horizontal', label='Peakness')
        #self.pkN.pack(pady=10)
        #self.pkN.configure(to=5)
        
        #text = tkinter.Text(master=self.root)
        #text.insert(tkinter.INSERT,"Select one of the following for the degree of peakedness:")
        #text.pack()
        
        self.pkN = tkinter.Listbox(master=self.root, selectmode='SINGLE')
        self.pkN.insert(0,'0. Flat')
        self.pkN.insert(1,'1. Not Peaked')
        self.pkN.insert(2,'2. A Bit Peaked')
        self.pkN.insert(3,'3. Very Peaked')
        self.pkN.insert(4,'4. Extremely Peaked')
        self.pkN.insert(5,'5. MIDAS')
        self.pkN.pack()
        
        self.day = tkinter.Scale(master=self.root, from_=1, to=self.entry_value.get(), resolution = 5, orient='horizontal', label='Day')
        self.day.pack(pady=10)
        self.day.configure(to=180)
        
    def set_value(self):
        self.entry_value.set(self.entry_box.get())
        
    def simulate(self):
        attackRate = self.attack.get() / 100
        symp = self.symp.get() / 100
        hosp = self.hosp.get() / 100
        ICU = self.icu.get() / 100
        dayPeak = self.dayPeak.get()
        pkN = int(self.pkN.curselection()[0])
        day = self.day.get()
        totalP = 8398748
        populationType = 2
        
        ad = calc.ageDist(totalP, populationType)
        CHR = calc.CHR()
        CCHR = calc.CCHR()
        THR = calc.totalHosp(attackRate, symp, ad, CHR)
        numICU = calc.totalICUs(attackRate, symp, ad, CHR, CCHR)
        WR = calc.totalWardCases(attackRate, symp, ad, CHR, CCHR)
        dICU = calc.dailyICU(ICU, eC, day)
        dWard = calc.dailyWard(WR, eC, day)
        
        eC = calc.epi_curve(dayPeak,pkN)
        
        
        plot_gamma(eC)
        pTHR = makeGT(THR, 'TOTAL Predicted Cases').show()
        pICU = makeGT(numICU, 'TOTAL Critical Care Cases').show()
        pWR = makeGT(WR, 'TOTAL Med/Surg Ward Cases').show()
        pdICU = makeGT(dICU, 'DAILY ICU Cases - Day '  + str(day)).show()
        pdWard = makeGT(dWard, 'DAILY Ward Cases - Day ' + str(day)).show()
        
        
        
        

app = Window()
app.root.mainloop()

#print(results)
