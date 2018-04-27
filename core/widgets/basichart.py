# QT chart
from PyQt5.QtChart import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ChartDlg(QDialog):
    
    def __init__(self, parent = None):
        super(CanvasPaint, self).__init__(parent)
        self.chart = DataChart()
        self.view = QChartView(self.chart)
        self.setCentralWidget(self.view)
        
    
    
class DataChart(QChart):
    
    """A axis setted Qt chart widget."""
    
    def __init__(self, Title, axisX, axisY, parent=None):
        super(DataChart, self).__init__(parent)
        self.setTitle(Title)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        legend = self.legend()
        legend.setAlignment(Qt.AlignBottom)
        legend.setFont(QFont(legend.font().family(), 12, QFont.Medium))
        self.addAxis(axisX, Qt.AlignBottom)
        self.addAxis(axisY, Qt.AlignLeft)
    
    def hadleTimeout(self):
        pass
        # TODO: add timer to get data to plot
        #Qtimer
