#############################################################################
#C4 Desktop Application by Vruj Patel & Lior Shtayer
#############################################################################
#pylint: disable=no-name-in-module
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QAbstractScrollArea, QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTableWidgetItem, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)
import pandas as pd

class c4(QDialog):
    def __init__(self, parent=None):
        super(c4, self).__init__(parent)

        self.originalPalette = QApplication.palette()

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftTabWidget()

        advancedCheck = QCheckBox("Advanced Options")
        advancedCheck.setChecked(True)
        advancedCheck.toggled.connect(self.bottomLeftTabWidget.setEnabled)
        
        runCalc = QPushButton("Calculate")
        printButton = QPushButton("Print")
        defaultButton = QPushButton("Default")
        instructions = QPushButton("Instructions")

        topLayout = QHBoxLayout()
        topLayout.addWidget(instructions)
        topLayout.addWidget(advancedCheck)
        topLayout.addWidget(defaultButton)
        topLayout.addWidget(printButton)
        topLayout.addWidget(runCalc) #make these into objects called by addWidget()

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("c4: Cornell COVID-19 Caseload Calculator")
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        QApplication.setPalette(QApplication.style().standardPalette())

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Population Parameters")
        
        totalPop = QSpinBox(self.topLeftGroupBox)
        totalPop.setGroupSeparatorShown(True)
        totalPop.setRange(0, 1000000000)
        totalPop.setValue(8398748)
        tPopLabel = QLabel("&Total Population:")
        tPopLabel.setBuddy(totalPop)
        
        popDist = QComboBox()
        popDist.addItems(('Young (Mali)', 'Young Adults (Bangladesh)', 'Middle-Aged (New York)', 'Old (Japan)'))
        popDistLabel = QLabel("Population Distribution:")
        popDistLabel.setBuddy(popDist)
        popDist.setCurrentIndex(2)
        
        infRate = QSlider(Qt.Horizontal, self.topLeftGroupBox)
        infRate.setTickInterval(10)
        infRate.setTickPosition(QSlider.TicksBothSides)
        infRate.setValue(40)
        infRateLabel = QLabel("Infection Rate:")
        infRateLabel.setBuddy(infRate)
        
        sympRate = QSlider(Qt.Horizontal, self.topLeftGroupBox)
        sympRate.setTickInterval(10)
        sympRate.setTickPosition(QSlider.TicksBothSides)
        sympRate.setValue(40)
        sympRateLabel = QLabel("% Symptomatic:")
        sympRateLabel.setBuddy(sympRate)
        
        layout = QVBoxLayout()
        layout.addWidget(tPopLabel)
        layout.addWidget(totalPop)
        layout.addStretch(1)
        layout.addWidget(popDistLabel)
        layout.addWidget(popDist)
        layout.addStretch(1)
        layout.addWidget(infRateLabel)
        layout.addWidget(infRate)
        layout.addStretch(1)
        layout.addWidget(sympRateLabel)
        layout.addWidget(sympRate)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)    

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Output Parameters")
        #TODO: add switch for mild/severe
        
        peaked = QComboBox()
        peaked.addItems(('A-type: Broad', 'B-type: Somewhat Broad', 'C-type: A Bit Peaked', 'D-type: Very Peaked', 'E-type: Extremely Peaked'))
        peakedLabel = QLabel("Shape of the epidemic curve: ")
        peakedLabel.setBuddy(peaked)
        peaked.setCurrentIndex(3)
        
        peakDay = QComboBox()
        peakDay.addItems(('30', '45', '60', '90'))
        peakDayLabel = QLabel("Choose the day of maximum cases: ")
        peakDayLabel.setBuddy(peakDay)
        peaked.setCurrentIndex(2)
        
        dayOutput = QDial(self.topRightGroupBox)
        dayOutput.setMinimum(1)
        dayOutput.setMaximum(180)
        dayOutput.setValue(60)
        dayOutput.setNotchesVisible(True)
        dayOutputLabel = QLabel("Day of Output:")
        dayOutputLabel.setBuddy(dayOutput)
        #dayCount = QLabel(str(dayOutput.valueChanged.connect(dayOutput.sliderMoved))) #Figure out how to display the current day as selected by slider
        #dayCount.setBuddy(dayOutput)

        layout = QVBoxLayout()
        layout.addWidget(peakedLabel)
        layout.addWidget(peaked)
        layout.addWidget(peakDayLabel)
        layout.addWidget(peakDay)
        layout.addWidget(dayOutputLabel)
        layout.addWidget(dayOutput)
        layout.addStretch(1)
        #layout.addWidget(dayCount)
        self.topRightGroupBox.setLayout(layout)

    def createBottomLeftTabWidget(self):
        self.bottomLeftTabWidget = QTabWidget()
        #there will be a policy here to resize all columns to fit (one liner)
        
        tab1 = QWidget()
        CHR = QTableWidget(7, 2)
        CHRLabel = QLabel("Case Hospitalization Ratio (%)")
        CHRLabel.setBuddy(CHR)
        CHRDefault = QPushButton("Default")
        tab1grid = QGridLayout()
        tab1grid.setContentsMargins(5, 5, 5, 5)
        tab1grid.addWidget(CHRLabel, 0, 0) 
        tab1grid.addWidget(CHRDefault, 0, 1)
        tab1grid.addWidget(CHR, 1, 0, 1, 2)
        tab1.setLayout(tab1grid)
        CHR.setHorizontalHeaderLabels(("Mild", "Severe"))
        CHR.setVerticalHeaderLabels(("0-19", "20-44", "45-54", "55-64", "65-74", "75-84", "=>85"))

        tab2 = QWidget()
        CCHF = QTableWidget(7, 2)
        CCHFLabel = QLabel("Critical Care Hospitalization Fraction (%)")
        CCHFLabel.setBuddy(CHR)
        CCHFDefault = QPushButton("Default")
        tab2grid = QGridLayout()
        tab2grid.setContentsMargins(5, 5, 5, 5)
        tab2grid.addWidget(CCHFLabel, 0, 0) 
        tab2grid.addWidget(CCHFDefault, 0, 1)
        tab2grid.addWidget(CCHF, 1, 0, 1, 2)
        tab2.setLayout(tab2grid)
        CCHF.setHorizontalHeaderLabels(("Mild", "Severe"))
        CCHF.setVerticalHeaderLabels(("0-19", "20-44", "45-54", "55-64", "65-74", "75-84", "=>85"))
        
        tab3 = QWidget()
        LOS = QTableWidget(4, 4)
        LOSLabel = QLabel("Enter min/max length of stay, %mortality, and change in LOS for patients who die.")
        LOSLabel.setBuddy(CHR)
        LOSDefault = QPushButton("Default")
        tab3grid = QGridLayout()
        tab3grid.setContentsMargins(5, 5, 5, 5)
        tab3grid.addWidget(LOSLabel, 0, 0)
        tab3grid.addWidget(LOSDefault, 0, 1)
        tab3grid.addWidget(LOS, 1, 0, 1, 2)
        tab3.setLayout(tab3grid)
        LOS.setHorizontalHeaderLabels(("Minimum LOS", "Maximum LOS", "Mortality Ratio", "LOS Adjustment"))
        LOS.setVerticalHeaderLabels(("Adult Ward Beds", "Adult ICU Beds", "Pediatric Ward Beds", "Pediatric ICU Beds"))
        
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
        noVent.setHorizontalHeaderLabels(("Mild", "Severe"))
        noVent.setVerticalHeaderLabels(("Survivor Minimum LOS", "Survivor Maximum LOS", "Mortality Ratio (%)", "LOS Adjustment (%)"))

        self.setDefaults(CHR, CCHF, capInputs, noVent, LOS)

        self.bottomLeftTabWidget.addTab(tab1, "CHR")
        self.bottomLeftTabWidget.addTab(tab2, "CCHF")
        self.bottomLeftTabWidget.addTab(tab3, "LOS")
        self.bottomLeftTabWidget.addTab(tab4, "Capacitated Inputs")
        self.bottomLeftTabWidget.addTab(tab5, "No Vents")
        
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
    def bedDefaults(self, bed):
        bed.setItem(0, 0, QTableWidgetItem("20,000"))
        bed.setItem(0, 1, QTableWidgetItem("1,800"))
        bed.setItem(0, 2, QTableWidgetItem("1,000"))
        bed.setItem(0, 3, QTableWidgetItem("1.25"))
        bed.setItem(0, 4, QTableWidgetItem("1,250"))
    def ventDefaults(self, vent):
        vent.setItem(0,0, QTableWidgetItem("2"))
        vent.setItem(1,0, QTableWidgetItem("10"))
        vent.setItem(2,0, QTableWidgetItem("95"))
        vent.setItem(3,0, QTableWidgetItem("5"))
        
        vent.setItem(0,1, QTableWidgetItem("2"))
        vent.setItem(1,1, QTableWidgetItem("10"))
        vent.setItem(2,1, QTableWidgetItem("0.95"))
        vent.setItem(3,1, QTableWidgetItem("0.5"))
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
    def setDefaults(self, CHR, CCHF, bed, vent, LOS):
        self.chrDefaults(CHR)
        self.cchfDefaults(CCHF)
        self.bedDefaults(bed)
        self.ventDefaults(vent)
        self.LOSDefaults(LOS)

    def getRatios(self, CHR): #Use this for CHR and CCHF
        df = pd.DataFrame(columns = ["Mild", "Severe"])
        df = df.append({'Mild': float(CHR.item(0,0)), 'Severe': float(CHR.item(0,1))}, ignore_index=True) #0-19
        df = df.append({'Mild': float(CHR.item(1,0)), 'Severe': float(CHR.item(1,1))}, ignore_index=True) #20-44
        df = df.append({'Mild': float(CHR.item(2,0)), 'Severe': float(CHR.item(2,1))}, ignore_index=True) #45-54
        df = df.append({'Mild': float(CHR.item(3,0)), 'Severe': float(CHR.item(3,1))}, ignore_index=True) #55-64
        df = df.append({'Mild': float(CHR.item(4,0)), 'Severe': float(CHR.item(4,1))}, ignore_index=True) #65-74
        df = df.append({'Mild': float(CHR.item(5,0)), 'Severe': float(CHR.item(5,1))}, ignore_index=True) #75-84
        df = df.append({'Mild': float(CHR.item(6,0)), 'Severe': float(CHR.item(6,1))}, ignore_index=True) #85+
        return df
    def getLOS(self, LOS): 
        df = pd.DataFrame(columns = ['Minimum LOS', 'Maximum LOS', 'Mortality Ratio', 'LOS Adjustment'])
        df = df.append({'Minimum LOS': float(LOS.item(0,0)), 'Maximum LOS': float(LOS.item(0,1)), 'Mortality Ratio': float(LOS.item(1,2)), 'LOS Adjustment': float(LOS.item(0,3))}, ignore_index=True) #adult ward beds
        df = df.append({'Minimum LOS': float(LOS.item(1,0)), 'Maximum LOS': float(LOS.item(1,1)), 'Mortality Ratio': float(LOS.item(2,2)), 'LOS Adjustment': float(LOS.item(1,3))}, ignore_index=True) #adult icu beds
        df = df.append({'Minimum LOS': float(LOS.item(2,0)), 'Maximum LOS': float(LOS.item(2,1)), 'Mortality Ratio': float(LOS.item(3,2)), 'LOS Adjustment': float(LOS.item(2,3))}, ignore_index=True) #ped ward beds
        df = df.append({'Minimum LOS': float(LOS.item(3,0)), 'Maximum LOS': float(LOS.item(3,1)), 'Mortality Ratio': float(LOS.item(4,2)), 'LOS Adjustment': float(LOS.item(3,3))}, ignore_index=True) #ped icu beds
        return df
    def getVents(self, vents):
        df = pd.DataFrame(columns = ['Available Ward Beds', 'Available ICU Beds', 'Available Ventilators', 'Patients per Ventilator', 'Effective Ventilator Supply'])
        df = df.append({'Available Ward Beds': float(vents.item(0,0)), 
                        'Available ICU Beds': float(vents.item(0,1)), 
                        'Available Ventilators': float(vents.item(0,2)), 
                        'Patients per Ventilator': float(vents.item(0,3)), 
                        'Effective Ventilator Supply': float(vents.item(0,4))}, ignore_index=True)
        return df
    def getNoVents(self, noVents):
        df = pd.DataFrame(columns = ['Mild', 'Severe'])
        df = df.append({'Mild': float(noVents.item(0,0)), 'Severe': float(noVents.item(1,1))}, ignore_index=True) #Survivor Minimum LOS
        df = df.append({'Mild': float(noVents.item(1,0)), 'Severe': float(noVents.item(2,1))}, ignore_index=True) #Survivor Maximum LOS
        df = df.append({'Mild': float(noVents.item(2,0)), 'Severe': float(noVents.item(3,1))}, ignore_index=True) #Mortality Ratio (%)
        df = df.append({'Mild': float(noVents.item(3,0)), 'Severe': float(noVents.item(4,1))}, ignore_index=True) #LOS Adjustment (%)
        return df
    
    def getInfectionRate(self, infRate): #returns a percentage
        return infRate.Value()
    def getSymptomatic(self, symp): #returns a percentage
        return symp.Value()
    def getPopDist(self, popDist): #returns an index
        return popDist.currentIndex()
    def getPop(self, totalPop): #returns an int
        return int(totalPop.Value())
    def getShapeCurve(self, peaked): #returns index
        return peaked.currentIndex()
    def getDayMax(self, peakDay): #returns an int
        return int(peakDay.currentText())
    def getDayOutput(self, dayOutput): #returns an int
        return int(dayOutput.Value())

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = c4()
    #window.showMaximized()
    window.show()
    sys.exit(app.exec_()) 
