# coding=utf-8
from func_Gerais import leCsv, leCsvPulaLinha, search, grava, gravaConfig
from func_manipulaArquivos import apagaArquivo

def excluiLigantesRepetidos():
    listaEstruturasFicam = []
    listaExclusao = []
    nomePdbs=leCsv("./inputFiles/pdbsProteina.txt")
    listaNova = criaListaUnicaLigantes(nomePdbs)
    for l in listaNova:
        # deixamos mesmo os que nao teem ki -> estou retirando essas
        a = search(listaEstruturasFicam, l[2]) # procura valor da lista em llistaEstruturasficam
        if len(a) > 0:
            ind = a[0][0] # pega o indice onde foi encontrado valor igual
            resolucaoNovo = float(l[1])
            resolucaoAnterior = float(listaEstruturasFicam[ind][1])
            if resolucaoNovo < resolucaoAnterior: # fica o que tem menor valor de resolucao cristalografica em REMARK 2
                listaEstruturasFicam[ind] = l
        elif l[2] != None:
            listaEstruturasFicam.append(l)
        else:
            pass
    for i in nomePdbs:
        if not search(listaEstruturasFicam, i):
            listaExclusao.append(i)
    if len(listaEstruturasFicam) < 20:
        return False, 0
    else:
        excluiArquivosRepetidos(listaExclusao)
        gravaArqProteina(listaEstruturasFicam)
        gravaConfig("quantidadeProteinas", str(len(listaEstruturasFicam)))
        return True, len(listaExclusao)
def gravaArqProteina(listaEstruturasFicam):
    # cria novo arquivo proteinas
    textoPdb = ''
    listaEstruturasFicam = sorted(listaEstruturasFicam)
    for i in listaEstruturasFicam:
        textoPdb = textoPdb+i[0]+","
    # retira ultima virgula
    pos = textoPdb.rfind(',')
    t1 = list(textoPdb)
    t1[pos] = ''
    textoPdb = "".join(t1)
    arqProteina = "./inputFiles/pdbsProteina.txt"
    arqTreino = "./inputFiles/pdbsProteinaTreino.txt" 
    arqTeste = "./inputFiles/pdbsProteinaTeste.txt" 
    grava(textoPdb, arqProteina)
    #retira estruturas no arquivo treino
    listaTreinoNova = []
    textoTreino = leCsv(arqTreino)
    if len(textoTreino) > 0: # ve se ja tem os arquivos ou se serao gerados apos preparo
        listaTreino = textoTreino
        for s in listaEstruturasFicam:
            if str(s[0]) in listaTreino:
                listaTreinoNova.append(s[0])
        
        # retira estrutura arquivo teste
        listaTesteNova = []
        textoTeste = leCsv(arqTeste)
        listaTeste = textoTeste
        for s in listaEstruturasFicam:
            if str(s[0]) in listaTeste:
                listaTesteNova.append(s[0])       
        
        textoTreino = ",".join(listaTreinoNova)
        textoTeste = ",".join(listaTesteNova) 
        grava(textoTreino, arqTreino)
        grava(textoTeste, arqTeste)
    """
    ler ki concatenado e ir criando novo arquivo pdbsProteinas.txt
   apos, apagar arquivos pdb e ki que nao estiverem em pdbsPreteinas
   algumas funcoes abaixo nao serao utilizadas mais -> apagar
   
    Se entendi suas perguntas são sobre como eliminar as estruturas com ligantes repetidos, certo?
     Se for este o caso, eu uso o critério cristalográfico, quando o mesmo ligante aparece para
     duas ou mais estruturas, escolho aquela com menor resolução cristalográfica.
    
    """
def excluiArquivosRepetidos(listaExcluir):
    
    dirKi = "./ki/"
    dirPdb = "./pdbs/"
    for i in listaExcluir:
        apagaArquivo(dirKi+i.lower()+".csv")
        apagaArquivo(dirPdb+i.upper()+".pdb")
    


def criaListaUnicaLigantes(nomePdbs): # concatena todos os arquivos de ki
    lista = []
    listaNova = []
    dirKi = "./ki/" # define diretorio para pegar arquivo
    
    for arqKi in nomePdbs: # gera lista linha a linha com os arquivos csv existentes
        txtKi = leCsvPulaLinha(dirKi+arqKi.lower()+".csv")
        tam = int(len(txtKi)/4)
        lista = list(chunks(txtKi,tam)) # divide linha com multiplos valores
        for l in lista:
            if (l[3] !=''):
                l[1] = retornaResolucao(l[0]) # a coluna 2 trara a resolucao
                listaNova.append(l)    
    return listaNova

def chunks(lista, n): # divide lista em grupo de ligantes
    inicio = 0
    for i in range(n):
        final = inicio + len(lista[i::n])
        yield lista[inicio:final]
        inicio = final

def retornaResolucao(pdb):
    diretorio ="./pdbs/"
    pdb = pdb.upper()
    arq = open(diretorio+pdb+".pdb",'r')
    list = None
    for l in arq:
        if (('RESOLUTION' in l) or ('resolution' in l))\
        and (('REMARK   2' in l)  or ('remark   2' in l))\
        and (('ANGSTROMS' in l) or ('angstroms' in l))\
        and (not ('RANGE' in l) and not ('range' in l)):
            list = l.split()
    arq.close
    return list[3]
    
'''
def main():
    
    arq = "./inputFiles/pdbsProteina.txt"
    concatenaArquivos()
    
     
if __name__ == "__main__":
    main()
'''