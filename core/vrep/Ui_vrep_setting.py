# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Y:\Pyquino\core\vrep\vrep_setting.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(797, 512)
        Dialog.setSizeGripEnabled(True)
        self.yAxisdown = QtWidgets.QPushButton(Dialog)
        self.yAxisdown.setGeometry(QtCore.QRect(190, 250, 91, 61))
        self.yAxisdown.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/arrow-down-b.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.yAxisdown.setIcon(icon)
        self.yAxisdown.setIconSize(QtCore.QSize(30, 30))
        self.yAxisdown.setObjectName("yAxisdown")
        self.xAxisleft = QtWidgets.QPushButton(Dialog)
        self.xAxisleft.setGeometry(QtCore.QRect(80, 150, 91, 61))
        self.xAxisleft.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/arrow-left-b.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.xAxisleft.setIcon(icon1)
        self.xAxisleft.setIconSize(QtCore.QSize(30, 30))
        self.xAxisleft.setObjectName("xAxisleft")
        self.yAxisup = QtWidgets.QPushButton(Dialog)
        self.yAxisup.setGeometry(QtCore.QRect(190, 50, 91, 61))
        self.yAxisup.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/arrow-up-b.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.yAxisup.setIcon(icon2)
        self.yAxisup.setIconSize(QtCore.QSize(30, 30))
        self.yAxisup.setObjectName("yAxisup")
        self.xAxisrigh = QtWidgets.QPushButton(Dialog)
        self.xAxisrigh.setGeometry(QtCore.QRect(300, 150, 91, 61))
        self.xAxisrigh.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/arrow-right-b.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.xAxisrigh.setIcon(icon3)
        self.xAxisrigh.setIconSize(QtCore.QSize(30, 30))
        self.xAxisrigh.setObjectName("xAxisrigh")
        self.stepbox = QtWidgets.QSpinBox(Dialog)
        self.stepbox.setGeometry(QtCore.QRect(380, 370, 42, 20))
        self.stepbox.setMaximum(100)
        self.stepbox.setSingleStep(0)
        self.stepbox.setProperty("value", 10)
        self.stepbox.setObjectName("stepbox")
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(330, 370, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(Dialog)
        self.label_12.setGeometry(QtCore.QRect(420, 370, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.unlockMachine = QtWidgets.QPushButton(Dialog)
        self.unlockMachine.setGeometry(QtCore.QRect(80, 370, 101, 31))
        self.unlockMachine.setObjectName("unlockMachine")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_11.setText(_translate("Dialog", "step"))
        self.label_12.setText(_translate("Dialog", "mm"))
        self.unlockMachine.setText(_translate("Dialog", "connect"))

#import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

