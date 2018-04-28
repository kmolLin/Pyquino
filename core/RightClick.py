## function of right-click

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def rightClick(self):
    self.mainCanvas.customContextMenuRequested.connect(self.on_mainCanvas_customContextMenuRequested)
    self.popMenu_treeWidget = QMenu(self)
    self.action_treeWidget_add =  QMenu("Add", self)
    self.jointmenu = QMenu("joint", self)
    self.action_treeWidget_add.addMenu(self.jointmenu)
    
    def connect_func(index):

        def func():
            print(index)

        return func
    
    for i in range(10):
        action = QAction(f"print{i}", self)
        action.triggered.connect(connect_func(i))
        self.jointmenu.addAction(action)
    
    self.popMenu_treeWidget.addMenu(self.action_treeWidget_add)
    self.popMenu_treeWidget.addSeparator()
    self.action_treeWidget_send =  QAction("Send", self)
    self.popMenu_treeWidget.addAction(self.action_treeWidget_send)
    self.popMenu_treeWidget.addSeparator()
    self.action_treeWidget_del =  QAction("Delete", self)
    self.popMenu_treeWidget.addAction(self.action_treeWidget_del)
    
    
