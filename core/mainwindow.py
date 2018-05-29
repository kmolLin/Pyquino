# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .Ui_mainwindow import Ui_MainWindow
from .monitor.machine_mointor import Machine
from .serial.serialport import Serialport
from .RightClick import rightClick
from .settingForm import SettingForm
from .widgets.simulation import CanvasPaint
from .vrep.vrep_setting import vrepsetting
from .IO.representation import *

import matplotlib.pyplot as plt
import numpy as np

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, args, parent=None):
        
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.main_splitter.setSizes([200, 200])
        self.actionserial.triggered.connect(self.__serialport__)
        self.actionVrep.triggered.connect(self.__teset__)
        self.actionControl.triggered.connect(self.__control__)
        self.mainCanvas = CanvasPaint(self)
        self.painter_layout.addWidget(self.mainCanvas)
        self.sim_start.clicked.connect(self.let)
        self.sim_stop.clicked.connect(lambda:self.mainCanvas.setTimer(2))
        rightClick(self)
    
    def let(self):
        self.mainCanvas.setTimer(0)
        self.mainCanvas.setMotor(10)
        self.mainCanvas.update()
        
    
    @pyqtSlot(QPoint)
    def on_mainCanvas_customContextMenuRequested(self, point):
        action = self.popMenu_treeWidget.exec_(self.mainCanvas.mapToGlobal(point))
        
    
    @pyqtSlot(QPoint)
    def on_treeWidget_customContextMenuRequested(self, point):
        action = self.popMenu_treeWidget.exec_(self.treeWidget.mapToGlobal(point))
        if action == self.action_treeWidget_add:
            dlg = SettingForm()
            dlg.show()
            if dlg.exec_():
                self.formfile = dlg.getlist
                self.reflesh()
        elif action ==self.action_treeWidget_del:
            try :
                self.tree.takeTopLevelItem(self.treeitemSelct[1])
            except:
                print("No select")
        elif action == self.action_treeWidget_send:
            try :
                data = 'asa'
                if self._serial_context_.isRunning():
                    if len(data) > 0: self._serial_context_.send(data, 0)
                    print(self.tree.currentItem().takeChildren())
            except:
                pass
                
                
    def treewidgetupdate(self):
        root = QTreeWidgetItem(["123", "234"])
        root.setFlags((root.flags() | Qt.ItemIsEditable))
        root.addChild(QTreeWidgetItem(["Max", "20" ]))
        self.tree.addTopLevelItem(root)

    
    def reflesh(self):
        if self.formfile['component'] == "Motor":
            root = QTreeWidgetItem([self.formfile['Name'], self.formfile['component']])
            root.setFlags((root.flags() | Qt.ItemIsEditable))
            root.addChild(QTreeWidgetItem(["Max", str(self.formfile['Mini']) ]))
            root.addChild(QTreeWidgetItem(["Min", str(self.formfile['Max'])]))
            root.addChild(QTreeWidgetItem(["signal", self.formfile['signal']]))
            
            self.tree.addTopLevelItem(root)
        elif self.formfile['component'] == "Sensor":
            root = QTreeWidgetItem([self.formfile['Name'], self.formfile['component']])
            root.setFlags((root.flags() | Qt.ItemIsEditable))
            root.addChild(QTreeWidgetItem(["signal", self.formfile['signal']]))
            
            self.tree.addTopLevelItem(root)
        elif self.formfile['component'] == "Light":
            root = QTreeWidgetItem([self.formfile['Name'], self.formfile['component']])
            root.setFlags((root.flags() | Qt.ItemIsEditable))
            root.addChild(QTreeWidgetItem(["signal", self.formfile['signal']]))
            self.tree.addTopLevelItem(root)
    
    def __teset__(self):
        dlg = vrepsetting()
        dlg.show()
        dlg.exec_()
    
    def __serialport__(self):
        dlg = Serialport()
        dlg.yield_signal.connect(self.mainCanvas.setMotor)
        dlg.show()
        dlg.exec_()
    
    def __control__(self):
        print("control open")
        dlg = Machine()
        dlg.show()
        dlg.exec_()
    
    @pyqtSlot(QTreeWidgetItem, QTreeWidgetItem)
    def on_tree_currentItemChanged(self, current, previous):
        """
        Slot documentation goes here.
        
        @param current DESCRIPTION
        @type QTreeWidgetItem
        @param previous DESCRIPTION
        @type QTreeWidgetItem
        """
        # TODO: not implemented yet
        #print(current.text(0))

    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_tree_itemChanged(self, item, column):
        if column==0:
            finder = lambda x: self.tree.findItems(x, (Qt.MatchFixedString), 1)
            checkName = finder('Sensor')
            checkName += finder('Motor')
            checkName += finder('Light')
            names = [item.text(0) for item in checkName]
            del names[names.index(item.text(0))]
            print(names)
            print(item.text(0) in names)
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_tree_itemClicked(self, item, column):
        self.treeitemSelct = [item, column]
        print(column)
    
    @pyqtSlot()
    def on_openfile_triggered(self):
        """ Open file in machine"""
        example, inputs = ("M[" +
        "J[R, color[Green], P[0.0, 0.0], L[ground, link_1]], " +
        "J[R, color[Green], P[12.92, 32.53], L[link_1, link_2]], " +
        "J[R, color[Green], P[73.28, 67.97], L[link_2, link_3]], " +
        "J[R, color[Green], P[33.3, 66.95], L[link_2]], " +
        "J[R, color[Green], P[90.0, 0.0], L[ground, link_3]]" +
        "]", {0: ('ground', 'link_1')})
        
        self.mainCanvas.loaddata(parse_vpoints(example))
        self.mainCanvas.update()
        self.treewidgetupdate()
    
    @pyqtSlot()
    def on_go_clicked(self):
        self.mainCanvas.setTimer(0)
        self.mainCanvas.target = self.Target.value()
        self.mainCanvas.update()
    
    @pyqtSlot()
    def on_plot_clicked(self):
        #print(self.mainCanvas.plotdata)
        print(len(self.mainCanvas.plotdata))
        plt.plot(np.arange(len(self.mainCanvas.plotdata)), self.mainCanvas.plotdata)
        plt.show()
    
    @pyqtSlot()
    def on_sim_pause_clicked(self):
        self.mainCanvas.setTimer(1)
