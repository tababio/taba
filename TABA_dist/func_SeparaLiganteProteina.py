# coding=utf-8
# programa para separar ligante (Heatatm) e proteina (Atom) 
import sys

from func_FiltraKi import filtraHetatm
from func_Gerais import leCsv

def separa(pdbIn):
    '''
    atencao a funcao filtraHetatm anula arquivos soHetatm que nao possuam valor de afinidade de ligantes no KI
    '''
    diretorio ="./pdbs/"
    pdbInMauisculo = pdbIn.upper()
    pdbInMinusculo = pdbIn.lower()
    
    pdbInteiro= str(pdbIn)
    pdbInteiro = pdbInteiro.replace(".pdb", "") 
    soLigante = diretorio+pdbInteiro+"_soHetatm"+".pdb"
    soProteina = diretorio+pdbInteiro+"_soAtom"+".pdb"
    # Try to open PDB file
    # espera-se que o nome do arquivo seja "XXXX.pdb" talvez seja interessante criar uma rotina para renomear em maiusculo
    try:# caso arquivo esteja maiusculo        
        arquivo = (diretorio+pdbInMauisculo).strip()
        arquivo = arquivo.replace(".PDB",".pdb") # tem que usar ponto pois tem arquivos que tem PDB
        arquivoEntrada = open(arquivo,"r")
    except IOError: # caso o arquivo esteja minusculo
        '''
        print ("|---------------------------------------|")
        print ("|  VERIFIQUE SE A PASTA PDBS ESTA LIMPA |")
        print ("|---------------------------------------|")
        '''
        sys.exit("\nI can't file: "+arquivo+" file!")
    # cria arquivos com proteinas e ligantes separados    
    proteina = open(soProteina,"w")
    ligante = open(soLigante,"w")
    for line in arquivoEntrada:        
        if line[0:6].strip() == "ATOM":  
            proteina.write(line)  
        if line[0:6].strip() == "HETATM":
            ligante.write(line)
      
    ligante.close()
    proteina.close()
def separaLiganteProteina(diretorio,arquivo,tipo,ligante):
    
    proteina = leCsv(diretorio+arquivo) # le arquivo com os pdbs a serem processados como proteinas
    contHetatm1 = 0
    for prot in proteina:
        protArq=prot.strip()
        protArq=protArq.lower()+".pdb"
        separa(protArq)
    '''
    print ("|-------------------------------------------------|")
    print ("| * Foram criados arquivos so com Hetatm          |")
    print ("| * Foram criados arquivos so com Atomo           |")
    print ("|-------------------------------------------------|") 
    print(".....Em processamento!(2)")
    '''

    for prot in proteina:
        protArq=prot.strip()
        protArq=protArq.lower()
        cont1 = filtraHetatm(protArq,tipo, ligante)# filtra os arquivos dos Hetero atomos para ficar so os que tem ki
        contHetatm1 = contHetatm1+cont1
    '''
    print("")
    print("|---------------------------------------------------------------------------|")
    print("| Foram filtrados",contHetatm1,"arquivos nao nulos com hetatm com ligante no KI       |")
    print("|---------------------------------------------------------------------------|")
    print("")
    print ("|-------------------------------------------|")
    print ("| Os arquivos HetAtm foram filtrados        |")
    print ("| para ficar so os ligantes que estao no KI |")
    print ("| (arquivos que estao no diretorio ki)      |")
    print ("| (foram obtidos no sandres)                |")
    print ("|-------------------------------------------|" ) 
    print("")
    '''
