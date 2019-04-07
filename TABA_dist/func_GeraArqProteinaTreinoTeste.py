# coding=utf-8
# gera uma arquivo somente com dpbs com arquivo de KI
import random
import string
import numpy.random

from func_Gerais import grava
from func_Gerais import leCsv
from PyQt4 import QtGui, QtCore  # Import the PyQt4 module we'll need

def le(arquivo):
    diretorio = "./ki/" # define diretorio para salvar o download
    arq = diretorio+arquivo
    try:
        fo = open(arq, 'r')
    except IOError:
        return "N" # nao foi encontrado arquivo de KI
    return "S"

def geraArquivoTesteTreino(diret, arquivo, seed):
    conteudo = []
    semConteudo = [] # arquivo de pdbs sem ki
    arquivoParaLer = leCsv(diret+arquivo) # le arquivo com os pdbs a serem processados como proteinas
    tamLista = len(arquivoParaLer)
    tamTreino = int(tamLista*0.7)+1 # pega 70% para treino  
    random.seed(seed)  
    lista_aleatoria = random.sample(range(0,tamLista), tamTreino)
    #lista_aleatoria = numpy.random.seed()(range(0,tamLista), tamTreino,100)
    listaTreino = []
    listaTeste = []
    x = 0
    QtGui.QApplication.processEvents() # para não travar usar antes de loops   
    for prot in arquivoParaLer:
        if x in lista_aleatoria:
            listaTreino.append(prot)
        else:
            listaTeste.append(prot)
        x+=1 # acresce posição
    textoTreino = ', '.join(listaTreino)
    textoTeste = ', '.join(listaTeste)
    grava(textoTreino, diret+"pdbsProteinaTreino.txt")
    grava(textoTeste, diret+"pdbsProteinaTeste.txt")
     
