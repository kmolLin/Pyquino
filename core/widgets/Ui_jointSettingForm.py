# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Lin\Desktop\Pyquino\core\widgets\jointSettingForm.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_JointForm(object):
    def setupUi(self, JointForm):
        JointForm.setObjectName("JointForm")
        JointForm.resize(400, 300)
        JointForm.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(JointForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtWidgets.QLabel(JointForm)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.compemontName = QtWidgets.QLineEdit(JointForm)
        self.compemontName.setObjectName("compemontName")
        self.horizontalLayout_3.addWidget(self.compemontName)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label = QtWidgets.QLabel(JointForm)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.comboBoxtype = QtWidgets.QComboBox(JointForm)
        self.comboBoxtype.setObjectName("comboBoxtype")
        self.horizontalLayout_3.addWidget(self.comboBoxtype)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(JointForm)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.line = QtWidgets.QFrame(JointForm)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.label_3 = QtWidgets.QLabel(JointForm)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.spinBoxMax = QtWidgets.QSpinBox(JointForm)
        self.spinBoxMax.setMaximum(360)
        self.spinBoxMax.setObjectName("spinBoxMax")
        self.horizontalLayout_2.addWidget(self.spinBoxMax)
        self.label_4 = QtWidgets.QLabel(JointForm)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.spinBoxMin = QtWidgets.QSpinBox(JointForm)
        self.spinBoxMin.setMaximum(360)
        self.spinBoxMin.setObjectName("spinBoxMin")
        self.horizontalLayout_2.addWidget(self.spinBoxMin)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButtonCancel = QtWidgets.QPushButton(JointForm)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonAdd = QtWidgets.QPushButton(JointForm)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.horizontalLayout.addWidget(self.pushButtonAdd)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(JointForm)
        QtCore.QMetaObject.connectSlotsByName(JointForm)

    def retranslateUi(self, JointForm):
        _translate = QtCore.QCoreApplication.translate
        JointForm.setWindowTitle(_translate("JointForm", "Dialog"))
        self.label_5.setText(_translate("JointForm", "Name"))
        self.label.setText(_translate("JointForm", "Choose "))
        self.label_2.setText(_translate("JointForm", "Motor limit"))
        self.label_3.setText(_translate("JointForm", "Max"))
        self.label_4.setText(_translate("JointForm", "Mini"))
        self.pushButtonCancel.setText(_translate("JointForm", "Cancel"))
        self.pushButtonAdd.setText(_translate("JointForm", "Add"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    JointForm = QtWidgets.QDialog()
    ui = Ui_JointForm()
    ui.setupUi(JointForm)
    JointForm.show()
    sys.exit(app.exec_())

