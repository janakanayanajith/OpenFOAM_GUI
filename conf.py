'''
Created on Jun 2, 2020

@author: janaka'''
from PyQt5 import  QtWidgets#, QtCore
import confGui, os
#from PyQt5.QtWidgets import QListWidgetItem, QMessageBox


class Conf(object):
    def __init__(self,path,solver):
        #self.solver=solver
        Dialog = QtWidgets.QDialog()
        ui = confGui.Ui_Dialog()
        self.ui=ui
        ui.setupUi(Dialog)
        self.stPath=path+"/settings/solvers"
        self.flLst=sorted(next(os.walk(self.stPath))[2])
        ui.slType.addItems(self.flLst)
        ui.slType.currentIndexChanged.connect(self.sel)
        ui.buttonBox.accepted.connect(self.accp) 
        indexSlType=self.flLst.index(solver[0])
        ui.slType.setCurrentIndex(indexSlType)
        lst=self.sel(indexSlType)
        ui.slLst.setCurrentRow(lst.index(solver[1]))
        ui.np.setValue(int(solver[2]))
        Dialog.exec_()
        
        
    def sel(self,indexSlType):
        f= open(self.stPath+"/"+self.flLst[indexSlType],"r")
        solver=f.readlines()
        for i in range(len(solver)-1):
            solver[i]=solver[i][:-1]
        self.ui.slLst.clear()
        self.ui.slLst.addItems(solver)
        self.ui.slLst.setCurrentRow(0)
        return solver

    def accp(self):
        self.solver=[self.ui.slType.currentText(),self.ui.slLst.currentItem().text(),str(self.ui.np.value())]

        