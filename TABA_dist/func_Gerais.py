# coding=utf-8
#funcoes genericas
import csv
from datetime import datetime
import sys  
import os, re, psutil
from func_manipulaArquivos import existeArquivo, criaArquivo, apagaArquivos,apagaArquivo, arquivosNaPastaKi, arquivosNaPastaPdb
import urllib.request as ur
from PyQt4 import QtGui  # Import the PyQt4 module we'll need
import urllib.request
import time,platform
import zipfile

# faz a media para andamento do programa
def andamento(vet):
    '''
    recebe um vetor com 7 posicoes onde as ultimas posicoes nao preenchidas sao preenchida regressivamente com 36,35,34,33
    
    '''
    # preenche posicoes faltanes o vetor tem no minimo 3 posicoes e estamos considerando um vetor so com 7 posicoes teremos preciao para 10 posicoes
    tam = len(vet) 
    if tam ==3:
        vet.append(33) # lembrar vetor comeca em 0
        vet.append(34)
        vet.append(35)
        vet.append(36)
    if tam ==4:
        vet.append(34)
        vet.append(35)
        vet.append(36)
    if tam ==5:
        vet.append(35)
        vet.append(36)
    if tam ==7:
        vet.append(36)       
    #########
    div = 1
    soma = 0
    QtGui.QApplication.processEvents() # para nao travar usar antes de loop
    for i in vet: # divide cada posicao do vetor por um multiplo de 10 e soma
        div = div*10 # vai acrescendo o divisor
        soma = soma+(i/div) 
    resultado = soma*10000000
    # o  valor de referencia e a soma do vetor [31,32,33,34,35,36] dividindo cada posicao por 10 na n+1 e depois multiplica por 10,000,000
    valRef = 33456786
    return valRef, resultado
# Program to download PDB file

def download_PDB_file(my_url,pdb_access_in):
    """Function to get data from an url"""    
    # url_in = 'http://files.rcsb.org/download/'
    # Set up file name
    #pdb_file = "./pdbs/"+pdb_access_in+".pdb" # inclui diretorio e sufixo
    pdb_file = pdb_access_in # inclui diretorio e sufixo # modificado pois nao aceita /pdbs
    # Set up URL
    #print(my_url+pdb_file)
    
    try:
        QtGui.QApplication.processEvents() # para nao travar usar antes de loop
        file_object = ur.urlopen(my_url+pdb_file)
        structure = file_object.read()        
        file_object.close()
    except:
        print("Could not access server")
        mensagem = "Could not access server"
        return mensagem
    
    # Download file
    diretorioParaBaixar = "./pdbs/"
    QtGui.QApplication.processEvents() # para nao travar usar antes de loop
    with open(diretorioParaBaixar+pdb_file,"wb") as my_file_4_download:
        my_file_4_download.write(structure)
    mensagem = "\nFinishing downloading of "+pdb_file+" file!" # nao mudar mensagem pois pode impactar em validacoes
    return(mensagem)
def get_Bind(my_dir_in,structureId,binding_info):
    """Function to download CSV file with binding affinty"""


    # String for local time
    my_local_time = str(time.strftime("%Y_%m_%d__%Hh%Mmin%Ss"))
    
    # Sets up initial values for variable and list
    check_if_code_in = False
    my_structureId_string = structureId.lower()
    my_binding_list = ["Ki","Kd","EC50","IC50","deltaG","deltaH","Ka"]
       
    # Looping through my_binding_list
    QtGui.QApplication.processEvents() # para nao travar usar antes de loop
    for bind_in in my_binding_list:
        if binding_info.upper().strip() == bind_in.upper().strip():
            binding_info1 = bind_in.strip()
            

    # Specify file
    file_2_download =my_structureId_string+".csv"
    
    # Check if file is already in the structure directory
    flag_4_file_present = pre_download(my_dir_in,file_2_download)
    if flag_4_file_present:
        check_if_code_in = True
        return check_if_code_in
    
    # Specify url
    #my_url = 'http://www.rcsb.org/pdb/rest/customReport?pdbids='+my_structureId_string+'&customReportColumns=structureId,chainId,ligandId,'+binding_info+',&service=wsfile&format=csv&ssa=n'
    my_url = 'http://www.rcsb.org/pdb/rest/customReport?pdbids='+my_structureId_string+'&customReportColumns=structureId,chainId,ligandId,'+binding_info1+'&service=wsfile&format=csv&ssa=n'

    # Try to download file    
    
    try: 
        QtGui.QApplication.processEvents() # para nao travar usar antes de loop
        file_object = urllib.request.urlopen(my_url)
        structure = file_object.read()
        file_object.close()
    except:
        check_if_code_in = False
        my_iteraction = 1
        #print("RCSB is complaining about 'High User Activity'.")
        #print("I will try to wait longer for each file...")
        my_time_to_wait = my_iteraction*20
        #print("Waiting for",my_time_to_wait," seconds...")
        time.sleep(my_time_to_wait)
        #print("\n "+file_2_download+" file downloaded from http://www.rcsb.org/")
        loop_flag = True
        
        # while loop to keep trying to download
        QtGui.QApplication.processEvents() # para nao travar usar antes de loop
        while loop_flag:
            try: 
                file_object = urllib.request.urlopen(my_url)
                structure = file_object.read()
                file_object.close()
        
                file_object = urllib.request.urlopen(my_url)
            #structure_line = file_object.readline()
                file_object.close()
                loop_flag = False
                check_if_code_in = True
            except:
                my_iteraction += 1
                loop_flag = True
                check_if_code_in = False
    
            if my_time_to_wait > 359:
                #print("It is taking too long!")
                #print("Try to split in different inputs getbind.in, with a smaller number of structures per input.\n")
                return check_if_code_in
                break
            
    time.sleep(1)
    QtGui.QApplication.processEvents() # para nao travar usar antes de loop
    with open(my_dir_in+file_2_download,"wb") as my_file_4_download:
        my_file_4_download.write(structure)
        my_file_4_download.close()
        check_if_code_in = True
def pre_download(my_dir_in,my_file_in):
    """Function to check if the file is already in the structure directory"""
    file_present = False
    my_fo = None
    # Try to open file
    try:
        my_fo = open(my_dir_in+my_file_in,"r")
        file_present  = True
        my_fo.close()
    except:
        file_present  = False
                
    # Return boolean variable
    return file_present
def grava(conteudo,arquivoSai):
    arquivo = open(arquivoSai, 'w')
    arquivo.writelines(conteudo)
    arquivo.close()

# Le um arquivo delimitado e mostra os campos na tela. """
  
def leCsv(arquivo):
    retorno = []
    try:
        fo = open(arquivo, 'r')
    except IOError:
        return False
    with fo as ficheiro:
        reader = csv.reader(ficheiro)
        for linha in reader:
            retorno = retorno+linha
    return retorno  
def leCsvPulaLinha(arquivo): #pula a primeira linha do arquivo
    retorno = []
    try:
        fo = open(arquivo, 'r')
    except IOError:
        sys.exit ("\n O arquivo "+arquivo+" nao foi encontrado")
    with fo as ficheiro:
        reader = csv.reader(ficheiro)
        next(reader)
        for linha in reader:
            retorno = retorno+linha
    return retorno  
# verifica se uma string pode ser float
def isfloat(value):
        try:
            float(value)
            return True
        except:
            return False 
def tempoEstatistica(now,cont,quant): # mostra estimativas de duracao do processamento
        now2 = datetime.now()
        tempo = now2-now
        mediaAtual = tempo/cont
        total = tempo+(mediaAtual*(quant-cont))
        tempoRestante = total-tempo
        '''
        print ("|------------- tempo = hh:mm:ss --------------------|")
        print ("| tempo de processamento total:", tempo)
        print ("| estimativa de duracao:", total)
        print ("| tempo restante estimado:", tempoRestante)
        print ("|----------------------------------------------------|")
        ''' 
def contaCaracter(caracter,frase):  
    y = 0
    for x in frase:
        if x == caracter:
            y+=1
    return y    
def get_pastas(direct):
    return [os.path.join(direct, f) for f in os.listdir(direct)]
def get_arquivosTreino(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            if "saida" in filepath and not "SF" in filepath and "Tre" in filepath: # para usar somente os que contem saida
                file_paths.append(filepath)  # Add it to the list.

    return file_paths
def get_arquivosSf(directory,distancia):

    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            if "SF_" in filepath and "Tre" in filepath and distancia in filepath: # para usar somente os que contem saida
                file_paths.append(filepath)  # Add it to the list.

    return file_paths
def limpa_arquivosSf(directory): #limpa arquivos SF nulos por interrupcao

    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            if "SF_" in filepath and "Tre" in filepath: # para usar somente os que contem saida
                if os.path.getsize(filepath) == 0:
                    os.remove(filepath, dir_fd=None)
    return file_paths
def limpaArquivosOutput():
    folder = './outputFiles'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        #    elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            pass
def limpaArquivosModelos():
    folder = './models'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        #    elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            pass
def get_arquivosTeste(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            if "saida" in filepath and not "SF" in filepath and "Tes" in filepath: # para usar somente os que contem saida
                file_paths.append(filepath)  # Add it to the list.

    return file_paths

def get_listaDistancias(directory):
    listaDistancias = []
    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            if "3.5" in filepath and not "Usu" in filepath and not "3.5" in listaDistancias: # para usar somente os que contem saida
                listaDistancias.append("3.5")  # Add it to the list.
            if "4.5" in filepath and not "Usu" in filepath and not "4.5" in listaDistancias: # para usar somente os que contem saida
                listaDistancias.append("4.5")  # Add it to the list.
            if "6.0" in filepath and not "Usu" in filepath and not "6.0" in listaDistancias: # para usar somente os que contem saida
                listaDistancias.append("6.0")  # Add it to the list.
            if "7.5" in filepath and not "Usu" in filepath and not "7.5" in listaDistancias: # para usar somente os que contem saida
                listaDistancias.append("7.5")  # Add it to the list.
            if "9.0" in filepath and not "Usu" in filepath and not "9.0" in listaDistancias: # para usar somente os que contem saida
                listaDistancias.append("9.0")  # Add it to the list.
            if "12.0" in filepath and not "Usu" in filepath and not "12.0" in listaDistancias: # para usar somente os que contem saida
                listaDistancias.append("12.0")  # Add it to the list.
            if "15.0" in filepath and not "Usu" in filepath and not "15.0" in listaDistancias: # para usar somente os que contem saida
                listaDistancias.append("15.0")  # Add it to the list.
                

    return listaDistancias 
def get_listaColunas(directory):
    listaColunas = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            if "3cols" in filepath and not "2" in listaColunas: # para usar somente os que contem saida
                listaColunas.append("2")  # desconta a contante            
            if "4cols" in filepath and not "3" in listaColunas: # para usar somente os que contem saida
                listaColunas.append("3")  # desconta a contante
            if "5cols" in filepath and not "4" in listaColunas: # para usar somente os que contem saida
                listaColunas.append("4")  # desconta a contante
            if "6cols" in filepath and not "5" in listaColunas: # para usar somente os que contem saida
                listaColunas.append("5")  # desconta a contante
            if "7cols" in filepath and not "6" in listaColunas: # para usar somente os que contem saida
                listaColunas.append("6")  # desconta a contante
            if "8cols" in filepath and not "7" in listaColunas: # para usar somente os que contem saida
                listaColunas.append("7")  # desconta a contante 
            if "9cols" in filepath and not "8" in listaColunas: # para usar somente os que contem saida
                listaColunas.append("8")  # desconta a contante
            if "10cols" in filepath and not "9" in listaColunas: # para usar somente os que contem saida
                listaColunas.append("9")  # desconta a contante
            if "11cols" in filepath and not "10" in listaColunas: # para usar somente os que contem saida
                listaColunas.append("10")  # desconta a contante                                                                                       
    return listaColunas
def get_listaColunasDistancia(directory): #verifica distancias e colunas nos arquivos de saida
    listaColDist = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            if "SF_saida" in filename:
                texto = filename.replace("_","#") # separa para criar lista
                texto = texto.replace("cols","#")
                lista = texto.split("#") # cria lista com partes numericas separadas
                dist = str(extraiNumeros(lista[1])/10) # 1 e a posicao da distancia na lista criada
                col = str(int(extraiNumeros(lista[5])-1))# 5 e a posicao da quantidade de coluna na lista criada
                texto = dist+str(chr(197))+" and "+str(col)+" Variables"
                if not texto in listaColDist:
                    listaColDist.append(texto)
    return listaColDist
            
def gravaConfig(tag,valor):
    valor = valor.strip() # retira espacos pois pode resultar em strings maiores que o campo definido para mostrar    
    tag = "<"+tag+">"# criar tags para descricao pdbs proteinas, ligante ou inibidor,
    arq = "./inputFiles/config.csv"
    textoNovo = ''
    try:
        fd = open(arq, 'r')    
        for line in fd:
            line = line.strip()
            if tag in line:
     
                strRemove = line
                newLine = line.replace(strRemove,tag+","+valor)
                textoNovo = textoNovo+newLine+"\n"
            else:
    
                textoNovo = textoNovo+line+"\n"
        if not tag in textoNovo:
                textoNovo = textoNovo+tag+","+valor+"\n"
        fd.close()
        fdw = open(arq, 'w')
        fdw.write(textoNovo)
        fdw.close()
    except:  
        print("file not found")
        #next(input_fd) para pular cabecalho, mas nao precisa neste caso
def gravaConfigTaba(tag,valor):
    valor = valor.strip() # retira espacos pois pode resultar em strings maiores que o campo definido para mostrar    
    tag = "<"+tag+">"# criar tags para descricao pdbs proteinas, ligante ou inibidor,
    arq = "configTaba.csv"
    textoNovo = ''
    try:
        fd = open(arq, 'r') 

        #next(input_fd) para pular cabecalho, mas nao precisa neste caso
        for line in fd:
            line = line.strip()
            if tag in line:
     
                strRemove = line
                newLine = line.replace(strRemove,tag+","+valor)
                textoNovo = textoNovo+newLine+"\n"
            else:
    
                textoNovo = textoNovo+line+"\n"
        if not tag in textoNovo:
                textoNovo = textoNovo+tag+","+valor+"\n"
        fd.close()
        fdw = open(arq, 'w')
        fdw.write(textoNovo)
        fdw.close()
    except:  
        print("file not found")
def gravaModelo(arq,tag,valor):
    valor = valor.strip() # retira espacos pois pode resultar em strings maiores que o campo definido para mostrar    
    tag = "<"+tag+">"# criar tags para descricao pdbs proteinas, ligante ou inibidor,
    arq = "./models/"+arq
    textoNovo = ''
    try:
        fd = open(arq, 'r')   

    except:  
        print("file not found")
        #next(input_fd) para pular cabecalho, mas nao precisa neste caso
    for line in fd:
        line = line.strip()
        if tag in line:
 
            strRemove = line
            newLine = line.replace(strRemove,tag+","+valor)
            textoNovo = textoNovo+newLine+"\n"
        else:

            textoNovo = textoNovo+line+"\n"
    if not tag in textoNovo:
            textoNovo = textoNovo+tag+","+valor+"\n"
    fd.close()
    fdw = open(arq, 'w')
    fdw.write(textoNovo)
    fdw.close()    
def pegaConfig(tag):    
    tag = "<"+tag.strip()+">"# criar tags para descricao pdbs proteinas, ligante ou inibidor,
    arq = "./inputFiles/config.csv"
    my_fo = open(arq,"r")  
    try:
        my_fo = open(arq,"r")   
    except:            
        print("--->file not found")
    for lin in my_fo:
        texto = lin.split(",") 
        if texto[0] == tag:
            return texto[1]
def pegaConfigTaba(tag):    
    tag = "<"+tag.strip()+">"# criar tags para descricao pdbs proteinas, ligante ou inibidor,
    arq = "configTaba.csv"
    my_fo = open(arq,"r")  
    try:
        my_fo = open(arq,"r")   
    except:            
        print("--->file not found")
    for lin in my_fo:
        texto = lin.split(",") 
        if texto[0] == tag:
            return texto[1]
def pegaModelo(arq,tag):    
    tag = "<"+tag.strip()+">"# criar tags para descricao pdbs proteinas, ligante ou inibidor,
    arq = "./models/"+arq
    my_fo = open(arq,"r")  
    try:
        my_fo = open(arq,"r")   
    except:            
        print("--->file not found")
    for lin in my_fo:
        texto = lin.split(",") 
        #print("****", texto)
        if texto[0] == tag:
            return texto[1]
def substituiSeedEmMLin(valor): 
    '''
    substitui as sementes no arquivo ml.in para que fiquem igual a semente da geracao dos arquivos para regresao
    caso esteja utilizando experimentos mais antigos sera considerada a semente para a distancia de 4.5
    '''
    
    geraMlin()# gera novo ml.in para nao pegar valores antigos
    my_fo = None
    valor = valor.replace('.','') # retirar o ponto para bucar a tag
    tag = "seed"+valor 
    
    tag1 = pegaConfig(tag) # pega valor da semente para uma distancia

    if (tag1 == None): # caso seja experimento antigo vai utilizar o valor padrao do ml.in
        tag1 = '1123581321'
    texto2 = ''
    arq = "./inputFiles/ml.in" 
    try:
        my_fo = open(arq,"r")   
    except:            
        print("file not found")

    for lin in my_fo:
        texto = lin.split(",") 
        if 'Lasso' in texto:  
            texto[11] = tag1
        if 'LassoCV' in texto:        
            texto[11] = tag1              
        if 'ElasticNet' in texto:        
            texto[11] = tag1
        if 'ElasticNetCV' in texto:      
            texto[13] = tag1
        str1 = ','.join(texto)
        str2 = str1.replace('\n', '')+'\n' # para deixar somente um \n
        texto2 = texto2+str2
        
    
    my_fo.close()
    # grava novo ml.in 
    fd = open(arq, 'w')
    fd.write(texto2)
    fd.close()
    return tag1 # retorna a semente para a winRegressao
   
def temLigante(diretorio, arquivo):
    arq = ''.join(arquivo)
    arq = diretorio+arq.lower()+"_soHetatm.pdb"
    if os.stat(arq).st_size==0:
        return False
    else:
        return True
'''
def limpaPastas():
    # remove pastas existentes
    pasta = "./outputFiles/"
    removePasta(pasta)
    pasta = "./pdbs/"
    removePasta(pasta)
    pasta = "./ki/"
    removePasta(pasta)
    pasta = "./inputFiles/"
    removePasta(pasta)
    # cria novas pastas
    nomePasta = "./outputFiles/"
    criaPasta(nomePasta)
    nomePasta = "./pdbs/"
    criaPasta(nomePasta)
    nomePasta = "./ki/"
    criaPasta(nomePasta)
    nomePasta = "./inputFiles/"
    criaPasta(nomePasta)
    criaArquivoBase()
'''
def limpaPastas():
    # remove parquivos nas pastas
    pasta = "./outputFiles/"
    apagaArquivos(pasta)
    pasta = "./pdbs/"
    apagaArquivos(pasta)
    pasta = "./ki/"
    apagaArquivos(pasta)
    pasta = "./inputFiles/"
    apagaArquivos(pasta)
    pasta = "./models/"
    apagaArquivos(pasta)
    criaArquivoBase()
def limpaPastaSaida():
    # remove parquivos nas pastas
    pasta = "./outputFiles/"
    apagaArquivos(pasta)
    criaArquivoBase()
def limpaArquivosOutlier():
    # remove parquivos nas pastas
    arq = "./inputFiles/pdbsProteinaFinalTes.txt"
    apagaArquivo(arq)
    arq = "./inputFiles/pdbsProteinaFinalTre.txt"
    apagaArquivo(arq)
    arq = "./inputFiles/pdbsProteinaTeste.txt"
    apagaArquivo(arq)
    arq = "./inputFiles/pdbsProteinaTreino.txt"
    apagaArquivo(arq)
def limpaPastasSaidaOutlier():
    # remove parquivos nas pastas
    pasta = "./outputFiles/"
    apagaArquivos(pasta)
    pasta = "./models/"
    apagaArquivos(pasta)
def limpaPastaAdjustmentFunctions():
    # remove parquivos nas pastas
    pasta = "./adjustmentFunctions/"
    apagaArquivos(pasta)
def geraMlin():
    #regrava arquivo ml.in
    l1 = "LinearRegression,True,True,True"+"\n"
    l2 = "Lasso,0.1,True,True,False,True,1000,0.0001,True,False,random,1123581321"+"\n"
    l3 = "LassoCV,0.1,True,True,False,True,1000,0.0001,True,False,random,1123581321"+"\n"
    l4 = "Ridge,1.0,True,True,True,1000,0.001,auto"+"\n"
    l5 = "RidgeCV,0.05,2.0,0.05,True,False,True,1000,0.001,auto"+"\n"
    l6 = "ElasticNet,0.1,0.5,True,False,True,1000,True,0.0001,True,False,1123581321,random"+"\n"
    l7 = "ElasticNetCV,0.1,0.15,15,0.5,True,False,True,1000,True,0.0001,True,False,1123581321,random"
    texto1 = l1+l2+l3+l4+l5+l6+l7
    arquivoSaida = "./inputFiles/ml.in"
    grava(texto1, arquivoSaida)
def criaArquivoBase():
    #regrava arquivo ml.in
    # esta sendo gerado na regressao geraMlin
    texto2 = "null"
    # tags para arquivo config
    t31 = "<descricaoDataset>,null"+"\n"
    t32 = "<tipoAfinidade>,Ki"+"\n"
    t33 = "<quantidadeProteinas>,null"+"\n"
    t34 = "<quantidadeInicialProteinas>,null"+"\n"
    t35 = "<spearman>,null"+"\n"
    t36 = "<melhorEquacao>,null"+"\n"
    t37 = "<tipoMedia>,null"+"\n"
    t38 = "<comentarios>,null"+"\n"    
    t39 = "<nomeExperimento>,null"+"\n"    
    t40 = "<seed35>,null"+"\n"
    t41 = "<seed45>,null"+"\n" 
    t42 = "<seed60>,null"+"\n" 
    t43 = "<seed75>,null"+"\n" 
    t44 = "<seed90>,null"+"\n"  
    t50 = "<outlier>,no"    
    texto3 = t31+t32+t33+t34+t35+t36+t37+t38+t39+t40+t41+t42+t43+t44+t50
    arquivoSaida = "./inputFiles/pdbsProteina.txt"
    grava(texto2, arquivoSaida)
    arquivoSaida = "./inputFiles/config.csv"
    grava(texto3, arquivoSaida)
def pastaVazia(path): 
    if os.listdir(path) == []: 
        return True
    else: 
        return False 
def existeArquivo(arquivo):
    try:
        fo = open(arquivo, 'r')
    except IOError:
        return False
    return True

def numeroLinhas(arquivo):
    try:
        num_lines = sum(1 for line in open(arquivo))
    except:
        return 0
    return num_lines
def completaArquivoConfig(): #quando algum campo estiver vazio, vai complementar
    arquivo = "./inputFiles/config.csv"
    if existeArquivo(arquivo):
        texto = leCsv(arquivo)
    else:
        texto = ""
        criaArquivo(arquivo)  
    if not("<descricaoDataset>" in texto):
        gravaConfig("descricaoDataset", "null")  
    if not("<outlier>" in texto):
        gravaConfig("outlier", "no")
    if not("<nomeExperimento>" in texto):
        gravaConfig("nomeExperimento", "null")        
    if not("<tipoMedia>" in texto):
        gravaConfig("tipoMedia", "training")
    if not("<quantidadeInicialProteinas>" in texto):
        gravaConfig("quantidadeInicialProteinas", "null")
    if not("<excluiLigantes>" in texto):
        gravaConfig("excluiLigantes", "null")
    if not("<geraSets>" in texto):
        gravaConfig("geraSets", "null")
    if not("<data>" in texto):
        gravaConfig("data", "null")
    if not("<comentarios>" in texto):
        gravaConfig("comentarios", "null")
        
    diret = "./inputFiles/"
    arq = diret+"pdbsProteinaTreino.txt"
    if not existeArquivo(arq):
        criaArquivo(arq)
    diret = "./inputFiles/"
    arq = diret+"pdbsProteinaTeste.txt"
    if not existeArquivo(arq):
        criaArquivo(arq) 
def completaArquivoModelo(arq): #quando algum campo estiver vazio, vai complementar
    texto = leCsv("./models/"+arq)
    if not("<valorCoeficiente>" in texto):
        gravaModelo(arq,"valorCoeficiente", "null")  
def completaArquivoConfigTaba(): #quando algum campo estiver vazio, vai complementar
    arquivo = "configTaba.csv"
    texto = ''
    if existeArquivo(arquivo):
        texto = leCsv(arquivo)
    else:        
        criaArquivo(arquivo)  
    if not("<atalho>" in texto):
        gravaConfigTaba("atalho", "yes")
    if not("<versao>" in texto):
        gravaConfigTaba("versao", "novaVersao")
def get_desktop_path():

    D_paths = list()

    try:
        fs = open(os.sep.join((os.path.expanduser("~"), ".config", "user-dirs.dirs")),'r')
        data = fs.read()
        fs.close()
    except:
        data = ""

    D_paths = re.findall(r'XDG_DESKTOP_DIR=\"([^\"]*)', data)

    if len(D_paths) == 1:
        D_path = D_paths[0]
        D_path = re.sub(r'\$HOME', os.path.expanduser("~"), D_path)

    else:
        D_path = os.sep.join((os.path.expanduser("~"), 'Desktop'))

    if os.path.isdir(D_path):
        path = str(D_path)
        return path
    else:
        return None
        
        
def get_platform():
    platforms = {
        'linux1' : 'Linux',
        'linux2' : 'Linux',
        'darwin' : 'OS X',
        'win32' : 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform
    
    return platforms[sys.platform]

def rodandoTaba():
    conta = 0    
    for pid in psutil.pids():
        p = psutil.Process(pid)
        if "TABA" in (p.name()).upper():
            conta += 1
    if conta > 1: # utilizando o CX_freeze e so uma instancia      
        return True
    else:
        return False
    '''
    para outros geradores de exe pode ser gerada duas instancias ????
    conta = 0    
    for pid in psutil.pids():
        p = psutil.Process(pid)
        if "TABA" in (p.name()).upper():
            conta += 1
    if "WINDOWS" in (platform.system()).upper(): # para linux ha 2 instancias no windows só uma por isto soma 1 para equivaler o true
        conta += 1
    if conta > 2: # para linux ha 2 instâncias no windows so uma        
        return True
    else:
        return False
    '''
def converteStringDeltaG(string): # converte texto deltaG para simbolo
    if string.upper() == "DELTAG":
        return(chr(916)+'G')
    else:
        return string
def search (lista, valor):
    return [(lista.index(x), x.index(valor)) for x in lista if valor in x]
def extraiNumero(input_str): # extrai numero da string
    input_str = input_str.replace(".txt","")
    if input_str is None or input_str == '':
        return 0
    num = ""
    pos = input_str.rfind("model")
    pos = pos+5 #ultima posicao do caractere
    num = (input_str[pos:])
    if num.isdigit():
        return num
    else:
        return "9999999"

def kiVazio():
    diret = "./ki/"
    arqs = arquivosNaPastaKi()
    arquivosVazios = []
    for i in arqs:
        texto = leCsvPulaLinha(diret+i)
        if not texto:
            arquivosVazios.append(i)
    return(arquivosVazios)
def pdbVazio():
    diret = "./pdbs/"
    arqs = arquivosNaPastaPdb()
    arquivosVazios = []
    for i in arqs:
        atomo = "_soAtom"
        heat = "_soHetatm"
        tam = os.path.getsize(diret+i)
        if tam < 3000: # se for arquivo pequeno considera sem dados
            if (atomo not in i) and (heat not in i): # para excluir os arquivos que foram separados em make files
                arquivosVazios.append(i)
    return(arquivosVazios)

def make_zipfile(output_filename, source_dir):
    relroot = os.path.abspath(os.path.join(source_dir, os.pardir))
    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk(source_dir):
            # add directory (needed for empty dirs)
            zip.write(root, os.path.relpath(root, relroot))
            for file in files:
                filename = os.path.join(root, file)
                if os.path.isfile(filename): # regular files only
                    arcname = os.path.join(os.path.relpath(root, relroot), file)
                    zip.write(filename, arcname)
def unzipFolder(arq, destino):
    zip = zipfile.ZipFile(arq)
    zip.extractall(destino)
    
def retornaDigito(st):
    l = ''
    for t in st:
        if (t.isdigit()) or (t == '.'):
            l = l+t
    pos = l.rfind('.')
    rs = l[:pos]
    if rs[0] == '.':
        rr = rs[1:]
    else:
        rr = rs
    return rr.strip()
def pegaPosicaoExpPred(): # pega as posicoes das colunas eperimentaal e predito
    posPre = 0
    posExp = 0
    arquivo = "./outputFiles/resultadoTreino.csv"
    fo = open(arquivo, 'r')
    lines = fo.readlines() # Lê as linhas e separa em um vetor
    firstLine = lines.pop(0).split(",") #Remove a primeira linha
    posPre = firstLine.index("Predicted")
    posExp = firstLine.index(" Experimental\n") # tem que ter espaco e \n
    return posPre,posExp

def extraiNumeros(input_str):
    if input_str is None or input_str == '':
        return 0
    out_number = ''
    for ele in input_str:
        if ele.isdigit():
            out_number += ele
    return float(out_number)  
