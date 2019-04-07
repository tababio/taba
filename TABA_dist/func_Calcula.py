# coding=utf-8
from func_TrataColunas import *
from func_Sf import *
from datetime import datetime
from func_Gerais import grava, numeroLinhas
from PyQt4 import QtGui  # Import the PyQt4 module we'll need
totalCol = 36 # numero total de colunas do arquivo para calculo de tempo

def clean_line(line_in):
    """Function to get rid of [ ] ' and spaces"""
    line0 = str(line_in)
    line00 = line0.replace(" ","")
    line000 = line00.replace("[","")
    line0000 = line000.replace("]","")
    line00000 = line0000.replace("'","")
    
    return line00000 

def generate_LOO_files(csv_in,n):
    """Function to generate LOO files for cross-validated r2"""

    #csv_in = scaled_data.csv
    my_list = []
    # Try to open csv_in
    try:
        fo1 =  open(csv_in,"r")
        csv1 = csv.reader(fo1)
    except IOError:
        mensagem = "\nI can't find"+ csv+" file! Finishing execution!(1)"
        arquivoSai = "./logs/error"+str(datetime.now())
        grava(mensagem, arquivoSai)
        sys.exit("see error in TABA/logs folder")
   
    # Get first line
    for line in csv1:
        first_line =  line
        break
    # Get data
    for line in csv1:
        my_list.append(line)
    fo1.close()
 
    for i in range(len(my_list)):
        # Write LOO files
        # Fix the number of characters
        diretorio = "./adjustmentFunctions/"
        my_str_3_char = str(i)
        if len(my_str_3_char)< 4:
            my_str_lig = str((3-len(my_str_3_char) )*"0")+my_str_3_char
            my_str = my_str_lig # We must have three columns
        else:
            my_str = my_str_3_char
        fo1 = open(diretorio+"loo_file_"+my_str+".csv","w")
        aux0 = clean_line(str(first_line))
        fo1.write(aux0+"\n")
        for j in range(len(my_list)):
            aux1 = clean_line(str(my_list[j])) 
            fo1.write(aux1+"\n")

            if i != j:
                aux1 = clean_line(str(my_list[j])) 
                fo1.write(aux1+"\n")
    
        fo1.close()
        
def scale_data():
    """Function to scale explanatory variable data"""
    
    # Import libraries
    from sklearn import preprocessing
    import numpy as np
    
    # Read first line
    diretorio = "./adjustmentFunctions/"
    try:
        f = open(diretorio+"prep_data.csv","r")
        first_line = f.readline()
        #print("\nExplanatory and response variables: ",end="")
    except IOError:
        mensagem = "\nI can't find prep_data.csv file! Finishing execution!!!"
        arquivoSai = "./logs/error"+str(datetime.now())
        grava(mensagem, arquivoSai)
        sys.exit("see error in TABA/logs folder")
        
    f.close()
    
    # Read data
    fo1 = np.genfromtxt(diretorio+"prep_data.csv",delimiter = ",",skip_header = 1)
    # Get number of columns and rows
    # caso não tenha ligante ativo dara erro
    try:
        cols = len(fo1[1,:])
        rows = len(fo1[1:,0])
    except IndexError:
        mensagem = "There is some compatibility problem in the selected structures."+"\n"+"Probably the Type of Affinity does not correspond to the others datas. Try to generate a new experiment with a correct Type of Affinity"
        arquivoSai = "./logs/error"+str(datetime.now())
        grava(mensagem, arquivoSai)
        sys.exit("see error in TABA/logs folder")
 
    # Explanatory variable data
    X = fo1[:,:cols-1]
    # Response variable data
    y = fo1[:,cols-1]
        
    # Scale it with unit-variance scaling and mean centering
    X_scaled = preprocessing.scale(X)
    # Open scaled_data.csv
    diretorio = "./adjustmentFunctions/"
    fo2 = open(diretorio+"scaled_data.csv","w")    
    # Write new csv file
    fo2.write(first_line)   # Write headers
    
    # Looping through numerical data
    for i in range(0,rows+1):# ----> soma 1 para pegar última linha (09/111/2018)
        line_aux = ""
        for j in range(cols-1):
            line_aux += ","+str(X_scaled[i,j])
        fo2.write(line_aux[1:]+","+str(y[i])+"\n")
    fo2.close()
#============================================================================ 
def calcula3(csv_file1,col1,col2,col3, protocolo):   
    ''' se a coluna só tiver valores = 0 não funciona '''
    # Call  prep_3_col_csv_file()
    # colunaNula retorna falso se so tiver valores 0
    colunaNula = prep_3_col_csv_file(csv_file1,col1,col2,col3)  # This function generate prep_data.csv file
    if not colunaNula:# se tiver coluna nula não roda
        linha = chamaSf(protocolo)
        return linha
    else:
         
        return("")         
#-------------------------------------------------------------------------------
def calcula4(csv_file1,col1,col2,col3,col4, protocolo):   
    ''' se a coluna só tiver valores = 0 não funciona '''
    # Call  prep_4_col_csv_file()
    # colunaNula retorna falso se so tiver valores 0
    colunaNula = prep_4_col_csv_file(csv_file1,col1,col2,col3,col4)  # This function generate prep_data.csv file
    if not colunaNula:# se tiver coluna nula não roda
        linha = chamaSf(protocolo)
        return linha
    else:
         
        return("")         
#-------------------------------------------------------------------------------
def calcula5(csv_file1,col1,col2,col3,col4,col5, protocolo):   
    ''' se a coluna só tiver valores = 0 não funciona '''
    # Call  prep_4_col_csv_file()
    # colunaNula retorna falso se so tiver valores 0
    colunaNula = prep_5_col_csv_file(csv_file1,col1,col2,col3,col4,col5)  # This function generate prep_data.csv file
    if not colunaNula:# se tiver coluna nula não roda
        linha = chamaSf(protocolo)
        return linha
    else:
          
        return("")   
#-------------------------------------------------------------------------------
def calcula6(csv_file1,col1,col2,col3,col4,col5,col6, protocolo):   
    ''' se a coluna só tiver valores = 0 não funciona '''
    # Call  prep_4_col_csv_file()
    # colunaNula retorna falso se sótiver valores 0
    colunaNula = prep_6_col_csv_file(csv_file1,col1,col2,col3,col4,col5,col6)  # This function generate prep_data.csv file
    if not colunaNula:# se tiver coluna nula não roda
        linha = chamaSf(protocolo)
        return linha
    else:
          
        return("")
#-------------------------------------------------------------------------------
def calcula7(csv_file1,col1,col2,col3,col4,col5,col6,col7, protocolo):   
    ''' se a coluna só tiver valores = 0 não funciona '''
    # Call  prep_4_col_csv_file()
    # colunaNula retorna falso se sótiver valores 0
    colunaNula = prep_7_col_csv_file(csv_file1,col1,col2,col3,col4,col5,col6,col7)  # This function generate prep_data.csv file
    if not colunaNula:# se tiver coluna nula não roda
        linha = chamaSf(protocolo)
        return linha
    else:
         
        return("")
#-------------------------------------------------------------------------------
def calcula8(csv_file1,col1,col2,col3,col4,col5,col6,col7,col8, protocolo):   
    ''' se a coluna só tiver valores = 0 não funciona '''
    # Call  prep_4_col_csv_file()
    # colunaNula retorna falso se sótiver valores 0
    colunaNula = prep_8_col_csv_file(csv_file1,col1,col2,col3,col4,col5,col6,col7,col8)  # This function generate prep_data.csv file
    if not colunaNula:# se tiver coluna nula não roda
        linha = chamaSf(protocolo)
        return linha
    else:
          
        return("")
#-------------------------------------------------------------------------------
def calcula9(csv_file1,col1,col2,col3,col4,col5,col6,col7,col8,col9,protocolo):   
    ''' se a coluna só tiver valores = 0 não funciona '''
    # Call  prep_4_col_csv_file()
    # colunaNula retorna falso se sótiver valores 0
    colunaNula = prep_9_col_csv_file(csv_file1,col1,col2,col3,col4,col5,col6,col7,col8,col9)  # This function generate prep_data.csv file
    if not colunaNula:# se tiver coluna nula não roda
        linha = chamaSf(protocolo)
        return linha
    else:
         
        return("")
#-------------------------------------------------------------------------------
def calcula10(csv_file1,col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,protocolo):   
    ''' se a coluna só tiver valores = 0 não funciona '''
    # Call  prep_4_col_csv_file()
    # colunaNula retorna falso se sótiver valores 0
    colunaNula = prep_10_col_csv_file(csv_file1,col1,col2,col3,col4,col5,col6,col7,col8,col9,col10)  # This function generate prep_data.csv file
    if not colunaNula:# se tiver coluna nula não roda
        linha = chamaSf(protocolo)
        return linha
    else:
         
        return("")
#-------------------------------------------------------------------------------
def calcula11(csv_file1,col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11,protocolo):   
    ''' se a coluna só tiver valores = 0 não funciona '''
    # Call  prep_4_col_csv_file()
    # colunaNula retorna falso se sótiver valores 0
    colunaNula = prep_11_col_csv_file(csv_file1,col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11)  # This function generate prep_data.csv file
    if not colunaNula:# se tiver coluna nula não roda
        linha = chamaSf(protocolo)
        return linha
    else:
        
        return("")
#============================================================================  
def gera_equacao3(colIn,colFin,csv_file1,metodo,progressBar):
    # para estimar duracao do processo
    texto=''
    a = colFin-1 #<------ atencao, tem que ser -1 (09/11/2018) eh a coluna do ki
    x1 = colIn
    progresso = 0
    while x1 <=(a-2):
        x2 = x1+1 
        QtGui.QApplication.processEvents() # para não travar usar antes de loops
        while x2<=(a-1):
            col1 = x1
            col2 = x2
            col3 = colFin
            linha = calcula3(csv_file1,col1,col2,col3,metodo)
            # fim calculando tempo restante
            if linha:   #verifica se linha nao e nula
                texto = texto+linha  
            x2 +=1 
        x1 +=1
        varia = 100/colFin
        progresso = progresso+varia
        progressBar.setValue(progresso)
    progressBar.setValue(0)
    return texto
#-------------------------------------------------------------------------------   
def gera_equacao4(colIn,colFin,csv_file1,metodo,progressBar):
    # para estimar duracao do processo
    texto=''
    a = colFin-1# so para teste. vale o anterior ---> retira -1 pois não pega última coluna
    x1 = colIn 
    progresso = 0
    while x1 <=(a-3):
        x2 = x1+1 
        while x2<=(a-2):   
            x3 = x2+1  
            QtGui.QApplication.processEvents() # para não travar usar antes de loops      
            while x3<=(a-1):  
                col1 = x1
                col2 = x2
                col3 = x3
                col4 = colFin    
                #print("[Colunas em processamento:",col1,col2,col3," | Metodo:",metodo," | Arquivo:",csv_file1)            
                # fim calculando tempo restante
                linha = calcula4(csv_file1,col1,col2,col3,col4,metodo)
                if linha:   #verifica se linha nao e nula
                    texto = texto+linha  
                x3 +=1 
            x2 +=1
        x1 +=1
        varia = 100/colFin
        progresso = progresso+varia
        progressBar.setValue(progresso)
    progressBar.setValue(0)
    return texto
#-------------------------------------------------------------------------------
def gera_equacao5(colIn,colFin,csv_file1,metodo,progressBar):
    # para estimar duracao do processo
    #a = colFin-1 
    texto=''
    a = colFin-1
    x1 = colIn 
    progresso = 0
    while x1 <=(a-4):
        x2 = x1+1 
        while x2<=(a-3):   
            x3 = x2+1
            while x3<=(a-2):   
                x4 = x3+1 
                QtGui.QApplication.processEvents() # para não travar usar antes de loops       
                while x4<=(a-1):  
                    col1 = x1
                    col2 = x2
                    col3 = x3
                    col4 = x4
                    col5 = colFin                
                    #print("[Colunas em processamento:",col1,col2,col3,col4," | Metodo:",metodo," | Arquivo:",csv_file1)
                    # fim calculando tempo restante                  
                    linha = calcula5(csv_file1,col1,col2,col3,col4,col5,metodo)    
                    if linha:   
                        texto = texto+linha     
                    x4 +=1 
                x3 +=1
            x2 +=1
        x1 +=1
        varia = 100/colFin
        progresso = progresso+varia
        progressBar.setValue(progresso)
    progressBar.setValue(0)
    return texto
#-------------------------------------------------------------------------------
def gera_equacao6(colIn,colFin,csv_file1,metodo,progressBar):
    # para estimar duracao do processo

    texto=''
    a = colFin-1
    x1 = colIn 
    progresso = 0
    while x1 <=(a-5):
        x2 = x1+1 
        while x2<=(a-4):   
            x3 = x2+1 
            while x3<=(a-3):   
                x4 = x3+1   
                while x4<=(a-2):   
                    x5 = x4+1   
                    QtGui.QApplication.processEvents() # para não travar usar antes de loops   
                    while x5<=(a-1):  
                        col1 = x1
                        col2 = x2
                        col3 = x3
                        col4 = x4
                        col5 = x5
                        col6 = colFin                
                  
                        # fim calculando tempo restante                         
                        linha = calcula6(csv_file1,col1,col2,col3,col4,col5,col6,metodo)    
                        if linha:   
                            texto = texto+linha              
                        x5 +=1
                    x4 +=1
                x3 +=1
            x2 +=1
        x1 +=1
        varia = 100/colFin
        progresso = progresso+varia
        progressBar.setValue(progresso)
    progressBar.setValue(0)
    return texto
#-------------------------------------------------------------------------------
def gera_equacao7(colIn,colFin,csv_file1,metodo,progressBar):
    # para estimar duracao do processo
    texto=''
    a = colFin-1
    x1 = colIn 
    progresso = 0
    while x1 <=(a-6):
        x2 = x1+1 
        while x2<=(a-5):   
            x3 = x2+1 
            while x3<=(a-4):   
                x4 = x3+1   
                while x4<=(a-3):   
                    x5 = x4+1 
                    while x5<=(a-2):   
                        x6 = x5+1     
                        QtGui.QApplication.processEvents() # para não travar usar antes de loops   
                        while x6<=(a-1):  
                            col1 = x1
                            col2 = x2
                            col3 = x3
                            col4 = x4
                            col5 = x5
                            col6 = x6
                            col7 = colFin                
                            # fim calculando tempo restante                             
                            linha = calcula7(csv_file1,col1,col2,col3,col4,col5,col6,col7,metodo)    
                            if linha:   
                                texto = texto+linha                   
                            x6 +=1
                        x5 +=1
                    x4 +=1
                x3 +=1
            x2 +=1
        x1 +=1
        varia = 100/colFin
        progresso = progresso+varia
        progressBar.setValue(progresso)
    progressBar.setValue(0)
    return texto
#-------------------------------------------------------------------------------
def gera_equacao8(colIn,colFin,csv_file1,metodo,progressBar):
    # para estimar duracao do processo
    texto=''
    a = colFin-1
    x1 = colIn 
    progresso = 0
    while x1 <=(a-7):
        x2 = x1+1 
        while x2<=(a-6):   
            x3 = x2+1 
            while x3<=(a-5):   
                x4 = x3+1   
                while x4<=(a-4):   
                    x5 = x4+1 
                    while x5<=(a-3):   
                        x6 = x5+1        
                        while x6<=(a-2):  
                            x7 = x6+1 
                            QtGui.QApplication.processEvents() # para não travar usar antes de loops       
                            while x7<=(a-1):  
                                col1 = x1
                                col2 = x2
                                col3 = x3
                                col4 = x4
                                col5 = x5
                                col6 = x6
                                col7 = x7
                                col8 = colFin                
                                # fim calculando tempo restante 
                                linha = calcula8(csv_file1,col1,col2,col3,col4,col5,col6,col7,col8,metodo)    
                                if linha:   
                                    texto = texto+linha   
                                x7 +=1
                            x6 +=1
                        x5 +=1
                    x4 +=1
                x3 +=1
            x2 +=1
        x1 +=1
        varia = 100/colFin
        progresso = progresso+varia
        progressBar.setValue(progresso)
    progressBar.setValue(0)
    return texto
#-------------------------------------------------------------------------------
def gera_equacao9(colIn,colFin,csv_file1,metodo,progressBar):
    # para estimar duracao do processo
    texto=''
    a = colFin-1
    x1 = colIn 
    progresso = 0
    while x1 <=(a-8):
        x2 = x1+1 
        while x2<=(a-7):   
            x3 = x2+1 
            while x3<=(a-6):   
                x4 = x3+1   
                while x4<=(a-5):   
                    x5 = x4+1 
                    while x5<=(a-4):   
                        x6 = x5+1        
                        while x6<=(a-3):  
                            x7 = x6+1        
                            while x7<=(a-2):
                                x8 = x7+1 
                                QtGui.QApplication.processEvents() # para não travar usar antes de loops       
                                while x8<=(a-1):  
                                    col1 = x1
                                    col2 = x2
                                    col3 = x3
                                    col4 = x4
                                    col5 = x5
                                    col6 = x6
                                    col7 = x7
                                    col8 = x8
                                    col9 = colFin                
                                    # fim calculando tempo restante  
                                    linha = calcula9(csv_file1,col1,col2,col3,col4,col5,col6,col7,col8,col9,metodo)    
                                    if linha:   
                                        texto = texto+linha                               
                                    x8 +=1
                                x7 +=1
                            x6 +=1
                        x5 +=1
                    x4 +=1
                x3 +=1
            x2 +=1
        x1 +=1
        varia = 100/colFin
        progresso = progresso+varia
        progressBar.setValue(progresso)
    progressBar.setValue(0)
    return texto
#-------------------------------------------------------------------------------
def gera_equacao10(colIn,colFin,csv_file1,metodo,progressBar):
    # para estimar duracao do processo
    texto=''
    a = colFin-1
    x1 = colIn 
    progresso = 0
    while x1 <=(a-9):
        x2 = x1+1 
        while x2<=(a-8):   
            x3 = x2+1 
            while x3<=(a-7):   
                x4 = x3+1   
                while x4<=(a-6):   
                    x5 = x4+1 
                    while x5<=(a-5):   
                        x6 = x5+1        
                        while x6<=(a-4):  
                            x7 = x6+1        
                            while x7<=(a-3):
                                x8 = x7+1        
                                while x8<=(a-2):  
                                    x9 = x8+1       
                                    QtGui.QApplication.processEvents() # para não travar usar antes de loops 
                                    while x9<=(a-1): 
                                        col1 = x1
                                        col2 = x2
                                        col3 = x3
                                        col4 = x4
                                        col5 = x5
                                        col6 = x6
                                        col7 = x7
                                        col8 = x8
                                        col9 = x9
                                        col10 = colFin                
                                        # fim calculando tempo restante                                        
                                        linha = calcula10(csv_file1,col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,metodo)    
                                        if linha:   
                                            texto = texto+linha                                                                               
                                        x9 +=1
                                    x8 +=1 
                                x7 +=1
                            x6 +=1
                        x5 +=1
                    x4 +=1
                x3 +=1
            x2 +=1
        x1 +=1
        varia = 100/colFin
        progresso = progresso+varia
        progressBar.setValue(progresso)
    progressBar.setValue(0)
    return texto
#-------------------------------------------------------------------------------
def gera_equacao11(colIn,colFin,csv_file1,metodo,progressBar):
    # para estimar duracao do processo
    texto=''
    a = colFin-1
    x1 = colIn 
    progresso = 0
    while x1 <=(a-10):
        x2 = x1+1 
        while x2<=(a-9):   
            x3 = x2+1 
            while x3<=(a-8):   
                x4 = x3+1   
                while x4<=(a-7):   
                    x5 = x4+1 
                    while x5<=(a-6):   
                        x6 = x5+1        
                        while x6<=(a-5):  
                            x7 = x6+1        
                            while x7<=(a-4):
                                x8 = x7+1        
                                while x8<=(a-3):  
                                    x9 = x8+1        
                                    while x9<=(a-2): 
                                        x10 = x9+1 
                                        QtGui.QApplication.processEvents() # para não travar usar antes de loops       
                                        while x10<=(a-1): 
                                            col1 = x1
                                            col2 = x2
                                            col3 = x3
                                            col4 = x4
                                            col5 = x5
                                            col6 = x6
                                            col7 = x7
                                            col8 = x8
                                            col9 = x9
                                            col10 = x10
                                            col11 = colFin                
                                       
                                            # fim calculando tempo restante                                              
                                            linha = calcula11(csv_file1,col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11,metodo)    
                                            if linha:   
                                                texto = texto+linha                                      
                                            x10 +=1
                                        x9 +=1
                                    x8 +=1 
                                x7 +=1
                            x6 +=1
                        x5 +=1
                    x4 +=1
                x3 +=1
            x2 +=1
        x1 +=1
        varia = 100/colFin
        progresso = progresso+varia
        progressBar.setValue(progresso)
    progressBar.setValue(0)
    return texto  
#============================================================================ 
def chama_calcula(csv_file1,metodo,num_col,cabecalho,diretorio,progressBar):
    texto = ""
    csv1 = csv_file1.replace("./outputFiles/","")
    csv = csv1.replace(".csv","")
    # Try to open SFgeral.log
    nomeArquivoParcial = "SF"+"_"+csv+"_"+metodo+"_"+str(num_col)+"cols"+".csv" 
    arquivo = diretorio+nomeArquivoParcial
    existe = False
    linhas = numeroLinhas(arquivo)
    try:
        with open(arquivo):
            existe = True
    except:
        existe = False
    if (existe == True) and (linhas > 2): # se já foi gerado o arquivo com mais de 2 linhas não gera novamente
        return True
    else:
        try:
            folGeral = open(arquivo,"w")
        except IOError:
            mensagem = "\nI can't find"+ arquivo+" file! Finishing execution!(1)"
            arquivoSai = "./logs/error"+str(datetime.now())
            grava(mensagem, arquivoSai)
            sys.exit("see error in TABA/logs folder")

            # This function will create a new csv file with data restricted to selected columns
        colIn = 2 # comeca em zero
        colFin = 37 # e a coluna do log(ki) não pode mandar arquivos com menos colunas

        # chama funcao conforme a quantidade de colunas
        
        if num_col == 3:        
            texto = gera_equacao3(colIn,colFin,csv_file1,metodo,progressBar)
        if num_col == 4:        
            texto = gera_equacao4(colIn,colFin,csv_file1,metodo,progressBar)
        if num_col == 5:
            texto = gera_equacao5(colIn,colFin,csv_file1,metodo,progressBar)
        if num_col == 6:
            texto = gera_equacao6(colIn,colFin,csv_file1,metodo,progressBar)
        if num_col == 7:
            texto = gera_equacao7(colIn,colFin,csv_file1,metodo,progressBar)
        if num_col == 8:
            texto = gera_equacao8(colIn,colFin,csv_file1,metodo,progressBar)
        if num_col == 9:
            texto = gera_equacao9(colIn,colFin,csv_file1,metodo,progressBar)
        if num_col == 10:
            texto = gera_equacao10(colIn,colFin,csv_file1,metodo,progressBar)
        if num_col == 11:
            texto = gera_equacao11(colIn,colFin,csv_file1,metodo,progressBar)
      
        #rodape = "\n"+"Metodo:"+metodo+" Arquivo:"+csv_file1
        #folGeral.write(cabecalho+texto+rodape)
        folGeral.write(cabecalho+texto)
        folGeral.close()

        return False
def chamaSf(protocolo):
    # Call scale_data()    
    scale_data()
    diretorio = "./adjustmentFunctions/"
    csv_file2 = diretorio+"scaled_data.csv"
    
    # Call get_number_of_cols()
    n_columns = get_number_of_cols(csv_file2)
        
    # Call generate_LOO_files()
    generate_LOO_files(csv_file2,n_columns)
    
    # Call SF()
    try:
        SF(csv_file2,n_columns-1,protocolo)   
    except:
        return None    
    # Call show_SF()
    #show_SF() 
    linha = monta_SF() 
    return(linha) 

