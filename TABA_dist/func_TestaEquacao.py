# coding=utf-8
#Usa arquivos separados para teste e aplica melhor formula
import sys
from func_Gerais import grava, retornaDigito

def geraCalculoPelaFormula(diretorio,arquivo,formula,tipo):
    listaVariaveis = criaListaVariaveis(formula)    
    '''
    ver se a funcao calcula2 eh mais adequada do que a calcula
    Parece que nao, pois calcula2 utiliza a media, enquanto calcula utilia o termo de energia
    '''    
    return calcula(listaVariaveis,diretorio, arquivo, formula,tipo) #calcula usando os termoo de energia e gera arquivo com resultados para comparar

def calcula(listaVariaveis,diretorio,arquivo,formula,tipo):#calcula usando os termoo de energia e gera arquivo com resultados para comparar
    '''
    utiliza o termo de energia de todos os arquivos Pdb
    '''
    arquivo = arquivo.replace("Tre", tipo)#o arquivo que vem eh o de treino por isto substitui pelo tipo de arquivo
    arq = diretorio+arquivo
    pos = posicaoVariaveis(listaVariaveis, diretorio, arquivo) # pega posiccao dos valores das colunas das variaveis
    listaValores = []
    listaResultados = ''
    try:
        fo = open(arq, 'r')
    except IOError:
        sys.exit ("\n O arquivo "+arq+" nao foi encontrado")    
    try:
        fo.readline() # para pular primeira linha
        for line in fo: # percorre arquivo
            linha = line.split(",")
            for x in pos:  # percorre lista de posicao e pega valores no arquivo de teste ou treino    
                listaValores.append(linha[x])
            n = 0
            equacao = formula
            for lin2 in listaVariaveis:  #substitui valores na equacao    
                equacao = equacao.replace(listaVariaveis[n], listaValores[n]) #substitui variavel pelo valor
                n = n+1     
            #equacao = limpaEquacao(equacao)  # estava desativada pois dava erro
            #print("+++++",equacao)
            valor = resolveEquacao(equacao)
            listaValores = [] 
            ligante = linha[0].replace("[","")
            ligante = ligante.replace("]","")
            pdb = linha[1]
            distancia = retornaDigito(arquivo)
            arqMedia = "medDistPdb_"+distancia+"_"+tipo.upper()+".csv"
            lin = ""
            for atomo in listaVariaveis:
                media = pegaMediaPdb(pdb,atomo,arqMedia)
                lin = lin+","+media
            lin.split()
            lin = pdb+","+ligante+lin                
            listaResultados = listaResultados+lin+","+str(valor)+","+linha[36].replace("\n","")+"\n"
            #print("====Lista resultados", listaResultados)
    except:
        pass
    fo.close()    
    if tipo == "Tes":        
        arquivoParaSalvar = "resultadoTeste.csv"
    elif tipo == "Tre":
        arquivoParaSalvar = "resultadoTreino.csv"
        
    li = 'PDB,Ligand'
    for atomo in listaVariaveis:
        li =li+',d'+atomo
    cabecalho = li+","+'Predicted, Experimental'+"\n"
    texto = cabecalho+listaResultados
    grava(texto,diretorio+arquivoParaSalvar)
    #print("---->listaResultados",listaResultados)
    return listaResultados  


def resolveEquacao(equacao):
    result = eval(equacao)
    return result

def criaListaVariaveis(formula):
    #prepara para split
    form = formula.replace("-","#")
    form = form.replace("+","#")
    form = form.replace("*","#")
    form = form.replace("(","#")
    form = form.replace(")","#")
    form = form.replace(".","") # nãp pode ter ponto para isdigit()
    form = form.replace("\n","")
    form_aux = form.split("#")
    form_aux = [x for x in form_aux if x != '']
    listaVariaveis = []
    for i in form_aux:
        aux = str(i).strip()
        if (not aux.isdigit()):
            listaVariaveis.append(i)
    return listaVariaveis

def limpaEquacao(equacao):
    # não utilizar -> avaliar
    equacao = equacao.replace("(","") #retira parentes a esquerda
    equacao = equacao.replace("-","-(")
    equacao = equacao.replace("+","+(")
    equacao = equacao.replace("(","",1) # ao final retira o primeiro parentese

    return equacao 
def pegaMediaPdb(pd, atom, arq):
    arquivo = "./outputFiles/"+arq
    atomo = atom.upper()
    pdb = pd.upper()
    fo = open(arquivo, 'r')
    lines = fo.readlines() # Lê as linhas e separa em um vetor
    firstLine = lines.pop(0) #Remove a primeira linha
    cabecalho = firstLine.split(",")
    pos = cabecalho.index(atomo) # pega a posicao do atomo no cabecalho
    for i in lines:
        m = i.split(",")
        if m[0] == pdb: 
            distanciaMedia = m[pos]
            dist = str(  "%6.4f"%float(distanciaMedia)  )
            return dist

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
    # retorna lista de posicoes dos pares de atomos
    return posicao
