# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Lin\Desktop\Pyquino\core\graphy\graphy.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(945, 652)
        Dialog.setSizeGripEnabled(True)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 30, 411, 591))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.xhorizontalSlider = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.xhorizontalSlider.setMaximum(360)
        self.xhorizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.xhorizontalSlider.setObjectName("xhorizontalSlider")
        self.horizontalLayout.addWidget(self.xhorizontalSlider)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.yhorizontalSlider = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.yhorizontalSlider.setMaximum(360)
        self.yhorizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.yhorizontalSlider.setObjectName("yhorizontalSlider")
        self.horizontalLayout_4.addWidget(self.yhorizontalSlider)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.zhorizontalSlider = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.zhorizontalSlider.setMaximum(360)
        self.zhorizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.zhorizontalSlider.setObjectName("zhorizontalSlider")
        self.horizontalLayout_3.addWidget(self.zhorizontalSlider)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "xRot"))
        self.label_3.setText(_translate("Dialog", "yRot"))
        self.label_2.setText(_translate("Dialog", "zRot"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

