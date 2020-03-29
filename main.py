#############################################################################
#C4 Desktop Application by Vruj Patel & Lior Shtayer
#############################################################################
#pylint: disable=no-name-in-module
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QAbstractScrollArea, QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)


class c4(QDialog):
    def __init__(self, parent=None):
        super(c4, self).__init__(parent)

        self.originalPalette = QApplication.palette()

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftTabWidget()
        #self.createBottomRightGroupBox()

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
        #topLayout.addWidget(self.useStylePaletteCheckBox)
        

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0, 1, 2)
        #mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)
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
        CHRLabel = QLabel("Case Hospitalization Ratio")
        CHRLabel.setBuddy(CHR)
        CHRDefault = QPushButton("Default")
        tab1grid = QGridLayout()
        tab1grid.setContentsMargins(5, 5, 5, 5)
        tab1grid.addWidget(CHRLabel, 0, 0) 
        tab1grid.addWidget(CHRDefault, 0, 1)
        tab1grid.addWidget(CHR, 1, 0, 1, 2)
        tab1.setLayout(tab1grid)
        CHR.setHorizontalHeaderLabels(("Mild", "Severe"))
        CHR.setVerticalHeaderLabels(("0-9", "20-44", "45-54", "55-64", "65-74", "75-84", "=>85"))

        tab2 = QWidget()
        CCHF = QTableWidget(7, 2)
        CCHFLabel = QLabel("Critical Care Hospitalization Fraction")
        CCHFLabel.setBuddy(CHR)
        CCHFDefault = QPushButton("Default")
        tab2grid = QGridLayout()
        tab2grid.setContentsMargins(5, 5, 5, 5)
        tab2grid.addWidget(CCHFLabel, 0, 0) 
        tab2grid.addWidget(CCHFDefault, 0, 1)
        tab2grid.addWidget(CCHF, 1, 0, 1, 2)
        tab2.setLayout(tab2grid)
        CCHF.setHorizontalHeaderLabels(("Mild", "Severe"))
        CCHF.setVerticalHeaderLabels(("0-9", "20-44", "45-54", "55-64", "65-74", "75-84", "=>85"))
        
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
        capInputs = QTableWidget(1, 4)
        capInputLabel = QLabel("Enter parameters for capacitated model:")
        capInputLabel.setBuddy(capInputs)
        capInputDefault = QPushButton("Default")
        tab4grid = QGridLayout()
        tab4grid.setContentsMargins(5, 5, 5, 5)
        tab4grid.addWidget(capInputLabel, 0, 0)
        tab4grid.addWidget(capInputDefault, 0, 1)
        tab4grid.addWidget(capInputs, 1, 0, 1, 2)
        tab4.setLayout(tab4grid)
        capInputs.setHorizontalHeaderLabels(("Available Ward Beds", "Available ICU Beds", "Available Ventilators", "Patients per Ventilator"))
        
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
        noVent.setVerticalHeaderLabels(("Survivor Minimum LOS", "Survivor Maximum LOS", "Mortality Ratio", "LOS Adjustment"))

        self.bottomLeftTabWidget.addTab(tab1, "CHR")
        self.bottomLeftTabWidget.addTab(tab2, "CCHF")
        self.bottomLeftTabWidget.addTab(tab3, "LOS")
        self.bottomLeftTabWidget.addTab(tab4, "Capacitated Inputs")
        self.bottomLeftTabWidget.addTab(tab5, "No Vents")
        
    def chrDefaults(self):
        pass
    def cchfDefaults(self):
        pass
    def bedDefaults(self):
        pass
    def ventDefaults(self):
        pass
    def LOSdefaults(self):
        pass

"""
    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Group 3")
        self.bottomRightGroupBox.setCheckable(True)
        self.bottomRightGroupBox.setChecked(True)

        lineEdit = QLineEdit('s3cRe7')
        lineEdit.setEchoMode(QLineEdit.Password)

        spinBox = QSpinBox(self.bottomRightGroupBox)
        spinBox.setValue(50)

        dateTimeEdit = QDateTimeEdit(self.bottomRightGroupBox)
        dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        slider = QSlider(Qt.Horizontal, self.bottomRightGroupBox)
        slider.setValue(40)

        scrollBar = QScrollBar(Qt.Horizontal, self.bottomRightGroupBox)
        scrollBar.setValue(60)

        dial = QDial(self.bottomRightGroupBox)
        dial.setValue(30)
        dial.setNotchesVisible(True)

        layout = QGridLayout()
        layout.addWidget(lineEdit, 0, 0, 1, 2)
        layout.addWidget(spinBox, 1, 0, 1, 2)
        layout.addWidget(dateTimeEdit, 2, 0, 1, 2)
        layout.addWidget(slider, 3, 0)
        layout.addWidget(scrollBar, 4, 0)
        layout.addWidget(dial, 3, 1, 2, 1)
        layout.setRowStretch(5, 1)
        self.bottomRightGroupBox.setLayout(layout)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)
"""

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = c4()
    #window.showMaximized()
    window.show()
    sys.exit(app.exec_()) 
