 #-*- coding: utf-8 -*-
import sys

from PyQt4 import QtCore, QtGui
import interfaceGeraArquivos
import interfaceGeraArquivosCodigo
import interfacePrincipal


class MyForm(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = interfacePrincipal.Ui_MainWindow()
        self.ui.setupUi(self)
    def baixaPdbsProteinas(self):
        print("ppp")
        self.ui.textBrowser.setText("Baixa proteinas")
    def fazRegressao(self):
        print("ppp")
    def geraArquivoMedias(self):
        print("ppp")
    def geraArquivoParaRegressao(self,parent = None):
        print("pppppp")
        self.ui.textBrowser.setText("Gera arquivos para regressão linear")
        QtGui.QWidget.__init__(self, parent)
        self.ui2 = interfaceGeraArquivosCodigo.WindowGeraArquivos()
        self.ui2.show()
    def sair(self):
        sys.exit()
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainwin = MyForm()
    mainwin.show()
    sys.exit(app.exec_())