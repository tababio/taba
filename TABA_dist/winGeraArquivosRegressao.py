#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt4 import QtGui  # Import the PyQt4 module we'll need
from func_Gerais import grava, pegaConfig, get_listaDistancias, pastaVazia, converteStringDeltaG
import interfaceGeraArquivosRegressao
from func_ContaInterMolCalcTermo import inter_mol_term
from func_mediaDistanciaPorPdb import mediaDistanciaPorPdb
from func_mediaDistanciaTodosPdb import mediaDistanciaTodosPdb
from func_Gerais import leCsv, gravaConfig

from func_GeraArqProteinaComKi import geraArquivoProteinaFinal
from func_SeparaLiganteProteina import separaLiganteProteina
from datetime import datetime
from func_GeraArqProteinaTreinoTeste import geraArquivoTesteTreino

class geraArquivosRegressao(QtGui.QMainWindow, interfaceGeraArquivosRegressao.Ui_MainWindowGeraArquivos):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.window1 = None
        self.setFixedSize(900,500)
        self.radioButton_45.setChecked(True)
        self.label_cabecalho.setText("")
        self.label_textoProgresso.setText("")
        nome = pegaConfig("descricaoDataset").strip()
        quantia = pegaConfig("quantidadeProteinas").strip()
        afinidade = pegaConfig("tipoAfinidade").strip()
        afinidade = converteStringDeltaG(afinidade)
        self.label_distanciaUsada.setText("Cut Distances Already Used ("+chr(197)+")")
        self.groupBox.setTitle("Cut Distance ("+chr(197)+")")
        self.label_system.setText(nome)
        self.label_afinidade.setText(afinidade)
        self.label_quantia.setText(quantia)
        self.label_relogio.hide()
        self.label_distanciasUsadas.setText(self.get_distanciasUsadas())
        if pegaConfig("tipoMedia").strip() == 'individual':
            self.label_tipoMedia.setText("Both sets")
        elif pegaConfig("tipoMedia").strip() == 'training':
            self.label_tipoMedia.setText("Training set")
        self.label_outliers.setText(pegaConfig("outlier").strip())
        self.label_estruturaInicial.setText(pegaConfig("quantidadeInicialProteinas").strip())  
        self.setWindowTitle(self.windowTitle()+" to Experiment: "+pegaConfig("nomeExperimento").strip())
        self.movie = QtGui.QMovie("./img/gifTempo.gif")
        self.label_relogio.setMovie(self.movie)        

    def geraArquivosTermoEnergia(self): 
        path ="./pdbs"

        if pastaVazia(path) == True:
            reply = QtGui.QMessageBox.warning(self, 'Attention !!',"Pdbs files have not been downloaded yet", QtGui.QMessageBox.Ok)
        else:
            reply = QtGui.QMessageBox.question(self, 'Message',"This operation may take several minutes. Do you want to proceed?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:            
                self.geraArquivos()
            else:
                pass
 
    def sair(self):        
        self.close()
        
    def geraArquivos(self):
        self.escondeBotoes()
        diretorio = "./inputFiles/" # define diretorio para salvar o download
        self.chamaRotinasPreparacao(diretorio) # chama runcoes para preparar arquivos para processamento
        arquivosParaLerTes = leCsv(diretorio+"pdbsProteinaFinalTes.txt") # le arquivo com os pdbs a serem processados como proteinas. Este arquvivo so contem pdbs que tem arquivo de KI correspondente
        arquivosParaLerTre = leCsv(diretorio+"pdbsProteinaFinalTre.txt")    
        # entra o valor da distância
        # entra o valor da distância
        distancia = 4.5 # padrao
        seedNum = self.comboBox_seed.currentText()
        seed = 'seed45' # semente que sera gravada no arquivo config.csv para usar no SF
        
        if self.radioButton_35.isChecked():
            distancia = 3.5
            seed = 'seed35'
        elif self.radioButton_45.isChecked():
            distancia = 4.5
            seed = 'seed45'
        elif self.radioButton_60.isChecked():
            distancia = 6.0
            seed = 'seed60'
        elif self.radioButton_75.isChecked():
            distancia = 7.5
            seed = 'seed75'
        elif self.radioButton_90.isChecked():
            distancia = 9.0 
            seed = 'seed90'
        elif self.radioButton_120.isChecked():
            distancia = 12.0 
            seed = 'seed120'
        elif self.radioButton_150.isChecked():
            distancia = 15.0 
            seed = 'seed150'
        quantidadeArquivos = len(arquivosParaLerTes)+len(arquivosParaLerTre)
        if quantidadeArquivos <20:
            QtGui.QMessageBox.information(self, "Message", "The number of structures is very small. Use another set!")
            self.mostraBotoes()   
        else:
            self.geraArquivoMediaDistanciaPorPdb(arquivosParaLerTre,distancia,"TRE") #gera medias distancias no arquivo PDB para treino
            self.geraArquivoMediaDistanciaPorPdb(arquivosParaLerTes,distancia,"TES") #gera medias distancias no arquivo PDB para teste
            self.geraArquivoComTermoDeEnergia(arquivosParaLerTre,distancia,"Tre") #gera arquivo de treino
            self.geraArquivoComTermoDeEnergia(arquivosParaLerTes,distancia,"Tes") #gera arquivo de teste            
            self.mostraBotoes() 
            self.progressBar.setValue(0)
            self.label_cabecalho.setText('')    
            self.label_textoProgresso.setText('')     
            QtGui.QMessageBox.information(self, "Message", "Operation completed")
            self.label_distanciasUsadas.setText(self.get_distanciasUsadas())
        gravaConfig(seed, seedNum) # salva valores de seed no arquivo config para usar no SF e substituir no Mml.in
    def geraArquivoMediaDistanciaPorPdb(self,arquivosParaLer,distancia,tipo):
        if tipo == "TRE":
            complemento = "Training Set"
        elif tipo == "TES":
            complemento = "Test Set"
        self.label_textoProgresso.setText('')
        self.label_cabecalho.setText("Generating average distance for "+complemento+" from Pdb file")
        self.progressBar.setValue(0) 
        mediaDistanciaPorPdb(arquivosParaLer,distancia,tipo, self.progressBar)
        
    def geraArquivoComTermoDeEnergia(self,arquivosParaLer,distancia,tipo):        
        if tipo == "Tre":
            tipoCheio = "Training"
        elif tipo == "Tes":
            tipoCheio = "Test" 
        self.label_textoProgresso.setText('')
        self.label_cabecalho.setText("Generating average distance for "+tipoCheio+". Please wait!")
        if tipo == 'Tre':
            self.progressBar.setValue(0) 
            mediaDistanciaTodosPdb(arquivosParaLer,distancia,"TRE", self.progressBar) # gera arquivo com medias do conjunto treino
            
        elif (tipo == 'Tes') and (self.tipoMedia == "ALL"): # se for somente media treino nao entra aqui e nao calcula media teste
            self.progressBar.setValue(0) 
            mediaDistanciaTodosPdb(arquivosParaLer,distancia,"TES", self.progressBar) 
              
        now = datetime.now()
        progresso = 0
        self.label_cabecalho.setText("Generating "+tipoCheio+" Files")       
        QtGui.QApplication.processEvents() # para não travar usar antes de loops

        if pegaConfig("tipoMedia").strip() == "training":
            self.tipoMedia = 'TRE'
        else:
            self.tipoMedia = 'ALL'
        inter_mol_term(distancia,tipo,self.tipoMedia)                

          
    def chamaRotinasPreparacao(self,diretorio):
        seed = int(self.comboBox_seed.currentText())
        if not (pegaConfig("geraSets").strip() == "y"):
            geraArquivoTesteTreino(diretorio,"pdbsProteina.txt", seed)
        geraArquivoProteinaFinal(diretorio,"pdbsProteinaTreino.txt","Tre") # gera arquivo so com proteinas que tem arquivo de ki correspondente
        separaLiganteProteina(diretorio,"pdbsProteinaTreino.txt","Tre","") # separa PDB em 2 arquivos: proteina(Atom), ligante(Hetatm)
        geraArquivoProteinaFinal(diretorio,"pdbsProteinaTeste.txt","Tes") # gera arquivo so com proteinas que tem arquivo de ki correspondente
        separaLiganteProteina(diretorio,"pdbsProteinaTeste.txt","Tes","")            
    
    def escondeBotoes(self):
        self.toolButton_iniciar.setEnabled(False)
        self.toolButton_exit.setEnabled(False)
        self.label_relogio.show()
        self.movie.start()
    def mostraBotoes(self):
        self.toolButton_iniciar.setEnabled(True)
        self.toolButton_exit.setEnabled(True) 
        self.label_relogio.hide()
        self.movie.stop()
    def get_distanciasUsadas(self):
        diret = "./outputFiles/"
        list = get_listaDistancias(diret)
        #list = sorted(list)
        list.sort(key=float)
        texto = ""
        for x in list:
            texto = texto+" - "+x+str(chr(197))
        return texto[3:]
    