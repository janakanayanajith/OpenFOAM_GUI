'''
Created on Jun 1, 2020

@author: janaka
'''
import gui, conf, synHighlighter, codeEditor
from PyQt5 import  QtWidgets, QtCore#, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog, QFileSystemModel, QMessageBox
import os, shutil, sys
from threading import Thread
#from _ast import Try
#from itertools import count


class main:
    model = QFileSystemModel()
    #frozen = 'not'
    if getattr(sys, 'frozen', False):
            # we are running in a bundle
            #frozen = 'ever so'
            path = sys._MEIPASS
    else:
            # we are running in a normal Python environment
            path = os.path.dirname(os.path.abspath(__file__))
    #path=__file__
    #path=path[:path.rindex('/')]
    os.chdir(path)
    
    def start(self,g):
        self.g=g
        g.actionOpen.triggered.connect(self.open)
        g.actionExit.triggered.connect(self.exitAc)
        g.actionreactingFoam.triggered.connect(self.solve)
        g.actionBlock_Mesh.triggered.connect(self.blockMesh)
        g.actionDecompose.triggered.connect(self.decompose)
        g.actionReconstruct.triggered.connect(self.reconstruct)
        g.actionSettings.triggered.connect(self.conf)
        g.actionNew_File.triggered.connect(self.new)
        g.dlt.triggered.connect(self.dltFile)
        g.cPar.triggered.connect(self.dltPar)
        g.pv.triggered.connect(self.pF)
        g.svBtn.clicked.connect(self.saveFile)
        g.cAl.triggered.connect(self.clean)
        g.rPara.triggered.connect(self.rPara)
        g.chMesh.triggered.connect(self.checkMesh)
        g.intd.triggered.connect(self.funcautoindent)

        g.actionSave.triggered.connect(self.saveFile)
        g.treeView.doubleClicked.connect(self.treeClck)
        g.rld.clicked.connect(self.reload)
        g.tRn.clicked.connect(self.terminalRun)
        g.tln.returnPressed.connect(self.terminalRun)
        f= open("settings/terminal","r")
        trn=f.readline()
        f.close()
        g.tln.setText(trn)

        f= open("settings/solver","r")
        solver=f.readlines()
        f.close()
        self.solver=[solver[0][:-1],solver[1][:-1],solver[2]]
        #g.plainTextEdit.setStyleSheet("""QPlainTextEdit{    font-family:'Consolas';     color: #ccc;    background-color: #2b2b2b;}""")
        self.h = synHighlighter.PythonHighlighter(g.plainTextEdit.document())
        #synHighlighter.PythonHighlighter(self.cdE.document())
        #QtGui.QSyntaxHighlighter(g.plainTextEdit.document)
        #h.rehighlight()
        
        try:
            f= open("settings/pth","r")
            cnfData=f.readline()
            f.close()
            os.chdir(cnfData)
            g.pth.setText(cnfData)
            self.model = QFileSystemModel()
            self.model.setRootPath(cnfData)
            g.treeView.setModel(self.model)
            g.treeView.setRootIndex(self.model.index(cnfData))
            g.treeView.hideColumn(1)
            g.treeView.hideColumn(2)
            g.treeView.hideColumn(3)

        except FileNotFoundError:
            pass
     
    def funcautoindent(self):
        def insert(times):
            r = ''
            indent_width = '    '
            r=r+indent_width*times
            return r
        txtInput=self.g.plainTextEdit   
        cc = txtInput.textCursor()
        initialPos=cc.position()       
        textOld = str(txtInput.toPlainText())
        text=''
        for t in textOld.split('\n'):
            tmp=t.strip()
            try:
                if tmp[0]=='/' or tmp[0]=='=' or tmp[0]=='\\':
                    text+=t+'\n'                    
                else:
                    text+=tmp+'\n'
            except:
                text+=t+'\n'
        txtInput.clear()
        txtInput.insertPlainText(text) 
        cc = txtInput.textCursor()
        cc.movePosition(cc.Start,cc.MoveAnchor)
        index=0
        while(cc.movePosition(cc.NextCharacter,cc.KeepAnchor)==True):
            word = cc.selectedText()
            cc.clearSelection()
            if word == '{': 
                if '/' not in text[text.rindex('\n',0,index):index]:
                    if text[index+1] != '\n':
                        cc.insertText('\n')
            else:
                if word == '}':
                    if '/' not in text[text.rindex('\n',0,index):index]:
                        if text[index+1] != '\n':
                            cc.insertText('\n')
            index +=1
        
        text = str(txtInput.toPlainText())
        '''text=''
        for t in textOld.split('\n'):
            tmp=t.strip()
            try:
                if tmp[0]=='/' or tmp[0]=='=' or tmp[0]=='\\':
                    text+=t+'\n'                    
                else:
                    text+=tmp+'\n'
            except:
                text+=t+'\n' '''
        txtInput.clear()
        txtInput.insertPlainText(text) 
        cc = txtInput.textCursor()
        cc.setPosition(0,cc.MoveAnchor)
        index=0
        indent_level  = 0
        while(cc.movePosition(cc.NextCharacter,cc.KeepAnchor)==True):
            word = cc.selectedText()
            cc.clearSelection()
            if word == '{': 
                if '/' not in text[text.rindex('\n',0,index):index]:
                    if index != 0 and text[index-1] != '\n':
                        pos = cc.position()
                        if pos !=0:
                            cc.setPosition(pos-1,cc.MoveAnchor)
                            cc.insertText('\n')
                            cc.setPosition(pos+1,cc.MoveAnchor)
            else:
                if word == '}':
                    if '/' not in text[text.rindex('\n',0,index):index]:
                        if index != 0 and text[index-1] != '\n':
                            pos = cc.position()
                            if pos !=0:
                                cc.setPosition(pos-1,cc.MoveAnchor)
                                cc.insertText('\n')
                                cc.setPosition(pos+1,cc.MoveAnchor)
            index +=1
        index=0
        text = str(txtInput.toPlainText())
        '''text=''
        for t in textOld.split('\n'):
            tmp=t.strip()
            try:
                if tmp[0]=='/' or tmp[0]=='=' or tmp[0]=='\\':
                    text+=t+'\n'                    
                else:
                    text+=tmp+'\n'
            except:
                text+=t+'\n'
                '''
        txtInput.clear()
        txtInput.insertPlainText(text) 
        cc.setPosition(0,cc.MoveAnchor)
        while(cc.movePosition(cc.NextCharacter,cc.KeepAnchor)==True):
            word = cc.selectedText()
            cc.clearSelection()
            if word == '{': 
                if '/' not in text[text.rindex('\n',0,index):index]:
                    indent_level +=1
            else:
                if word == '}':
                    if '/' not in text[text.rindex('\n',0,index):index]:
                        indent_level -=1
                else:
                    try:
                        if '/'!=text[index:text.index('\n',index+1)].strip()[0]:                            
                            if text[index] == '\n' and text[index+1] != '}':
                                cc.insertText(insert(indent_level))
                            elif text[index] == '\n':
                                cc.insertText(insert(indent_level-1))
                    except:
                        pass
            index +=1
        index=0
        text = str(txtInput.toPlainText())
        txtInput.clear()
        txtInput.insertPlainText(text) 
        indent_level=0
        cc.setPosition(0,cc.MoveAnchor)
        while(cc.movePosition(cc.NextCharacter,cc.KeepAnchor)==True):
            word = cc.selectedText()
            cc.clearSelection()
            if word == '(': 
                if '/' not in text[text.rindex('\n',0,index):index]:
                    #print('if '+text[text.rindex('\n',0,index):index]+'---')
                    indent_level +=1
                else:
                    pass
                    #print('else  -'+text[text.rindex('\n',0,index):index]+'---')
            else:
                if word == ')':
                    if '/' not in text[text.rindex('\n',0,index):index]:
                        indent_level -=1
                else:
                    try:
                        if text[index] == '\n':
                            if '/'!=text[index:text.index('\n',index+1)].strip()[0]:                            
                                lfInx=text.index('\n',index+1)
                                cmImx=text.index('/',index+1)
                                t=text[index:min([lfInx,cmImx])]
                                if t.count(')')>t.count('('):
                                    cc.insertText(insert(indent_level-1))#+'-add1-')
                                elif t.count(')')<=t.count('('):
                                    cc.insertText(insert(indent_level))#+'-add1-')
                    except:
                        pass
            index +=1 
        text = str(txtInput.toPlainText())
        text=text[:-1]
        txtInput.clear()
        txtInput.insertPlainText(text) 
        cc.setPosition(initialPos,cc.MoveAnchor)  
        txtInput.setTextCursor(cc)        
     
    def dltPar(self):
        ret=QMessageBox.question(self.g.treeView, "Clean Processor dir's", "Are you sure you want to clean processor directories?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)        
        if ret==QMessageBox.Yes:
            for d in os.listdir(os.getcwd()):
                if "processor" in d:
                    shutil.rmtree(d)
                    
        
    def clean(self):
        ret=QMessageBox.question(self.g.treeView, "Clean", "Are you sure you want to clean results?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)        
        if ret==QMessageBox.Yes:
            for d in os.listdir(os.getcwd()):
                try:
                    if(float(d)!=0):
                        shutil.rmtree(d)
                except ValueError:
                    pass
                    
            self.dltPar()
        

    def dltFile(self):
        index=self.g.treeView.selectedIndexes()[0]
        filePath = self.model.filePath(index)
        ret=QMessageBox.question(self.g.treeView, 'Delete file', "Do you want to delete file \""+filePath.split("\"/")[-1]+"\"?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)        
        if ret==QMessageBox.Yes:
            try:    
                os.remove(filePath)
            except IsADirectoryError:
                shutil.rmtree(filePath)
        
    def conf(self):
        cw=conf.Conf(self.path,self.solver)
        try:
            self.solver=cw.solver
            try:
                f= open(self.path+"/settings/solver","w")
                f.writelines([self.solver[0]+"\n",self.solver[1]+"\n",self.solver[2]])
                f.close()
            except IsADirectoryError:
                pass
        except AttributeError:
            pass

    def saveFile(self):
        filePath=self.g.pth.text()
        if os.path.isfile(filePath):
            f= open(filePath,"r")
            if "".join(f.readlines())!=self.g.plainTextEdit.toPlainText():
                ret=QMessageBox.question(self.g.treeView, 'Save file', "Do you want to save changes of \""+filePath.split("\"/")[-1]+"\"?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        
                if ret==QMessageBox.Yes:
                    try:
                        f= open(filePath,"w")
                        f.writelines(self.g.plainTextEdit.toPlainText())
                    except IsADirectoryError:
                        pass
        
    def reload(self):
        filePath=self.g.pth.text()
        ret=QMessageBox.question(self.g.treeView, 'Save file', "Do you want to discard changes of \""+filePath.split("\"/")[-1]+"\"?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if ret==QMessageBox.Yes:
            f= open(filePath,"r")
            self.g.pth.setText(filePath)
            self.g.plainTextEdit.clear()
            for l in f.readlines:
                self.g.plainTextEdit.insertPlainText(l)
            f.close()

    def treeClck(self,index):
        self.saveFile()
        self.g.plainTextEdit.clear()
        indexItem = self.model.index(index.row(), 0, index.parent())
        filePath = self.model.filePath(indexItem)
        try:
            f= open(filePath,"r")
            self.g.pth.setText(filePath)
            for l in f.readlines():
                self.g.plainTextEdit.insertPlainText(l)
                #self.g.cd.insertPlainText(l)
            f.close()
        except IsADirectoryError:
            pass

        
    def open(self):
        p=str(QFileDialog.getExistingDirectory())
        print(p)
        os.chdir(p)
        self.g.pth.setText(p)
        
        self.model.setRootPath(p)
        self.g.treeView.setModel(self.model)
        self.g.treeView.setRootIndex(self.model.index(p))
        
        try:
            f= open(self.path+"/settings/pth","w")
            f.writelines(p)
            f.close()
        except IsADirectoryError:
            pass
    
    def new(self):
        p=str(QFileDialog.getSaveFileName())
        f= open(p.split("'")[1],"a+")
        f.close()       
    
    def exitAc(self):
        sys.exit(app.exec_())
        
    def solve(self):
        self.saveFile()
        srt="gnome-terminal -e \"bash -c \\\""+self.solver[1]+"; exec bash\\\"\""
        os.system(srt)
    
    def rPara(self):
        self.saveFile()
        srt="gnome-terminal -e \"bash -c \\\" mpirun -np "+self.solver[2]+" "+ self.solver[1]+" -parallel; exec bash\\\"\""
        os.system(srt)

    def blockMesh(self):
        self.saveFile()
        srt="gnome-terminal -e \"bash -c \\\"blockMesh; exec bash\\\"\""
        os.system(srt) 
        
    def checkMesh(self):
        srt="gnome-terminal -e \"bash -c \\\"checkMesh; exec bash\\\"\""
        os.system(srt) 

    def decompose(self):
        self.saveFile()
        srt="gnome-terminal -e \"bash -c \\\"decomposePar; exec bash\\\"\""
        os.system(srt) 
        
    def reconstruct(self):
        srt="gnome-terminal -e \"bash -c \\\"reconstructPar; exec bash\\\"\""
        os.system(srt) 
    
    def pF(self):
        #Thread(target = lambda: os.system("paraFoam")).start()
        Thread(target = lambda: os.system("paraFoam -builtin")).start()
            
    def terminalRun(self):
        self.saveFile()
        srt="gnome-terminal -e \"bash -c \\\""+self.g.tln.text()+"; exec bash\\\"\""
        os.system(srt)
        try:
            f= open(self.path+"/settings/terminal","w")
            f.writelines(self.g.tln.text())
            f.close()
        except IsADirectoryError:
            pass 

if __name__ == '__main__':
    #os.system("pyuic5 conf.ui -o confGui.py")
    #os.system("pyuic5 gui.ui -o gui.py")

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = gui.Ui_MainWindow()
    ret=ui.setupUi(MainWindow)
    ui.plainTextEdit=codeEditor.QCodeEditor(ui.centralwidget)
    ui.plainTextEdit.setGeometry(QtCore.QRect(430, 20, 821, 571))
       
    MainWindow.show()
    mn=main()
    mn.start(ui)
    sys.exit(app.exec_())
