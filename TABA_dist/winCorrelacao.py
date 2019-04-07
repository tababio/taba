#!/usr/bin/env python3
# coding=utf-8
import sys

from PyQt4 import QtGui  # Import the PyQt4 module we'll need
import interfaceCorrelacao
from func_Gerais import get_arquivosSf, get_listaColunasDistancia,converteStringDeltaG, completaArquivoModelo, leCsv
from func_calculaCorrelacao import correlation_coefficient2 
from func_TestaEquacao import geraCalculoPelaFormula
from func_MelhorEquacao import melhor
from func_Gerais import grava, pegaConfig, gravaConfig, extraiNumero, extraiNumeros, pegaModelo, pegaPosicaoExpPred
from func_manipulaArquivos import arquivosNaPastaModels, apagaArquivo, copiaArquivoNovoNome
import csv
from func_Tuning import tuning

from func_TestaEquacao import pegaMediaPdb
#from sklearn.linear_model.tests.test_ransac import outliers
import winOutliers, winGraficos, winCaixaTexto
class fazCorrelacao(QtGui.QMainWindow, interfaceCorrelacao.Ui_MainWindow_correlacao):
    def __init__(self, parent = None):
        diret = "./outputFiles/"
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setFixedSize(1000,670)
        self.window1 = None
        self.window10 = None
        self.window11 = None # graficos
        self.window12 = None # caixa texto
        self.window0 = None
        self.melhorArquivo = None
        self.melhorCoeficiente = None
        self.limpaCampos()
        self.desabilitaSetas()
        self.carregaModelos()
        self.comboBox_dataBase.clear()
        self.toolButton_outlier.setEnabled(False)
        self.pushButton_deleta.setEnabled(True)
        self.pushButton_adiciona.setEnabled(False)
        self.toolButton_graficos.setEnabled(False)
        self.label_nomeModelo.setText("")
        self.percentualReducaoTreino = 0
        self.percentualReducaoTeste = 0
        self.fineTuning = False
        self.tuned = False
        self.label_tuned.hide()
        distancia = "" 
        list1 = get_arquivosSf(diret,distancia)# manda a distancia nula pois interessa todas
        self.listDist = []
        listDb = []     
        nome = pegaConfig("descricaoDataset").strip()
        self.label_estruturaInicial.setText(pegaConfig("quantidadeInicialProteinas").strip())
        quantia = pegaConfig("quantidadeProteinas").strip()
        if quantia !=None:
            quantia = quantia.strip()
        afinidade = pegaConfig("tipoAfinidade").strip()
        afinidade = converteStringDeltaG(afinidade)
        self.label_system.setText(nome)
        self.label_afinidade.setText(afinidade)
        self.label_quantia.setText(quantia)
        if pegaConfig("tipoMedia").strip() == 'individual':
            self.label_tipoMedia.setText("Both sets")
        elif pegaConfig("tipoMedia").strip() == 'training':
            self.label_tipoMedia.setText("Training set")
        self.label_outliers.setText(pegaConfig("outlier").strip())  
       
        for text in list1: #pega variaveis arquivos
            if text.find("SF_") > -1:
                tam = text.find("_TE_Tre")
                text = (text[:tam])
                text = text.replace("./outputFiles/","")
                text = text.replace ("saida","")
                text = text.replace ("_saidaBMOAD","")
                text = text.replace ("_saidaTodos","")
                text = text.replace ("_saidaPDBbind","")
                text = text.replace ("_saidaTodos","")
                text = text.replace ("SF_","")
                textDist = str(extraiNumeros(text)/10)
                textDB = text.replace(textDist, "")
                textDB = textDB.replace("Todos","All") # para ficar em inglês
                if textDB not in listDb:
                    self.comboBox_dataBase.addItem(textDB) # pega dbmoad,pdbbind, tex
                   
                listDb.append(textDB)
                self.listDist.append(textDist)  
        list3 = get_listaColunasDistancia("./outputFiles/")
       
        for text in list3:
            self.comboBox_distCol.addItem(text)        
        self.comboBox_dataBase.model().sort(0)
        self.comboBox_distCol.model().sort(0)
        self.comboBox_distCol.setCurrentIndex(0)
        tam = self.comboBox_dataBase.count()
        self.comboBox_dataBase.setCurrentIndex(0) 
        self.setWindowTitle(self.windowTitle()+": "+pegaConfig("nomeExperimento").strip())
    def iniciarCorrelacao(self):
        if self.fineTuning:
            self.label_tuned.show()
        else:
            self.label_tuned.hide()
            
        if self.listDist == []:
            QtGui.QMessageBox.warning(self, 'Attention !!',"The files aren't prepared yet. Do the previous steps first!!!", QtGui.QMessageBox.Ok)
            pass
        else:
            self.iniciarCorrelacaoOK()
            alfa, atom = self.pegaElementosMelhorEquacao()
            media = self.pegaMedias(atom)
            self.plainTextEdit_modelo.setPlainText(self.criaTextoModelo(alfa, media))
   
    def iniciarCorrelacaoOK(self):         
        self.diretorio = "./outputFiles/"
        texto = self.comboBox_distCol.currentText()
        texto = texto.replace("and", "#")
        lista = texto.split("#")
        dist = str(extraiNumeros(lista[0])/10)
        dist = dist.replace("0.0",".0")
        col = str(int(extraiNumeros(lista[1])))
        col = col.replace("0.0","")
        self.dist = dist
        self.col = col
        self.num_col = int(self.col)+1 #  soma 1 para incluir constante
        self.base = str(self.comboBox_dataBase.currentText())
        self.base = self.base.replace("All", "Todos") # substitui para achar o nome certo do arquivo
        self.arquivo = "saida"+self.base+self.dist
        self.label_nomeModelo.setText("")
        self.percentualReducaoTreino = 0 # zera redutor para elementos do grafico
        self.percentualReducaoTeste = 0 # zera redutor para elementos do grafico
        #self.arquivo = self.arquivo.replace(".csv", "_TE_Tre.csv") # corrige nome do arquivo escolhido
        self.metodos = ["LinearRegression","Ridge","RidgeCV","Lasso","LassoCV","ElasticNet","ElasticNetCV"]
        # verifica se existem os arquivos
        #SF_saidaTodos4.5_TE_Tre_ElasticNet_3cols
      
        existe = True
        listaArq = []

        for metodo in self.metodos:
            arq = self.diretorio+"SF_"+self.arquivo+"_TE_Tre_"+metodo+"_"+str(self.num_col)+"cols.csv"
            if not self.existeArquivo(arq):                
                existe = False
            else:
                listaArq.append(arq) # cria lista de arquivos SF para fazer a correlacao
        if len(listaArq)>0: # deve existir pelo mneos um arquivo SF no caso o linear regression
            existe = True
        ###################################    
        if existe: # so executa se o arquvio existir
            if self.radioButton_r1.isChecked():
                self.coef = "R"
            if self.radioButton_r2.isChecked():
                self.coef = "R"+chr(178)
            if self.radioButton_sp.isChecked():
                self.coef = "Spearman"  
                
            if self.radioButton_pvs.isChecked():
                self.coef = "p-value Spearman"    
            if self.radioButton_pvp.isChecked():
                self.coef = "p-value Pearson" 
            if self.radioButton_sd.isChecked():
                self.coef = "Standard Deviation"
            if self.radioButton_rmse.isChecked():
                self.coef = "RMSE" 
            
            self.fazCorrelacao(listaArq)            
            self.label_caracteristica = (self.col+" variables and "+ self.dist+chr(197)+" using "+self.coef)
            if self.fineTuning:
                self.label_tuned.hide()
                self.tuned = True
            else:
                self.fineTuning = True
                self.toolButton_tuning.setEnabled(True)
                self.tuned = False
        else:
            QtGui.QMessageBox.information(self,"Error", "File not found. Verify if you do linear regression with this variables")
            pass

    def sair(self):        
        self.close()
        
    def fazCorrelacao(self,listaArq):       
        self.escondeBotoes() 
        if self.fineTuning:
            self.testaEquacao()   
            self.calculaCorelacaoTeste() 
            self.calculaCorelacaoTreino()  
        elif fazCorrelacao.melhorEquacao(self,listaArq) == True: # prestar atencao como chamear o mettodo
            self.testaEquacao()       
            self.calculaCorelacaoTeste() 
            self.calculaCorelacaoTreino()   
        else:
            pass
        self.mostraBotoes()
        if not (pegaConfig("outlier").strip() ==  "yes"):
            self.toolButton_outlier.setEnabled(True)
        else:
            self.toolButton_outlier.setEnabled(False)
        self.pushButton_adiciona.setEnabled(True)
    def testaEquacao(self):
        diretorio = "./outputFiles/"
        arquivo = diretorio+"melhorEquacao.csv"
   
        try:
            fo = open(arquivo, 'r')
        except IOError:
            sys.exit ("\n the file "+arquivo+" was not found!")
        for line in fo:
            linha = line.split(",")
            if "[melhor Equacao]" in linha:
                self.formula = linha[1]
        #arquivo = str(self.comboBox_arquivos.currentText()) 
        base = str(self.comboBox_dataBase.currentText())
        base = base.replace("All", "Todos") # substitui para achar o nome certo do arquivo
        arquivo = "saida"+base+str(self.dist)+"_TE_Tre.csv"
        #arquivo = arquivo.replace(".csv", "_TE_Tes.csv") # corrige nome do arquivo escolhido
        diretorio = "./outputFiles/"
        tipo = "Tre"
        geraCalculoPelaFormula(diretorio, arquivo, self.formula, tipo) # utilizando arquivo treino
        tipo = "Tes"
        geraCalculoPelaFormula(diretorio, arquivo, self.formula, tipo) # utilizando arquivo teste
        fo.close()
    def calculaCorelacaoTeste(self):     # calcula correlacao para conjunto teste
        diretorio = "./outputFiles/"
        arq = diretorio+"resultadoTeste.csv"
        '''
        06/11/2018 -> conferi o calculo dos resultados de treino e estah sendo feito certo
        '''

        lista1 = []
        lista2 = []
        posPre,posExp = pegaPosicaoExpPred()
        try:
            fo = open(arq, 'r')
        except IOError:
            sys.exit ("\n the file "+arq+" was not found!!")

        try:
            fo.readline() # para pular primeira linha
            for line in fo: # percorre arquivo de teste
                
                linha = line.split(",")
                lista1.append(float(linha[posPre])) # previsto
                lista2.append(float(linha[posExp].replace("\n",''))) # experimental
        except:
            pass
        correlacaoSpearman,pValueSpearman,coeficienteCorrelacaoPerson,pValuePerson,r, r2, rmse, std_deviation = correlation_coefficient2(lista1,lista2)
        if abs(std_deviation) < 0.000000000001:
            QtGui.QMessageBox.information(self,"Information", "It is not possible to calculate correlations to Test Set")
            self.limpaModelo()
            pass
        else:
            self.label_bestSpearmanTeste.setText(str("%6.5f"%correlacaoSpearman))
            self.label_RTeste.setText(str("%6.5f"%coeficienteCorrelacaoPerson))
            self.label_pValueSpearmanTeste.setText(str("%6.5f"%pValueSpearman))
            self.label_pValuePerson.setText(str("%6.5f"%pValuePerson))
            self.label_R2Teste.setText(str("%6.5f"%r2))
            self.label_rmse.setText(str("%6.5f"%rmse))
            self.label_stdDev.setText(str("%6.5f"%std_deviation))
            # coloca setas
            if (abs(correlacaoSpearman)>0.5):
                self.label_setaSC.setPixmap(QtGui.QPixmap("img/setaCima.png"))
                self.label_setaSC.setToolTip("Good result!")
            else:
                self.label_setaSC.setPixmap(QtGui.QPixmap("img/setaBaixo.png"))
                self.label_setaSC.setToolTip( "Bad result!")
            
            if (abs(coeficienteCorrelacaoPerson)>0.5):
                self.label_setaPC.setPixmap(QtGui.QPixmap("img/setaCima.png"))
                self.label_setaPC.setToolTip("Good result!")
            else:
                self.label_setaPC.setPixmap(QtGui.QPixmap("img/setaBaixo.png"))
                self.label_setaPC.setToolTip( "Bad result!")
                
            if (abs(pValueSpearman)<0.05):
                self.label_setaPVS.setPixmap(QtGui.QPixmap("img/setaCima.png"))
                self.label_setaPVS.setToolTip("Good result!")
            else:
                self.label_setaPVS.setPixmap(QtGui.QPixmap("img/setaBaixo.png"))
                self.label_setaPVS.setToolTip( "Bad result!")
                
            if (abs(pValuePerson)<0.05):
                self.label_setaPVP.setPixmap(QtGui.QPixmap("img/setaCima.png"))
                self.label_setaPVP.setToolTip("Good result!")
            else:
                self.label_setaPVP.setPixmap(QtGui.QPixmap("img/setaBaixo.png"))
                self.label_setaPVP.setToolTip("Bad result!")
        fo.close()            
    def calculaCorelacaoTreino(self):     # calcula correlacao para conjunto treino   

        diretorio = "./outputFiles/"
        arq = diretorio+"resultadoTreino.csv" # so para teste
        '''
        06/11/2018 -> conferi o calculo dos resultados de treino e esta sendo feito certo
        '''

        lista1 = []
        lista2 = []
        posPre,posExp = pegaPosicaoExpPred()
        try:
            fo = open(arq, 'r')
        except IOError:
            sys.exit ("\n the file "+arq+" was not found!!")

        try:
            fo.readline() # para pular primeira linha
            for line in fo: # percorre arquivo de treino
                linha = line.split(",")
                lista1.append(float(linha[posPre])) # previsto
                lista2.append(float(linha[posExp].replace("\n",''))) # experimental
        except:
            pass
        correlacaoSpearman,pValueSpearman,coeficienteCorrelacaoPerson,pValuePerson,r, r2, rmse, std_deviation = correlation_coefficient2(lista1,lista2)
        if abs(std_deviation) < 0.000000000001: # se o desvio for muito pequeno os calculos serao incorretos
            QtGui.QMessageBox.information(self,"Information", "It is not possible to calculate correlations to Training Set")
            self.limpaModelo()
            pass
        else:
            self.label_bestSpearmanTreino.setText(str("%6.5f"%correlacaoSpearman))
            self.label_RTreino.setText(str("%6.5f"%coeficienteCorrelacaoPerson))
            self.label_pValueSpearmanTreino.setText(str("%6.5f"%pValueSpearman))
            self.label_pValuePersonTreino.setText(str("%6.5f"%pValuePerson))
            self.label_R2Treino.setText(str("%6.5f"%r2))
            self.label_rmseTreino.setText(str("%6.5f"%rmse))
            self.label_stdDevTreino.setText(str("%6.5f"%std_deviation))
                        # coloca setas
            if (abs(correlacaoSpearman)>0.5):
                self.label_setaSCTreino.setPixmap(QtGui.QPixmap("img/setaCima.png"))
                self.label_setaSCTreino.setToolTip("Good result!")
            else:
                self.label_setaSCTreino.setPixmap(QtGui.QPixmap("img/setaBaixo.png"))
                self.label_setaSCTreino.setToolTip( "Bad result!")
            
            if (abs(coeficienteCorrelacaoPerson)>0.5):
                self.label_setaPCTreino.setPixmap(QtGui.QPixmap("img/setaCima.png"))
                self.label_setaPCTreino.setToolTip("Good result!")
            else:
                self.label_setaPCTreino.setPixmap(QtGui.QPixmap("img/setaBaixo.png"))
                self.label_setaPCTreino.setToolTip( "Bad result!")
                
            if (abs(pValueSpearman)<0.05):
                self.label_setaPVSTreino.setPixmap(QtGui.QPixmap("img/setaCima.png"))
                self.label_setaPVSTreino.setToolTip("Good result!")
            else:
                self.label_setaPVSTreino.setPixmap(QtGui.QPixmap("img/setaBaixo.png"))
                self.label_setaPVSTreino.setToolTip( "Bad result!")
                
            if (abs(pValuePerson)<0.05):
                self.label_setaPVPTreino.setPixmap(QtGui.QPixmap("img/setaCima.png"))
                self.label_setaPVPTreino.setToolTip("Good result!")
            else:
                self.label_setaPVPTreino.setPixmap(QtGui.QPixmap("img/setaBaixo.png"))
                self.label_setaPVPTreino.setToolTip("Bad result!") 
        fo.close()
    def melhorEquacao(self,listaArq):
        if self.fineTuning: #se o fine tuning está marcado nao faz nada"
            return True
        diretorio = "./outputFiles/"
        self.escondeBotoes()      
        retorno = 0
        valorPartida = 0
        peloMenor = True # define se o melhor coeficiente é o menor valor (pvs,pvp,sd, rmse) ou o maior valor (r1,r2,sp)
        # define coeficiente para comparar a melhor equação 
        if self.radioButton_r1.isChecked():
            self.coeficiente = "r1"
            peloMenor = False
        if self.radioButton_r2.isChecked():
            self.coeficiente = "r2"
            peloMenor = False
        if self.radioButton_sp.isChecked():
            self.coeficiente = "sp"
            peloMenor = False             
        if self.radioButton_pvs.isChecked():
            self.coeficiente = "pvs"
            peloMenor = True 
        if self.radioButton_pvp.isChecked():
            self.coeficiente = "pvp"
            peloMenor = True
        if self.radioButton_sd.isChecked():
            self.coeficiente = "sd"
            peloMenor = True
        if self.radioButton_rmse.isChecked():
            self.coeficiente = "rmse"
            peloMenor = True                         
        if peloMenor: # se procura o menor valor
            retorno = 9999999
            valorPartida = 9999999 # para verificar se houve retorno de algum valor
        for arq in listaArq:
            QtGui.QApplication.processEvents() # para não travar
            coef, pv2, melhorEq = melhor(arq, self.coeficiente, peloMenor, self.dist)
            if peloMenor:
                if coef < float(retorno):
                    retorno = coef
                    self.melhorEquacao = melhorEq
                    melhorArquivo = arq
                    pv2Melhor = pv2

            else:
                if coef > float(retorno):
                    retorno = coef
                    self.melhorEquacao = melhorEq
                    melhorArquivo = arq
                    pv2Melhor = pv2

        if retorno == valorPartida:
            mensagem1 = "There is no information for your selection."
            mensagem2 = "Some times, linear regression not generate data for the chosen experiment configuration: Experiments with a number of variables greater than 6, where the number of structures is small, may not generate linear regression results."
            mensagem3 = "Try others configurations for this experiment!"
            mensagem = mensagem1+"\n"+"\n"+mensagem2+"\n"+"\n"+mensagem3
            QtGui.QMessageBox.information(self, "Attention!", mensagem)
            return False
        else:
            if self.coeficiente == "sp":
                self.coefStr = "Spearman"
            elif self.coeficiente == "r1":
                self.coefStr = "R"
            elif self.coeficiente == "r2":
                self.coefStr = "R2"
            elif self.coeficiente == "pvs":
                self.coefStr = "p-value Spearman"
            elif self.coeficiente == "pvp":
                self.coefStr = "p-value Pearson"
            elif self.coeficiente == "sd":
                self.coefStr = "Standard Deviation"
            elif self.coeficiente == "rmse":
                self.coefStr = "RMSE"
            
            self.melhor = self.melhorEquacao
            self.melhorArquivo = (melhorArquivo.replace("./outputFiles/",""))
            coef = ("Best "+self.coefStr)
            self.melhorCoeficiente = str(retorno)       
            texto = "[melhor Coeficiente("+self.coefStr+")]"+","+str(retorno)+"\n"+"[melhor Equacao]"+","+self.melhorEquacao+"\n"+"[melhor Arquivo]"+","+self.melhorArquivo
            grava(texto, diretorio+"melhorEquacao.csv")
        self.mostraBotoes()
        self.salvaConfig()        
        return True
                     
    def escondeBotoes(self):
        self.toolButton_iniciar.setEnabled(False)
        self.toolButton_exit.setEnabled(False)
        self.toolButton_graficos.setEnabled(False)
    def mostraBotoes(self):
        self.toolButton_iniciar.setEnabled(True)
        self.toolButton_exit.setEnabled(True)
        self.toolButton_graficos.setEnabled(True)
    def existeArquivo(self,arq): 
        # Try to open file
        try:
            my_fo = open(arq,"r")   
            return  True
            my_fo.close()
        except:            
            return False     
        my_fo.close()
    def salvaConfig(self):
        gravaConfig("spearman", str(self.melhorCoeficiente))     
        gravaConfig("melhorEquacao", str(self.melhor.strip()))
    def medias(self):
        diret = "./outputFiles/"
        fileName = "medDist_"+str(self.dist)+"_"+"TRE"+".csv"
        file = diret+fileName
        with open(file) as f:
            data=[tuple(line) for line in csv.reader(f)]
        linha1 = data[0]
        linha2 = data[1]
        texto = "Atoms Pair |  Average Distance ("+u'\u212b'+")"+'\n'
        texto = texto+28*chr(175)+"\n"
        tam = len(linha1)
        for i in range(tam):            
            cont = i-1
            if float(linha2[cont])>0:
                lin = "  "+'{:3s}'.format(str(linha1[cont]).strip())+15*" "
                texto = texto+lin+linha2[cont]+"\n"
        texto = texto+"\n"+"Showing only averages > 0"
        f.close()
        return texto
    def pegaMedias(self,atom):
        diret = "./outputFiles/"
        fileName = "medDist_"+str(self.dist)+"_"+"TRE"+".csv"
        file = diret+fileName
        with open(file) as f:
            data=[tuple(line) for line in csv.reader(f)]
        dist = []
        list1 = list((data[0]))
        list2 = list((data[1]))
        cont = 0
        for i in list1:
            if i in atom:
                dist.append(i+" = "+list2[cont])
            cont = cont+1
        f.close()
        return dist
    
    def retiraOutliers(self): 
        distancia  = self.comboBox_distCol.currentText()[0:3].strip();
        gravaConfig("distanciaAtual", str(distancia)) # grava distancia para usar na tela outlier
        reply = QtGui.QMessageBox.question(self,"Important !!!", "This window will be closed!"+"\n"+"\n"+"Do you want to proceed?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            if self.window10 is None:
                self.close() # fecha janela correlacao
                self.window10 = winOutliers.outliers(self)
                self.window10.show()
                self.window10 = None  
            else:
                pass
        else:
            pass
    def geraGraficos(self): 
        if self.window11 is None:
            #self.close() # fecha janela correlacao
            self.window11 = winGraficos.graficos(self)
            self.window11.show()
            self.window11 = None  
        else:
            pass
    def pegaElementosMelhorEquacao(self):
        eq = pegaConfig("melhorEquacao")
        eq = eq.replace("-",",-")
        eq = eq.replace("+",",+")
        eq = eq.replace("\n","")
        eq = eq.replace(",","",1) #retira a primeira virgula
        lista = eq.split(',')
        alfa = []
        alfa.append(lista[0])
        atom = []
        for i in lista[1:]:
            e = i.split('*')
            alfa.append(e[0])
            at= e[1]
            at = at.replace("(","")
            at = at.replace(")","")
            atom.append(at)
        return alfa, atom
    def criaTextoModelo(self,alfa, media):
        a = chr(945) # codigo para alfa
        hng = chr(550) # codigo para amgstrons
        #a = 'a'
        #a = u'\u03B1'
        #d = u'\u03B4'
        texto = ""
        x = 0
        for i in alfa:
            texto = texto+a+str(x)+" = "+i.replace("+","")+", " # deve usar | para pegar o modelo depos
            x = x+1
        texto = texto[:-2] # retira última virgula e espaco
        texto = texto+"\n"+"\n"
        for i in media:
            texto = texto+"d"+"0 "+i+" "+hng+"\n"
        texto = texto[:-1] # retira ultima mudanca de linha \n
        texto = texto +"\n"+"Best file: "+self.melhorArquivo
        texto = texto +"\n"+"Best equation: "+self.formula
        return texto
    def salvaModelo(self):
        if self.plainTextEdit_modelo.toPlainText().strip() == "":
            QtGui.QMessageBox.warning(self, 'Attention !!',"You must generate a model first ", QtGui.QMessageBox.Ok)
            pass
        else:
            self.salvaModeloOk()
    def salvaModeloOk(self):
        diret = "./models/"
        prefix = "_model"
        nomeComplementar = ''
        self.noe = ''
        arquivo = self.arquivo.strip()
        distancia = self.dist
        base0 = self.base.strip()
        base = base0.replace("Todos", "All")
        coeficiente = self.coefStr.strip()
        equacao = self.formula.strip()        
        colunas = str(int(self.col)+1)
        valorCoeficiente = str(self.melhorCoeficiente)
        melhorArquivo = self.melhorArquivo
        nomeInterno = arquivo+"_"+coeficiente+"_col"+colunas+"_"+melhorArquivo        
        mensagem = "Guive a name for this model!"
        nome, ok = QtGui.QInputDialog.getText(self, 'Additional Name to Model', mensagem)
        nomeExistente = (self.verificaRepetido(nome))
        if nomeExistente:
            QtGui.QMessageBox.warning(self, 'Attention !!',"This model has already been saved with the name: "+nomeExistente.replace(".txt",""), QtGui.QMessageBox.Ok)
            self.pushButton_adiciona.setEnabled(False)
            pass
        if ok:
            if nome == "":
                nome ="Taba"
            nomeComplementar = (str(nome.strip()))
            caixaTexto = self.plainTextEdit_modelo.toPlainText().replace("\n", "nn") # para recuperar corretamente depois
            caixaTexto = caixaTexto.replace(", ", "vv") # para recuperar corretamente depois
            caixaTexto = caixaTexto.replace(chr(945),"a") # troca alpha poar a
            caixaTexto = caixaTexto.replace(chr(550),"hng") # troca hngmgstrons poar hng
            textoCoeficientesCalculados = self.pegaCoeficientesCalculados()
            texto =  "<nomeInterno>,"+nomeInterno+"\n"+"<melhorArquivo>,"+melhorArquivo+"\n"+"<distancia>,"+distancia+"\n"+"<colunas>,"+colunas+"\n"+  "<arquivo>,"+arquivo+"\n"+"<base>,"+base+"\n"+"<coeficiente>,"+coeficiente+"\n"+"<valorCoeficiente>,"+textoCoeficientesCalculados+"\n"+"<equacao>,"+equacao+"\n"+"<tuned>,"+str(self.tuned)+"\n"+"<modelo>,",caixaTexto
            
            arqs = arquivosNaPastaModels()
            numero = self.verificaUltimoModelo(arqs)
            numero = str(numero+1)
            self.nomeModelo = nomeComplementar+prefix+numero
            arquivoSai = diret+self.nomeModelo+".txt"
            grava(texto, arquivoSai)
            self.label_nomeModelo.setText(self.nomeModelo+" saved")
            self.carregaModelos()
            self.pushButton_deleta.setEnabled(False)
            self.pushButton_adiciona.setEnabled(False)
            self.salvaDadosModelo(self.nomeModelo)
        else:
            pass
   
            

    def verificaUltimoModelo(self,arqs):
        maior = 0
        for i in arqs:
            num = int(extraiNumero(i))
            if num >maior:
                maior = num
        return maior
    def verificaRepetido(self,nomeInterno):
        arqs = arquivosNaPastaModels()
        for i in arqs:
            nome = pegaModelo(i, "nomeInterno")
            if nomeInterno.strip() == nome.strip():
                return i
        return ""
    def deletaModelo(self):
        diret = "./models/"
        modeloMensagem = self.modeloEscolhido.replace(".txt","")
        reply = QtGui.QMessageBox.question(self, 'Message',"Do you really want to delete the "+modeloMensagem+"?",  QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            apagaArquivo(diret+self.modeloEscolhido)
            self.carregaModelos()
        else:
            pass
        # apaga arquivos com dados de afinidade do modelo
        diretDestino = "./results/"
        arqTesteDestino = diretDestino+"binding_affinity_test_set_"+modeloMensagem+".csv"
        arqTreinoDestino = diretDestino+"binding_affinity_training_set_"+modeloMensagem+".csv"
        apagaArquivo(arqTesteDestino)
        apagaArquivo(arqTreinoDestino)
        self.pushButton_deleta.setEnabled(False)
    def selecionaModelo(self,index):
        self.modeloEscolhido = index.data().strip()+".txt"
        self.pushButton_deleta.setEnabled(True)        
    def carregaModelos(self):
        arquivos = arquivosNaPastaModels()
        arquivos.sort()
        model = QtGui.QStandardItemModel()
        self.listView_modelo.setModel(model)
        for i in arquivos:
            completaArquivoModelo(i) # verifica se existe arquivo modelo de versao anterior e completa valores faltantes
            item = QtGui.QStandardItem(i.replace(".txt",""))
            model.appendRow(item)
    def limpaModelo(self):
        self.plainTextEdit_modelo.clear()
        self.toolButton_graficos.setEnabled(False)
        self.toolButton_outlier.setEnabled(False)        
        self.desabilitaSetas()
        self.limpaCampos()
        self.label_bestPvSperman2 = None
        self.label_caracteristica  = None
    def mostraModelo(self):
        self.carregaModelos()
        arq = self.modeloEscolhido  
        nomeModelo = arq.replace(".txt","")
        texto = pegaModelo(arq,"modelo")
        texto =texto.replace("nn","\n")
        texto =texto.replace("vv", ", ")        
        distancia = (pegaModelo(self.modeloEscolhido, "distancia")).replace("\n","")
        arqMelhor = (pegaModelo(self.modeloEscolhido, "melhorArquivo")).replace("\n","") 
        equacao = (pegaModelo(self.modeloEscolhido, "equacao")).replace("\n","") 
        base = (pegaModelo(self.modeloEscolhido, "base")).replace("\n","")
        coeficiente = (pegaModelo(self.modeloEscolhido, "coeficiente")).replace("\n","")
        valorCoeficiente = (pegaModelo(self.modeloEscolhido, "valorCoeficiente")).replace("+*+","\n")
        
        variaveis = str(int(pegaModelo(self.modeloEscolhido, "colunas"))-1)     
        tuned =  (pegaModelo(self.modeloEscolhido, "tuned")).replace("\n","")  
        textoInformacoes = " Data Base: "+base+"\n"+" Cut Distance: "+distancia+chr(197)+"\n"+" Variables: "+variaveis+"\n"+" Coefficient used in the evaluation : "+coeficiente+"\n"+"\n"+" Training Coefficients: "+"\n"+valorCoeficiente+"\n"+" Fine tuning: "+tuned
        complemento = "\n"+" Regression File: "+arqMelhor+"\n"+" Equation: "+equacao
        textoInformacoes = textoInformacoes+complemento
        textoModelo = texto+"\n"
        textoModelo = textoModelo.replace('a',chr(945)) # troca a por alpha
        textoModelo = textoModelo.replace('hng',chr(550)) # troca hng por amgstrons
                
        #QtGui.QMessageBox.information(self, "Model Description: "+nomeModelo, texto)
        self.caixatexto(textoModelo, textoInformacoes, nomeModelo)
        self.pushButton_deleta.setEnabled(False)
        
    def salvaDadosModelo(self,modelo):           
        diret = "./outputFiles/"
        arqTeste = diret+"resultadoTeste.csv"
        arqTreino = diret+"resultadoTreino.csv"
        diretDestino = "./results/"
        arqTesteDestino = diretDestino+"binding_affinity_test_set_"+modelo+".csv"
        arqTreinoDestino = diretDestino+"binding_affinity_training_set_"+modelo+".csv"
        mensagem = "The theoretical and binding affinity data were saved in "+arqTreinoDestino+" and "+arqTesteDestino
        copiaArquivoNovoNome(arqTeste, arqTesteDestino)
        copiaArquivoNovoNome(arqTreino, arqTreinoDestino)
        QtGui.QMessageBox.information(self,"Information", mensagem)
    def caixatexto(self, textoModelo, textoInformacoes, nomeModelo): 
        if self.window12 is None:
            diret = "./results/"
            arqTeste = diret+"binding_affinity_test_set_"+nomeModelo+".csv"
            arqTreino = diret+"binding_affinity_training_set_"+nomeModelo+".csv"
            self.window12 = winCaixaTexto.textos(self)
            self.window12.label.setText("Visualization for "+nomeModelo)
            self.window12.textBrowser_modelo.setPlainText(textoModelo)
            self.window12.textBrowser_informacoes.setPlainText(textoInformacoes)
            list = leCsv(arqTreino)
            texto = self.formataTextoCaixa(list)
            self.window12.textBrowser_treino.setPlainText(texto)
            list = leCsv(arqTeste)
            texto = self.formataTextoCaixa(list)
            self.window12.textBrowser_teste.setPlainText(texto)
            self.window12.show()
            self.window12 = None  
        else:
            pass
    '''
    def formataTextoCaixa(self, list):
        col = 0 #
        texto = ''
        tl = []
        for i in list:            
            if col > 2:
                tl.append(i+",")
                st1 = '{:5} {:4} {:10}  {:10}'.format(tl[0], tl[1], tl[2], tl[3].strip())
                texto = texto+st1+'\n'
                col = 0
                tl = []
            else:
                tl.append(i+",")
                col = col+1
        return texto
    '''
    def formataTextoCaixa(self, list):
        
        totalColunas = list.index("Predicted", )
        col = 0 #
        texto = ''
        for lin in list:
            if col > totalColunas:      
                texto = texto+lin+"\n"
                col = 0
            else:
                texto = texto+lin+","
                col = col+1
        return texto
    def desabilitaSetas(self):
        self.label_setaSC.setPixmap(QtGui.QPixmap("img/setaNula.png")) 
        self.label_setaPC.setPixmap(QtGui.QPixmap("img/setaNula.png")) 
        self.label_setaPVS.setPixmap(QtGui.QPixmap("img/setaNula.png")) 
        self.label_setaPVP.setPixmap(QtGui.QPixmap("img/setaNula.png"))
        self.label_setaSCTreino.setPixmap(QtGui.QPixmap("img/setaNula.png")) 
        self.label_setaPCTreino.setPixmap(QtGui.QPixmap("img/setaNula.png")) 
        self.label_setaPVSTreino.setPixmap(QtGui.QPixmap("img/setaNula.png")) 
        self.label_setaPVPTreino.setPixmap(QtGui.QPixmap("img/setaNula.png"))
    def limpaCampos(self):
        self.label_RTeste.clear()
        self.label_RTreino.clear()
        self.label_pValuePerson.clear()
        self.label_pValuePersonTreino.clear()
        self.label_bestSpearmanTeste.clear()
        self.label_bestSpearmanTreino.clear()
        self.label_pValueSpearmanTeste.clear()
        self.label_pValueSpearmanTreino.clear()
        self.label_R2Teste.clear()
        self.label_R2Treino.clear()
        self.label_rmse.clear()
        self.label_rmseTreino.clear()
        self.label_stdDev.clear()
        self.label_stdDevTreino.clear()
        self.toolButton_tuning.setEnabled(False)
        self.fineTuning = False
        self.label_tuned.hide()
    def ajustaModelo(self):
        #teste com codigo professor Walter
        
        if tuning():
            self.iniciarCorrelacao()
            self.label_tuned.show()
            self.toolButton_tuning.setEnabled(False)
            self.fineTuning = False
            self.tuned = True
    def pegaCoeficientesCalculados(self):
        texto = ""
        texto = "   Spearman's Correlation = "+self.label_bestSpearmanTreino.text()+"+*+"
        texto = texto+"   Pearson's Correlation (R) = "+self.label_RTreino.text()+"+*+"
        texto = texto+"   P Value for Spearman = "+self.label_pValueSpearmanTreino.text()+"+*+"
        texto = texto+"   P Value for Pearson = "+self.label_pValuePersonTreino.text()+"+*+"
        texto = texto+"   R2 = "+self.label_R2Treino.text()+"+*+"
        texto = texto+"   RMSE = "+self.label_rmseTreino.text()+"+*+"
        texto = texto+"   Standard Deviation = "+self.label_stdDevTreino.text()

        return texto
        