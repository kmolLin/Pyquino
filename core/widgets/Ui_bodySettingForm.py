# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Lin\Desktop\Pyquino\core\widgets\bodySettingForm.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_bodyform(object):
    def setupUi(self, bodyform):
        bodyform.setObjectName("bodyform")
        bodyform.resize(398, 305)
        bodyform.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(bodyform)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtWidgets.QLabel(bodyform)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.compemontName = QtWidgets.QLineEdit(bodyform)
        self.compemontName.setObjectName("compemontName")
        self.horizontalLayout_3.addWidget(self.compemontName)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(bodyform)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.xsize = QtWidgets.QLineEdit(bodyform)
        self.xsize.setObjectName("xsize")
        self.horizontalLayout.addWidget(self.xsize)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(bodyform)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.ysize = QtWidgets.QLineEdit(bodyform)
        self.ysize.setObjectName("ysize")
        self.horizontalLayout_2.addWidget(self.ysize)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(bodyform)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.densityform = QtWidgets.QLineEdit(bodyform)
        self.densityform.setObjectName("densityform")
        self.horizontalLayout_4.addWidget(self.densityform)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.pushButtonCancel = QtWidgets.QPushButton(bodyform)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout_5.addWidget(self.pushButtonCancel)
        self.pushButtonAdd = QtWidgets.QPushButton(bodyform)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.horizontalLayout_5.addWidget(self.pushButtonAdd)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi(bodyform)
        QtCore.QMetaObject.connectSlotsByName(bodyform)

    def retranslateUi(self, bodyform):
        _translate = QtCore.QCoreApplication.translate
        bodyform.setWindowTitle(_translate("bodyform", "Dialog"))
        self.label_5.setText(_translate("bodyform", "Name"))
        self.label.setText(_translate("bodyform", "X-size"))
        self.label_2.setText(_translate("bodyform", "Y-size"))
        self.label_3.setText(_translate("bodyform", "Material density"))
        self.pushButtonCancel.setText(_translate("bodyform", "Cancel"))
        self.pushButtonAdd.setText(_translate("bodyform", "Add"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    bodyform = QtWidgets.QDialog()
    ui = Ui_bodyform()
    ui.setupUi(bodyform)
    bodyform.show()
    sys.exit(app.exec_())

