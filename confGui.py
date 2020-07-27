# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'conf.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(341, 575)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(70, 520, 221, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 50, 67, 17))
        self.label.setObjectName("label")
        self.slType = QtWidgets.QComboBox(Dialog)
        self.slType.setGeometry(QtCore.QRect(100, 50, 191, 25))
        self.slType.setObjectName("slType")
        self.slLst = QtWidgets.QListWidget(Dialog)
        self.slLst.setGeometry(QtCore.QRect(40, 90, 261, 371))
        self.slLst.setObjectName("slLst")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 480, 181, 17))
        self.label_2.setObjectName("label_2")
        self.np = QtWidgets.QSpinBox(Dialog)
        self.np.setGeometry(QtCore.QRect(230, 480, 71, 26))
        self.np.setMinimum(1)
        self.np.setMaximum(999999999)
        self.np.setObjectName("np")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Configurations"))
        self.label.setText(_translate("Dialog", "Solver"))
        self.label_2.setText(_translate("Dialog", "No of parallel processors:"))

