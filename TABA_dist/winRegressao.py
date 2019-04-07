#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt4 import QtGui  # Import the PyQt4 module we'll need
from func_Gerais import pegaConfig
import interfaceRegressao
from func_Calcula import *
from func_manipulaArquivos import apagaArquivos
from func_Gerais import get_arquivosTreino, substituiSeedEmMLin, limpaPastaAdjustmentFunctions, extraiNumeros
from func_Gerais import get_listaColunas, get_listaColunasDistancia, converteStringDeltaG

class fazRegressao(QtGui.QMainWindow, interfaceRegressao.Ui_MainWindow_regressao):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.window1 = None
        self.setFixedSize(900,600)
        self.comboBox_dataBase.clear()
        self.comboBox_distance.clear()
        self.label_tempoInicio.clear()
        self.label_tempoTranscrorrido.clear()
        self.label_arquivoEmProcesso.clear()
        self.label_tempoEstimado.clear()
        self.label_seed.clear()
        self.label_distancia.setText("Cut Distance ("+chr(197)+")")
        if pegaConfig("tipoMedia").strip() == 'individual':
            self.label_tipoMedia.setText("Both sets")
        elif pegaConfig("tipoMedia").strip() == 'training':
            self.label_tipoMedia.setText("Training set")
        self.escondeLabels()
        self.checkBox_rl.setChecked(True)
        list1 = get_arquivosTreino("./outputFiles/")
        self.listDist = []
        listDb = []
        nome = pegaConfig("descricaoDataset").strip()
        quantia = pegaConfig("quantidadeProteinas").strip()
        self.label_estruturaInicial.setText(pegaConfig("quantidadeInicialProteinas").strip())
        afinidade = pegaConfig("tipoAfinidade").strip()
        afinidade = converteStringDeltaG(afinidade)
        self.label_outliers.setText(pegaConfig("outlier").strip())  
        self.label_system.setText(nome)
        self.label_afinidade.setText(afinidade)
        self.label_quantia.setText(quantia)
        for text in list1:
            numero = str(extraiNumeros(text)/10)
            textDist = numero.replace("0.0",".0")
            text = text.replace("./outputFiles/","")
            text2 = text.replace("_TE_Tre.csv","")
            text2 = text2.replace ("saida","")            
            textDB = text2.replace(textDist, "")
            textDB = textDB.replace("Todos","All") # para ficar em inglês
            if textDB not in listDb:
                self.comboBox_dataBase.addItem(textDB) # pega dbmoad,pdbbind, tex
            listDb.append(textDB)
            if textDist not in self.listDist:
                self.listDist.append(textDist)
        self.listDist.sort(key=float)
        for item in self.listDist:
            self.comboBox_distance.addItem(item) # pega ditanica
        self.comboBox_distance.setCurrentIndex(0)
        self.comboBox_dataBase.model().sort(0)
        self.comboBox_dataBase.setCurrentIndex(0)        

        #self.preencheColunas()
        get_listaColunasDistancia("./outputFiles/")
        self.setWindowTitle(self.windowTitle()+" to Experiment: "+pegaConfig("nomeExperimento").strip())
        self.movie = QtGui.QMovie("./img/gifTempo.gif")
        self.label_relogio.setMovie(self.movie)
        self.label_relogio.hide()
        self.movie.stop()
    def iniciarRegressao(self): 
        # limpa pasta adjustmentFunctions
        limpaPastaAdjustmentFunctions()
        if (self.listDist == []):
            reply = QtGui.QMessageBox.warning(self, 'Attention !!',"The files aren't prepared yet. Do the previous steps first!!!", QtGui.QMessageBox.Ok)
            pass
        metodoMarcado = False
        dist = float(self.comboBox_variaveis.currentText())
        quantEstru = int(self.label_quantia.text())
        regraOuro = quantEstru/dist
        n = quantEstru/5
        resto = (n % 1)
        maximo = str(int(round(n-resto,0)))
        mensagem = 'The ratio of structure quantity to number of variables is small.'+'\n'+'Reduce the number of variables (maximum '+maximo+').'+'\n'+'Do you want to continue anyway?'
        if regraOuro < 5:
            reply = QtGui.QMessageBox.question(self, 'Message',mensagem, QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        else:
            reply = QtGui.QMessageBox.Yes    
        if reply == QtGui.QMessageBox.No: 
            pass
        else:
            for checkbox in self.groupBox_2.findChildren(QtGui.QCheckBox):
                if checkbox.isChecked():
                    metodoMarcado = True
            if not metodoMarcado:
                reply = QtGui.QMessageBox.warning(self, 'Attention !!',"No selected method!", QtGui.QMessageBox.Ok)
                pass
            else:
                if (self.listDist == []):
                    reply = QtGui.QMessageBox.warning(self, 'Attention !!',"The files aren't prepared yet. Do the previous steps first!!!", QtGui.QMessageBox.Ok)
                    pass
                else:
                    reply = QtGui.QMessageBox.question(self, 'Message',"This operation takes some time. Do you want to proceed?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

                    if reply == QtGui.QMessageBox.Yes:
                        self.desabilitaCheckBox()
                        self.label_relogio.show()   
                        self.movie.start()             
                        apagaArquivos("./adjustmentFunctions/")
                        self.escondeLabels()
                        self.fazRegressao()
                    else:
                        pass
 
    def sair(self):        
        self.close()
        
    def fazRegressao(self):
        self.tempoInicio = datetime.now()
        self.label_tempoEstimado.setText("")
        self.label_tempoTranscrorrido.setText("")
        dist = str(self.comboBox_distance.currentText())
        seed = substituiSeedEmMLin(dist) # substitui a semente no arquivo ml.in pelo valor da semente utilizada quando gera arquivos para correlação (30/12/2017)
        self.label_tempoInicio.setText(self.tempoInicio.strftime('%H:%M:%S - %d/%b/%y'))
        mensagem ="Doing linear regression"
        self.label_seed.setText(seed)
        self.escondeBotoes()
        self.label_relogio.show()
        self.movie.start()
        self.progressBar.setValue(0)
        diretorio = "./outputFiles/"
        #parametros para alterar    
        num_col = int(self.comboBox_variaveis.currentText())+1
        base = str(self.comboBox_dataBase.currentText())
        base = base.replace("All", "Todos") # substitui para achar o nome certo do arquivo
        nomeArquivo = "saida"+base+str(dist)+"_TE_Tre.csv"
        arquivo = nomeArquivo
        #arquivo = arquivo.replace(".csv", "_TE_Tre.csv") # corrige nome do arquivo escolhido
        csv_file1 = diretorio+arquivo    # Not a scaled file    
        v1 = "Pred. Log(Ki)" 
        v2 = "N"
        v3 = "Standard deviation" 
        v4 = "R"
        v5 = "R-squared"
        v6 = "p-value1 (pearson)" # os p-value devem ter nomes diferentes # pearson
        v7 = "Adjusted R-square"
        v8 = "Spearman correlation"
        v9 = "p-value2 (Spearman)"  # os p-value devem ter nomes diferentes # spearman
        v10 = "Quality factor (Q)"
        v11 = "q-squared for LOO"
        v12 = "F-stat"
        v13 = "Chi-squared"
        v14 = "RMSE"
        cabecalho = v1+","+v2+","+v3+","+v4+","+v5+","+v6+","+v7+","+v8+","+v9+","+v10+","+v11+","+v12+","+v13+","+v14+"\n"
        metodos = []
        if self.checkBox_all.isChecked():
            metodos = ["LinearRegression","Ridge","RidgeCV","Lasso","LassoCV","ElasticNet","ElasticNetCV"]
            #metodos = ["LinearRegression","Ridge","Lasso","LassoCV","ElasticNet","ElasticNetCV"]
        if self.checkBox_rl.isChecked():
            metodos.append("LinearRegression")
        if self.checkBox_rd.isChecked():
            metodos.append("Ridge")
            
        if self.checkBox_rdcv.isChecked():
            metodos.append("RidgeCV")
            
        if self.checkBox_la.isChecked():
            metodos.append("Lasso")
        if self.checkBox_lacv.isChecked():
            metodos.append("LassoCV")
        if self.checkBox_el.isChecked():
            metodos.append("ElasticNet")
        if self.checkBox_elcv.isChecked():
            metodos.append("ElasticNetCV")                        
            
        quantidadeMetodos = len(metodos)
        cont =0
        for metodo in metodos:   
            cont = cont+1
            if metodo == "LinearRegression":
                self.label_seta_1.show()
            if metodo == "Ridge":
                self.label_seta_2.show()    
            if metodo == "RidgeCV":
                self.label_seta_3.show()
            if metodo == "Lasso":                 
                self.label_seta_4.show()
            if metodo == "LassoCV":                
                self.label_seta_5.show()
            if metodo == "ElasticNet":
                self.label_seta_6.show()   
            if metodo == "ElasticNetCV":
                self.label_seta_7.show()

            try:
                fo1 = open(csv_file1,"r") # so para verificar se existe arquivo
                fo1.close()
                mensagem =(str(csv_file1)+" "+str(metodo)+" "+str(num_col))
                self.label_arquivoEmProcesso.setText(mensagem.replace("./outputFiles/",""))
                #QtGui.QApplication.processEvents() # para não travar
                # Chama rotinas para regressao
                QtGui.QApplication.processEvents() # para não travar  tem que repetir depois
                existe = chama_calcula(csv_file1,metodo,num_col,cabecalho,diretorio, self.progressBar)
                QtGui.QApplication.processEvents() # para não travar  tem que repetir depois
                #QtGui.QApplication.processEvents() # para não travar
            except IOError:
                mensagem ="The file "+csv_file1+" not exist. Generate in the main window with 'Do File' button"
                reply = QtGui.QMessageBox.warning(self, 'Alert',mensagem,QtGui.QMessageBox.Ok)
            
            # barra progresso
            # marca metodos
            if metodo == "LinearRegression":
                self.label_linearRegression.show()
            if metodo == "Ridge":
                self.label_ridge.show()
            if metodo == "RidgeCV":
                self.label_ridgeCV.show()
            if metodo == "Lasso":  
                self.label_lasso.show()
            if metodo == "LassoCV": 
                self.label_lassoCV.show()
            if metodo == "ElasticNet":
                self.label_elasticNet.show()
            if metodo == "ElasticNetCV":
                self.label_elasticNetCV.show()
               
            tempoPassado = datetime.now() - self.tempoInicio
            tempoEstimado = (tempoPassado/cont)*quantidadeMetodos
            self.label_tempoTranscrorrido.setText(str(tempoPassado))  
            self.label_tempoEstimado.setText(str(tempoEstimado))           
        self.mostraBotoes()
        self.label_relogio.hide()
        self.movie.stop()
        if existe:
            mensagemExtra = ". This file was already generated before."
        else:
            mensagemExtra = ""
        QtGui.QMessageBox.information(self, "Message", "Operation completed"+mensagemExtra)
        self.habilitaCheckBox()
        self.escondeLabels()
    def escondeBotoes(self):
        self.toolButton_iniciar.setEnabled(False)
        self.toolButton_exit.setEnabled(False)
    def mostraBotoes(self):
        self.toolButton_iniciar.setEnabled(True)
        self.toolButton_exit.setEnabled(True)  
    def escondeLabels(self):       
        self.label_seta_1.hide()
        self.label_seta_2.hide()
        self.label_seta_3.hide()
        self.label_seta_4.hide()
        self.label_seta_5.hide()
        self.label_seta_6.hide()
        self.label_seta_7.hide()
        self.label_seta_8.hide()
        self.label_linearRegression.hide()
        self.label_ridge.hide()
        self.label_ridgeCV.hide()
        self.label_lasso.hide()
        self.label_lassoCV.hide()
        self.label_elasticNet.hide()
        self.label_elasticNetCV.hide()
        self.label_all.hide()
        
    def preencheColunas(self):   # preenche combo com colunas que ainda nao foram geradas
        self.comboBox_variaveis.clear()
        list2 = get_listaColunas("./outputFiles/")
        for x in range(2, 10):
            col = str(x)
            if not col in list2:
                self.comboBox_variaveis.addItem(col)  
    def todos(self): 
        self.escondeLabels()   
        if self.checkBox_all.isChecked():        
            self.checkBox_rl.setChecked(True)
            self.checkBox_rd.setChecked(True)
            self.checkBox_rdcv.setChecked(True)
            self.checkBox_la.setChecked(True)
            self.checkBox_lacv.setChecked(True)
            self.checkBox_el.setChecked(True)
            self.checkBox_elcv.setChecked(True)
        else:
            self.checkBox_rl.setChecked(False)
            self.checkBox_rd.setChecked(False)
            self.checkBox_rdcv.setChecked(False)
            self.checkBox_la.setChecked(False)
            self.checkBox_lacv.setChecked(False)
            self.checkBox_el.setChecked(False)
            self.checkBox_elcv.setChecked(False)          
        
    def desabilitaCheckBox(self):
        self.checkBox_rl.setEnabled(False)
        self.checkBox_rd.setEnabled(False)
        self.checkBox_rdcv.setEnabled(False)
        self.checkBox_la.setEnabled(False)
        self.checkBox_lacv.setEnabled(False)
        self.checkBox_el.setEnabled(False)
        self.checkBox_elcv.setEnabled(False)
        self.checkBox_all.setEnabled(False)
    def habilitaCheckBox(self):
        self.checkBox_rl.setEnabled(True)
        self.checkBox_rd.setEnabled(True)
        self.checkBox_rdcv.setEnabled(True)
        self.checkBox_la.setEnabled(True)
        self.checkBox_lacv.setEnabled(True)
        self.checkBox_el.setEnabled(True)
        self.checkBox_elcv.setEnabled(True)
        self.checkBox_all.setEnabled(True)
        