# coding=utf-8
from func_Gerais import grava, leCsvPulaLinha
from func_TrataKi import calculaKi
from PyQt4 import QtGui  # Import the PyQt4 module we'll need

def inter_mol_term(distancia,tipo,tipoMedia):
    """Funcao para calcular o termo de energia"""
    cabecalho = "liganteAtivo"+","+"arquivo"+","+"CC"+","+"CN"+","+"CO"+","+"CS"+","+"CP"+","+"CF"+","+"CBr"+","+"CCl"+","+"CI"+","+"CAt"+","+"NN"+","+"NO"+","+"NS"+","+"NP"+","+"NF"+","+"NBr"+","+"NCl"+","+"NI"+","+"NAt"+","+"OO"+","+"OS"+","+"OP"+","+"OF"+","+"OBr"+","+"OCl"+","+"OI"+","+"OAt"+","+"SS"+","+"SP"+","+"SF"+","+"SBr"+","+"SCl"+","+"SI"+","+"SAt"+","+"Log(Ki)"+"\n"
    textoKiBDB = cabecalho
    textoKiPDBbind = cabecalho
    textoKiBMOAD = cabecalho 
    textoKiTodos = cabecalho
    #atomos = ['CC','CN','CO','CS','CP','CF','CBr','CCl','CI','CAt','NN','NO','NS','NP','NF','NBr','NCl','NI','NAt','OO','OS','OP','OF','OBr','OCl','OI','OAt','SS','SP','SF','SBr','SCl','SI','SAt']

    if tipoMedia == "TRE": # vai considera somente o conjunto treino para calcular a media
        conj = "TRE"
    else:
        conj = tipo.upper()
    diret = "./outputFiles/"
    fileNameTodos = diret+"medDist_"+str(distancia)+"_"+conj+".csv"
    foTodos = leCsvPulaLinha(fileNameTodos)
    fileNamePorPDB = diret+"medDistPdb_"+str(distancia)+"_"+tipo.upper()+".csv"
    try:
        foPdb = open(fileNamePorPDB, 'r')
    except IOError:
        print("\n O arquivo "+fileNamePorPDB+" nao foi encontrado")
        exit()
    linha = ''
    first_line = foPdb.readline() # pula primeira linha
    for i in foPdb:
        list = i.split(",")
        ind = 1
        linha = list[0]+","
        for x in foTodos:
            mediaPdb = float(list[ind])
            mediaTodos =  float(x)
            val = (mediaTodos-mediaPdb)**2 # conferir
            valStr = str(val)
            linha = linha+valStr+","
            ind = ind+1
        arquivo = list[0]
        liganteAtivo,logKiBDB,logKiPDBbind,logKiBMOAD,logKiTodos = calculaKi(arquivo.lower()+".csv")
        if logKiBDB!=0:
            textoKiBDB= textoKiBDB+liganteAtivo+","+linha+str(logKiBDB)+"\n" # so cria linha se logki for difeerente de zero
        if logKiPDBbind!=0:
            textoKiPDBbind= textoKiPDBbind+liganteAtivo+","+linha+str(logKiPDBbind)+"\n"
        if logKiBMOAD!=0:
            textoKiBMOAD= textoKiBMOAD+liganteAtivo+","+linha+str(logKiBMOAD)+"\n"
        if logKiTodos!=0:
            textoKiTodos= textoKiTodos+liganteAtivo+","+linha+str(logKiTodos)+"\n"
    diret = "./outputFiles/"
    strDist = str(distancia)
    #    ATENCAO NAO PODE GERAR LINHA ANTES E APOS O TEXTO 
    # retirei Ki do nome em 29/04/2017
    grava(textoKiBDB,diret+'saidaBDB'+strDist+'_TE_'+tipo+'.csv')
    grava(textoKiPDBbind,diret+'saidaPDBbind'+strDist+'_TE_'+tipo+'.csv')
    grava(textoKiBMOAD,diret+'saidaBMOAD'+strDist+'_TE_'+tipo+'.csv')
    grava(textoKiTodos,diret+'saidaTodos'+strDist+'_TE_'+tipo+'.csv')    

