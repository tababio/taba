#!/usr/bin/env python3
# coding=utf-8
import func_manipulaArquivos as manip
import os
import shutil
from datetime import datetime
from PyQt4 import QtGui, QtCore # Import the PyQt4 module we'll need
import interfaceGestaoExperimentos
from func_Gerais import make_zipfile, unzipFolder, pegaConfig, pegaConfigTaba, get_pastas, gravaConfig, gravaConfigTaba, completaArquivoConfig, get_platform, converteStringDeltaG
from func_manipulaArquivos import removePasta, completaPastas
class gestaoExperimentos(QtGui.QMainWindow, interfaceGestaoExperimentos.Ui_MainWindow_manageFiles):
    def __init__(self, parent = None):
                   
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.window1 = None
        self.setFixedSize(950,600)        
        nome = pegaConfig("nomeExperimento").strip()
        self.label_outliers.setText(pegaConfig("outlier").strip()) 
        self.label_estruturaInicial.setText(pegaConfig("quantidadeInicialProteinas").strip())  
        self.listaExperimentos = []
        now = str(datetime.now())
        now = now.replace(" ", "")
        now = now.replace("-", "")
        now = now.replace(":", "")
        #d = "_"+now[0:14]
        self.atualizaNomes()
        self.atualizaNomesDeletar()
        #self.lineEdit_experimento.setText(nome+d)
        self.lineEdit_experimento.setText(nome)
        self.recuperaInfos()
        
        self.label_relogio.hide()  
        self.movie = QtGui.QMovie("./img/gifTempo.gif")
        self.label_relogio.setMovie(self.movie)
        if pegaConfigTaba('atalho').strip() == 'yes':
            self.checkBox_atalho.setChecked(True)
        else:
            self.checkBox_atalho.setChecked(False)
        if not ('LINUX' in get_platform().upper()): # ve se nao e linux e esconde botal de criacao de atalho
            self.checkBox_atalho.hide()
        else:
            if self.checkBox_atalho.isChecked():
                self.criaAtalho()
            
    def atualizaNomes(self):
        self.list1 = get_pastas("./setsExperiments/")
        self.comboBox_arquivos.clear()
        for text in self.list1:
            text = text.replace("./setsExperiments/","")
            self.listaExperimentos.append(text)
            self.comboBox_arquivos.addItem(text) # pega so arquivos de treino
            self.comboBox_arquivos.model().sort(0)
            self.comboBox_arquivos.setCurrentIndex(1)
    def atualizaNomesDeletar(self):
        self.list1 = get_pastas("./setsExperiments/")
        self.comboBox_deletaArquivos.clear()
        for text in self.list1:
            text = text.replace("./setsExperiments/","")
            self.listaExperimentos.append(text)
            self.comboBox_deletaArquivos.addItem(text) # pega so arquivos de treino
            self.comboBox_deletaArquivos.model().sort(0)
            self.comboBox_deletaArquivos.setCurrentIndex(1) 
    def salvarExperimentos(self): 
        self.listaExperimentos = []
        self.list1 = get_pastas("./setsExperiments/")
        for text in self.list1:
            text = text.replace("./setsExperiments/","")
            self.listaExperimentos.append(text)

        # cria pasta para novo conjunto
        self.nomeConjunto = self.lineEdit_experimento.text()
        if self.nomeConjunto in self.listaExperimentos:
            reply = QtGui.QMessageBox.question(self, 'Message',"This set of experiments already exists. Do you want to replace?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.salva()
                
        else:
            self.label_relogio.show() 
            self.movie.start()
            self.salva()
            self.label_relogio.hide()  
            self.movie.stop()
        pass
    def salva(self):
        pastaParaSalvar = "TABA/setsExperiments/"+self.nomeConjunto
        reply = QtGui.QMessageBox.question(self, 'Message',"All files from this experiment will be saved in: "+pastaParaSalvar+"\n"+"\n"+"Do you really want to save this experiment?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:        
            
            nomePasta = "./setsExperiments/"+self.nomeConjunto
            gravaConfig("nomeExperimento", self.nomeConjunto)
            manip.criaPasta(nomePasta)
            # copia pastas para o novo conjunto
            origem = "./outputFiles/"
            destino = nomePasta+origem.replace(".", "")
            removePasta(destino)
            manip.copiaPasta(origem, destino)
            origem = "./pdbs/"
            destino = nomePasta+origem.replace(".", "")
            removePasta(destino)
            manip.copiaPasta(origem, destino)
            origem = "./ki/"
            destino = nomePasta+origem.replace(".", "")
            removePasta(destino)
            manip.copiaPasta(origem, destino)
            origem = "./inputFiles/"
            destino = nomePasta+origem.replace(".", "")
            removePasta(destino)
            manip.copiaPasta(origem, destino)
            origem = "./models/"
            destino = nomePasta+origem.replace(".", "")
            removePasta(destino)
            manip.copiaPasta(origem, destino)
            origem = "./results/"
            destino = nomePasta+origem.replace(".", "")
            removePasta(destino)
            manip.copiaPasta(origem, destino)
            self.atualizaNomes()
            self.atualizaNomesDeletar()
            experimento = pegaConfig("nomeExperimento").strip()
            self.label_experimento.setText(experimento)
            QtGui.QMessageBox.information(self, "Message", "Operation completed")
            data = datetime.now()
            data = str(data.strftime("%Y-%m-%d   %H:%M:%S"))
            gravaConfig("data", data)
            self.recuperaInfos()
        else:
            pass              

    def recuperarExperimentos(self):
        self.escondeBotoes()
        reply = QtGui.QMessageBox.question(self, 'Message',"Attention: It is important to save the current experiment before!!!"+"\n"+"\n"+"Do you really want to recover this experiment?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            QtGui.QApplication.processEvents() # para não travar usar antes de loops   
            self.label_relogio.show()  
            self.movie.start()
            QtGui.QApplication.processEvents() # para não travar   
            self.nomeConjunto = self.comboBox_arquivos.currentText()
            # copia pastas para o novo conjunto
            origem = "./setsExperiments/"+self.nomeConjunto+"/outputFiles/"
            destino = "./outputFiles/"
            removePasta(destino)
            manip.copiaPasta(origem, destino)
            origem = "./setsExperiments/"+self.nomeConjunto+"/pdbs/"
            destino = "./pdbs/"
            removePasta(destino)
            manip.copiaPasta(origem, destino)
            origem =  "./setsExperiments/"+self.nomeConjunto+"/ki/"
            destino = "./ki/"
            removePasta(destino)
            manip.copiaPasta(origem, destino)
            origem =  "./setsExperiments/"+self.nomeConjunto+"/inputFiles/"
            destino = "./inputFiles/"
            removePasta(destino)
            manip.copiaPasta(origem, destino)
            origem =  "./setsExperiments/"+self.nomeConjunto+"/models/"
            destino = "./models/"
            removePasta(destino)
            manip.copiaPasta(origem, destino)
            
            origem =  "./setsExperiments/"+self.nomeConjunto+"/results/"
            destino = "./results/"
            removePasta(destino)
            manip.copiaPasta(origem, destino)
            
            # as funcoes abaixo demv ficar nesta ordem
            completaPastas() # cria pastas que nao existam
            completaArquivoConfig() # novas versões podem conter novas tags

            self.recuperaInfos()
            now = str(datetime.now())
            now = now.replace(" ", "")
            now = now.replace("-", "")
            now = now.replace(":", "")
            #d = "_"+now[0:14]
            self.lineEdit_experimento.setText(pegaConfig("nomeExperimento").strip())
            self.label_comentarios.setText(pegaConfig("comentarios").replace("<vg>", ","))
            self.label_quantia.setText(pegaConfig("quantidadeProteinas").strip())
            self.label_estruturaInicial.setText(pegaConfig("quantidadeInicialProteinas").strip()) 
            QtGui.QMessageBox.information(self, "Message", "Operation completed")
            self.label_relogio.hide()  
            self.movie.stop
            self.mostraBotoes()
            self.label_outliers.setText(pegaConfig("outlier").strip())  
        else:
            self.mostraBotoes()
            pass            
        
                
    def sair(self):        
        self.close()
        
                
    def escondeBotoes(self):
        self.pushButton_salvar.setEnabled(False)
        self.pushButton_recuperar.setEnabled(False)
        self.toolButton_exit.setEnabled(False)
    def mostraBotoes(self):
        self.pushButton_salvar.setEnabled(True)
        self.pushButton_recuperar.setEnabled(True)
        self.toolButton_exit.setEnabled(True)
        

    def recuperaInfos(self):
        
        completaArquivoConfig()
        descricao = pegaConfig("descricaoDataset").strip()
        afinidade = pegaConfig("tipoAfinidade").strip()        
        afinidade = converteStringDeltaG(afinidade)
        data = pegaConfig("data").strip()
        experimento = pegaConfig("nomeExperimento").strip()
        self.label_descricao.setText(descricao)
        self.label_afinidade.setText(afinidade)
        self.label_toExperiment.setText(experimento)
        self.label_experimento.setText(experimento)
        self.label_experimento.setText(experimento)
        self.label_data.setText(data)
        excluiLigantes = pegaConfig("excluiLigantes").strip()
        if excluiLigantes != "yes":
            self.label_deleteLigand.setText("no")
        else:
            self.label_deleteLigand.setText("yes")
        if not(pegaConfig("spearman") is None):
            self.label_comentarios.setText(pegaConfig("comentarios").replace("<vg>", ","))
            self.label_quantia.setText(pegaConfig("quantidadeProteinas").strip())
        else:
            self.label_comentarios.setText("null")
            self.label_spearman.setText("null")
            self.label_quantia.setText("null")
            
    def deletar(self): 
        self.escondeBotoes()
        reply = QtGui.QMessageBox.question(self, 'Message',"Do you really want to delete this experiment from 'setsExperiments' folder?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes: 
            self.label_relogio.show()    
            self.movie.start()
            self.nomeConjunto = self.comboBox_deletaArquivos.currentText()
            # copia pastas para o novo conjunto
            pasta = "./setsExperiments/"+self.nomeConjunto
            manip.removePasta(pasta)
            QtGui.QMessageBox.information(self, "Message", "Operation completed")
            self.mostraBotoes()
            self.atualizaNomes()
            self.atualizaNomesDeletar()
            self.label_relogio.hide() 
            self.movie.stop()
        else:
            self.mostraBotoes()
             
            pass
    
 
    def apagaArquivos(self):
        if (self.radioButton_1.isChecked()) or (self.radioButton_2.isChecked()) or (self.radioButton_3.isChecked()) or (self.radioButton_4.isChecked()):
            self.apagaArquivosOk()
        else:
            QtGui.QMessageBox.information(self, "Message", "You must select a option first!")
            pass
    def apagaArquivosOk(self):
        reply = QtGui.QMessageBox.question(self, 'Message',"Do you really want to delete selected files?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            if self.radioButton_4.isChecked():            
                manip.apagaArquivos("./pdbs")
                manip.apagaArquivos("./ki")
                manip.apagaArquivos("./outputFiles")
                manip.apagaArquivos("./models")
                manip.apagaArquivos("./results")
   
            if self.radioButton_3.isChecked():
                manip.apagaArquivos("./outputFiles")
                manip.apagaArquivos("./models")
                manip.apagaArquivos("./results")
   
            if self.radioButton_2.isChecked():
                arqOutput = manip.arquivosNaPastaOutput()
                dir = "./outputFiles/"
                for i in arqOutput:
                    if "SF_saida" in i:
                        manip.apagaArquivo(dir+i)
                manip.apagaArquivos("./models")
                manip.apagaArquivos("./results")
                
            if self.radioButton_1.isChecked():
                manip.apagaArquivos("./models")
                manip.apagaArquivos("./results")
                
            QtGui.QMessageBox.information(self, "Message", "The selected files have been deleted!")
            self.limpaRadioButtons()
        else:
            pass
    def limpaRadioButtons(self):
        self.radioButton_1.setAutoExclusive(False)
        self.radioButton_1.setChecked(False)
        self.radioButton_1.setAutoExclusive(True)
        self.radioButton_2.setAutoExclusive(False)
        self.radioButton_2.setChecked(False)
        self.radioButton_2.setAutoExclusive(True)
        self.radioButton_3.setAutoExclusive(False)
        self.radioButton_3.setChecked(False)
        self.radioButton_3.setAutoExclusive(True)
        self.radioButton_4.setAutoExclusive(False)
        self.radioButton_4.setChecked(False)
        self.radioButton_4.setAutoExclusive(True)

    def criaAtalho(self):
        if self.checkBox_atalho.isChecked():
            gravaConfigTaba("atalho", "yes")                
        else:
            gravaConfigTaba("atalho", "no")
    def importaArquivo(self):
        reply = QtGui.QMessageBox.question(self, 'Import Experiment',"The experiment to be imported must be in the ZIP format."+"\n"+"Do you want to proceed?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.label_relogio.show() 
            self.movie.start()
            arq, nomeSimples = self.escolheArquivoImporta()
            if arq > "":  
                unzipFolder(arq, "./setsExperiments")
                nome = nomeSimples.replace(".zip","")
                self.atualizaNomes()
                self.atualizaNomesDeletar()
                self.recuperaInfos()
                QtGui.QMessageBox.information(self, "Experiment Imported", "The "+nome+" was imported! "+"\n"+"To use this experiment, select it in recover.")
            self.label_relogio.hide()  
            self.movie.stop()    
    def exportaArquivo(self):
        texto = 'In the next box choose the folder with the experiment to be exported. This folder is inside the "Sets Experiments" folder.'
        texto = texto+"\n\n"+"If the experiment being exported is in progress, you must save it first so that the information is up to date."+"\n\n"+"Do you want to proceed?"
        reply = QtGui.QMessageBox.question(self, 'Export Experiment',texto, QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.label_relogio.show() 
            self.movie.start()
            arquivo, pasta = self.escolheArquivoExporta()
            if arquivo > "":  
                make_zipfile("./importExport/"+pasta+".zip", arquivo)
                caminho = arquivo.replace("setsExperiments", "importExport")
                caminho = caminho.replace(pasta,"")
                QtGui.QMessageBox.information(self, "Experiment Exported", "The "+pasta+" experiment was saved as a ZIP file in "+caminho)
            self.label_relogio.hide()  
            self.movie.stop()   
    def escolheArquivoExporta(self):
        home = "./setsExperiments"
        dir = QtGui.QFileDialog.getExistingDirectory(self,"Chose a folder experiment",home,QtGui.QFileDialog.ShowDirsOnly)
        pasta = os.path.basename(dir)
        return dir, pasta
    def escolheArquivoImporta(self):
        self.filename = QtGui.QFileDialog.getOpenFileName(parent=self, caption='Open file', directory='./importExport', filter='*.zip')
        self.nomeSimples = os.path.basename(self.filename)
        return self.filename, self.nomeSimples
    