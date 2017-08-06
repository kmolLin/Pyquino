## function of right-click

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def rightClick(self):
    self.treeWidget.customContextMenuRequested.connect(self.on_treeWidget_context_menu)
    self.popMenu_treeWidget = QMenu(self)
    self.action_treeWidget_add =  QAction("Add", self)
    self.popMenu_treeWidget.addAction(self.action_treeWidget_add)
    self.popMenu_treeWidget.addSeparator()
    self.action_treeWidget_del =  QAction("Delete", self)
    self.popMenu_treeWidget.addAction(self.action_treeWidget_del)
