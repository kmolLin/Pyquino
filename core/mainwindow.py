# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets , QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import platform
from . import serialportcontext
import threading
import time
import serial

from .Ui_mainwindow import Ui_MainWindow
#from .Ui_mainwindow2 import Ui_MainWindow2
from .monitor.machine_mointor import Machine
from .serial.serialport import Serialport
from .RightClick import rightClick
from .settingForm import SettingForm
from .widgets.simulation import CanvasPaint
from .vrep.vrep_setting import vrepsetting



class MainWindow(QMainWindow, Ui_MainWindow):

    _receive_signal = QtCore.pyqtSignal(str)
    _auto_send_signal = QtCore.pyqtSignal()
    def __init__(self, args, parent=None):
        
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.main_splitter.setSizes([200, 200])
        rightClick(self)
        '''
        pal = QPalette()
        pal.setColor(QPalette.Background, QColor(125,125 ,125))
        
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        '''
        #self.initForms()
        self.actionserial.triggered.connect(self.__serialport__)
        self.actionVrep.triggered.connect(self.__teset__)
        self.actionControl.triggered.connect(self.__control__)
        
        self.mainCanvas = CanvasPaint(self)
        self.painter_layout.addWidget(self.mainCanvas)
        self.sim_start.clicked.connect(lambda:self.mainCanvas.setTimer(True))
        self.sim_stop.clicked.connect(lambda:self.mainCanvas.setTimer(False))
        self.treecontextMenu = QMenu(self)
        self.treecontextMenuadd = QMenu("add", self)
        self.aaaction = QAction("add", self)
        self.treecontextMenu.addAction(self.aaaction)
        self.treecontextMenu.addMenu(self.treecontextMenuadd)
        self.canvasMenu = QMenu(self)
    
        
    @pyqtSlot(QPoint)
    def on_treeWidget_context_menu(self, point):
        action = self.popMenu_treeWidget.exec_(self.treeWidget.mapToGlobal(point))
        if action == self.action_treeWidget_add:
            dlg = SettingForm()
            dlg.show()
            if dlg.exec_():
                self.formfile = dlg.getlist
                self.reflesh()
                print(self.formfile)
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
        dlg1 = vrepsetting()
        dlg1.show()
        if dlg1.exec_(): pass
        print("I'm test")
    
    def __serialport__(self):
        dlg2 = Serialport()
        dlg2.show()
        if dlg2.exec_(): pass
    
    def __control__(self):
        print("control open")
        dlg = Machine()
        dlg.show()
        if dlg.exec_(): pass
    
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
    
