#!/usr/bin/env python3.5
# coding=utf-8
######################################################
#TO DO
# 
#Importante
# quando usa o instalador py2exe a mensagem rodando taba deve ser desabilitada
######################################################
from PyQt4 import QtGui  # Import the PyQt4 module we'll need
import sys  # We need sys so that we can pass argv to QApplication
from func_Gerais import get_platform
# it also keeps events etc that we defined in Qt Designer

#import linear_regression_4
import interfacePrincipal
import winInformacoes
import winBaixaPdbs
import winExperimentoUsuario
import winGeraArquivosRegressao
import winRegressao
import winCorrelacao
import winGestaoExperimentos
import winAjuda
import os, platform
from func_Gerais import limpa_arquivosSf, existeArquivo, grava,gravaConfigTaba, pegaConfigTaba,completaArquivoConfig, completaArquivoConfigTaba,rodandoTaba, limpaPastas, get_desktop_path
from func_manipulaArquivos import apagaArquivo, criaArquivo, completaPastas
#import platform
#print(platform.python_version())

class principal(QtGui.QMainWindow, interfacePrincipal.Ui_MainWindowPrincipal):
    def __init__(self):
        self.versao = "Version 2.3.1.2" # seta a versao do taba na tela principal
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us todi
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()         
        self.setupUi(self)  # This is defined in design.py file automatically
        # It sets up layout and widgets that are defined
        #self.toolButton_regressao.clicked.connect(self.fazRegressao())  # When the button is pressed
        # Execute browse_folder function
        #QtGui.QMessageBox.information(self, "Attention", "Entrou novamente")
        self.move(80,50)
        self.setFixedSize(822,300)
        self.window2 = None
        self.window3 = None
        self.window4 = None
        self.window5 = None
        self.window6 = None
        self.window7 = None
        self.window8 = None
        self.window9 = None
        diret = "./arquivosSaida/"
        self.label_version.setText(self.versao)
        limpa_arquivosSf(diret)
        # as funcoes abaixo devem ficar nesta ordem
        completaPastas() # cria pastas que nao existam
        completaArquivoConfig() # novas versões podem conter novas tags
        completaArquivoConfigTaba() # novas versões podem conter novas tags
        self.limparExperimento()  
        self.verificaRodando()        
        apagaArquivo("logs.log") # limpa arquivo de log de erros que são necessarios somente em testes
        criaArquivo("logs.log")
        self.criaAtalho()        
    def informacoes(self):
        if self.window2 is None:
            self.window2 = winInformacoes.informacoes(self)
        self.window2.show()
        self.window2 = None
    def baixaPdbsProteinas(self):
        if self.window3 is None:
            self.window3 = winBaixaPdbs.baixaPdbs(self)
        QtGui.QApplication.processEvents() # para não travar
        self.window3.show()
        self.window3 = None
    def fazExperimento(self):
        if self.window4 is None:
            self.window4 = winExperimentoUsuario.experimentoUsuario(self)
        QtGui.QApplication.processEvents() # para não travar        
        self.window4.lineEdit_estrutura.clear()# apaga dados anteriores
        self.window4.lineEdit_Ligante.clear()# apaga dados anteriores
        self.window4.show()
        self.window4 = None
    def geraArquivoParaRegressao(self):
        if self.window5 is None:
            self.window5 = winGeraArquivosRegressao.geraArquivosRegressao(self)
        QtGui.QApplication.processEvents() # para não travar
        self.window5.show()
        self.window5 = None
    def fazRegressao(self):
        if self.window6 is None:
            self.window6 = winRegressao.fazRegressao(self)
        QtGui.QApplication.processEvents() # para não travar
        self.window6.show()
        self.window6 = None
    def fazCorrelacao(self):
        if self.window7 is None:
            self.window7 = winCorrelacao.fazCorrelacao(self)
        QtGui.QApplication.processEvents() # para não travar
        self.window7.show()
        self.window7 = None 
    def gerenciarExperimentos(self):
        if self.window8 is None:
            self.window8 = winGestaoExperimentos.gestaoExperimentos(self)
        QtGui.QApplication.processEvents() # para não travar
        self.window8.show()
        self.window8 = None 
    def sair(self):     
        self.close() 

    def ajuda(self):     
        if self.window9 is None:
            self.window9 = winAjuda.ajuda(self)
        self.window9.show()
        self.window9 = None   
    
    def limparExperimento(self):
        if (pegaConfigTaba("versao").strip() == 'novaVersao'):
            QtGui.QMessageBox.information(self, "Message", "A new version of Taba will be installed.." +"\n"+ "If a Taba version already exists, the experiment in progress will be deleted." +"\n"+"You can recover them if you saved them earlier.")
            limpaPastas()
            gravaConfigTaba("versao", self.versao.strip())
            QtGui.QMessageBox.information(self, "Message", "Operation completed")
        else:
            pass
    def criaAtalho(self):
        if ('LINUX' in get_platform().upper()): # ve se nao e linux e esconde botal de criacao de atalho
            self.criaAtalhoOk()
        else:
            pass
    def criaAtalhoOk(self):  
        if pegaConfigTaba("atalho").strip() == "yes":
            desktop = get_desktop_path()
            dirAtual = os.getcwd()+"/"
            dirBase = os.path.dirname(os.path.dirname(dirAtual)) # pega o diretorio acima do Taba
            programa = "./Taba"
            fonte = "python3 taba.py" 
            icone = "img/beagle3.png"
            arquivoAtalho = desktop+"/Taba.desktop"
            if existeArquivo(dirAtual+"taba.py"):
                textoScript = "#! /bin/bash"+"\n"+"cd "+dirAtual+"\n"+fonte              
            else:
                textoScript = "#! /bin/bash"+"\n"+"cd "+dirAtual+"\n"+programa   
            if existeArquivo(arquivoAtalho) == False:
                reply = QtGui.QMessageBox.question(self, "Create a desktop shortcut","Do you want to create a shortcut on the desktop?"+"\n"+"If you do not want to see this message again, uncheck 'Create a shortcut on the desktop' at the bottom of this window", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    if desktop.strip() == dirBase.strip(): # nao e possivel criar icone quando o taba esta no desktop
                        QtGui.QMessageBox.information(self, "Attention!", "It is not possible to create a shortcut when the Taba folder is on the Desktop."+"\n"+\
                        "Move the Taba folder to another location in the user's folder and check 'Create a shortcut on the desktop' at the bottom of the screen again.")
                        gravaConfigTaba("atalho", "no")                
                        pass
                    else:
                        TextoLancador = "[Desktop Entry]"+"\n"+"Name=Taba"+"\n"+"Type=Application"+"\n"+"Exec=sh "+dirAtual+"taba.sh"+"\n"+"Icon="+dirAtual+icone
                        grava(textoScript, "./taba.sh")
                        grava(TextoLancador, arquivoAtalho)
                        os.chmod(arquivoAtalho, 0o777)# muda permissao
                        QtGui.QMessageBox.information(self, "Message", "The shortcut to Taba was created on the desktop!")
                else:
                    pass
            else:
                pass
        else:
            pass  
    def verificaRodando(self):
        if (rodandoTaba()) and ("WINDOWS" in (platform.system()).upper()): 
            QtGui.QMessageBox.information(self, "Attention", "Taba is already running. You can only run one instance.")
            sys.exit()  
        elif rodandoTaba(): # e linux
            sys.exit()  
def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = principal()  # We set the form to be our ExampleApp (design)
    form.show()  # Show the form
    app.exec_()  # and execute the app
    '''
    aqui podem vir tarefas de finzlizacao
    '''
if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function
    

