# coding=utf-8
from func_ContaInterMolLeArquivos import read_PDB_return_coord_and_lines
from func_Gerais import grava
import numpy as np
from PyQt4 import QtGui  # Import the PyQt4 module we'll need

def mediaDistanciaPorPdb(arquivosParaLer,distancia,conjunto,progressBar):
    # conjunto -> qual o conjunto que e para fazer a distancia media
    """
    calcula a media da distancia entre os atomos que satisfazem uma distancia em cada arquivo pdb (individual)
    o paramentro dataSet diz qual dataset sera utilizado para calcular a distancia:
    podera usar somente o arquivo treino ou podera calcular individualmente nos arquivos de treino teste e experimento do usuario
    """
    textoFinal = ''
    tam=int(34)
    conta = np.zeros(tam,dtype = int)
    soma = np.zeros(tam,dtype = float)
    cont = 0
    progresso = 0
    quantidadeArquivos = len(arquivosParaLer)
    var = 100/quantidadeArquivos
    QtGui.QApplication.processEvents() # para não travar usar antes de loops
    for prot in arquivosParaLer:
        progresso = progresso+var
        progressBar.setValue(progresso) 
        cont = cont +1 #quantidade arquivos processados

        diretorio = "./pdbs/"
        arquivo = prot.strip() # nome do arquivo pdb que est'em pdbsProteinas
        arquivo = arquivo.lower()
        protArq=diretorio+arquivo+"_soAtom.pdb" # coloca a terminacao para ler o arquivo so de proteinas que foram separados
        ligArq=diretorio+arquivo+"_soHetatm.pdb" # coloca a terminacao para ler o arquivo so de ligantes que foram separados
        #parAtm = ['CC','CN','CO','CS','CP','CF','CBr','CCl','CI','CAt','NN','NO','NS','NP','NF','NBr','NCl','NI','NAt','OO','OS','OP','OF','OBr','OCl','OI','OAt','SS','SP','SF','SBr','SCl','SI','SAt'] 
        # Call read_PDB_return_coor_and_lines()
        x1,y1,z1,l1 = read_PDB_return_coord_and_lines(protArq)
        x2,y2,z2,l2 = read_PDB_return_coord_and_lines(ligArq)
   
        #print ("x1----------------------------->",x1,y1,z1,l1,x2,y2)
        # Get the length of the arrays
        n1 = len(x1)
        n2 = len(x2)
        QtGui.QApplication.processEvents() # para não travar usar antes de loops
        for i in range(n1): # proteinas  
            QtGui.QApplication.processEvents() # para não travar usar antes de loops
            for j in range(n2): # ligantes
                d =  np.sqrt( ((x1[i] - x2[j] )**2) + ((y1[i] - y2[j])**2) + ((z1[i] - z2[j])**2))
                if d <= distancia:

#---------- CC CN  CO  CS  CP  CF  CBR CCL CI  CAT  

                    if (l1[i][12:14]).strip() == "C" and (l2[j][12:14]).strip()  == "C":
                        conta[0] += 1
                        soma[0] = soma[0]+d                   
                    elif (l1[i][12:14]).strip() == "C" and (l2[j][12:14]).strip() == "N":
                        conta[1] += 1
                        soma[1] = soma[1]+d                                 
                    elif (l1[i][12:14]).strip() == "C" and (l2[j][12:14]).strip() == "O":
                        conta[2] += 1
                        soma[2] = soma[2]+d                     
                    elif (l1[i][12:14]).strip() == "C" and (l2[j][12:14]).strip() == "S":
                        conta[3] += 1
                        soma[3] = soma[3]+d 
                    elif (l1[i][12:14]).strip() == "C" and (l2[j][12:14]).strip() == "P":
                        conta[4] += 1
                        soma[4] = soma[4]+d
                    elif (l1[i][12:14]).strip() == "C" and (l2[j][12:14]).strip() == "F": 
                        conta[5] += 1
                        soma[5] = soma[5]+d 
                    elif (l1[i][12:14]).strip() == "C" and (l2[j][12:14]).strip() == "Br":
                        conta[6] += 1
                        soma[6] = soma[6]+d  
                    elif (l1[i][12:14]).strip() == "C" and (l2[j][12:14]).strip() == "Cl":
                        conta[7] += 1
                        soma[7] = soma[7]+d                      
                    elif (l1[i][12:14]).strip() == "C" and (l2[j][12:14]).strip() == "I":                    
                        conta[8] += 1
                        soma[8] = soma[8]+d  
                    elif (l1[i][12:14]).strip() == "C" and (l2[j][12:14]).strip() == "At":
                        conta[9] += 1
                        soma[9] = soma[9]+d                  
                    #---------- NN  NO  NS  NP  NF  NBR NCL NI  NAT
                    elif (l1[i][12:14]).strip() == "N" and (l2[j][12:14]).strip() == "N":  
                        conta[10] += 1
                        soma[10] = soma[10]+d 
                    elif (l1[i][12:14]).strip() == "N" and (l2[j][12:14]).strip() == "O":
                        conta[11] += 1
                        soma[11] = soma[11]+d
                    elif (l1[i][12:14]).strip() == "N" and (l2[j][12:14]).strip() == "S":
                        conta[12] += 1
                        soma[12] = soma[12]+d
                    elif (l1[i][12:14]).strip() == "N" and (l2[j][12:14]).strip() == "P":
                        conta[13] += 1
                        soma[13] = soma[13]+d            
                    elif (l1[i][12:14]).strip() == "N" and (l2[j][12:14]).strip() == "F":
                        conta[14] += 1
                        soma[14] = soma[14]+d 
                    elif (l1[i][12:14]).strip() == "N" and (l2[j][12:14]).strip() == "Br":
                        conta[15] += 1
                        soma[15] = soma[15]+d 
                    elif (l1[i][12:14]).strip() == "N" and (l2[j][12:14]).strip() == "Cl":
                        conta[16] += 1
                        soma[16] = soma[16]+d
                    elif (l1[i][12:14]).strip() == "N" and (l2[j][12:14]).strip() == "I":
                        conta[17] += 1
                        soma[17] = soma[17]+d 
                    elif (l1[i][12:14]).strip() == "N" and (l2[j][12:14]).strip() == "At":
                        conta[18] += 1
                        soma[181] = soma[18]+d 
                    #-------- OO  OS  OP  OF  OBR OCL OI  OAT 
                    elif (l1[i][12:14]).strip() == "O" and (l2[j][12:14]).strip() == "O":  
                        conta[19] += 1
                        soma[19] = soma[19]+d 
                    elif (l1[i][12:14]).strip() == "O" and (l2[j][12:14]).strip() == "S":
                        conta[20] += 1
                        soma[20] = soma[20]+d 
                    elif (l1[i][12:14]).strip() == "O" and (l2[j][12:14]).strip() == "P":
                        conta[21] += 1
                        soma[21] = soma[21]+d            
                    elif (l1[i][12:14]).strip() == "O" and (l2[j][12:14]).strip() == "F":
                        conta[22] += 1
                        soma[22] = soma[22]+d        
                    elif (l1[i][12:14]).strip() == "O" and (l2[j][12:14]).strip() == "Br":
                        conta[23] += 1
                        soma[23] = soma[23]+d 
                    elif (l1[i][12:14]).strip() == "O" and (l2[j][12:14]).strip() == "Cl":
                        conta[24] += 1
                        soma[24] = soma[24]+d                                         
                    elif (l1[i][12:14]).strip() == "O" and (l2[j][12:14]).strip() == "I":
                        conta[25] += 1
                        soma[25] = soma[25]+d 
                    elif (l1[i][12:14]).strip() == "O" and (l2[j][12:14]).strip() == "At":
                        conta[26] += 1
                        soma[26] = soma[26]+d                                          
                    #-------- SS  SP  SF  SBR SCL SI  SAT
                    elif (l1[i][12:14]).strip() == "S" and (l2[j][12:14]).strip() == "S":  
                        conta[27] += 1
                        soma[27] = soma[27]+d 
                    elif (l1[i][12:14]).strip() == "S" and (l2[j][12:14]).strip() == "P" :
                        conta[28] += 1
                        soma[28] = soma[28]+d               
                    elif (l1[i][12:14]).strip() == "S" and (l2[j][12:14]).strip() == "F" :
                        conta[29] += 1
                        soma[29] = soma[29]+d 
                    elif (l1[i][12:14]).strip() == "S" and (l2[j][12:14]).strip() == "Br":
                        conta[30] += 1
                        soma[30] = soma[30]+d 
                    elif (l1[i][12:14]).strip() == "S" and (l2[j][12:14]).strip() == "Cl":
                        conta[31] += 1
                        soma[31] = soma[31]+d     
                    elif (l1[i][12:14]).strip() == "S" and (l2[j][12:14]).strip() == "I":
                        conta[32] += 1
                        soma[32] = soma[32]+d 
                    elif (l1[i][12:14]).strip() == "S" and (l2[j][12:14]).strip() == "At":
                        conta[33] += 1
                        soma[33] = soma[33]+d  
                                                                                                     
    #calcula media de cada interacao com os dados gerados acima
        texto = ''
        QtGui.QApplication.processEvents() # para não travar usar antes de loops
        for a in range(34):  
            if conta[a]>0:    # verifica se existe media 
                med = soma[a]/conta[a] #vetor com as medias 
            else:
                med = 0
            texto =  texto+str(med)+","
        texto = prot+","+texto[:-1]
        textoFinal = textoFinal+"\n"+texto.strip()        
        # zera contadores
        conta = np.zeros(tam,dtype = int)
        soma = np.zeros(tam,dtype = float)
        cont = 0
    atm =  "PDB,CC,CN,CO,CS,CP,CF,CBr,CCl,CI,CAt,NN,NO,NS,NP,NF,NBr,NCl,NI,NAt,OO,OS,OP,OF,OBr,OCl,OI,OAt,SS,SP,SF,SBr,SCl,SI,SAt"
    textoFinal = atm+textoFinal
    diret = "./outputFiles/"
    strDist = str(distancia)   
    conj = conjunto.upper()
    arquivoSai = diret+'medDistPdb_'+strDist+'_'+conj+'.csv'
    grava(textoFinal, arquivoSai)


    ##############################

