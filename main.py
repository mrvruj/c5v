#############################################################################
#C4 Desktop Application by Vruj Patel & Lior Shtayer
#############################################################################
#pylint: disable=no-name-in-module

import sys
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5.QtCore import QDateTime, Qt, QTimer, QAbstractTableModel
from PyQt5.QtWidgets import (QAbstractScrollArea, QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLCDNumber, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTableWidgetItem, 
        QTabWidget, QTableView, 
        QTextEdit, QVBoxLayout, QWidget, QHeaderView)
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import pandas as pd
import LOS_model
import calc
from imp import reload

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class c4(QDialog):
    def __init__(self, parent=None):
        super(c4, self).__init__(parent)

        self.originalPalette = QApplication.palette()

        self.createTopLeftGroupBox()
        #self.createTopRightGroupBox()
        self.createBottomLeftTabWidget()
        #self.createPlotWidget1([0,0,0,0,0],[0,0,0,0,0])
        #self.createPlotWidget2()
        #self.createPlotWidget3()
        self.createTableWidget()

        advancedCheck = QCheckBox("Advanced Options")
        advancedCheck.setChecked(True)
        advancedCheck.toggled.connect(self.bottomLeftTabWidget.setEnabled)
        
        runCalc = QPushButton("Calculate")
        runCalc.clicked.connect(self.calc) ##fix this back to calc after buttons work again
        printButton = QPushButton("Print")
        defaultButton = QPushButton("Default")
        instructions = QPushButton("Instructions")

        topLayout = QHBoxLayout()
        topLayout.addWidget(instructions)
        topLayout.addWidget(advancedCheck)
        topLayout.addWidget(defaultButton)
        topLayout.addWidget(printButton)
        topLayout.addWidget(runCalc) 
        
        x, y = [0,0,0,0,0], [0,0,0,0,0]
        self.sc1 = MplCanvas(self, width=4, height=2, dpi=100)
        self.sc1.axes.plot(x,y)
        
        w, x, y, z,  = [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]
        self.sc2 = MplCanvas(self, width=5, height=2, dpi=100)
        self.sc2.axes.plot(w,x,y,z)
        
        w, x, y, z = [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]
        self.sc3 = MplCanvas(self, width=5, height=2, dpi=100)
        self.sc3.axes.plot(w,x,y,z)
                
        self.mainLayout = QGridLayout()
        self.mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        self.mainLayout.addWidget(self.topLeftGroupBox, 1, 0, 1, 2)
        self.mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0, 1, 2)
        self.mainLayout.addWidget(self.sc1, 1, 2)
        self.mainLayout.addWidget(self.sc2, 1, 3)
        self.mainLayout.addWidget(self.sc3, 1, 4)
        #mainLayout.addWidget(self.plotWidget1, 1, 2)
        #mainLayout.addWidget(self.plotWidget2, 1, 3)
        #mainLayout.addWidget(self.plotWidget3, 1, 4)
        self.mainLayout.addWidget(self.tableWidget, 2, 2, 3, 4)
        self.mainLayout.setRowStretch(1, 1)
        self.mainLayout.setRowStretch(2, 1)
        self.mainLayout.setColumnStretch(0, 1)
        self.mainLayout.setColumnStretch(1, 1)
        self.setLayout(self.mainLayout)

        self.setWindowTitle("c4: Cornell COVID-19 Caseload Calculator")
        #self.width = 640
        #self.height = 720
        #self.left = 100
        #self.top = 100
        #self.setGeometry(self.left, self.top, self.width, self.height)
        
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        QApplication.setPalette(QApplication.style().standardPalette())
        
    def changeValue(self,value):
        return value
        
    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Input Parameters")
        
        totalPop = QSpinBox(self.topLeftGroupBox)
        totalPop.setGroupSeparatorShown(True)
        totalPop.setRange(0, 1000000000)
        totalPop.setValue(8398748)
        tPopLabel = QLabel("&Total Population:")
        tPopLabel.setBuddy(totalPop)
        
        popDist = QComboBox()
        popDist.addItems(('Young (Mali)', 'Young Adults (Bangladesh)', 'Middle-Aged (United States)', 'Old (Japan)'))
        popDistLabel = QLabel("Population Distribution:")
        popDistLabel.setBuddy(popDist)
        popDist.setCurrentIndex(2)
        
        infRate = QSlider(Qt.Horizontal, self.topLeftGroupBox)
        infRate.setTickInterval(10)
        infRate.setTickPosition(QSlider.TicksBothSides)
        infRate.setValue(40)
        infRateLabel = QLabel("Infection Rate: ")
        infRateLabel.setBuddy(infRate)
        def infRateVal(self,val):
            infRateVal = QSpinBox(self.topLeftGroupBox)
            infRateVal.setValue(val)
        infRate.valueChanged.connect(infRateVal)
        
        sympRate = QSlider(Qt.Horizontal, self.topLeftGroupBox)
        sympRate.setTickInterval(10)
        sympRate.setTickPosition(QSlider.TicksBothSides)
        sympRate.setValue(40)
        sympRateLabel = QLabel("% Symptomatic: ")
        sympRateLabel.setBuddy(sympRate)
        
        peaked = QComboBox()
        peaked.addItems(('A-type: Broad', 'B-type: Somewhat Broad', 'C-type: A Bit Peaked', 'D-type: Very Peaked', 'E-type: Extremely Peaked'))
        peakedLabel = QLabel("Shape of the epidemic curve: ")
        peakedLabel.setBuddy(peaked)
        peaked.setCurrentIndex(2)
        
        peakDay = QComboBox()
        peakDay.addItems(('30', '60', '90'))
        peakDayLabel = QLabel("Choose the day of maximum cases: ")
        peakDayLabel.setBuddy(peakDay)
        peakDay.setCurrentIndex(1)
        
        dayOutput = QDial(self.topLeftGroupBox)
        dayOutput.setMinimum(1)
        dayOutput.setMaximum(180)
        dayOutput.setValue(60)
        dayOutput.setNotchesVisible(True)
        dayOutputLabel = QLabel("Day of Output:")
        dayOutputLabel.setBuddy(dayOutput)
        #dayCount = QLabel(str(dayOutput.valueChanged.connect(dayOutput.sliderMoved))) #Figure out how to display the current day as selected by slider
        #dayCount.setBuddy(dayOutput)
        
        layout = QVBoxLayout()
        layout.addWidget(tPopLabel)
        layout.addWidget(totalPop)
        layout.addStretch(1)
        layout.addWidget(popDistLabel)
        layout.addWidget(popDist)
        layout.addStretch(1)
        layout.addWidget(infRateLabel)
        layout.addWidget(infRate)
        #layout.addWidget(infRateVal)
        layout.addStretch(1)
        layout.addWidget(sympRateLabel)
        layout.addWidget(sympRate)
        layout.addStretch(1)
        layout.addWidget(peakedLabel)
        layout.addWidget(peaked)
        layout.addStretch(1)
        layout.addWidget(peakDayLabel)
        layout.addWidget(peakDay)
        layout.addStretch(1)
        layout.addWidget(dayOutputLabel)
        layout.addWidget(dayOutput)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)    

    def createBottomLeftTabWidget(self):
        self.bottomLeftTabWidget = QTabWidget()
        #there will be a policy here to resize all columns to fit (one liner)
        
        tab1 = QWidget()
        CHR = QTableWidget(7, 2)
        CHRLabel = QLabel("Case Hospitalization Ratio (%)")
        CHRLabel.setBuddy(CHR)
        CHRDefault = QPushButton("Default")
        #CHRDefault.clicked.connect(self.chrDefaults(CHR))
        tab1grid = QGridLayout()
        tab1grid.setContentsMargins(5, 5, 5, 5)
        tab1grid.addWidget(CHRLabel, 0, 0) 
        tab1grid.addWidget(CHRDefault, 0, 1)
        tab1grid.addWidget(CHR, 1, 0, 1, 2)
        tab1.setLayout(tab1grid)
        CHR.setHorizontalHeaderLabels(("Mild Scenario", "Severe Scenario"))
        CHR.setVerticalHeaderLabels(("0-19", "20-44", "45-54", "55-64", "65-74", "75-84", "=>85"))
        header = CHR.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents) 

        tab2 = QWidget()
        CCHF = QTableWidget(7, 2)
        CCHFLabel = QLabel("Critical Care Hospitalization Fraction (%)")
        CCHFLabel.setBuddy(CCHF)
        CCHFDefault = QPushButton("Default")
        tab2grid = QGridLayout()
        tab2grid.setContentsMargins(5, 5, 5, 5)
        tab2grid.addWidget(CCHFLabel, 0, 0) 
        tab2grid.addWidget(CCHFDefault, 0, 1)
        tab2grid.addWidget(CCHF, 1, 0, 1, 2)
        tab2.setLayout(tab2grid)
        CCHF.setHorizontalHeaderLabels(("Mild Scenario", "Severe Scenario"))
        CCHF.setVerticalHeaderLabels(("0-19", "20-44", "45-54", "55-64", "65-74", "75-84", "=>85"))
        header = CCHF.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents) 
        
        tab3 = QWidget()
        LOS = QTableWidget(4, 4)
        LOSLabel = QLabel("Enter min/max length of stay, %mortality, and change in LOS for patients who die.")
        LOSLabel.setBuddy(LOS)
        LOSDefault = QPushButton("Default")
        tab3grid = QGridLayout()
        tab3grid.setContentsMargins(5, 5, 5, 5)
        tab3grid.addWidget(LOSLabel, 0, 0)
        tab3grid.addWidget(LOSDefault, 0, 1)
        tab3grid.addWidget(LOS, 1, 0, 1, 2)
        tab3.setLayout(tab3grid)
        LOS.setHorizontalHeaderLabels(("Minimum LOS", "Maximum LOS", "Mortality Ratio", "LOS Adjustment"))
        LOS.setVerticalHeaderLabels(("Adult Ward Beds", "Adult ICU Beds", "Pediatric Ward Beds", "Pediatric ICU Beds"))
        header = LOS.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents) 
        
        tab4 = QWidget()
        capInputs = QTableWidget(1, 5)
        capInputLabel = QLabel("Enter parameters for capacitated model:")
        capInputLabel.setBuddy(capInputs)
        capInputDefault = QPushButton("Default")
        tab4grid = QGridLayout()
        tab4grid.setContentsMargins(5, 5, 5, 5)
        tab4grid.addWidget(capInputLabel, 0, 0)
        tab4grid.addWidget(capInputDefault, 0, 1)
        tab4grid.addWidget(capInputs, 1, 0, 1, 2)
        tab4.setLayout(tab4grid)
        capInputs.setHorizontalHeaderLabels(("Available Ward Beds", "Available ICU Beds", "Available Ventilators", "Patients per Ventilator", "Effective Ventilator Supply"))
        header = capInputs.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents) 
        
        tab5 = QWidget()
        noVent = QTableWidget(4, 2)
        noVentLabel = QLabel("Unventilated ICU Patient Parameters:")
        noVentLabel.setBuddy(noVent)
        noVentDefault = QPushButton("Default")
        tab5grid = QGridLayout()
        tab5grid.setContentsMargins(5, 5, 5, 5)
        tab5grid.addWidget(noVentLabel, 0, 0)
        tab5grid.addWidget(noVentDefault, 0, 1)
        tab5grid.addWidget(noVent, 1, 0, 1, 2)
        tab5.setLayout(tab5grid)
        noVent.setHorizontalHeaderLabels(("Mild Scenario", "Severe Scenario"))
        noVent.setVerticalHeaderLabels(("Survivor Minimum LOS", "Survivor Maximum LOS", "Mortality Ratio (%)", "LOS Adjustment (%)"))
        header = noVent.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents) 

        self.setDefaults(CHR, CCHF, capInputs, noVent, LOS)

        self.bottomLeftTabWidget.addTab(tab1, "CHR")
        self.bottomLeftTabWidget.addTab(tab2, "CCHF")
        self.bottomLeftTabWidget.addTab(tab3, "LOS")
        self.bottomLeftTabWidget.addTab(tab4, "Capacitated Inputs")
        self.bottomLeftTabWidget.addTab(tab5, "No Vents")
        
    def createPlotWidget1(self,x,y):
        self.plotWidget1 = QGroupBox("Possible COVID-19 Hospital-Apparent Epidemic Curves")    
        
        sc1 = MplCanvas(self, width=3, height=2, dpi=100)
        sc1.axes.plot(x,y)
        
        layout = QVBoxLayout()
        layout.addWidget(sc1)
        self.plotWidget1.setLayout(layout)
        
    def createPlotWidget2(self):
        self.plotWidget2 = QGroupBox("Adult Patient Daily Census by Location and Scenario")    
        
        sc2 = MplCanvas(self, width=3, height=2, dpi=100)
        sc2.axes.plot([0,1,2,3,4], [40,3,20,1,10])

        layout = QVBoxLayout()
        layout.addWidget(sc2)
        self.plotWidget2.setLayout(layout)
        
    def createPlotWidget3(self):
        self.plotWidget3 = QGroupBox("Pediatric Patient Daily Census by Location and Scenario")    
        
        sc3 = MplCanvas(self, width=3, height=2, dpi=100)
        sc3.axes.plot([0,1,2,3,4], [10,1,20,3,40])
                
        layout = QVBoxLayout()
        layout.addWidget(sc3)
        self.plotWidget3.setLayout(layout)
           
    def createTableWidget_OLD(self):
        self.tableWidget = QTabWidget()
        
        tab1 = QWidget()
        THR = QTableWidget(8, 2)
        THRLabel = QLabel("Total Hospitalizations")
        THRLabel.setBuddy(THR)
        tab1grid = QGridLayout()
        tab1grid.setContentsMargins(5, 5, 5, 5)
        tab1grid.addWidget(THRLabel, 0, 0) 
        tab1grid.addWidget(THR, 1, 0, 1, 2)
        tab1.setLayout(tab1grid)
        THR.setHorizontalHeaderLabels(("Mild Scenario", "Severe Scenario"))
        THR.setVerticalHeaderLabels(("0-19", "20-44", "45-54", "55-64", "65-74", "75-84", "=>85", "Total"))
        header = THR.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents) 
        
        tab2 = QWidget()
        MILD = QTableWidget(6, 7)
        MILDLabel = QLabel("Detailed Results of the MILD Scenario")
        MILDLabel.setBuddy(MILD)
        tab2grid = QGridLayout()
        tab2grid.setContentsMargins(5, 5, 5, 5)
        tab2grid.addWidget(MILDLabel, 0, 0) 
        tab2grid.addWidget(MILD, 1, 0, 1, 2)
        tab2.setLayout(tab2grid)
        MILD.setHorizontalHeaderLabels(("Total Number Admitted","Peak Daily Admissions","Day of Peak Admissions", "Peak Hospital Census",
                                       "Day of Peak Census", "Total Deaths", "Total Discharges"))
        MILD.setVerticalHeaderLabels(("ADULT:","Ward Cases", "ICU Cases", "PEDIATRIC:", "Ward Cases", "ICU Cases"))
        header = MILD.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        
        tab3 = QWidget()
        SEVERE = QTableWidget(6, 7)
        SEVERELabel = QLabel("Detailed Results of the SEVERE Scenario")
        SEVERELabel.setBuddy(SEVERE)
        tab3grid = QGridLayout()
        tab3grid.setContentsMargins(5, 5, 5, 5)
        tab3grid.addWidget(SEVERELabel, 0, 0) 
        tab3grid.addWidget(SEVERE, 1, 0, 1, 2)
        tab3.setLayout(tab3grid)
        SEVERE.setHorizontalHeaderLabels(("Total Number Admitted","Peak Daily Admissions","Day of Peak Admissions", "Peak Hospital Census",
                                       "Day of Peak Census", "Total Deaths", "Total Discharges"))
        SEVERE.setVerticalHeaderLabels(("ADULT:","Ward Cases", "ICU Cases", "PEDIATRIC:", "Ward Cases","ICU Cases"))
        header = SEVERE.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        tab4 = QWidget()
        MED = QTableWidget(2, 4)
        MEDLabel = QLabel("Adult Ward Beds")
        MEDLabel.setBuddy(MED)
        tab4grid = QGridLayout()
        tab4grid.setContentsMargins(5, 5, 5, 5)
        tab4grid.addWidget(MEDLabel, 0, 0) 
        tab4grid.addWidget(MED, 1, 0, 1, 2)
        tab4.setLayout(tab4grid)
        MED.setHorizontalHeaderLabels(("Total Medical Ward Patients", "Peak SIMULTANEOUS Beds (Max Census)", "Day of Max Census",
                                       "TOTAL Patient-Days for COVID Med/Surg Patients"))
        MED.setVerticalHeaderLabels(("MILD SCENARIO", "SEVERE SCENARIO"))
        header = MED.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        
        tab5 = QWidget()
        ICU = QTableWidget(2, 5)
        ICULabel = QLabel("Adult ICU Beds and Ventilators")
        ICULabel.setBuddy(ICU)
        tab5grid = QGridLayout()
        tab5grid.setContentsMargins(5, 5, 5, 5)
        tab5grid.addWidget(ICULabel, 0, 0) 
        tab5grid.addWidget(ICU, 1, 0, 1, 2)
        tab5.setLayout(tab5grid)
        ICU.setHorizontalHeaderLabels(("Total ICU Patients", "Peak SIMULTANEOUS ICU Bed Requirement", "Day of Max Census",
                                       "TOTAL Patient-Days for COVID ICU Patients", 
                                       "Peak Ventilator Need (80% Ventilated Fraction)"))
        ICU.setVerticalHeaderLabels(("MILD Scenario", "SEVERE Scenario"))
        header = ICU.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        
        self.tableWidget.addTab(tab1, "Total Hospitalizations")
        self.tableWidget.addTab(tab2, "Detailed Results of the MILD Scenario")
        self.tableWidget.addTab(tab3, "Detailed Results of the SEVERE Scenario")
        self.tableWidget.addTab(tab4, "Adult Ward Beds")
        self.tableWidget.addTab(tab5, "Adult ICU Beds and Ventilators")
        
    def createTableWidget(self):
        self.tableWidget = QTabWidget()
        
        tab1 = QTableView(None)
        tab2 = QTableView(None)
        tab3 = QTableView(None)
        tab4 = QTableView(None)
        tab5 = QTableView(None)

        self.tableWidget.addTab(tab1, "Total Hospitalizations")
        self.tableWidget.addTab(tab2, "Detailed Results of the MILD Scenario")
        self.tableWidget.addTab(tab3, "Detailed Results of the SEVERE Scenario")
        self.tableWidget.addTab(tab4, "Adult Ward Beds")
        self.tableWidget.addTab(tab5, "Adult ICU Beds and Ventilators")
                
### GETTERS AND SETTERS ###

    def chrDefaults(self, CHR): 
        CHR.setItem(0,0, QTableWidgetItem("1.6"))
        CHR.setItem(1,0, QTableWidgetItem("14.3"))
        CHR.setItem(2,0, QTableWidgetItem("21.2"))
        CHR.setItem(3,0, QTableWidgetItem("20.5"))
        CHR.setItem(4,0, QTableWidgetItem("28.6"))
        CHR.setItem(5,0, QTableWidgetItem("30.5"))
        CHR.setItem(6,0, QTableWidgetItem("31.3"))
        
        CHR.setItem(0,1, QTableWidgetItem("2.5"))
        CHR.setItem(1,1, QTableWidgetItem("20.8"))
        CHR.setItem(2,1, QTableWidgetItem("28.3"))
        CHR.setItem(3,1, QTableWidgetItem("30.1"))
        CHR.setItem(4,1, QTableWidgetItem("43.5"))
        CHR.setItem(5,1, QTableWidgetItem("58.7"))
        CHR.setItem(6,1, QTableWidgetItem("70.3"))
    def cchfDefaults(self, CCHF):
        CCHF.setItem(0,0, QTableWidgetItem("0"))
        CCHF.setItem(1,0, QTableWidgetItem("2.0"))
        CCHF.setItem(2,0, QTableWidgetItem("5.4"))
        CCHF.setItem(3,0, QTableWidgetItem("4.7"))
        CCHF.setItem(4,0, QTableWidgetItem("8.1"))
        CCHF.setItem(5,0, QTableWidgetItem("10.5"))
        CCHF.setItem(6,0, QTableWidgetItem("6.3"))
        
        CCHF.setItem(0,1, QTableWidgetItem("0"))
        CCHF.setItem(1,1, QTableWidgetItem("4.2"))
        CCHF.setItem(2,1, QTableWidgetItem("10.4"))
        CCHF.setItem(3,1, QTableWidgetItem("11.2"))
        CCHF.setItem(4,1, QTableWidgetItem("18.8"))
        CCHF.setItem(5,1, QTableWidgetItem("31.0"))
        CCHF.setItem(6,1, QTableWidgetItem("29.0"))
    def LOSDefaults(self, LOS):
        LOS.setItem(0,0, QTableWidgetItem("3"))
        LOS.setItem(1,0, QTableWidgetItem("7"))
        LOS.setItem(2,0, QTableWidgetItem("2"))
        LOS.setItem(3,0, QTableWidgetItem("3"))     
        LOS.setItem(0,1, QTableWidgetItem("7"))
        LOS.setItem(1,1, QTableWidgetItem("21"))
        LOS.setItem(2,1, QTableWidgetItem("4"))
        LOS.setItem(3,1, QTableWidgetItem("6"))
        LOS.setItem(0,2, QTableWidgetItem("5"))
        LOS.setItem(1,2, QTableWidgetItem("25"))
        LOS.setItem(2,2, QTableWidgetItem("0.01"))
        LOS.setItem(3,2, QTableWidgetItem("0.02"))
        LOS.setItem(0,3, QTableWidgetItem("150"))
        LOS.setItem(1,3, QTableWidgetItem("150"))
        LOS.setItem(2,3, QTableWidgetItem("100"))
        LOS.setItem(3,3, QTableWidgetItem("100"))      
    def bedDefaults(self, bed):
        bed.setItem(0, 0, QTableWidgetItem("20000"))
        bed.setItem(0, 1, QTableWidgetItem("1800"))
        bed.setItem(0, 2, QTableWidgetItem("1000"))
        bed.setItem(0, 3, QTableWidgetItem("1.25"))
        bed.setItem(0, 4, QTableWidgetItem("1250"))
    def ventDefaults(self, vent):
        vent.setItem(0,0, QTableWidgetItem("2"))
        vent.setItem(1,0, QTableWidgetItem("10"))
        vent.setItem(2,0, QTableWidgetItem("95"))
        vent.setItem(3,0, QTableWidgetItem("5"))
        
        vent.setItem(0,1, QTableWidgetItem("2"))
        vent.setItem(1,1, QTableWidgetItem("10"))
        vent.setItem(2,1, QTableWidgetItem("95"))
        vent.setItem(3,1, QTableWidgetItem("5"))
    def setDefaults(self, CHR, CCHF, bed, vent, LOS):
        self.chrDefaults(CHR)
        self.cchfDefaults(CCHF)
        self.bedDefaults(bed)
        self.ventDefaults(vent)
        self.LOSDefaults(LOS)

    def getCHR(self): 
        df = pd.DataFrame(columns = ["Mild", "Severe"])
        CHR = self.bottomLeftTabWidget.widget(0).children()[3]
        df = df.append({'Mild': float(CHR.item(0,0).text())/100, 'Severe': float(CHR.item(0,1).text())/100}, ignore_index=True) #0-19
        df = df.append({'Mild': float(CHR.item(1,0).text())/100, 'Severe': float(CHR.item(1,1).text())/100}, ignore_index=True) #20-44
        df = df.append({'Mild': float(CHR.item(2,0).text())/100, 'Severe': float(CHR.item(2,1).text())/100}, ignore_index=True) #45-54
        df = df.append({'Mild': float(CHR.item(3,0).text())/100, 'Severe': float(CHR.item(3,1).text())/100}, ignore_index=True) #55-64
        df = df.append({'Mild': float(CHR.item(4,0).text())/100, 'Severe': float(CHR.item(4,1).text())/100}, ignore_index=True) #65-74
        df = df.append({'Mild': float(CHR.item(5,0).text())/100, 'Severe': float(CHR.item(5,1).text())/100}, ignore_index=True) #75-84
        df = df.append({'Mild': float(CHR.item(6,0).text())/100, 'Severe': float(CHR.item(6,1).text())/100}, ignore_index=True) #85+
        return df
    def getCCHF(self): 
        df = pd.DataFrame(columns = ["Mild", "Severe"])
        CCHF = self.bottomLeftTabWidget.widget(1).children()[3]
        df = df.append({'Mild': float(CCHF.item(0,0).text())/100, 'Severe': float(CCHF.item(0,1).text())/100}, ignore_index=True) #0-19
        df = df.append({'Mild': float(CCHF.item(1,0).text())/100, 'Severe': float(CCHF.item(1,1).text())/100}, ignore_index=True) #20-44
        df = df.append({'Mild': float(CCHF.item(2,0).text())/100, 'Severe': float(CCHF.item(2,1).text())/100}, ignore_index=True) #45-54
        df = df.append({'Mild': float(CCHF.item(3,0).text())/100, 'Severe': float(CCHF.item(3,1).text())/100}, ignore_index=True) #55-64
        df = df.append({'Mild': float(CCHF.item(4,0).text())/100, 'Severe': float(CCHF.item(4,1).text())/100}, ignore_index=True) #65-74
        df = df.append({'Mild': float(CCHF.item(5,0).text())/100, 'Severe': float(CCHF.item(5,1).text())/100}, ignore_index=True) #75-84
        df = df.append({'Mild': float(CCHF.item(6,0).text())/100, 'Severe': float(CCHF.item(6,1).text())/100}, ignore_index=True) #85+
        return df
    def getLOS(self): 
        df = pd.DataFrame(columns = ['Minimum LOS', 'Maximum LOS', 'Mortality Ratio', 'LOS Adjustment'])
        LOS = self.bottomLeftTabWidget.widget(2).children()[3]
        df = df.append({'Minimum LOS': float(LOS.item(0,0).text()), 'Maximum LOS': float(LOS.item(0,1).text()), 'Mortality Ratio': float(LOS.item(0,2).text()), 'LOS Adjustment': float(LOS.item(0,3).text())}, ignore_index=True) #adult ward beds
        df = df.append({'Minimum LOS': float(LOS.item(1,0).text()), 'Maximum LOS': float(LOS.item(1,1).text()), 'Mortality Ratio': float(LOS.item(1,2).text()), 'LOS Adjustment': float(LOS.item(1,3).text())}, ignore_index=True) #adult icu beds
        df = df.append({'Minimum LOS': float(LOS.item(2,0).text()), 'Maximum LOS': float(LOS.item(2,1).text()), 'Mortality Ratio': float(LOS.item(2,2).text()), 'LOS Adjustment': float(LOS.item(2,3).text())}, ignore_index=True) #ped ward beds
        df = df.append({'Minimum LOS': float(LOS.item(3,0).text()), 'Maximum LOS': float(LOS.item(3,1).text()), 'Mortality Ratio': float(LOS.item(3,2).text()), 'LOS Adjustment': float(LOS.item(3,3).text())}, ignore_index=True) #ped icu beds
        return df
    def getBeds(self):
        df = pd.DataFrame(columns = ['Available Ward Beds', 'Available ICU Beds', 'Available Ventilators', 'Patients per Ventilator', 'Effective Ventilator Supply'])
        beds = self.bottomLeftTabWidget.widget(3).children()[3]
        df = df.append({'Available Ward Beds': float(beds.item(0,0).text()), 
                        'Available ICU Beds': float(beds.item(0,1).text()), 
                        'Available Ventilators': float(beds.item(0,2).text()), 
                        'Patients per Ventilator': float(beds.item(0,3).text()), 
                        'Effective Ventilator Supply': float(beds.item(0,4).text())}, ignore_index=True)
        return df
    def getNoVents(self):
        df = pd.DataFrame(columns = ['Mild', 'Severe'])
        noVents = self.bottomLeftTabWidget.widget(4).children()[3]
        df = df.append({'Mild': float(noVents.item(0,0).text()), 'Severe': float(noVents.item(0,1).text())}, ignore_index=True) #Survivor Minimum LOS
        df = df.append({'Mild': float(noVents.item(1,0).text()), 'Severe': float(noVents.item(1,1).text())}, ignore_index=True) #Survivor Maximum LOS
        df = df.append({'Mild': float(noVents.item(2,0).text()), 'Severe': float(noVents.item(2,1).text())}, ignore_index=True) #Mortality Ratio (%)
        df = df.append({'Mild': float(noVents.item(3,0).text()), 'Severe': float(noVents.item(3,1).text())}, ignore_index=True) #LOS Adjustment (%)
        return df
    
    def getInfectionRate(self): #returns a decimal between 0 and 1
        return self.topLeftGroupBox.children()[1].value()/100
    def getSymptomatic(self): #returns a decimal between 0 and 1
        return self.topLeftGroupBox.children()[2].value()/100
    def getPopDist(self): #returns an index
        return self.topLeftGroupBox.children()[7].currentIndex()
    def getPop(self): #returns an int
        return self.topLeftGroupBox.children()[0].value()
    def getShapeCurve(self): #returns index
        return self.topLeftGroupBox.children()[11].currentIndex()
    def getDayMax(self): #returns an int
        index = self.topLeftGroupBox.children()[13].currentIndex()
        if index == 0:
            return 30
        if index == 1:
            return 60
        if index == 2:
            return 90
    def getDayOutput(self): #returns an int
        return self.topLeftGroupBox.children()[3].value()

### TESTS AND SIMULATION ### 

    def test(self): #put this function in line 29 instead of calc to test the getters
        print(self.getCHR()) #CHR
        print(self.getCCHF()) #CCHF
        print(self.getLOS()) #LOS
        print(self.getBeds()) #beds
        print(self.getNoVents()) #noVents
        print(self.getInfectionRate()) #inf
        print(self.getSymptomatic()) #symp
        print(self.getPopDist()) #should be an index
        print(self.getPop()) #should be an int
        print(self.getShapeCurve()) #should be an index
        print(self.getDayMax()) #should be an int
        print(self.getDayOutput()) #should be an int
    
    def calc(self):
        #get GUI parameters
        attackRate = self.getInfectionRate()
        symptomatic = self.getSymptomatic()
        dayOfPeak = self.getDayMax()
        peakedness = self.getShapeCurve()
        dayOf = self.getDayOutput()
        totalP = self.getPop()
        populationType = self.getPopDist()
        CHR = self.getCHR()
        CCHF = self.getCCHF()
        LOS = self.getLOS()   
        
        #common dataframes
        ad = calc.ageDist(totalP, populationType) #age distribution based on inputs
        THR = calc.totalHosp(attackRate, symptomatic, ad, CHR) #total hospitalizations (by age); note this is a duplicated calculation since the below functions call totalHosp() themselves
        numICU = calc.totalICUs(THR, CCHF) #total ICU cases (by age)
        WR = calc.totalWardCases(THR, numICU) #total ward cases (by age)
        eC = calc.epi_curve(dayOfPeak,peakedness) #curve that tells us how total cases are distributed in time

        #ward and ICU cases by adult/peds status
        tICU_p = calc.tICU_peds(numICU) #total pediatric ICU cases
        tICU_a = calc.tICU_adults(numICU) #total adult ICU cases
        tWard_p = calc.tWard_peds(WR) #total pediatric ward cases
        tWard_a = calc.tWard_adults(WR) #total adult ward cases
        
        #daily cases (for output tables @ given day)
        dICU = calc.dailyICU(numICU, eC, dayOf) #daily ICU cases (by age)
        dWard = calc.dailyWard(WR, eC, dayOf) #daily ward cases (by age)
        dICU_p = calc.dICU_peds(dICU) #daily pediatric ICU cases
        dICU_a = calc.dICU_adults(dICU) #daily adult ICU cases
        dWard_p = calc.dWard_peds(dWard) #daily pediatric ward cases
        dWard_a = calc.dWard_adults(dWard) #daily adult ward cases
        
        #calculate grand totals
        totalWard = calc.getMaxes(WR) #sum total of all ward cases (mild AND severe scenarios)
        totalICU = calc.getMaxes(numICU) #sum total of all ICU cases
        mW = totalWard[0] #sum total of all ward cases in the mild scenario
        sW = totalWard[1] #sum total of all ward cases in the severe scenario
        mildICU = totalICU[0] #sum total of all ICU cases in the mild scenario
        sevICU = totalICU[1] #sum total of all ICu cases in the severe scenario
    
        LOS_model.calc_LOS_Admissions(eC, tICU_p, tICU_a, tWard_p, tWard_a)
        LOS_model.calc_LOS_data(LOS)
        LOS_model.calc_LOS_Deaths()
        LOS_model.calc_LOS_Discharges()
        LOS_model.calc_LOS_Occupancy()
        #calc.plot(eC,LOS_model.LOS_Occupancy_df)
        
        #Plot epi curve
        self.mainLayout.removeWidget(self.sc1)
        self.sc1.close()
        self.sc1 = MplCanvas(self, width=4, height=2, dpi=100)
        self.sc1.axes.plot(eC['Day'],eC['Gamma_Values'])
        self.mainLayout.addWidget(self.sc1, 1, 2)
        self.mainLayout.update()
        self.setLayout(self.mainLayout)
        
        #Plot adult scenario
        self.mainLayout.removeWidget(self.sc2)
        self.sc2.close()
        self.sc2 = MplCanvas(self, width=5, height=2, dpi=100)
        self.sc2.axes.plot(LOS_model.LOS_Occupancy_df['Day'],LOS_model.LOS_Occupancy_df['mW_A'],color='c', label='Adult Mild Ward')
        self.sc2.axes.plot(LOS_model.LOS_Occupancy_df['Day'],LOS_model.LOS_Occupancy_df['sW_A'],color='m', label='Adult Severe Ward')
        self.sc2.axes.plot(LOS_model.LOS_Occupancy_df['Day'],LOS_model.LOS_Occupancy_df['mICU_A'],color='b', label='Adult Mild ICU')
        self.sc2.axes.plot(LOS_model.LOS_Occupancy_df['Day'],LOS_model.LOS_Occupancy_df['sICU_A'],color='r', label='Adult Severe ICU')
        self.sc2.axes.legend()
        self.mainLayout.addWidget(self.sc2, 1, 3)
        self.mainLayout.update()
        self.setLayout(self.mainLayout)
        
        #Plot peds scenario
        self.mainLayout.removeWidget(self.sc3)
        self.sc3.close()
        self.sc3 = MplCanvas(self, width=5, height=2, dpi=100)
        self.sc3.axes.plot(LOS_model.LOS_Occupancy_df['Day'],LOS_model.LOS_Occupancy_df['mW_P'],color='c', label='Pediatric Mild Ward')
        self.sc3.axes.plot(LOS_model.LOS_Occupancy_df['Day'],LOS_model.LOS_Occupancy_df['sW_P'],color='m', label='Pediatric Severe Ward')
        self.sc3.axes.plot(LOS_model.LOS_Occupancy_df['Day'],LOS_model.LOS_Occupancy_df['mICU_P'],color='b', label='Pediatric Mild ICU')
        self.sc3.axes.plot(LOS_model.LOS_Occupancy_df['Day'],LOS_model.LOS_Occupancy_df['sICU_P'],color='r', label='Pediatric Severe ICU')
        self.sc3.axes.legend()
        self.mainLayout.addWidget(self.sc3, 1, 4)
        self.mainLayout.update()
        self.setLayout(self.mainLayout)
        #reload(calc)
        reload(LOS_model)

        
        self.tableWidget.removeTab(4)
        self.tableWidget.removeTab(3)
        self.tableWidget.removeTab(2)
        self.tableWidget.removeTab(1)
        self.tableWidget.removeTab(0)
        
        tab1 = QTableView(None)
        THR_mod = TableModel(THR) #need to round the dataframes
        tab1.setModel(THR_mod)
        
        tab2 = QTableView(None)
        MILD = QStandardItemModel()
        tab2.setModel(MILD)
        
        tab3 = QTableView(None)
        SEVERE = QStandardItemModel()
        tab3.setModel(SEVERE)
        
        tab4 = QTableView(None)
        AWARD = QStandardItemModel()
        tab4.setModel(AWARD)
        
        tab5 = QTableView(None)
        AICU = QStandardItemModel()
        tab5.setModel(AICU)
        
        self.tableWidget.addTab(tab1, "Total Hospitalizations")
        self.tableWidget.addTab(tab2, "Detailed Results of the MILD Scenario")
        self.tableWidget.addTab(tab3, "Detailed Results of the SEVERE Scenario")
        self.tableWidget.addTab(tab4, "Adult Ward Beds")
        self.tableWidget.addTab(tab5, "Adult ICU Beds and Ventilators")
        
class TableModel(QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]
    
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])        
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = c4()
    window.showMaximized()
    window.show()
    sys.exit(app.exec_()) 