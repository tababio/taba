# coding=utf-8
#Usa arquivos separados para teste e aplica melhor formula

import sys
from func_Gerais import grava, leCsvPulaLinha, leCsv
from func_TrataKi import calculaKi
from func_TestaEquacao import criaListaVariaveis
from PyQt4 import QtGui  # Import the PyQt4 module we'll need
def geraArquivoComTermoDeEnergiaExperimento(arquivosParaLerUsu,distancia,tipo,tipoMedia,ligante):
    """Funcao para calcular o termo de energia"""
    cabecalho = "liganteAtivo"+","+"arquivo"+","+"CC"+","+"CN"+","+"CO"+","+"CS"+","+"CP"+","+"CF"+","+"CBr"+","+"CCl"+","+"CI"+","+"CAt"+","+"NN"+","+"NO"+","+"NS"+","+"NP"+","+"NF"+","+"NBr"+","+"NCl"+","+"NI"+","+"NAt"+","+"OO"+","+"OS"+","+"OP"+","+"OF"+","+"OBr"+","+"OCl"+","+"OI"+","+"OAt"+","+"SS"+","+"SP"+","+"SF"+","+"SBr"+","+"SCl"+","+"SI"+","+"SAt"+","+"Log(Ki)"+"\n"

    textoKiTodos = cabecalho
    #atomos = ['CC','CN','CO','CS','CP','CF','CBr','CCl','CI','CAt','NN','NO','NS','NP','NF','NBr','NCl','NI','NAt','OO','OS','OP','OF','OBr','OCl','OI','OAt','SS','SP','SF','SBr','SCl','SI','SAt']
    conj = "TRE"  
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
        listaDistMediaPdb = i.split(",")
        ind = 1
        linha = listaDistMediaPdb [0]+","
        for x in foTodos:
            mediaPdb = float(listaDistMediaPdb[ind])
            mediaTodos =  float(x)
            val = (mediaTodos-mediaPdb)**2 # conferir
            valStr = str(val)
            linha = linha+valStr+","
            ind = ind+1
        arquivo = listaDistMediaPdb [0]
        liganteAtivo,logKiBDB,logKiPDBbind,logKiBMOAD,logKiTodos = calculaKi(arquivo.lower()+".csv")
        existeLigante = verificaLigange(arquivo.lower(), ligante)
        if (logKiTodos != 0) or (existeLigante):
            textoKiTodos= textoKiTodos+liganteAtivo+","+linha+str(logKiTodos)+"\n"
    diret = "./outputFiles/"
    strDist = str(distancia)
    #    ATENCAO NAO PODE GERAR LINHA ANTES E APOS O TEXTO 
    # retirei Ki do nome em 29/04/2017
    arqSaida = diret+'saidaTodos'+strDist+'_TE_'+"Usu"+'.csv'
    grava(textoKiTodos,arqSaida) 
    existeLigante = verificaLigange(arquivo.lower(), ligante)
    if not existeLigante:        
        diret = "nok"  # para informar que nao existe o ligante
    return diret, arqSaida


def posicaoVariaveis(listaVariaveis,diretorio,arquivo): # recebe o diretorio e o arquivo SF
    arq = diretorio+arquivo
    posicao = []
    
    try:
        fo = open(arq, 'r')
    except IOError:
        sys.exit ("\n O arquivo "+arq+" nao foi encontrado")

    try:
        for line in fo:
            linha = line.split(",")
            for indice,x in enumerate(linha):
                if x in listaVariaveis:
                    posicao.append(indice)               
    except:
        pass
    fo.close()
    return posicao

def calculaExperimento(listaVariaveis,diretorio,arquivo,formula):
    arq = diretorio+arquivo
    pos = posicaoVariaveis(listaVariaveis, diretorio, arquivo) # pega posiccao dos valores das colunas das variaveis
    listaValores = []
    try:
        fo = open(arq, 'r')
    except IOError:
        sys.exit ("\n O arquivo "+arq+" nao foi encontrado")

    try:
        fo.readline() # para pular primeira linha
        for line in fo: # percorre arquivo de teste
            #print("line:",line)
            linha = line.split(",")
            pdbNome = linha[0]
            for x in pos:  # percorre lista de posicao e pega valores no arquivo de teste               
                listaValores.append(linha[x])
            n = 0
            equacao = formula
            for lin2 in listaVariaveis:  #substitui valores na equacao          
                equacao = equacao.replace(listaVariaveis[n], listaValores[n]) #substitui variavel pelo valor
                n = n+1
            #print("--------------------------equacao:", equacao)
            logKi = resolveEquacaoExperimento(equacao)
            equacao = formula   
            listaValores = []                    
              
    except:
        pass
    fo.close()
    # nao esta usando mais este calculo de ki a partir do log 17/02/2017
    #ki = (10**(logKi))+9 # para retornar o ki apartir do log10 de ki
    ki = 0
    return pdbNome,logKi,ki
    
def resolveEquacaoExperimento(equacao):
    result = eval(equacao)
    return result

def listaVariaveis(formula):
    listaVariaveis = criaListaVariaveis(formula)
    return listaVariaveis
def geraExperimento(diretorio,arquivo,formula):
    variaveis = listaVariaveis(formula)
    return calculaExperimento(variaveis,diretorio, arquivo, formula) #calcula usando os termoo de energia e gera arquivo com resultados para comparar
def verificaLigange(arq, ligante):
    # verifica se o ligante esta no arquivo KI
    diretorio = "./ki/"
    arquivo = diretorio+arq+".csv"
    fo = open(arquivo, 'r')
    for i in fo:
        if ligante in i:
            return True
    return False

