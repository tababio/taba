# coding=utf-8
from func_Gerais import leCsv, leCsvPulaLinha
import numpy as np
from PyQt4 import QtGui, QtCore  # Import the PyQt4 module we'll need
from func_Gerais import pegaConfig
def calculaMedia(ki):    
    if ki == "":
        ki="0"
    str1 = ki 
    #pos = str1.find('-') # para ver se e faixa
    pos = str1.find('-')
    if pos == 0: # existe - na primeira posicao
        pos = str1.find('-', str1.find('-')+1) # para ver se e faixa desconsiderando a primeira ocorrencia
    if pos>0: 
        if '--' in str1:# un dos caracteres e sinal negativo agonteceu em deltaG
            pos = str1.find('--')   
        tam = len(str1)
        a1 = ki[0:pos]
        a2 = ki[pos+1:tam]
        media = (float(a1)+float(a2))/2   
    else:
        media = float(str1)
    #print("media:",ki,media)
    return media

def calculaLog(ki):
    if ki!= 0:          
        logKi = (np.log10(ki))-9 # log 10 -9
    else:
        logKi = 0
    return logKi # como o valor e em nano molar subtrai 9   
def separaKi(arquivo): # feita correcao em 21/07/2018 pois nao estava considerando ligantes com menos de 2 catacteres
    diretorio = "./ki/" # define diretorio para pegar arquivo
    kiBDB = ""
    kiPDBbind = ""
    kiBMOAD = ""
    liganteAtivo = ""
    # separa bases na linnha
    QtGui.QApplication.processEvents() # para não travar usar antes de loops
    #############################
    arq = open(diretorio+arquivo,'r')
    first_line = arq.readline() # somente para pular cabecalho
    lista = [line.split(',') for line in arq.readlines()] # converte em lista
    for l in lista:       
        linha = l[3]
        #print(l,"--",linha)
        if ("(BDB" in linha) or ("(PDBbind" in linha) or ("(BMOAD" in linha):
            liganteAtivo = l[2].replace('"','').strip()
            kiBDB = ""
            kiPDBbind = ""
            kiBMOAD = ""            
            li = ''.join(linha)
            li = li.replace('"', '')
            a = li.replace("<","")
            b = a.replace(">","")
            c = b.split("#")
            #print(l,"--",c)
            for d in c:
                if "(BDB" in d:
                    pos = d.find("(BDB")
                    kiBDB = d[:pos]                    
                if "(PDBbind" in d:
                    pos = d.find("(PDBbind")
                    kiPDBbind = d[:pos]
                if "(BMOAD" in d:
                    pos = d.find("(BMOAD")
                    kiBMOAD = d[:pos]
    #print(arquivo,liganteAtivo, kiBDB, kiPDBbind, kiBMOAD)
    return liganteAtivo, kiBDB, kiPDBbind, kiBMOAD
'''
def separaKiOld(arquivo): # este arquivo nao esta sendo usado em 21/07/2018 pois fiz correcoes
    diretorio = "./ki/" # define diretorio para pegar arquivo
    arquivoParaLer = leCsv(diretorio+arquivo) # le arquivo com os pdbs a serem processados como proteinas   posIni = 0
    kiBDB = ""
    kiPDBbind = ""
    kiBMOAD = ""
    liganteAtivo = ""
    liganteAtivoProv = ""
    # separa bases na linnha
    QtGui.QApplication.processEvents() # para não travar usar antes de loops
    for linha in arquivoParaLer:
        tamanho = len(linha)
        if tamanho == 3 or (tamanho ==2 and linha.isdigit()): # considerando que todo o ligante tera tamanho = 3 ou 2 digitos numericos
            liganteAtivoProv = linha        
        if ("(BDB" in linha) or ("(PDBbind" in linha) or ("(BMOAD" in linha):
            kiBDB = ""
            kiPDBbind = ""
            kiBMOAD = ""
            liganteAtivo = ""
            l = linha.split(")",6)
            liganteAtivo = liganteAtivoProv # pega a linha anterior com o ligante ativo
            QtGui.QApplication.processEvents() # para não travar usar antes de loops
            for a in l:
                b = a.replace("#","")
                c = b.replace("<","")
                d = c.replace(">","")
                if "(BDB" in d:
                    pos = d.find("(")
                    kiBDB = d[:pos]                    
                elif "(PDBbind" in d:
                    pos = d.find("(")
                    kiPDBbind = d[:pos]
                elif "(BMOAD" in d:
                    pos = d.find("(")
                    kiBMOAD = d[:pos]
    #print(arquivo,liganteAtivo, kiBDB, kiPDBbind, kiBMOAD)
    return liganteAtivo, kiBDB, kiPDBbind, kiBMOAD
'''
def calculaKi(arquivo):
    liganteAtivo,kiBDB,kiPDBbind,kiBMOAD = separaKi(arquivo)
    liganteAtivo = "["+liganteAtivo+"]" #para identificar ligantes numericos
    mediaKiBDB = calculaMedia(kiBDB)
    mediaKiPDBbind = calculaMedia(kiPDBbind)
    mediaKiBMOAD = calculaMedia(kiBMOAD)
    mediaKiTodos = 0
    items = []
    if mediaKiBDB != 0: 
        items.append(mediaKiBDB)
    if mediaKiPDBbind != 0:
        items.append(mediaKiPDBbind)
    if mediaKiBMOAD != 0:
        items.append(mediaKiBMOAD)
    if len(items) > 0:
        mediaKiTodos = np.average(items) 
    if pegaConfig("tipoAfinidade").strip() == "deltaG": ## se for deltaG nao calcula o log
        return liganteAtivo, mediaKiBDB, mediaKiPDBbind, mediaKiBMOAD, mediaKiTodos
    else:
        return liganteAtivo,calculaLog(mediaKiBDB),calculaLog(mediaKiPDBbind),calculaLog(mediaKiBMOAD),calculaLog(mediaKiTodos)
