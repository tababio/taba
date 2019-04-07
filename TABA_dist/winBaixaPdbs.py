#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import glob
from time import sleep
from PyQt4 import QtGui,QtCore # Import the PyQt4 module we'll need
from func_Gerais import grava, leCsv, pegaConfig, gravaConfig, download_PDB_file, pre_download, get_Bind, limpaPastas, completaArquivoConfig, limpaArquivosOutput, converteStringDeltaG, limpaArquivosModelos, kiVazio, pdbVazio
import interfaceBaixaPdbs  # This file holds our MainWindow and all design related things
import func_manipulaArquivos as manip
from func_manipulaArquivos import apagaArquivos, apagaArquivo, arquivosNaPastaPdb, arquivosNaPastaKi
from func_ExcluiKiRepetidos import excluiLigantesRepetidos

class baixaPdbs(QtGui.QMainWindow, interfaceBaixaPdbs.Ui_MainWindowBaixaPdbs):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)        
        self.window1 = None
        self.setFixedSize(900,645)
        completaArquivoConfig()
        self.label_cabecalho.setText("")
        self.label_textoProgresso.setText("")
        quantia = pegaConfig("quantidadeProteinas").strip()
        self.label_estruturaInicial.setText(pegaConfig("quantidadeInicialProteinas").strip())
        if quantia != None:
            self.label_quantia.setText(quantia.strip())
        self.desabilitaCampos()
        self.toolButton_saveText.setEnabled(False)
        self.toolButton_ClearText.setEnabled(False)
        self.toolButton_baixa.setEnabled(True)
        self.toolButton_cancela.setEnabled(False)
        self.toolButton_refina.setEnabled(False) 
        self.groupBox.setEnabled(False)
        self.groupBox_2.setEnabled(False)
        self.groupBox_3.setEnabled(False)
        self.label_relogio.hide()
        self.label_experimentName.setText(pegaConfig("nomeExperimento").strip()) 
        if self.label_experimentName.text() =="":
            self.label_experimentName.setText("*** Experiment not saved yet ***")
        self.label_outliers.setText(pegaConfig("outlier").strip())  
        self.movie = QtGui.QMovie("./img/gifTempo.gif")
        self.label_relogio.setMovie(self.movie)
        self.radioButton_deltaG.setText(converteStringDeltaG('deltaG'))
        if pegaConfig("geraSets").strip() ==  "y":
            self.radioButton_trainingTest.setChecked(True)
        else:
            self.radioButton_unico.setChecked(True)
        self.carrega()
        if not (self.radioButton_trainingTest.isChecked()): # o usuário nao separou os arquivos
            self.habilitaUmaCaixaPDB()
            self.carregaUmacaixaPDB()  # carrega uma caixa pois os arquvivos teste e treino serão separados depois
        #self.setWindowTitle(self.windowTitle()+" to Experiment: "+pegaConfig("nomeExperimento"))
    def marcaAfinidade(self):
        inib = pegaConfig("tipoAfinidade").strip()
        inib = inib.replace(" ","")
        inib = inib.replace("\n","")
        if inib == "Kd":
            self.radioButton_Kd.setChecked(True)
        if inib == "Ki":
            self.radioButton_Ki.setChecked(True)
        if inib == "IC50":
            self.radioButton_IC50.setChecked(True)
        if inib == "EC50":
            self.radioButton_EC50.setChecked(True)
        if inib == "deltaG":
            self.radioButton_deltaG.setChecked(True)
    def marcaTipoMedia(self):
        
        self.med = pegaConfig("tipoMedia").strip()
        if self.med == None:
            self.med = "training"
        self.med = self.med.replace(" ","")
        self.med = self.med.replace("\n","")
        if self.med == "training":
            self.radioButton_training.setChecked(True)
        if self.med == "individual":
            self.radioButton_individual.setChecked(True)
    def marcaExluiLigantesRepetidos(self):
        excluiLigantes = pegaConfig("excluiLigantes").strip()
        if excluiLigantes == "yes":
            self.checkBox_eliminateLigand.setChecked(True)
        else:
            self.checkBox_eliminateLigand.setChecked(False)
            
    def salva(self):
        if (self.textoInicalPdb.strip() != self.plainTextEdit_pdbs.toPlainText().strip()) or (self.textoInicalPdbTestSet.strip() != self.plainTextEdit_pdbsTestSet.toPlainText().strip()):
            mensagem = 'Changing the data will erase the previous results. If you have already generated data, you must generate them again.'
            reply = QtGui.QMessageBox.question(self, 'Message',mensagem+"Do you want to proceed?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:                
                limpaArquivosOutput()
                limpaArquivosModelos()
                QtGui.QMessageBox.information(self,"Attention!", "You should download the PDB files again!")
                self.salvaOk()
            else:
                self.cancela()
        else:
            self.salvaOk()
    def salvaOk(self):
        diretorio ="./inputFiles/"
        arquivo = "pdbsProteina.txt"
        arquivoSai = diretorio+arquivo
        self.textoConfig = self.plainTextEdit_descricao.toPlainText()
        self.textoConfig = self.textoConfig.strip()        
        textoPdbTraining = self.plainTextEdit_pdbs.toPlainText()
        textoPdbTraining = textoPdbTraining.replace(" ","")
        textoPdbTraining = textoPdbTraining.replace(",,",",")# caso tenha esquecido alguma virgula
        textoPdbTraining = textoPdbTraining.upper()
        textoPdbTraining = textoPdbTraining.strip()
        self.plainTextEdit_pdbs.setPlainText(textoPdbTraining)
        if textoPdbTraining.endswith(','): # retira virgula se apos o texto
            textoPdbTraining = textoPdbTraining[:-1]
            self.plainTextEdit_pdbs.setPlainText(textoPdbTraining) 
             
        textoPdbTest = self.plainTextEdit_pdbsTestSet.toPlainText()
        textoPdbTest = textoPdbTest.replace(" ","")    
        textoPdbTest = textoPdbTest.replace(",,",",")  
        textoPdbTest = textoPdbTest.upper()
        textoPdbTest = textoPdbTest.strip()
        self.plainTextEdit_pdbsTestSet.setPlainText(textoPdbTest)

        if textoPdbTest.endswith(','): # retira virgula se apos o texto
            textoPdbTest = textoPdbTest[:-1]
            self.plainTextEdit_pdbsTestSet.setPlainText(textoPdbTest) 
        if len(textoPdbTest) > 0: # se conjunto teste existe coloca virgula
            vg = ","
        else:
            vg = ""
        if self.radioButton_trainingTest.isChecked():
            textoPdb = textoPdbTraining+vg+textoPdbTest #une os dois conjunttos
        else:
            textoPdb = textoPdbTraining 
        grava(textoPdb, arquivoSai)
        
        if self.radioButton_trainingTest.isChecked(): # o usuário separou os arquivos
            self.gravaTreinoSet(textoPdbTraining,textoPdbTest,diretorio)  
        else:
            self.habilitaUmaCaixaPDB()
            self.carregaUmacaixaPDB()  # carrea uma caixa pois os arquvivos teste e treino serão separados depois    
        lista = leCsv(arquivoSai)
        self.quantidadeProteinas = len(lista)
        self.salvaConfig()
        self.label_quantia.setText(pegaConfig("quantidadeProteinas").strip())
 
        # define tipo inibidor
        if self.radioButton_Kd.isChecked():
            self.inibidor = "Kd"
        elif self.radioButton_Ki.isChecked():
            self.inibidor = "Ki"
        elif self.radioButton_IC50.isChecked():
            self.inibidor = "IC50"
        elif self.radioButton_EC50.isChecked():
            self.inibidor = "EC50"
        elif self.radioButton_deltaG.isChecked():
            self.inibidor = "deltaG"
        gravaConfig("tipoAfinidade", self.inibidor.strip())
        #define tipo media
        if self.radioButton_training.isChecked():
            self.media = "training"
        elif self.radioButton_individual.isChecked():
            self.media = "individual"
        gravaConfig("tipoMedia", self.media.strip())
        comentarios = self.plainTextEdit_Comentarios.toPlainText()
        comentarios = comentarios.replace(",","<vg>")
        gravaConfig("comentarios", comentarios)
        completaArquivoConfig()
        self.toolButton_baixa.setEnabled(True)
        self.desabilitaCampos()
        self.toolButton_saveText.setEnabled(False)
        self.toolButton_ClearText.setEnabled(False)
        self.toolButton_baixa.setEnabled(True)
        self.toolButton_cancela.setEnabled(False) 
        self.toolButton_edita.setEnabled(True)
        self.toolButton_refina.setEnabled(False)
        self.toolButton_novo.setEnabled(True)
        self.toolButton_exit.setEnabled(True)
        # para poder desfazer
        self.textoInicalPdb = self.plainTextEdit_pdbs.toPlainText()
        self.textoInicalPdbTestSet = self.plainTextEdit_pdbsTestSet.toPlainText()
        self.textoInicialConfig = self.plainTextEdit_descricao.toPlainText()
        self.textoInicialComentarios = self.plainTextEdit_Comentarios.toPlainText()
        self.plainTextEdit_pdbs.setEnabled(False)
    def carrega(self):
        completaArquivoConfig()
        self.plainTextEdit_descricao.setPlainText(pegaConfig("descricaoDataset").strip())
        self.plainTextEdit_Comentarios.setPlainText(pegaConfig("comentarios").replace("<vg>", ","))
        self.marcaAfinidade()
        self.marcaTipoMedia()
        self.marcaExluiLigantesRepetidos()
        self.label_estruturaInicial.setText(pegaConfig("quantidadeInicialProteinas").strip())
        self.label_quantia.setText(pegaConfig("quantidadeProteinas").strip())
        if self.existePdbSeparado():
            self.habilitaDuasCaixasPDB()
            self.carregaDuasCaixasPDB()
        else:
            self.habilitaUmaCaixaPDB()
            self.carregaUmacaixaPDB()
        self.textoInicalPdb = self.plainTextEdit_pdbs.toPlainText()
        self.textoInicalPdbTestSet = self.plainTextEdit_pdbsTestSet.toPlainText()
        self.textoInicialConfig = self.plainTextEdit_descricao.toPlainText()
        self.textoInicialComentarios = self.plainTextEdit_Comentarios.toPlainText()
    def sair(self):        
        self.close()
        
    def limpaTexto(self):
        self.plainTextEdit_pdbs.clear()
        self.plainTextEdit_pdbsTestSet.clear()
        self.plainTextEdit_Comentarios.clear()
        self.plainTextEdit_descricao.clear()
    def escondeBotoes(self):
        self.toolButton_baixa.setEnabled(False)
        self.toolButton_ClearText.setEnabled(False)
        self.toolButton_saveText.setEnabled(False)
        self.toolButton_exit.setEnabled(False)
        self.plainTextEdit_pdbs.setEnabled(False)
        self.plainTextEdit_Comentarios.setEnabled(False)
        self.toolButton_edita.setEnabled(False)
        self.toolButton_cancela.setEnabled(False) 
        self.toolButton_refina.setEnabled(False) 
        self.toolButton_novo.setEnabled(False)
    def mostraBotoes(self):
        self.toolButton_baixa.setEnabled(True)
        self.toolButton_ClearText.setEnabled(True)
        self.toolButton_saveText.setEnabled(True)
        self.toolButton_exit.setEnabled(True)
        self.plainTextEdit_pdbs.setEnabled(True)
        self.plainTextEdit_Comentarios.setEnabled(True)
        self.toolButton_edita.setEnabled(True)
        self.toolButton_novo.setEnabled(True)
          
    def baixaPdb(self):
        conj =(self.plainTextEdit_pdbs.toPlainText())
        conj = conj.replace(',', ', ')
        conj = conj.replace('  ', ' ')
        list = (conj.split())
        if (len(list)) < 20:
            reply = QtGui.QMessageBox.warning(self, 'Alert',"The amount of structures is insufficient (<20) for performing experiments."+"\n"+"The download will not be performed.", QtGui.QMessageBox.Ok)
            pass
        else:
            reply = QtGui.QMessageBox.question(self, 'Download Structures',"This operation may take several minutes. Do you want to proceed?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:
                quantIni = self.label_quantia.text()
                if pegaConfig("quantidadeInicialProteinas").strip() == "null":
                    gravaConfig("quantidadeInicialProteinas", quantIni)
                    self.label_estruturaInicial.setText(quantIni)
                else:
                    pass
                self.label_relogio.show()
                self.movie.start()
                self.baixaPdbOk(self)                
            else:
                pass 
        completaArquivoConfig()
    def baixaPdbOk(self,event):
        ############ baixa PDBs ##############
        
        self.escondeBotoes()
        # Set up PDB url
        url_in = 'https://files.rcsb.org/download/'
        
        # Set up PDB access code
        nomePdbs=leCsv("./inputFiles/pdbsProteina.txt")
        totalArquivos=nomePdbs.__len__()
        varia = 100/totalArquivos
        progresso = 0
        count=0
        contaPausa = 0
        mensagem = "Starting download PDB protein files from the site "+url_in
        self.label_cabecalho.setText(mensagem)
        self.progressBar.setValue(0)
        QtGui.QApplication.processEvents() # para não travar usar antes de loops
        for linha in nomePdbs:
            pdb_access = linha.strip()
            mensagem = pdb_access
            self.label_textoProgresso.setText(mensagem)
            # Call download_PDB_file()
            count=count+1
            my_dir_in = "./pdbs/"
            flag_4_file_present = pre_download(my_dir_in,pdb_access+".pdb") #verifica se ja existe arquvio
            if not flag_4_file_present:          
                download_PDB_file(url_in,pdb_access+".pdb")
                progresso = progresso+varia
                self.progressBar.setValue(progresso)
                contaPausa = contaPausa+1
                if contaPausa > 100:
                    contaPausa = 0
                    mensagem = "---> pausa tecnica. Aguarde que o programa continuara a rodar automaticamente..."
                    self.label_textoProgresso.setText(mensagem)
                    sleep(30) # pausa para por exigencia do site se nao nao baixa todos               
    
        mensagem = str(count)+' files were correctly downloaded'
        self.label_textoProgresso.setText(mensagem)
        self.progressBar.setValue(100)
        ########## BAIXA ki ###################################
        # limpar diretorio
        self.progressBar.setValue(0)
        progresso = 0
        files = glob.glob('./ki/*')
        QtGui.QApplication.processEvents() # para não travar
        '''
        for f in files:
            os.remove(f)
        '''
        my_dir_in ="./ki/" # futuramente e melhor ajustar o nome do diretorio para abranger todos os inibidores
        # define tipo inibidor
        if self.radioButton_Kd.isChecked():
            self.inibidor = "Kd"
        elif self.radioButton_Ki.isChecked():
            self.inibidor = "Ki"
        elif self.radioButton_IC50.isChecked():
            self.inibidor = "IC50"
        elif self.radioButton_EC50.isChecked():
            self.inibidor = "EC50"
        elif self.radioButton_deltaG.isChecked():
            self.inibidor = "deltaG"
        binding_info = self.inibidor
        # Set up PDB url
        url_in = 'http://files.rcsb.org/download/'
    
        # Set up PDB access code
        nomePdbs=leCsv("./inputFiles/pdbsProteina.txt")
        totalArquivos=nomePdbs.__len__()
        count=0
        mensagem = "Starting download PDB "+binding_info+" files (constant interation):"+url_in
        self.label_cabecalho.setText(mensagem)
        QtGui.QApplication.processEvents() # para não travar usar antes de loops
        for linha in nomePdbs:
            pdb_access = linha.strip()
            mensagem = "File: "+pdb_access
            self.label_textoProgresso.setText(mensagem)
            structureId = linha.strip()
            # Call download_PDB_file()
            get_Bind(my_dir_in,structureId,binding_info)
            progresso = progresso+varia
            self.progressBar.setValue(progresso)
        ## muda cor caixa texto
        self.progressBar.setValue(100)
        self.movie.stop()
        self.label_relogio.hide()
        self.movie.stop()
        if self.checkBox_eliminateLigand.isChecked():
            excluido, quantia = excluiLigantesRepetidos()
            if  excluido == True:
                gravaConfig("excluiLigantes", "yes")
                QtGui.QMessageBox.information(self, "Message", str(quantia)+ " repeated ligands were eliminated")
                self.carrega()
            else:
                QtGui.QMessageBox.information(self, "Message", "It is not possible to exclude repeated ligands because the amount of remaining structures is insufficient to obtain satisfactory results."+"\n"+"The download was successful.")
        QtGui.QMessageBox.information(self, "Message", "Operation completed")
        ## exclui arquivos que retornaram vazios
        arqKiVazio = kiVazio()
        textoKi =','.join(arqKiVazio)
        textoKi = textoKi.replace(",", ", ")                
        arqPdbVazio = pdbVazio()
        textoPdb =','.join(arqPdbVazio)
        textoPdb = textoPdb.replace(",", ", ")
        mensagem = "The following files contain no information and have been discarded:"+"\n"+"Ki files:"+"\n"+textoKi
        mensagem = mensagem+"\n"+"PDB file:"+"\n"+textoPdb
        mensagem = mensagem+"\n"+"You must edit the PDB code boxes and delete them manually."
        if arqKiVazio or arqPdbVazio:
            QtGui.QMessageBox.information(self, "Message", mensagem)
        diret = "./ki/"
        for i in arqKiVazio:
            apagaArquivo(diret+i) # apaga arquivos ki que nao tem informação
        diret = "./pdbs/"
        for i in arqPdbVazio:            
            apagaArquivo(diret+i) # apaga arquivos pdb que nao tem informação
        
        self.mostraBotoes() 
        self.toolButton_ClearText.setEnabled(False)
        self.toolButton_saveText.setEnabled(False)
        self.progressBar.setValue(0)
        self.plainTextEdit_pdbs.setEnabled(False)
    def edita(self):
        if (pegaConfig("descricaoDataset").strip() == 'novaVersao') and (pegaConfig("comentarios").strip() == 'novaVersao'):
            QtGui.QMessageBox.information(self, "Message", "This is a new Taba installation."+"\n"+"To edit, you must first create a new experiment or retrieve an existing experiment from Manage Experiments")
            pass
        else:
            self.habilitaCampos()
            self.toolButton_saveText.setEnabled(True)
            self.toolButton_ClearText.setEnabled(True)
            self.toolButton_baixa.setEnabled(False)
            self.toolButton_cancela.setEnabled(True)
            self.toolButton_edita.setEnabled(False)
            self.toolButton_refina.setEnabled(True)
            self.toolButton_novo.setEnabled(False)
            self.toolButton_exit.setEnabled(False)
         
    def cancela(self):
        self.toolButton_baixa.setEnabled(True)
        self.desabilitaCampos()
        self.toolButton_saveText.setEnabled(False)
        self.toolButton_ClearText.setEnabled(False)
        self.toolButton_baixa.setEnabled(True)  
        self.toolButton_cancela.setEnabled(False) 
        self.toolButton_refina.setEnabled(False) 
        self.toolButton_edita.setEnabled(True)
        self.groupBox.setEnabled(False)
        self.groupBox_2.setEnabled(False)
        self.groupBox_3.setEnabled(False)
        self.toolButton_novo.setEnabled(True)
        self.toolButton_exit.setEnabled(True)
        self.plainTextEdit_pdbs.setPlainText(self.textoInicalPdb)
        self.plainTextEdit_pdbsTestSet.setPlainText(self.textoInicalPdbTestSet)
        self.plainTextEdit_Comentarios.setPlainText(self.textoInicialComentarios)
        self.plainTextEdit_descricao.setPlainText(self.textoInicialConfig)
        self.label_experimentName.setText(pegaConfig("nomeExperimento").strip()) 
        if self.label_experimentName.text() =="":
            self.label_experimentName.setText("null")
    
    def desabilitaCampos(self):
        self.plainTextEdit_pdbs.setDisabled(True)
        self.plainTextEdit_pdbsTestSet.setDisabled(True)
        self.plainTextEdit_Comentarios.setDisabled(True)
        self.groupBox.setDisabled(True)
        self.groupBox_2.setDisabled(True)
        self.groupBox_3.setDisabled(True)
        self.plainTextEdit_descricao.setDisabled(True)
        self.groupBox_PdbEntrada.setDisabled(True)
    def habilitaCampos(self):
        self.plainTextEdit_pdbs.setDisabled(False)
        self.plainTextEdit_pdbsTestSet.setDisabled(False)
        self.plainTextEdit_Comentarios.setDisabled(False)
        self.plainTextEdit_descricao.setDisabled(False)   
    def salvaConfig(self):
        gravaConfig("quantidadeProteinas", str(self.quantidadeProteinas))        
        gravaConfig("descricaoDataset",self.textoConfig)
        textoComent = self.plainTextEdit_Comentarios.toPlainText()
        #textoComent = textoComent.replace("\n","")
        gravaConfig("comentarios", textoComent)
    def retira(self):  # retira codigos repetidos   
        textoTreino = self.plainTextEdit_pdbs.toPlainText().upper()
        textoTeste = self.plainTextEdit_pdbsTestSet.toPlainText().upper()
        listaTreino = textoTreino.split(',')
        listaTeste = textoTeste.split(',')
        listaNovaTreino = []
        listaNovaTeste = []
        listaNovaTeste2 = []
        remove = False
        # cria lista limpa treino       
        for s in listaTreino:  
            if not s in listaNovaTreino:
                listaNovaTreino.append(s)                
            else:
                remove = True
        # primeira limpesa lista teste em realacoa a ela mesma
        for s in listaTeste:  
            if not s in listaNovaTeste:
                listaNovaTeste.append(s)                
            else:
                remove = True
        # limpa teste em relação a treino
        for s in listaNovaTeste:  
            if not s in listaNovaTreino:
                listaNovaTeste2.append(s)
            else:
                remove = True
        textoTreino = ','.join(listaNovaTreino)
        textoTreino = textoTreino.replace(",,",", ")
        self.plainTextEdit_pdbs.setPlainText(textoTreino) 
        
        textoTeste = ','.join(listaNovaTeste2)
        textoTeste = textoTeste.replace(",,",", ")
        self.plainTextEdit_pdbsTestSet.setPlainText(textoTeste) 
        
        if remove: # houve exclusao de estrutura entao tem que apagar arquivos antigos de sf
            # remove pastas existentes
            pasta = "./outputFiles/"
            manip.removePasta(pasta)
            # cria novas pastas
            nomePasta = "./outputFiles/"
            manip.criaPasta(nomePasta)  
            QtGui.QMessageBox.information(self, "Message", "Operation completed. Remember to save this new set.")
        else:
            QtGui.QMessageBox.information(self, "Message", "There is no repeated structure.")
        self.toolButton_refina.setEnabled(False) 

    def novo(self):         
        self.escondeBotoes() 
        self.groupBox_PdbEntrada.setDisabled(False)
        self.checkBox_eliminateLigand.setChecked(True)
        mensagem = "The current experiment will be cleaned. It's important to save it before."+"\n"    
        if (pegaConfig("descricaoDataset")).strip() =='null':
            mensagem = '' 
        reply = QtGui.QMessageBox.question(self, 'Creates a new experiment',mensagem+"Do you want to proceed?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.textoInicalPdb = ''
            self.textoInicalPdbTestSet = ''
            self.textoInicialComentarios= 'null'
            self.textoInicialConfig= 'null'
            limpaPastas()
            completaArquivoConfig()
            self.limpaTexto()
            self.label_experimentName.clear()
            self.label_quantia.setText('')
            self.label_outliers.setText('no')
            self.label_estruturaInicial.setText('')
            self.habilitaCampos()
            self.toolButton_novo.setEnabled(False)
            self.toolButton_edita.setEnabled(False)
            self.toolButton_exit.setEnabled(False)
            self.toolButton_saveText.setEnabled(True)
            self.toolButton_cancela.setEnabled(True)
            self.groupBox.setEnabled(True)
            self.groupBox_2.setEnabled(True)  
            self.groupBox_3.setEnabled(True)
            self.radioButton_training.setChecked(True)   
            self.radioButton_Ki.setChecked(True)    
            self.plainTextEdit_descricao.setPlainText('null')
            self.plainTextEdit_pdbs.insertPlainText('')
            gravaConfig("quantidadeInicialProteinas", 'null')            
            self.habilitaUmaCaixaPDB()
            self.label_experimentName.setText("*** Experiment not saved yet ***")

        else:
            self.toolButton_novo.setEnabled(True)
            self.toolButton_edita.setEnabled(True)
            self.toolButton_exit.setEnabled(True)
            self.toolButton_baixa.setEnabled(True)
            self.toolButton_saveText.setEnabled(False)
            self.toolButton_cancela.setEnabled(False)
            self.groupBox.setEnabled(False)
            self.groupBox_2.setEnabled(False)  
            self.groupBox_3.setEnabled(False)
            self.radioButton_training.setChecked(False)   
            self.radioButton_Ki.setChecked(False) 
            pass
        
    def mensagemExcluiLigante(self):
        if self.checkBox_eliminateLigand.isChecked():
            QtGui.QMessageBox.information(self, "Message", "Repeated ligands will be deleted.")
        else:
            QtGui.QMessageBox.information(self, "Message", "Repeated ligands will not be deleted.")
    def gravaTreinoSet(self,textoTreino,textoTeste,diret):
        grava(textoTreino, diret+"pdbsProteinaTreino.txt")
        grava(textoTeste, diret+"pdbsProteinaTeste.txt")
        gravaConfig("geraSets", "y")
    def insereTrainingTestSet(self):
        if self.radioButton_trainingTest.isChecked():
            reply = QtGui.QMessageBox.question(self, 'Message','Do you want to inform Training set and Test Set separated?', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                gravaConfig("geraSets", "y") #tem que vir primeiro
                self.habilitaDuasCaixasPDB()                
            else:
                self.habilitaUmaCaixaPDB()
        else:
            self.habilitaUmaCaixaPDB()
    def habilitaDuasCaixasPDB(self):
        self.plainTextEdit_pdbsTestSet.show()
        self.label_editPdbTest.show()
        self.label_editPdb.setText("PDBs to Download (Training set)")
        if pegaConfig("geraSets").strip() ==  "y":
            self.radioButton_trainingTest.setChecked(True)
            self.radioButton_unico.setChecked(False)
        else:
            self.radioButton_unico.setChecked(True)
            self.radioButton_trainingTest.setChecked(False)
        self.plainTextEdit_pdbs.setGeometry(QtCore.QRect(10, 82, 475, 85))
    def habilitaUmaCaixaPDB(self):
        self.plainTextEdit_pdbsTestSet.hide()
        self.label_editPdbTest.hide()
        self.plainTextEdit_pdbs.setGeometry(QtCore.QRect(10, 82, 815, 85))
        self.radioButton_trainingTest.setChecked(False)
        self.radioButton_unico.setChecked(True)
    def carregaDuasCaixasPDB(self):
        diret = "./inputFiles/"
        arqTreino = diret+"pdbsProteinaTreino.txt"
        arqTeste = diret+"pdbsProteinaTeste.txt"
        listaTraining = leCsv(arqTreino)
        listaTeste = leCsv(arqTeste)
        textoTraining = ', '.join(listaTraining)
        textoTeste = ', '.join(listaTeste)
        self.plainTextEdit_pdbsTestSet.setPlainText(textoTeste)
        self.plainTextEdit_pdbs.setPlainText(textoTraining)
    def carregaUmacaixaPDB(self):           
        diret = "./inputFiles/"
        arqPdb = diret+"pdbsProteina.txt"
        listaPdb = leCsv(arqPdb)
        textoPdb = ', '.join(listaPdb)
        self.plainTextEdit_pdbs.setPlainText(textoPdb)
        self.textoInicalPdb = textoPdb
    def existePdbSeparado(self):
        '''
        verifica se foi gerado o arquivo teste e training,  pois a variavel de configuracao "geraSets" pode nao estar criada ainda
        '''
        arquivo = "./inputFiles/"+"pdbsProteinaTreino.txt"
        texto =leCsv(arquivo)
        #input("Press Enter to continue...")
        if len(texto)>10:
            return True
        else:
            return False
        
    def excluiPdb(self):
        quantPdbs = len(arquivosNaPastaPdb())
        quantKis = len(arquivosNaPastaKi()) 
        reply = QtGui.QMessageBox.question(self,"Warning!", "All existing PDB and KI files will be deleted."+"\n"+"You should download them again."+"\n\n"+"Do you want to proceed?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            mensagem = str(quantPdbs)+" PDBs files and "+str(quantKis)+" KIs files were deleted: "
            apagaArquivos("./pdbs/")
            apagaArquivos("./ki/")
            QtGui.QMessageBox.information(self, "Information", mensagem)
        else:
            QtGui.QMessageBox.information(self, "Information", "The PDBs and KIs files were not deleted.")            
            pass
                         