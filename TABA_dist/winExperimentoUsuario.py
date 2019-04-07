#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui# Import the PyQt4 module we'll need
import interfaceExperimentoUsuario
from func_Gerais import leCsv, grava, pegaConfig,pegaModelo, get_listaDistancias, download_PDB_file,get_Bind, temLigante, converteStringDeltaG, completaArquivoModelo
from func_AplicaEquacaoUsuario import geraExperimento, geraArquivoComTermoDeEnergiaExperimento
from func_manipulaArquivos import copiaArquivo, existeArquivo,arquivosNaPastaModels, apagaArquivo
import os
import sys
from func_SeparaLiganteProteina import separaLiganteProteina
from func_GeraArqProteinaComKi import geraArquivoProteinaFinal
from func_mediaDistanciaPorPdb import mediaDistanciaPorPdb
class experimentoUsuario(QtGui.QMainWindow, interfaceExperimentoUsuario.Ui_MainWindowExperimento):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.window1 = None
        self.setFixedSize(900,600)
        self.list1 = get_listaDistancias("./outputFiles/")
        self.modeloEscolhido = ""
        nome = pegaConfig("descricaoDataset")
        quantia = pegaConfig("quantidadeProteinas")
        self.label_estruturaInicial.setText(pegaConfig("quantidadeInicialProteinas").strip())
        self.afinidade = pegaConfig("tipoAfinidade").strip() 
        self.label_system.setText(nome)
        self.label_afinidade.setText(converteStringDeltaG(self.afinidade))
        self.label_quantia.setText(quantia)
        self.checkBox_aceitaNomeLongo.setChecked(False)
        self.carregaModelos()
        self.lineEdit_estrutura.setFocus()
        if pegaConfig("tipoMedia").strip() == 'individual':
            self.label_tipoMedia.setText("Both sets")
        elif pegaConfig("tipoMedia").strip() == 'training':
            self.label_tipoMedia.setText("Training set")
        self.label_outliers.setText(pegaConfig("outlier").strip())  
        self.label_logTeorico.clear()
        self.label_relogio.hide()
        self.inibidor = pegaConfig("tipoAfinidade").strip()
        if self.inibidor == "": # erro ao achar um inibidor
            reply = QtGui.QMessageBox.question(self, 'Message',"This PDB file was not downloaded yet. Please, do this first using 'Download' button in the main window.", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            if reply == QtGui.QMessageBox.Ok:
                self.sair()
        self.setWindowTitle(self.windowTitle()+" to Experiment: "+pegaConfig("nomeExperimento").strip())
        self.movie = QtGui.QMovie("./img/gifTempo.gif")
        self.label_relogio.setMovie(self.movie)
        self.movie.stop()
    def experimentar(self):
        diretorio = "./outputFiles/"
        arq = "SF.csv"
        if not (existeArquivo(diretorio+arq)):
            reply = QtGui.QMessageBox.warning(self, 'Attention !!',"The files aren't prepared yet. Do the previous steps first!!!", QtGui.QMessageBox.Ok)
            pass
        else:
            if self.modeloEscolhido: # verifica se escolheu modelo
                self.experimentarOk()
            else:
                reply = QtGui.QMessageBox.warning(self, 'Attention !!',"You must select a model first!", QtGui.QMessageBox.Ok)
                pass
    def experimentarOk(self): 
        self.progressBar.setValue(0)      
        self.label_logTeorico.clear()  
        self.inibeBotoes()
        if (self.validaPdb() == True) and (self.validaLigante() == True):  # se nao existir codigo abandona     
            self.label_relogio.show()
            self.movie.start()
            self.gravaPdb()
            self.progressBar.setValue(10)
            mensagemFinal = "Operation completed"
            if self.fazExperimento() == False: ## aplica modelo                 
                mensagem = self.textoEstrutura+"/"+self.ligante+" does not have affinity type "+self.inibidor+"."
                mensagemFinal = "Taba can not calculate the Theorical Log for this structure."
                mensagemFinal = mensagemFinal+"\n"+"\n"+"Try another structure!"
                QtGui.QMessageBox.warning(self, 'Warning!',mensagem, QtGui.QMessageBox.Ok)
                pass
            self.mostraBotoes()
            self.progressBar.setValue(100)
            self.label_relogio.hide()
            self.movie.stop()
            QtGui.QMessageBox.information(self, "Message", mensagemFinal)
            self.progressBar.setValue(0)
            self.habilitaBotoes()
        else:
            self.movie.stop()
            self.label_relogio.hide()
            self.progressBar.setValue(0)
            self.habilitaBotoes()
            pass   
        
    def sair(self):        
        self.close()
        
            
    def fazExperimento(self):
        logText = "The theoretical log "+ self.inibidor +" for:"
        self.label_log.setText(logText)
        diretorio = "./inputFiles/" # define diretorio para salvar o download
        self.ligante = self.lineEdit_Ligante.text().upper().strip()
        self.chamaRotinasPreparacao(diretorio, self.ligante) # chama runcoes para preparar arquivos para processamento
        arquivosParaLerUsu = leCsv(diretorio+"pdbsProteinaUsu.txt") # le arquivo com os pdbs a serem processados como proteinas. Este arquvivo so contem pdbs que tem arquivo de KI correspondente
        arqModelo = self.modeloEscolhido
        if temLigante("./pdbs/", arquivosParaLerUsu) == False:
            reply = QtGui.QMessageBox.question(self, 'Message',"The estructure to experiment don't have the ligand "+self.ligante,QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            pass
        else:
            # entra o valor da distância
            distancia = float(pegaModelo(arqModelo, "distancia").strip())
            tipoMedia = pegaConfig("tipoMedia")
            mediaDistanciaPorPdb(arquivosParaLerUsu,distancia,"USU",self.progressBar) # gera arquivo com medias do conjunto treino
            diretorio, arquivo = geraArquivoComTermoDeEnergiaExperimento(arquivosParaLerUsu,distancia,"Usu",tipoMedia, self.ligante) #gera arquivo de treino
            if diretorio == "nok": # significa que nao existe o ligante
                return False
            formula = pegaModelo(arqModelo, "equacao")
            pdbNome, logKi, ki = geraExperimento("", arquivo, formula)
            logKiS = ("%.3f" % logKi)
            # vamos pegar só um valor calculado de ki pois a funcçao e utilizada tambem para conjunto teste
            logText = "The theoretical log "+ self.inibidor +" for:"
            self.label_log.setText(logText.replace("\n", "")+"\n"+pdbNome )
            self.label_logTeorico.setText(str(logKiS))
            return True
    def gravaPdb(self):
        diretorio = "./inputFiles/"
        arq = "pdbsProteinaUsu.txt"
        arquivo = diretorio+arq
        self.textoEstrutura = self.lineEdit_estrutura.text().upper().strip()
        grava(self.textoEstrutura, arquivo)
    def validaLigante(self):
        textoLigante = self.lineEdit_Ligante.text().strip()
        # valida ligante
        if len(textoLigante)<2 or len(textoLigante)>3 :
            reply = QtGui.QMessageBox.question(self, 'Message',"The value of Ligand is incorrect.", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            return False
        else:
            return True      
    def validaPdb(self):
        valida = False
        textoPdb = self.lineEdit_estrutura.text().strip() 
        if (len(textoPdb)!= 4) and (self.aceitaNomeLongo() == False): # caso o usuario queira usar qualquer tamanho de nome de PDB nao fara este teste
            reply = QtGui.QMessageBox.question(self, 'Message',"The value of PDB is incorrect."+"\n"+'Maybe you can check "Accepts Long Name" to solve this.', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            return False
        else:
            # verifica se o arquivo exite
            my_dir_in = "./pdbs/"        
            if  not self.pre_download(my_dir_in,textoPdb):                
                valida = False
            else:
                valida = True   
        if valida:
            return True
        else:
            #opção para baixar direto o PDB, mas tem que gerar arquivos para regressão
            reply = QtGui.QMessageBox.question(self, 'Message',"This pdb code has not been downloaded yet. Do you want to do this now?", QtGui.QMessageBox.Yes|QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes: # vai baixar no saite
                self.label_relogio.show()
                self.movie.start()
                my_structureId_string = textoPdb.lower()
                #pdb
                myUrl = "http://files.rcsb.org/download/" 
                
                mensagemBaixaPdb = download_PDB_file(myUrl, my_structureId_string.upper()+".pdb")
                if not ("Finishing downloading" in mensagemBaixaPdb): # se a mensagem nao conter "Finishing downloading" e por que o codigo nao existe
                    texto = "The code was not found to download on the PDB site."+"\n"+"Make sure the code name is correct!"
                    QtGui.QMessageBox.information(self, "Warning",texto)
                    return False
                my_dir_in = "./ki/"        
                binding_info = self.inibidor
                #http://www.rcsb.org/pdb/rest/customReport?pdbids=1a4l&customReportColumns=structureId,chainId,ligandId,Ki&service=wsfile&format=csv&ssa=n                
                get_Bind(my_dir_in, my_structureId_string, binding_info)
                return True
            else:
                return False
            
            reply = QtGui.QMessageBox.question(self, 'Message',"This pdb code has not been downloaded yet. Please do this first.",QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            return False
    def pre_download(self, my_dir_in,my_file_in):
        """Function to check if the file is already in the structure directory"""
        # Try to open file
        my_file_in = my_file_in.upper()+".pdb"

        try:
            my_fo = open(my_dir_in+my_file_in,"r")
            my_fo.close()
            return True 
        except:
            return False
                
    def escondeBotoes(self):
        self.toolButton_iniciar.setEnabled(False)
        self.toolButton_exit.setEnabled(False)
    def mostraBotoes(self):
        self.toolButton_iniciar.setEnabled(True)
        self.toolButton_exit.setEnabled(True)
        
    def escolheArquivo(self):
        self.filename = QtGui.QFileDialog.getOpenFileName(parent=self, caption='Open file', directory='.', filter='*.pdb')
        self.nomeSimples = os.path.basename(self.filename)
        if self.filename:
            self.importaArquivo()
    def importaArquivo(self):
        diret = "./pdbs/"  
        arquivo = self.filename
        if len(arquivo) == 0: 
            QtGui.QMessageBox.information(self, "Message", "You must choose a file to import first")
        else:          
            if existeArquivo(diret+self.nomeSimples):
                mensagem = "The file "+self.nomeSimples+" already exists. Do you want to import it to Taba anyway?"
            else:
                mensagem = "Do you want import file '"+self.nomeSimples+"' to Taba."+"\n"+"The original name will be converted to capital letters!"
            reply = QtGui.QMessageBox.question(self, 'Message',mensagem, QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                copiaArquivo(arquivo, diret)
                self.renomeiaMaiusculo(self.nomeSimples)
                self.lineEdit_estrutura.setText(self.nomeSimples.replace(".pdb","").strip().upper())
            else:
                self.lineEdit_estrutura.setText("")
                pass
            
    def carregaModelos(self):
        arquivos = arquivosNaPastaModels()
        arquivos.sort()
        model = QtGui.QStandardItemModel()
        self.listView_modelo.setModel(model)
        for i in arquivos:
            completaArquivoModelo(i) # verifica se existe arquivo modelo de versao anterior e completa valores faltantes
            item = QtGui.QStandardItem(i.replace(".txt",""))
            model.appendRow(item)
        if len(arquivos) == 0:
            item = QtGui.QStandardItem("You need at least one Model"+"\n"+ "for this analysis."+"\n"+"\n"+ 'Use the "Correlation" button'+"\n"+"in the main window for this.")
            model.appendRow(item)

    def selecionaModelo(self,index):
        self.modeloEscolhido = index.data().strip()+".txt"
        modelo = self.modeloEscolhido.replace(".txt","")
        distancia = pegaModelo(self.modeloEscolhido, "distancia")
        base = pegaModelo(self.modeloEscolhido, "base")
        coeficiente = pegaModelo(self.modeloEscolhido, "coeficiente")
        variaveis = str(int(pegaModelo(self.modeloEscolhido, "colunas"))-1)
        texto = " [Data Base: "+base+" - Distance: "+distancia+chr(197)+" - Variables: "+variaveis+" - Coefficient: "+coeficiente+"]"
        texto = texto.replace("\n","")
        self.mostraModelo()
    def aceitaNomeLongo(self):
        if self.checkBox_aceitaNomeLongo.isChecked():
            return True
        else:
            return False
    def renomeiaMaiusculo(self,arquivo):
        diret = "./pdbs/"
        novoNome = arquivo.upper()
        novoNome = novoNome.replace("PDB","pdb")        
        os.rename(diret+arquivo, diret+novoNome)
    def limpaModelo(self):
        self.plainTextEdit_modelo.clear()
    def mostraModelo(self):
        #self.carregaModelos()
        arq = self.modeloEscolhido      
        texto = pegaModelo(arq,"modelo")
        texto =texto.replace("nn","\n")
        texto =texto.replace("vv", ", ")    
        equacao = pegaModelo(self.modeloEscolhido, "equacao")    
        distancia = pegaModelo(self.modeloEscolhido, "distancia")
        base = pegaModelo(self.modeloEscolhido, "base")
        coeficiente = pegaModelo(self.modeloEscolhido, "coeficiente")
        valorCoeficiente = pegaModelo(self.modeloEscolhido, "valorCoeficiente").replace("+*+","\n")
        variaveis = str(int(pegaModelo(self.modeloEscolhido, "colunas"))-1)
        tuned = pegaModelo(self.modeloEscolhido, "tuned")
        texto2 = "# Data Base: "+base+" | Distance: "+distancia+chr(197)+" | Variables: "+variaveis+" | Coefficient: "+coeficiente
        texto2 = texto2.replace("\n","")
        texto2 = texto2+"\n"+"# Training Coefficients: "+"\n"+valorCoeficiente
        texto = texto+"\n"+texto2
        texto = texto+"# Tuned: "+tuned
        texto = texto.replace('a',chr(945)) # troca a por alpha
        texto = texto.replace('hng',chr(550)) # troca hng por amgstrons
        self.label_modelo.setText("Model: "+self.modeloEscolhido.replace(".txt",""))
        self.plainTextEdit_modelo.setPlainText(texto)

    def chamaRotinasPreparacao(self,diretorio,ligante):
        # separa PDB em 2 arquivos: proteina(Atom), ligante(Hetatm)
        self.geraArquivoKiFake(ligante)
        geraArquivoProteinaFinal(diretorio,"pdbsProteinaUsu.txt","Usu") # gera arquivo so com proteinas que tem arquivo de ki correspondente
        separaLiganteProteina(diretorio,"pdbsProteinaUsu.txt","Usu",ligante)
    
    def geraArquivoKiFake(self,ligante): # caso a proteina não tenha arquivo Ki

        arquivo = "./inputFiles/pdbsProteinaUsu.txt"
        texto = leCsv(arquivo)
        estrutura = ''.join(texto).upper()
        arq = "./ki/"+estrutura.lower()+".csv"
        self.apagaFake(arq)
        if not(existeArquivo(arq)):
            cab = "structureId"+","+"chainId"+","+"ligandId"+","+"KiFake"+"\n"
            textoInibidor =cab+'"'+estrutura+'","'+"A"+'","'+ligante+'","'"10000000(BDB)FAKE"+'"'+"\n"
            open(arq, 'a').close() # cria arquivo Ki da estrutura
            try:
                my_PDB_fo = open(arq,"w")            
                my_PDB_fo.write(textoInibidor) # grava dados fake de ki para a estrutura
                my_PDB_fo.close()
            except IOError:
                sys.exit("\nI can't file "+arq+" file!")
        else:
            pass
    def apagaFake(self,arq):
        # verifica se o arquivo ki eh fake e apaga
        lista = leCsv(arq)
        if lista:
            texto = ''.join(lista)
            if "FAKE" in texto:
                apagaArquivo(arq)
        else:
            pass
        
    def inibeBotoes(self):
        self.toolButton_iniciar.setEnabled(False)
        self.toolButton_exit.setEnabled(False)
        self.toolButton_escolhe.setEnabled(False)
    def habilitaBotoes(self):
        self.toolButton_iniciar.setEnabled(True)
        self.toolButton_exit.setEnabled(True)
        self.toolButton_escolhe.setEnabled(True)
        