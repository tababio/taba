# coding=utf-8
def filtraHetatm(arquivo,tipo,ligante):
    """funcao que exclui dos arquivos soHeatm o ligante ativo (terceira coluna) que nao tem correspondente no arquivo KI (terceira coluna"""
    # Import libraries
    import sys
    cont = 0
    diretorioPdb = "./pdbs/"
    diretorioKi = "./ki/"
    arquivoPdb = diretorioPdb+arquivo+"_soHetatm.pdb"
    arquivoKi = diretorioKi+arquivo+".csv"
    texto = ""
    # Try to open PDB file
    try:
        my_PDB_fo = open(arquivoPdb,"r")
    except IOError:
        sys.exit("\nI can't file "+arquivoPdb+" file!")
    # Try to open KI file
    try:
        my_KI_fo = open(arquivoKi,"r")
    except IOError:
        sys.exit("\nI can't file "+arquivoKi+" file!")
    # Looping through PDB e KI file  
    
    listaKi = [linha.strip() for linha in my_KI_fo]
    if not ligante == "":
        listaKi =[ligante]
    tamKi = len(listaKi)     
    listaPdb = [linha.strip() for linha in my_PDB_fo]     
    tamPdb = len(listaPdb)
    listaLig = []
    for x in range(tamKi):
        if ligante == "": # o ligante vem vazio caso esteja gerando arquivos para treino e teste se virer do experimento usuário vira com o nome do ligante
            lig = pegaLiganteKi(listaKi[x]) 
            
            listaLig = [] # esvazia para poder incluir
        else:
            lig = ligante
        if lig not in listaLig: # verifica se ja nao adicionou
            listaLig.append(lig)
            for y in range(tamPdb):
                if lig in listaPdb[y]:   
                    #print("lig")
                    texto=texto+listaPdb[y]+"\n"            
    #fecha arquivo
    my_PDB_fo.close()
    my_KI_fo.close()
    # grava novo arquivo
    try:
        my_PDB_fo = open(arquivoPdb,"w")
    except IOError:
        sys.exit("\nI can't file "+arquivoPdb+" file!")
    if len(texto)>0:
        cont +=1
    my_PDB_fo.write(texto)
    my_PDB_fo.close()
    return(cont)

def pegaLiganteKi(lig):
    # pega so o lignate do arquivo KI
    lig = lig[12:]    
    pos = lig.find(",")
    if len(lig)<1:
        return "##"    
    if lig.find("(")>0:
        return lig[0:pos-1] 
    else:
        return("##")
