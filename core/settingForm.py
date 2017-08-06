# -*- coding: utf-8 -*-

"""
Module implementing SettingForm.
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .Ui_settingForm import Ui_Dialog


class SettingForm(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(SettingForm, self).__init__(parent)
        self.setupUi(self)
        
        self.initform()
    
    def initform(self):
        choose_type = ["Motor","Light","Sensor"]
        self.comboBoxtype.addItems(choose_type)
        self.comboBoxtype.setCurrentIndex(len(choose_type) - 1)
        
        self.pushButtonAdd.clicked.connect(self.addOK)
        
        
        
    def checkForm(self):
        if self.textEdit.toPlainText():
            self.getlist = {
                "signal":self.textEdit.toPlainText(),
                "component":self.comboBoxtype.currentIndex(),
                "Max":self.spinBoxMax.value(),
                "Mini":self.spinBoxMin.value()
            }
            self.accept()
        else:
            dlg = QMessageBox(QMessageBox.Warning, "Waring", "Signal have no input", (QMessageBox.Ok), self)
            dlg.exec()
            
        
    def addOK(self):
        self.checkForm()
        
        
        
