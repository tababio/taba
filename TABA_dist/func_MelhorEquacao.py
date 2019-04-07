# coding=utf-8
import sys

def melhor(arq, coeficiente, peloMenor, distancia): # recebe o diretorio e o arquivo SF
    # posiçoes R [3] R2 [4] speraman = 7
    val = 0
    melhorEquacao = ""
    pv1 = 0
    pv2 = 0
    if peloMenor: # se procura o menor valor
            retorno = 9999999
    else:
        retorno = 0
    # define com qual coeficiente deve comparar o valor corresponde a coluna em SF_
    if coeficiente == "r1": # coeficiente R
        coef = 3
    elif coeficiente == "r2": # coeficiente R squared ao quadrado
        coef = 4      
    elif coeficiente == "pvs": # confirmado que é spearman
        coef = 8 
    elif coeficiente == "pvp": # verificar  
        coef = 5  
    elif coeficiente == "sd": # coeficiente R
        coef = 2  
    elif coeficiente == "rmse": # coeficiente R
        coef = 13       
    elif coeficiente == "sp":
        coef = 7 # coeficiente spearman     
    try:
        fo = open(arq, 'r')
    except IOError:
        sys.exit ("\n O arquivo "+arq+" nao foi encontrado!!!")
    try:
        fo.readline()
        for line in fo:
            linhalimpa = line.replace(" ", "") #retira brancos
            linha = linhalimpa.split(",")
            lin = linha[coef]                    
            val = float(lin)
            if peloMenor:           
                #if (val < retorno) and (procuraDistanciaNula(linha[0],distancia) == False): # se a equacao contem valores nulos desconsidera
                if val < retorno:
                    retorno = val
                    melhorEquacao = linha[0]
                    procuraDistanciaNula(melhorEquacao)
                    pv2 = linha[8] 
            else:                   
                #if (val > retorno) and (procuraDistanciaNula(linha[0],distancia) == False): # se a equacao contem valores nulos desconsidera
                if val > retorno:
                    retorno = val
                    melhorEquacao = linha[0]                    
                    pv2 = linha[8] 
    except:
        pass
    return retorno,pv2,melhorEquacao

def procuraDistanciaNula(melhorEquacao,distancia): # se a equacao contem variaveis nulas retrona True
    listaVariaveis = retornaVariaveis(melhorEquacao)
    diret = "./outputFiles/"
    arqMedia = diret+"medDistPdb_"+distancia+"_TRE.csv"
    try:
        foMedias = open(arqMedia, 'r')
    except:
        print("The file "+arqMedia+"not found!") 
    cabecalho = foMedias.readline()  
    listaCabecalho = cabecalho.split(",") 
    for l in listaVariaveis:
        ind = listaCabecalho.index(l)
        for i in foMedias:
            lista = i.split(",") 
            if float(lista[ind]) == 0:
                return True

    return False
def retornaVariaveis(melhorEquacao):    
    m = melhorEquacao.replace("*",",")
    m = m.replace("+",",")
    m = m.replace("-",",")
    lista = m.split(',')
    listaRetorno = []
    for i in lista:
        if "(" in i:
            r = lista.index(i)
            a = i.replace("(","")
            a = a.replace(")","")
            listaRetorno.append(a)
    return listaRetorno
        
        