#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt4 import QtGui  # Import the PyQt4 module we'll need
import interfaceOutliers
import csv
from func_Gerais import grava, pegaConfig, gravaConfig, leCsv, limpaArquivosOutlier, limpaPastasSaidaOutlier, get_listaColunasDistancia
from func_manipulaArquivos import apagaArquivo, apagaArquivos
import numpy as np


class outliers(QtGui.QMainWindow, interfaceOutliers.Ui_MainWindow):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setFixedSize(600,350)
        self.window7 = None
        self.horizontalSlider_percent.setValue(40)
        listCol = get_listaColunasDistancia("./outputFiles/")
        self.label_inicial.setText(pegaConfig('quantidadeProteinas').strip())
        self.label_final.setText('')
        
    def sair(self):
        self.close()
        '''
        if self.window7 is None:
            self.window7 = winCorrelacao.fazCorrelacao(self)
            QtGui.QApplication.processEvents() # para não travar
            self.window7.show()
            self.window7 = None 
        '''
       
    def outliers(self): 
         
        percent = self.horizontalSlider_percent.value()/100 # corta o que esta acima de 70% do desvio/10
        self.concatenaArquivos()
        diret = "./outputFiles/"
        arq = open(diret+"juntos.csv", 'r')
        reader = csv.reader(arq)
        allRows = [row for row in reader]
        arrEstru = []
        arrVal = []
        for x in allRows:
            if not x[0] == "PDB": # elimina linhas de cabecalho
                arrVal.append(float(x[2])) # cria lista com valores experimentais
                arrEstru.append(x[0]) # cria lista com estruturas
        elements = np.array(arrVal)
        mean = np.mean(elements, axis=0)
        listaOutliers = []
        ind = 0
        for x in arrVal:
            dif = np.abs(x-mean)
            if abs(dif/mean)>percent: # verifica se nao esta na faixa
                listaOutliers.append(arrEstru[ind].upper())
            ind = ind+1
        texto = str(listaOutliers)
        texto = texto.replace("]", '')
        texto = texto.replace("[", '')
        grava(texto.split("'"), diret+"outliers.txt")
        arq.close()
        apagaArquivo(diret+"juntos.csv")
        self.limpaArquivoProteinas()
        
    def concatenaArquivos(self):
        diret = "./outputFiles/"
        fileTreino = diret+"resultadoTreino.csv"
        fileTeste = diret+"resultadoTeste.csv"
        fileJuntos = diret+"juntos.csv"
        arq = open(fileJuntos, "w") 
        arq1 = open(fileTreino, "r")
        arq2 = open(fileTeste, "r")
        arq.write(arq1.read()+arq2.read())
        arq.close()
        arq1.close()
        arq2.close()
    def limpaArquivoProteinas(self):
        diret1 = "./outputFiles/"
        diret2 = "./inputFiles/"
        proteinas = leCsv(diret2+"pdbsProteina.txt")
        outliers = leCsv(diret1+"outliers.txt")
        listProt = []
        listOutliers = []
        listNovoProt = []
        tamInicial = (len(proteinas))
        #gravaConfig("quantidadeInicialProteinas", str(tamInicial).strip())
        
        for x in proteinas:
            listProt.append(x.strip())
        for x in outliers:
            listOutliers.append(x.strip())
            
        for x in listProt:
            if not(x in listOutliers):
                listNovoProt.append(x+",".strip())
   
        tam = len(listNovoProt)
        if tamInicial-tam < 1:
            QtGui.QMessageBox.information(self, "Message", "There are no outliers"+"\n"+"\n"+"Try to reducing the percentual value in the slider.")
            pass
        elif tam <20:
            QtGui.QMessageBox.information(self, "Message", "After this operation, the number of structures will be very small (only "+str(tam)+" structures)."+"\n"+"Is not possible exclude outliers!"+"\n"+"\n"+"Try increasing the percentage on the slider,")
            pass
        else:
            listNovoProt[tam-1] = listNovoProt[tam-1].replace(",","") # retira ultima virgula
            
            distancia  = pegaConfig("distanciaAtual").strip()
            txtOut = str(outliers).replace("'", "")
            txtOut = txtOut.replace("[", "")
            txtOut = txtOut.replace("]", "")
            txtOut = txtOut.lower()
            tracos = "-"*90
            tamOut = tamInicial-tam
            texto = "This "+str(tamOut)+" structures will be excluded:"+"\n" +tracos+"\n" + txtOut
            texto = texto+"\n"+tracos
            texto = texto+"\n" +"\n"+"These outliers are considering only experiments with distances < "+distancia+u'\u212b'
            texto = texto +"\n"+"\n" + "Do you want to proceed?"
            reply = QtGui.QMessageBox.question(self, "List of Outliers",texto,QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.toolButton_iniciar.setEnabled(False)
                self.horizontalSlider_percent.setEnabled(False)
                limpaArquivosOutlier()
                limpaPastasSaidaOutlier()
                
                grava(listNovoProt, diret2+"pdbsProteina.txt") 
                gravaConfig("outlier", "yes")
                gravaConfig ("quantidadeProteinas",str(tam) )
                self.label_inicial.setText(pegaConfig('quantidadeInicialProteinas').strip())
                self.label_final.setText(pegaConfig('quantidadeProteinas').strip())
                QtGui.QMessageBox.information(self, "Important !!!", "Operation completed"+"\n"+"\n"+'You must redo "Make File"  and "Regression" again!')
               
                
            else:
                pass
    def atualizaSlider(self):
        self.percent = self.horizontalSlider_percent.value()
        self.label_percent.setText(str(self.percent)+"%")
    '''
    def retiraOutliers(self):  
        fator = 1 # corta o que esta acima de 70% do desvio
        self.concatenaArquivos()
        diret = "./outputFiles/"
        arq = open(diret+"juntos.csv", 'r')
        reader = csv.reader(arq)
        allRows = [row for row in reader]
        arrEstru = []
        arrVal = []
        for x in allRows:
            if not x[0] == "PDB": # elimina linhas de cabecalho
                arrVal.append(float(x[2])) # cria lista com valores preditos
                arrEstru.append(x[0]) # cria lista com estruturas
        elements = np.array(arrVal)
        mean = np.mean(elements, axis=0)
        sd = np.std(elements, axis=0)
        listaOutliers = []
        ind = 0

        for x in arrVal:
            if ((x < (mean - (fator * sd))) or (x > (mean + (fator * sd)))): # verifica se nao esta na faixa
                listaOutliers.append(arrEstru[ind].upper())
            ind = ind+1
        texto = str(listaOutliers)
        texto = texto.replace("]", '')
        texto = texto.replace("[", '')
        grava(texto.split("'"), diret+"outliers.txt")
        arq.close()
        apagaArquivo(diret+"juntos.csv")
        self.limpaArquivoProteinas()
        '''
        