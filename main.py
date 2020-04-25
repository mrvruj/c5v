#############################################################################
#C4 Desktop Application by Vruj Patel & Lior Shtayer
#############################################################################
#pylint: disable=no-name-in-module

## IMPORTS ##

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
        QTextEdit, QVBoxLayout, QWidget, QHeaderView, QMessageBox)
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QFontMetrics
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import pandas as pd
import LOS_model
import calc
from imp import reload

class c4(QDialog):
    def __init__(self, parent=None):
        super(c4, self).__init__(parent)

        x = [1, 2, 3, 4, 5]
        self.createTopLeftGroupBox()
        self.createBottomLeftTabWidget()
        self.createEpiCurvePlot(x, x)
        self.createAdultPlot(x, x, x, x, x)
        self.createPedPlot(x, x, x, x, x)
        self.createTableWidget()

        advancedCheck = QCheckBox("Advanced Options")
        advancedCheck.setChecked(True)
        advancedCheck.toggled.connect(self.bottomLeftTabWidget.setEnabled)
        
        runCalc = QPushButton("Calculate")
        runCalc.clicked.connect(self.calc) 
        printButton = QPushButton("Print")
        defaultButton = QPushButton("Default")
        instructions = QPushButton("Instructions")
        instructions.clicked.connect(self.instructions)

        self.topLayout = QHBoxLayout()
        self.topLayout.addWidget(instructions)
        self.topLayout.addWidget(advancedCheck)
        self.topLayout.addWidget(defaultButton)
        self.topLayout.addWidget(printButton)
        self.topLayout.addWidget(runCalc) 
        
        self.results = QLabel() #placeholder so the deleteLater() in calc doesn't shit a brick
                        
        self.mainLayout = QGridLayout()
        self.mainLayout.addLayout(self.topLayout, 0, 0)
        self.mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        self.mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        self.mainLayout.addWidget(self.epiPlot, 1, 1)
        self.mainLayout.addWidget(self.adultPlot, 1, 2)
        self.mainLayout.addWidget(self.pedPlot, 1, 3)
        self.mainLayout.addWidget(self.tableWidget, 2, 1, 1, 3) #the 3 is so it spans the length of 3 plots
        self.mainLayout.setColumnStretch(0, 0) #ensures that the plots are larger than the input groupbox when window is stretched
        self.mainLayout.setColumnStretch(1, 2) 
        self.mainLayout.setColumnStretch(2, 2)
        self.mainLayout.setColumnStretch(3, 2)
        self.setLayout(self.mainLayout)

        self.setWindowTitle("C5V Modeling Tool: Cornell COVID-19 Caseload Calculator with Capacity and Ventilators")
        
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        QApplication.setPalette(QApplication.style().standardPalette())
        
## INPUT ##
        
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
     
## OUTPUT ##
        
    def createEpiCurvePlot(self, x, y):
        self.epiPlot = QGroupBox("Possible COVID-19 Hospital-Apparent Epidemic Curve")    
        
        epiCurve = MplCanvas(self, width=3, height=2, dpi=100)
        epiCurve.axes.plot(x, y)
    
        layout = QGridLayout()
        layout.addWidget(epiCurve)
        self.epiPlot.setLayout(layout)
        
    def createAdultPlot(self, x, y_occ_mW_A, y_occ_sW_A, y_occ_mICU_A, y_occ_sICU_A):
        self.adultPlot = QGroupBox("Adult Patient Daily Census by Location and Scenario")    
        
        adult = MplCanvas(self, width=3, height=2, dpi=100)
        adult.axes.plot(x, y_occ_mW_A, color='c', label='Adult Mild Ward')
        adult.axes.plot(x, y_occ_sW_A, color='m', label='Adult Severe Ward')
        adult.axes.plot(x, y_occ_mICU_A, color='b', label='Adult Mild ICU')
        adult.axes.plot(x, y_occ_sICU_A, color='r', label='Adult Severe ICU')
        
        adult.axes.legend()
        adult.axes.set_xlabel('Day')
        adult.axes.set_ylabel('Daily Admissions')
    
        layout = QGridLayout()
        layout.addWidget(adult)
        self.adultPlot.setLayout(layout)
        
    def createPedPlot(self, x, y_occ_mW_P, y_occ_sW_P, y_occ_mICU_P, y_occ_sICU_P):
        self.pedPlot = QGroupBox("Pediatric Patient Daily Census by Location and Scenario")    
        
        ped = MplCanvas(self, width=3, height=2, dpi=100)
        ped.axes.plot(x, y_occ_mW_P, color='c', label='Pediatric Mild Ward')
        ped.axes.plot(x, y_occ_sW_P, color='m', label='Pediatric Severe Ward')
        ped.axes.plot(x, y_occ_mICU_P, color='b', label='Pediatric Mild ICU')
        ped.axes.plot(x, y_occ_sICU_P, color='r', label='Pediatric Severe ICU')

        ped.axes.legend()
        ped.axes.set_xlabel('Day')
        ped.axes.set_ylabel('Daily Admissions')
                
        layout = QGridLayout()
        layout.addWidget(ped)
        self.pedPlot.setLayout(layout)
           
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
        return self.topLeftGroupBox.children()[6].currentIndex()
    def getPop(self): #returns an int
        return self.topLeftGroupBox.children()[0].value()
    def getShapeCurve(self): #returns index
        return self.topLeftGroupBox.children()[10].currentIndex()
    def getDayMax(self): #returns an int
        index = self.topLeftGroupBox.children()[12].currentIndex()
        if index == 0:
            return 30
        if index == 1:
            return 60
        if index == 2:
            return 90

    def testGetters(self): #put this function in line 29 instead of calc to test the getters
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

## CALCULATE ##
    
    def calc(self):
        #get GUI parameters
        attackRate = self.getInfectionRate()
        symptomatic = self.getSymptomatic()
        dayOfPeak = self.getDayMax()
        peakedness = self.getShapeCurve()
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
    
        LOS_model.calc_LOS_Admissions(eC, tICU_p, tICU_a, tWard_p, tWard_a)
        LOS_model.calc_LOS_data(LOS)
        LOS_model.calc_LOS_Deaths()
        LOS_model.calc_LOS_Discharges()
        LOS_model.calc_LOS_Occupancy()
        #calc.plot(eC,LOS_model.LOS_Occupancy_df)
        
        #Plotting        
        self.epiPlot.deleteLater() #removeWidget() does not actually delete the widget, so use deleteLater() 
        self.adultPlot.deleteLater()
        self.pedPlot.deleteLater()
        self.createEpiCurvePlot(eC['Day'],eC['Gamma_Values'])
        self.createAdultPlot(LOS_model.LOS_Occupancy_df['Day'], LOS_model.LOS_Occupancy_df['mW_A'], LOS_model.LOS_Occupancy_df['sW_A'], LOS_model.LOS_Occupancy_df['mICU_A'], LOS_model.LOS_Occupancy_df['sICU_A'])
        self.createPedPlot(LOS_model.LOS_Occupancy_df['Day'], LOS_model.LOS_Occupancy_df['mW_P'], LOS_model.LOS_Occupancy_df['sW_P'], LOS_model.LOS_Occupancy_df['mICU_P'], LOS_model.LOS_Occupancy_df['sICU_P'])
        self.mainLayout.addWidget(self.epiPlot, 1, 1)
        self.mainLayout.addWidget(self.adultPlot, 1, 2)
        self.mainLayout.addWidget(self.pedPlot, 1, 3)
        self.mainLayout.setColumnStretch(0, 0) #ensures that the plots are larger than the input groupbox when window is stretched
        self.mainLayout.setColumnStretch(1, 2) 
        self.mainLayout.setColumnStretch(2, 2)
        self.mainLayout.setColumnStretch(3, 2)
        self.mainLayout.update()
        self.setLayout(self.mainLayout)      

        #Total Hospitalizations Output
        THR = pd.DataFrame(columns=['Total Number Hospitalized', '% of Symptomatic Population', 'Hospitalized Case Fatality Ratio (HFR)',
                                    'Overall Symptomatic Case Fatality Ratio (CFR)'], index=['Mild Scenario', 'Severe Scenario'])
        numPx = totalP*attackRate*symptomatic
        fracPx = numPx/totalP
        totMild = LOS_model.LOS_Admissions_df[['mW_A','mICU_A','mW_P','mICU_P']].values.sum()
        totSevere = LOS_model.LOS_Admissions_df[['sW_A','sICU_A','sW_P','sICU_P']].values.sum()
        fracMild = totMild/numPx
        fracSevere = totSevere/numPx
        deathMild = LOS_model.LOS_Deaths_df[['mW_A','mICU_A','mW_P','mICU_P']].sum().sum()
        deathSevere = LOS_model.LOS_Deaths_df[['sW_A','sICU_A','sW_P','sICU_P']].sum().sum()
        mildHFR = (deathMild/totMild)*100
        severeHFR = (deathSevere/totSevere)*100
        mildCFR = (deathMild/numPx)*100
        severeCFR = (deathSevere/numPx)*100
        THR.loc['Mild Scenario']['Total Number Hospitalized'] = totMild
        THR.loc['Severe Scenario']['Total Number Hospitalized'] = totSevere
        THR.loc['Mild Scenario']['% of Symptomatic Population'] = fracMild*100
        THR.loc['Severe Scenario']['% of Symptomatic Population'] = fracSevere*100
        THR.loc['Mild Scenario']['Hospitalized Case Fatality Ratio (HFR)'] = mildHFR
        THR.loc['Severe Scenario']['Hospitalized Case Fatality Ratio (HFR)'] = severeHFR
        THR.loc['Mild Scenario']['Overall Symptomatic Case Fatality Ratio (CFR)'] = mildCFR
        THR.loc['Severe Scenario']['Overall Symptomatic Case Fatality Ratio (CFR)'] = severeCFR
        THR = THR.astype(float).round(1)
        THR = THR.astype(float).round({'Total Number Hospitalized': 0})
        THR['Total Number Hospitalized'] = THR['Total Number Hospitalized'].astype(int)
        THR['Total Number Hospitalized'] = THR.apply(lambda x: "{:,}".format(x['Total Number Hospitalized'])[:-2], axis=1)

        #Mild Scenario Output
        MILD = pd.DataFrame(columns=["Total Number Admitted","Peak Daily Admissions","Day of Peak Admissions", 
                                     "Peak Hospital Census","Day of Peak Census", "Total Deaths", "Total Discharges"],
                            index=["Adult Ward Cases", "Adult ICU Cases", "Pediatric Ward Cases", "Pediatric ICU Cases"])
        
        MILD.loc['Adult Ward Cases']['Total Number Admitted'] = LOS_model.LOS_Admissions_df['mW_A'].sum()
        MILD.loc['Adult ICU Cases']['Total Number Admitted'] = LOS_model.LOS_Admissions_df['mICU_A'].sum()
        MILD.loc['Pediatric Ward Cases']['Total Number Admitted'] = LOS_model.LOS_Admissions_df['mW_P'].sum()
        MILD.loc['Pediatric ICU Cases']['Total Number Admitted'] = LOS_model.LOS_Admissions_df['mICU_P'].sum()
        
        MILD.loc['Adult Ward Cases']['Peak Daily Admissions'] = LOS_model.LOS_Admissions_df['mW_A'].max()
        MILD.loc['Adult ICU Cases']['Peak Daily Admissions'] = LOS_model.LOS_Admissions_df['mICU_A'].max()
        MILD.loc['Pediatric Ward Cases']['Peak Daily Admissions'] = LOS_model.LOS_Admissions_df['mW_P'].max()
        MILD.loc['Pediatric ICU Cases']['Peak Daily Admissions'] = LOS_model.LOS_Admissions_df['mICU_P'].max()

        MILD.loc['Adult Ward Cases']['Day of Peak Admissions'] = LOS_model.LOS_Admissions_df['mW_A'].idxmax()
        MILD.loc['Adult ICU Cases']['Day of Peak Admissions'] = LOS_model.LOS_Admissions_df['mICU_A'].idxmax()
        MILD.loc['Pediatric Ward Cases']['Day of Peak Admissions'] = LOS_model.LOS_Admissions_df['mW_P'].idxmax()
        MILD.loc['Pediatric ICU Cases']['Day of Peak Admissions'] = LOS_model.LOS_Admissions_df['mICU_P'].idxmax()

        MILD.loc['Adult Ward Cases']['Peak Hospital Census'] = LOS_model.LOS_Occupancy_df['mW_A'].max()
        MILD.loc['Adult ICU Cases']['Peak Hospital Census'] = LOS_model.LOS_Occupancy_df['mICU_A'].max()
        MILD.loc['Pediatric Ward Cases']['Peak Hospital Census'] = LOS_model.LOS_Occupancy_df['mW_P'].max()
        MILD.loc['Pediatric ICU Cases']['Peak Hospital Census'] = LOS_model.LOS_Occupancy_df['mICU_P'].max()

        MILD.loc['Adult Ward Cases']['Day of Peak Census'] = LOS_model.LOS_Occupancy_df['mW_A'].astype(float).idxmax()
        MILD.loc['Adult ICU Cases']['Day of Peak Census'] = LOS_model.LOS_Occupancy_df['mICU_A'].astype(float).idxmax()
        MILD.loc['Pediatric Ward Cases']['Day of Peak Census'] = LOS_model.LOS_Occupancy_df['mW_P'].astype(float).idxmax()
        MILD.loc['Pediatric ICU Cases']['Day of Peak Census'] = LOS_model.LOS_Occupancy_df['mICU_P'].astype(float).idxmax()
        
        MILD.loc['Adult Ward Cases']['Total Deaths'] = LOS_model.LOS_Deaths_df['mW_A'].sum()
        MILD.loc['Adult ICU Cases']['Total Deaths'] = LOS_model.LOS_Deaths_df['mICU_A'].sum()
        MILD.loc['Pediatric Ward Cases']['Total Deaths'] = LOS_model.LOS_Deaths_df['mW_P'].sum()
        MILD.loc['Pediatric ICU Cases']['Total Deaths'] = LOS_model.LOS_Deaths_df['mICU_P'].sum()

        MILD.loc['Adult Ward Cases']['Total Discharges'] = LOS_model.LOS_Discharges_df['mW_A'].sum()
        MILD.loc['Adult ICU Cases']['Total Discharges'] = LOS_model.LOS_Discharges_df['mICU_A'].sum()
        MILD.loc['Pediatric Ward Cases']['Total Discharges'] = LOS_model.LOS_Discharges_df['mW_P'].sum()
        MILD.loc['Pediatric ICU Cases']['Total Discharges'] = LOS_model.LOS_Discharges_df['mICU_P'].sum()
        
        MILD = MILD.astype(float).round(0)
        MILD['Total Number Admitted'] = MILD.apply(lambda x: "{:,}".format(x['Total Number Admitted'])[:-2], axis=1)
        MILD['Peak Daily Admissions'] = MILD.apply(lambda x: "{:,}".format(x['Peak Daily Admissions'])[:-2], axis=1)
        MILD['Day of Peak Admissions'] = MILD.apply(lambda x: "{:,}".format(x['Day of Peak Admissions'])[:-2], axis=1)
        MILD['Peak Hospital Census'] = MILD.apply(lambda x: "{:,}".format(x['Peak Hospital Census'])[:-2], axis=1)
        MILD['Day of Peak Census'] = MILD.apply(lambda x: "{:,}".format(x['Day of Peak Census'])[:-2], axis=1)
        MILD['Total Deaths'] = MILD.apply(lambda x: "{:,}".format(x['Total Deaths'])[:-2], axis=1)
        MILD['Total Discharges'] = MILD.apply(lambda x: "{:,}".format(x['Total Discharges'])[:-2], axis=1)

        
        #Severe Scenario Output
        SEVERE = pd.DataFrame(columns=["Total Number Admitted","Peak Daily Admissions","Day of Peak Admissions", 
                                     "Peak Hospital Census","Day of Peak Census", "Total Deaths", "Total Discharges"],
                              index=["Adult Ward Cases", "Adult ICU Cases", "Pediatric Ward Cases", "Pediatric ICU Cases"])
        
        SEVERE.loc['Adult Ward Cases']['Total Number Admitted'] = LOS_model.LOS_Admissions_df['sW_A'].sum()
        SEVERE.loc['Adult ICU Cases']['Total Number Admitted'] = LOS_model.LOS_Admissions_df['sICU_A'].sum()
        SEVERE.loc['Pediatric Ward Cases']['Total Number Admitted'] = LOS_model.LOS_Admissions_df['sW_P'].sum()
        SEVERE.loc['Pediatric ICU Cases']['Total Number Admitted'] = LOS_model.LOS_Admissions_df['sICU_P'].sum()
        
        SEVERE.loc['Adult Ward Cases']['Peak Daily Admissions'] = LOS_model.LOS_Admissions_df['sW_A'].max()
        SEVERE.loc['Adult ICU Cases']['Peak Daily Admissions'] = LOS_model.LOS_Admissions_df['sICU_A'].max()
        SEVERE.loc['Pediatric Ward Cases']['Peak Daily Admissions'] = LOS_model.LOS_Admissions_df['sW_P'].max()
        SEVERE.loc['Pediatric ICU Cases']['Peak Daily Admissions'] = LOS_model.LOS_Admissions_df['sICU_P'].max()

        SEVERE.loc['Adult Ward Cases']['Day of Peak Admissions'] = LOS_model.LOS_Admissions_df['sW_A'].idxmax()
        SEVERE.loc['Adult ICU Cases']['Day of Peak Admissions'] = LOS_model.LOS_Admissions_df['sICU_A'].idxmax()
        SEVERE.loc['Pediatric Ward Cases']['Day of Peak Admissions'] = LOS_model.LOS_Admissions_df['sW_P'].idxmax()
        SEVERE.loc['Pediatric ICU Cases']['Day of Peak Admissions'] = LOS_model.LOS_Admissions_df['sICU_P'].idxmax()

        SEVERE.loc['Adult Ward Cases']['Peak Hospital Census'] = LOS_model.LOS_Occupancy_df['sW_A'].max()
        SEVERE.loc['Adult ICU Cases']['Peak Hospital Census'] = LOS_model.LOS_Occupancy_df['sICU_A'].max()
        SEVERE.loc['Pediatric Ward Cases']['Peak Hospital Census'] = LOS_model.LOS_Occupancy_df['sW_P'].max()
        SEVERE.loc['Pediatric ICU Cases']['Peak Hospital Census'] = LOS_model.LOS_Occupancy_df['sICU_P'].max()

        SEVERE.loc['Adult Ward Cases']['Day of Peak Census'] = LOS_model.LOS_Occupancy_df['sW_A'].astype(float).idxmax()
        SEVERE.loc['Adult ICU Cases']['Day of Peak Census'] = LOS_model.LOS_Occupancy_df['sICU_A'].astype(float).idxmax()
        SEVERE.loc['Pediatric Ward Cases']['Day of Peak Census'] = LOS_model.LOS_Occupancy_df['sW_P'].astype(float).idxmax()
        SEVERE.loc['Pediatric ICU Cases']['Day of Peak Census'] = LOS_model.LOS_Occupancy_df['sICU_P'].astype(float).idxmax()
        
        SEVERE.loc['Adult Ward Cases']['Total Deaths'] = LOS_model.LOS_Deaths_df['sW_A'].sum()
        SEVERE.loc['Adult ICU Cases']['Total Deaths'] = LOS_model.LOS_Deaths_df['sICU_A'].sum()
        SEVERE.loc['Pediatric Ward Cases']['Total Deaths'] = LOS_model.LOS_Deaths_df['sW_P'].sum()
        SEVERE.loc['Pediatric ICU Cases']['Total Deaths'] = LOS_model.LOS_Deaths_df['sICU_P'].sum()

        SEVERE.loc['Adult Ward Cases']['Total Discharges'] = LOS_model.LOS_Discharges_df['sW_A'].sum()
        SEVERE.loc['Adult ICU Cases']['Total Discharges'] = LOS_model.LOS_Discharges_df['sICU_A'].sum()
        SEVERE.loc['Pediatric Ward Cases']['Total Discharges'] = LOS_model.LOS_Discharges_df['sW_P'].sum()
        SEVERE.loc['Pediatric ICU Cases']['Total Discharges'] = LOS_model.LOS_Discharges_df['sICU_P'].sum()
        
        SEVERE = SEVERE.astype(float).round(0)
        SEVERE['Total Number Admitted'] = SEVERE.apply(lambda x: "{:,}".format(x['Total Number Admitted'])[:-2], axis=1)
        SEVERE['Peak Daily Admissions'] = SEVERE.apply(lambda x: "{:,}".format(x['Peak Daily Admissions'])[:-2], axis=1)
        SEVERE['Day of Peak Admissions'] = SEVERE.apply(lambda x: "{:,}".format(x['Day of Peak Admissions'])[:-2], axis=1)
        SEVERE['Peak Hospital Census'] = SEVERE.apply(lambda x: "{:,}".format(x['Peak Hospital Census'])[:-2], axis=1)
        SEVERE['Day of Peak Census'] = SEVERE.apply(lambda x: "{:,}".format(x['Day of Peak Census'])[:-2], axis=1)
        SEVERE['Total Deaths'] = SEVERE.apply(lambda x: "{:,}".format(x['Total Deaths'])[:-2], axis=1)
        SEVERE['Total Discharges'] = SEVERE.apply(lambda x: "{:,}".format(x['Total Discharges'])[:-2], axis=1)

        #Adult Ward Beds output
        AWARD = pd.DataFrame(columns=["Total Medical Ward Patients", "Peak Simultaneous Ward Beds (Max Census)", "Day of Max Census",
                                       "Total Patient-Days for COVID Ward Patients"], index = ["Mild Scenario", "Severe Scenario"])
        AWARD.loc['Mild Scenario']['Total Medical Ward Patients'] = LOS_model.LOS_Admissions_df['mW_A'].sum()
        AWARD.loc['Severe Scenario']['Total Medical Ward Patients'] = LOS_model.LOS_Admissions_df['sW_A'].sum()
        AWARD.loc['Mild Scenario']['Peak Simultaneous Ward Beds (Max Census)'] = LOS_model.LOS_Occupancy_df['mW_A'].max()
        AWARD.loc['Severe Scenario']['Peak Simultaneous Ward Beds (Max Census)'] = LOS_model.LOS_Occupancy_df['sW_A'].max()
        AWARD.loc['Mild Scenario']['Day of Max Census'] = LOS_model.LOS_Occupancy_df['mW_A'].astype(float).idxmax()
        AWARD.loc['Severe Scenario']['Day of Max Census'] = LOS_model.LOS_Occupancy_df['sW_A'].astype(float).idxmax()
        AWARD.loc['Mild Scenario']['Total Patient-Days for COVID Ward Patients'] = LOS_model.LOS_Occupancy_df['mW_A'].sum()
        AWARD.loc['Severe Scenario']['Total Patient-Days for COVID Ward Patients'] = LOS_model.LOS_Occupancy_df['sW_A'].sum()
        AWARD = AWARD.astype(float).round(0)
        AWARD['Total Medical Ward Patients'] = AWARD.apply(lambda x: "{:,}".format(x['Total Medical Ward Patients'])[:-2], axis=1)
        AWARD['Peak Simultaneous Ward Beds (Max Census)'] = AWARD.apply(lambda x: "{:,}".format(x['Peak Simultaneous Ward Beds (Max Census)'])[:-2], axis=1)
        AWARD['Day of Max Census'] = AWARD.apply(lambda x: "{:,}".format(x['Day of Max Census'])[:-2], axis=1)
        AWARD['Total Patient-Days for COVID Ward Patients'] = AWARD.apply(lambda x: "{:,}".format(x['Total Patient-Days for COVID Ward Patients'])[:-2], axis=1)
        
        #Adult ICU Beds and Ventilators output
        AICU = pd.DataFrame(columns=["Total ICU Patients", "Peak Simultaneous ICU Bed Requirement", "Day of Max Census", 
                                     "Total Patient-Days for COVID ICU Patients", "Peak Ventilator Need (80% Ventilated Fraction)"], 
                                    index = ["Mild Scenario", "Severe Scenario"])
        AICU.loc['Mild Scenario']['Total ICU Patients'] = LOS_model.LOS_Admissions_df['mICU_A'].sum()
        AICU.loc['Severe Scenario']['Total ICU Patients'] = LOS_model.LOS_Admissions_df['sICU_A'].sum()
        AICU.loc['Mild Scenario']['Peak Simultaneous ICU Bed Requirement'] = LOS_model.LOS_Occupancy_df['mICU_A'].max()
        AICU.loc['Severe Scenario']['Peak Simultaneous ICU Bed Requirement'] = LOS_model.LOS_Occupancy_df['sICU_A'].max()
        AICU.loc['Mild Scenario']['Day of Max Census'] = LOS_model.LOS_Occupancy_df['mICU_A'].astype(float).idxmax()
        AICU.loc['Severe Scenario']['Day of Max Census'] = LOS_model.LOS_Occupancy_df['sICU_A'].astype(float).idxmax()
        AICU.loc['Mild Scenario']['Total Patient-Days for COVID ICU Patients'] = LOS_model.LOS_Occupancy_df['mICU_A'].sum()
        AICU.loc['Severe Scenario']['Total Patient-Days for COVID ICU Patients'] = LOS_model.LOS_Occupancy_df['sICU_A'].sum()
        AICU.loc['Mild Scenario']['Peak Ventilator Need (80% Ventilated Fraction)'] = LOS_model.LOS_Occupancy_df['mICU_A'].max()*0.8
        AICU.loc['Severe Scenario']['Peak Ventilator Need (80% Ventilated Fraction)'] = LOS_model.LOS_Occupancy_df['sICU_A'].max()*0.8
        AICU = AICU.astype(float).round(0)
        AICU['Total ICU Patients'] = AICU.apply(lambda x: "{:,}".format(x['Total ICU Patients'])[:-2], axis=1)
        AICU['Peak Simultaneous ICU Bed Requirement'] = AICU.apply(lambda x: "{:,}".format(x['Peak Simultaneous ICU Bed Requirement'])[:-2], axis=1)
        AICU['Day of Max Census'] = AICU.apply(lambda x: "{:,}".format(x['Day of Max Census'])[:-2], axis=1)
        AICU['Total Patient-Days for COVID ICU Patients'] = AICU.apply(lambda x: "{:,}".format(x['Total Patient-Days for COVID ICU Patients'])[:-2], axis=1)
        AICU['Peak Ventilator Need (80% Ventilated Fraction)'] = AICU.apply(lambda x: "{:,}".format(x['Peak Ventilator Need (80% Ventilated Fraction)'])[:-2], axis=1)
        
        
        self.tableWidget.removeTab(4) #figure out how to delete tabs, not just remove from view
        self.tableWidget.removeTab(3)
        self.tableWidget.removeTab(2)
        self.tableWidget.removeTab(1)
        self.tableWidget.removeTab(0)
        
        tab1 = QTableView(None)
        THR_mod = TableModel(THR) #need to round the dataframes, also need to add vertical headers
        tab1.setModel(THR_mod)

        tab2 = QTableView(None)
        MILD_mod = TableModel(MILD)
        tab2.setModel(MILD_mod)
        
        tab3 = QTableView(None)
        SEVERE = TableModel(SEVERE)
        tab3.setModel(SEVERE)
        
        tab4 = QTableView(None)
        AWARD = TableModel(AWARD)
        tab4.setModel(AWARD)
        
        tab5 = QTableView(None)
        AICU = TableModel(AICU)
        tab5.setModel(AICU)
        
        self.tableWidget.addTab(tab1, "Total Hospitalizations")
        self.tableWidget.addTab(tab2, "Detailed Results of the MILD Scenario")
        self.tableWidget.addTab(tab3, "Detailed Results of the SEVERE Scenario")
        self.tableWidget.addTab(tab4, "Adult Ward Beds")
        self.tableWidget.addTab(tab5, "Adult ICU Beds and Ventilators")
        
        #simulation run output above the plots 
        self.results.deleteLater()
        self.results = QLabel("This simulation run created " + str("{:,}".format(round(numPx,0))[:-2]) + " patients, representing " + str(round(fracPx,3)*100) + "% of the catchment area.")  
        self.mainLayout.addWidget(self.results, 0, 2)
                
        reload(LOS_model)
        
    def instructions(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("C5V Modeling Tool: Instructions for running a COVID-19 caseload and capacity simulation.")
        msg.setInformativeText("On the left side of the screen are the user specified inputs. Once the data is entered, the user can "
                               "press the calculate button to produce the simulation output in the right side of the screen. More detailed "
                               "instructions on running the model and specifics on each input/variable are available below under Show Details...")
        msg.setDetailedText("On the left side of the screen are the user inputs, in which the user will define the size of the population, "
                               "the catchment area which the hospital serves, select a type of population distribution, an infection and "
                               "symptomatic rate, and finally features of the epidemic curve such as the shape of the peak and the day of "
                               "maximum cases. \n \n "
                               "In the bottom left panel, we have included Advanced Options (which can be toggled with the check "
                               "button next to instructions). These are populated with current CDC data but can be updated as the user prefers. "
                               "After defining the inputs, the user can press the calculate button to produce the output on the right side of the "
                               "window, after which the inputs can be altered and outputs re-calculated as many times as one wishes. \n \n"
                               "In the outputs, the first plot shows the hospital-apparent epidemic curve based on a gamma distribution fit "
                               "to the inputs. The next two plots show the adult and pediatric daily census by location (ward or ICU) and by "
                               "the type of scenario (mild or severe). These daily census data are calculated using a length of stay (LOS) model. \n \n"
                               "Finally, the bottom right panel includes the numerical output, including detaild results of each scenario, adult "
                               "census data, and ICU bed requirement (along with ventilator need).")
        msg.setWindowTitle("C5V Instructions")
        msg.exec()
        
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

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = c4()
    window.showMaximized()
    window.show()
    sys.exit(app.exec_()) 