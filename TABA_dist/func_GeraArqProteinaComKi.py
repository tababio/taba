# coding=utf-8
# gera uma arquivo somente com dpbs com arquivo de KI
from func_Gerais import grava
from func_Gerais import leCsv


def le(arquivo):
    diretorio = "./ki/" # define diretorio para salvar o download
    arq = diretorio+arquivo
    try:
        fo = open(arq, 'r')
    except IOError:
        return "N" # nao foi encontrado arquivo de KI
    return "S"

def geraArquivoProteinaFinal(diret,arquivo,tipo):
    progresso = 0
    conteudo = []
    semConteudo = [] # arquivo de pdbs sem ki
    arquivoParaLer = leCsv(diret+arquivo) # le arquivo com os pdbs a serem processados como proteinas
    for prot in arquivoParaLer:      
        arquivo=prot.strip() # nome do arquivo pdb que esta em pdbsProteinas
        arquivo = arquivo.lower()+".csv"
        #print (arquivo)
        if le(arquivo) =="S":
            conteudo.append(prot)
            conteudo.append(",")
        else:
            semConteudo.append(prot)
            semConteudo.append(",")
    tam = len(conteudo)
    tam2 = len(semConteudo)
    conteudo.pop(tam-1) # para retirar a ultima virgula
    grava(conteudo, diret+"pdbsProteinaFinal"+tipo+".txt")
    if semConteudo:
        semConteudo.pop(tam2-1) # para retirar a ultima virgula
    '''
    print ("|---------------------------------------------------------|")
    print ("|  Quantidde de arquivos excluidos por nao terem Ki:",len(semConteudo)-1,"  |")
    print ("|---------------------------------------------------------|")
    print("")
    grava(semConteudo, diret+"LogPdbsProteinaSemKi.txt")    
    print ("|-----------------------------------------------------------|")
    print ("|  Foi gerado o arquivo com as proteinas a serem processadas|")
    print ("|  (pdbsProteinaFinal.txt)                                  |")
    print ("|-----------------------------------------------------------|") 
    print("")
    '''
