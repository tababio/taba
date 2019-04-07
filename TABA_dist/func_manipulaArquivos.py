#!/usr/bin/python
# coding=utf-8
import time
import shutil
from shutil import copyfile, copytree
#from distutils.dir_util import copy_tree
import os
from datetime import datetime

now = datetime.now()
'''
diret = glob("./*/")
print(diret[2])
'''
#copia pasta
def copiaPasta(origem,destino):
    if os.path.exists(destino):
        apagaArquivos(destino)
    if  not os.path.exists(origem):
        #print("origem nao existe1")
        print("ID_func_manipulaArquivos_01")
    else:
        copytree(origem,destino)
#criar arquivo
def criaArquivo(arquivo):
    # open(arquivo, 'w').close()

    f= open(arquivo,"w+")
    f.close()
#remover pasta
def removePasta(pasta):
    if os.path.exists(pasta):
        shutil.rmtree(pasta)

#verifica se existe arquivo
def existeArquivo(arquivo):
    if os.path.exists(arquivo):
        return True
    else:
        return False
def existePasta(pasta):
    if os.path.isdir(pasta):
        return True
    else:
        return False
#criar pasta
def criaPasta(pasta):
    if not os.path.exists(pasta):
        os.makedirs(pasta)
    else:
        #print("pasta ja existe!!!")
        print('ID_func_manipulaArquivos_02')
#copia arquivo sobrescrevendo
def copiaArquivo(arquivo, diret):
    if os.path.exists(diret):
        shutil.copy(arquivo, diret)
    else:
        #print("destino nao existe3")
        print('ID_func_manipulaArquvios_03')
def copiaArquivoNovoNome(origem, destino):
    copyfile(origem, destino)

def apagaArquivos(path): # apaga todos os arquivos de uma pasta
    diret = os.listdir(path)
    for file in diret:
        try:
            os.remove(path+"/"+file)
        except:
            print("o arquivo nao foi encontrado:",path+"/"+file)
def apagaArquivo(file):
        try:
            os.remove(file)
        except:
            pass
'''
deve ter opcao de apagar conjuntos
o nome deve ter mais a data e horario
'''
'''        
def main():
    # cria pasta para novo conjunto
    nomeConjunto = "teste"
    nomePasta = "./conjuntoExperimentos/"+nomeConjunto
    criaPasta(nomePasta)
    # copia pastas para o novo conjunto
    origem = "./outputFiles/"
    destino = nomePasta+origem.replace(".", "")
    copiaPasta(origem, destino)
    origem = "./pdbs/"
    destino = nomePasta+origem.replace(".", "")
    copiaPasta(origem, destino)
    origem = "./ki/"
    destino = nomePasta+origem.replace(".", "")
    copiaPasta(origem, destino)
   
    # remove pastas existentes
    pasta = "./outputFiles2/"
    removePasta(pasta)
    pasta = "./pdbs2/"
    removePasta(pasta)
    pasta = "./ki2/"
    removePasta(pasta)
    # cria novas pastas
    nomePasta = "./outputFiles2/"
    criaPasta(nomePasta)
    nomePasta = "./pdbs2/"
    criaPasta(nomePasta)
    nomePasta = "./ki2/"
    criaPasta(nomePasta)
main()
'''
def arquivosNaPasta(pasta):
    caminhos = [os.path.join(pasta, nome) for nome in os.listdir(pasta)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    csv = [arq for arq in arquivos if arq.lower().endswith(".csv")]
    #txt = []
    #for l in csv:
    #   txt.append(l.replace("./ki/",""))
    return csv
def arquivosNaPastaModels():  
    pasta = "./models/"  
    caminhos = [os.path.join(pasta, nome) for nome in os.listdir(pasta)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    arqs = [arq.replace(pasta,"") for arq in arquivos if arq.lower().endswith(".txt")]
    #txt = []
    #for l in csv:
    #   txt.append(l.replace("./ki/",""))
    return arqs
def arquivosNaPastaPdb():
    pasta = "./pdbs/"
    caminhos = [os.path.join(pasta, nome) for nome in os.listdir(pasta)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    arqs = [arq.replace(pasta,"") for arq in arquivos if arq.lower().endswith(".pdb")]
    #txt = []
    #for l in csv:
    #   txt.append(l.replace("./ki/",""))
    return arqs
def arquivosNaPastaKi():
    pasta = "./ki/"
    caminhos = [os.path.join(pasta, nome) for nome in os.listdir(pasta)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    arqs = [arq.replace(pasta,"") for arq in arquivos if arq.lower().endswith(".csv")]
    #txt = []
    #for l in csv:
    #   txt.append(l.replace("./ki/",""))
    return arqs
def arquivosNaPastaOutput():
    pasta = "./outputFiles/"
    caminhos = [os.path.join(pasta, nome) for nome in os.listdir(pasta)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    arqs = [arq.replace(pasta,"") for arq in arquivos if arq.lower().endswith(".csv")]
    #txt = []
    #for l in csv:
    #   txt.append(l.replace("./ki/",""))
    return arqs
def arquivosNaPastaResults():
    pasta = "./results/"
    caminhos = [os.path.join(pasta, nome) for nome in os.listdir(pasta)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    arqs = [arq.replace(pasta,"") for arq in arquivos if arq.lower().endswith(".csv")]
    #txt = []
    #for l in csv:
    #   txt.append(l.replace("./ki/",""))
    return arqs
def completaPastas():
    # coria pastas necessarias
    pasta = "./inputFiles"
    criaPasta(pasta)
    pasta = "./outputFiles/"
    criaPasta(pasta)
    pasta = "./pdbs/"
    criaPasta(pasta)
    pasta = "./ki/"
    criaPasta(pasta)
    pasta = "./models/"
    criaPasta(pasta)
    pasta = "./results/"
    criaPasta(pasta)
    pasta = "./setsExperiments"
    criaPasta(pasta)
    pasta = "./adjustmentFunctions"
    criaPasta(pasta)
    pasta = "./logs"
    criaPasta(pasta)      
    pasta = "./importExport"
    criaPasta(pasta)       

        
