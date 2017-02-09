# -*- coding: utf-8 -*-

"""
Module implementing graphy.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets

from Ui_graphy import Ui_Form

import pyqtgraph as pg

#app = QtWidgets.QApplication([])



class graphy(QWidget, Ui_Form): 
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(graphy, self).__init__(parent)
        self.setupUi(self)
        
        w = QWidget()
        
        plot = pg.PlotWidget()
        
        w.setLayout(self.gridLayout)
        
        self.gridLayout.addWidget(plot)
        
        w.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    run = graphy()
    run.show()
    sys.exit(app.exec_())

        
#w.show()


        
