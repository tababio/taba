# coding=utf-8
# Import libraries
import csv
import sys
from PyQt4 import QtGui  # Import the PyQt4 module we'll need

def prep_3_col_csv_file(file_in,c1,c2,c3):
    """Function to preparate csv file"""  
    # Set up empty list
    list_out = []
    csv1 = retornaArquivo(file_in)
    # Looping through data
    somaC1 = 0
    somaC2 = 0
    QtGui.QApplication.processEvents() # para não travar usar antes de loops
    for line in csv1:
        line_aux0 = str(line[c1])
        line_aux1 = edit_data(line_aux0)       
        line_aux0 = str(line[c2])
        line_aux2  = edit_data(line_aux0)
        line_aux = line_aux1+","+line_aux2        
        list_out.append(line_aux+","+str(line[c3-1])+"\n")        
        # para verificar se coluna có contém 0
        if not line[c1].isalpha(): #para pular primeira linha que é alfa
            somaC1 = somaC1+float(line[c1])
            somaC2 = somaC2+float(line[c2])         
    # Open new csv file
    diretorio ="./adjustmentFunctions/"
    fo2 =  open(diretorio+"prep_data.csv","w")    
    # Looping through list_out
    for line in list_out:
        fo2.write(line)                
    fo2.close()
    if (somaC1 == 0) or (somaC2 == 0):
        return True
    else:
        return False
#------------------------------------------------------------------------------

def prep_4_col_csv_file(file_in,c1,c2,c3,c4):
    """Function to preparate csv file"""  
    # Set up empty list
    list_out = []    
    csv1 = retornaArquivo(file_in)    
    # Looping through data
    somaC1 = 0
    somaC2 = 0
    somaC3 = 0
    QtGui.QApplication.processEvents() # para não travar usar antes de loops
    for line in csv1:
        line_aux0 = str(line[c1])
        line_aux1 = edit_data(line_aux0)       
        line_aux0 = str(line[c2])
        line_aux2  = edit_data(line_aux0)        
        line_aux0 = str(line[c3])
        line_aux3 = edit_data(line_aux0)
        line_aux = line_aux1+","+line_aux2+","+line_aux3        
        list_out.append(line_aux+","+str(line[c4-1])+"\n")        
        # para verificar se coluna có contém 0
        if not line[c1].isalpha(): #para pular primeira linha que é alfa
            somaC1 = somaC1+float(line[c1])
            somaC2 = somaC2+float(line[c2])
            somaC3 = somaC3+float(line[c3])           

    # Open new csv file
    diretorio ="./adjustmentFunctions/"
    fo2 =  open(diretorio+"prep_data.csv","w")    
    # Looping through list_out
    for line in list_out:
        fo2.write(line)        
    fo2.close()
    if (somaC1 == 0) or (somaC2 == 0) or (somaC3 == 0):
        return True
    else:
        return False
#------------------------------------------------------------------------------
def prep_5_col_csv_file(file_in,c1,c2,c3,c4,c5):
    """Function to preparate csv file""" 
    # Set up empty list
    list_out = []    
    csv1 = retornaArquivo(file_in)    
    # Looping through data
    somaC1 = 0
    somaC2 = 0
    somaC3 = 0
    somaC4 = 0
    QtGui.QApplication.processEvents() # para não travar usar antes de loops
    for line in csv1:        
        line_aux0 = str(line[c1])
        line_aux1 = edit_data(line_aux0)       
        line_aux0 = str(line[c2])
        line_aux2  = edit_data(line_aux0)        
        line_aux0 = str(line[c3])
        line_aux3 = edit_data(line_aux0)        
        line_aux0 = str(line[c4])
        line_aux4 = edit_data(line_aux0)
        line_aux = line_aux1+","+line_aux2+","+line_aux3+","+line_aux4        
        list_out.append(line_aux+","+str(line[c5-1])+"\n")        
        # para verificar se coluna có contém 0
        if not line[c1].isalpha(): #para pular primeira linha que é alfa
            somaC1 = somaC1+float(line[c1])
            somaC2 = somaC2+float(line[c2])
            somaC3 = somaC3+float(line[c3])
            somaC4 = somaC4+float(line[c4])            
    # Open new csv file
    diretorio ="./adjustmentFunctions/"
    fo2 =  open(diretorio+"prep_data.csv","w")    
    # Looping through list_out
    for line in list_out:
        fo2.write(line)        
    fo2.close()
    if (somaC1 == 0) or (somaC2 == 0) or (somaC3 == 0) or (somaC4 == 0):
        return True
    else:
        return False
#------------------------------------------------------------------------------
def prep_6_col_csv_file(file_in,c1,c2,c3,c4,c5,c6):
    """Function to preparate csv file"""   
    # Set up empty list
    list_out = []    
    csv1 = retornaArquivo(file_in)    
    # Looping through data
    somaC1 = 0
    somaC2 = 0
    somaC3 = 0
    somaC4 = 0
    somaC5 = 0
    QtGui.QApplication.processEvents() # para não travar usar antes de loops
    for line in csv1:        
        line_aux0 = str(line[c1])
        line_aux1 = edit_data(line_aux0)       
        line_aux0 = str(line[c2])
        line_aux2  = edit_data(line_aux0)        
        line_aux0 = str(line[c3])
        line_aux3 = edit_data(line_aux0)        
        line_aux0 = str(line[c4])
        line_aux4 = edit_data(line_aux0)        
        line_aux0 = str(line[c5])
        line_aux5 = edit_data(line_aux0)
        line_aux = line_aux1+","+line_aux2+","+line_aux3+","+line_aux4+","+line_aux5        
        list_out.append(line_aux+","+str(line[c6-1])+"\n")
        
        # para verificar se coluna có contém 0
        if not line[c1].isalpha(): #para pular primeira linha que é alfa
            somaC1 = somaC1+float(line[c1])
            somaC2 = somaC2+float(line[c2])
            somaC3 = somaC3+float(line[c3])
            somaC4 = somaC4+float(line[c4])
            somaC5 = somaC5+float(line[c5])             
    # Open new csv file
    diretorio ="./adjustmentFunctions/"
    fo2 =  open(diretorio+"prep_data.csv","w")    
    # Looping through list_out
    for line in list_out:
        fo2.write(line)        
    fo2.close()
    if (somaC1 == 0) or (somaC2 == 0) or (somaC3 == 0) or (somaC4 == 0) or (somaC5 == 0):
        return True
    else:
        return False
#------------------------------------------------------------------------------
def prep_7_col_csv_file(file_in,c1,c2,c3,c4,c5,c6,c7):
    """Function to preparate csv file"""   
    # Set up empty list
    list_out = []    
    csv1 = retornaArquivo(file_in)    
    # Looping through data
    somaC1 = 0
    somaC2 = 0
    somaC3 = 0
    somaC4 = 0
    somaC5 = 0
    somaC6 = 0
    QtGui.QApplication.processEvents() # para não travar usar antes de loops
    for line in csv1:        
        line_aux0 = str(line[c1])
        line_aux1 = edit_data(line_aux0)       
        line_aux0 = str(line[c2])
        line_aux2  = edit_data(line_aux0)        
        line_aux0 = str(line[c3])
        line_aux3 = edit_data(line_aux0)        
        line_aux0 = str(line[c4])
        line_aux4 = edit_data(line_aux0)        
        line_aux0 = str(line[c5])
        line_aux5 = edit_data(line_aux0)        
        line_aux0 = str(line[c6])
        line_aux6 = edit_data(line_aux0)
        line_aux = line_aux1+","+line_aux2+","+line_aux3+","+line_aux4+","+line_aux5+","+line_aux6        
        list_out.append(line_aux+","+str(line[c7-1])+"\n")
        
        # para verificar se coluna có contém 0
        if not line[c1].isalpha(): #para pular primeira linha que é alfa
            somaC1 = somaC1+float(line[c1])
            somaC2 = somaC2+float(line[c2])
            somaC3 = somaC3+float(line[c3])
            somaC4 = somaC4+float(line[c4])
            somaC5 = somaC5+float(line[c5])
            somaC6 = somaC6+float(line[c6])              

    # Open new csv file
    diretorio ="./adjustmentFunctions/"
    fo2 =  open(diretorio+"prep_data.csv","w")    
    # Looping through list_out
    for line in list_out:
        fo2.write(line)        
    fo2.close()
    if (somaC1 == 0) or (somaC2 == 0) or (somaC3 == 0) or (somaC4 == 0) or (somaC5 == 0) or (somaC6 == 0):
        return True
    else:
        return False
#------------------------------------------------------------------------------
def prep_8_col_csv_file(file_in,c1,c2,c3,c4,c5,c6,c7,c8):
    """Function to preparate csv file"""   
    # Set up empty list
    list_out = []    
    csv1 = retornaArquivo(file_in)    
    # Looping through data
    somaC1 = 0
    somaC2 = 0
    somaC3 = 0
    somaC4 = 0
    somaC5 = 0
    somaC6 = 0
    somaC7 = 0
    QtGui.QApplication.processEvents() # para não travar usar antes de loops
    for line in csv1:        
        line_aux0 = str(line[c1])
        line_aux1 = edit_data(line_aux0)       
        line_aux0 = str(line[c2])
        line_aux2  = edit_data(line_aux0)        
        line_aux0 = str(line[c3])
        line_aux3 = edit_data(line_aux0)        
        line_aux0 = str(line[c4])
        line_aux4 = edit_data(line_aux0)        
        line_aux0 = str(line[c5])
        line_aux5 = edit_data(line_aux0)        
        line_aux0 = str(line[c6])
        line_aux6 = edit_data(line_aux0)        
        line_aux0 = str(line[c7])
        line_aux7 = edit_data(line_aux0)
        line_aux = line_aux1+","+line_aux2+","+line_aux3+","+line_aux4+","+line_aux5+","+line_aux6+","+line_aux7        
        list_out.append(line_aux+","+str(line[c8-1])+"\n")
        
        # para verificar se coluna có contém 0
        if not line[c1].isalpha(): #para pular primeira linha que é alfa
            somaC1 = somaC1+float(line[c1])
            somaC2 = somaC2+float(line[c2])
            somaC3 = somaC3+float(line[c3])
            somaC4 = somaC4+float(line[c4])
            somaC5 = somaC5+float(line[c5])
            somaC6 = somaC6+float(line[c6])
            somaC7 = somaC7+float(line[c7])            

    # Open new csv file
    diretorio ="./adjustmentFunctions/"
    fo2 =  open(diretorio+"prep_data.csv","w")    
    # Looping through list_out
    for line in list_out:
        fo2.write(line)        
    fo2.close()
    if (somaC1 == 0) or (somaC2 == 0) or (somaC3 == 0) or (somaC4 == 0) or (somaC5 == 0) or (somaC6 == 0) or (somaC7 == 0):
        return True
    else:
        return False
#------------------------------------------------------------------------------
def prep_9_col_csv_file(file_in,c1,c2,c3,c4,c5,c6,c7,c8,c9):
    """Function to preparate csv file"""   
    # Set up empty list
    list_out = []    
    csv1 = retornaArquivo(file_in)    
    # Looping through data
    somaC1 = 0
    somaC2 = 0
    somaC3 = 0
    somaC4 = 0
    somaC5 = 0
    somaC6 = 0
    somaC7 = 0
    somaC8 = 0
    QtGui.QApplication.processEvents() # para não travar usar antes de loops
    for line in csv1:        
        line_aux0 = str(line[c1])
        line_aux1 = edit_data(line_aux0)       
        line_aux0 = str(line[c2])
        line_aux2  = edit_data(line_aux0)        
        line_aux0 = str(line[c3])
        line_aux3 = edit_data(line_aux0)        
        line_aux0 = str(line[c4])
        line_aux4 = edit_data(line_aux0)        
        line_aux0 = str(line[c5])
        line_aux5 = edit_data(line_aux0)        
        line_aux0 = str(line[c6])
        line_aux6 = edit_data(line_aux0)        
        line_aux0 = str(line[c7])
        line_aux7 = edit_data(line_aux0)        
        line_aux0 = str(line[c8])
        line_aux8 = edit_data(line_aux0)
        line_aux = line_aux1+","+line_aux2+","+line_aux3+","+line_aux4+","+line_aux5+","+line_aux6+","+line_aux7+","+line_aux8        
        list_out.append(line_aux+","+str(line[c9-1])+"\n")        
        # para verificar se coluna có contém 0
        if not line[c1].isalpha(): #para pular primeira linha que é alfa
            somaC1 = somaC1+float(line[c1])
            somaC2 = somaC2+float(line[c2])
            somaC3 = somaC3+float(line[c3])
            somaC4 = somaC4+float(line[c4])
            somaC5 = somaC5+float(line[c5])
            somaC6 = somaC6+float(line[c6])
            somaC7 = somaC7+float(line[c7]) 
            somaC8 = somaC8+float(line[c8])                 

    # Open new csv file
    diretorio ="./adjustmentFunctions/"
    fo2 =  open(diretorio+"prep_data.csv","w")    
    # Looping through list_out
    for line in list_out:
        fo2.write(line)        
    fo2.close()
    if (somaC1 == 0) or (somaC2 == 0) or (somaC3 == 0) or (somaC4 == 0) or (somaC5 == 0) or (somaC6 == 0) or (somaC7 == 0) or (somaC8 == 0):
        return True
    else:
        return False
#------------------------------------------------------------------------------
def prep_10_col_csv_file(file_in,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10):
    """Function to preparate csv file"""   
    # Set up empty list
    list_out = []    
    csv1 = retornaArquivo(file_in)    
    # Looping through data
    somaC1 = 0
    somaC2 = 0
    somaC3 = 0
    somaC4 = 0
    somaC5 = 0
    somaC6 = 0
    somaC7 = 0
    somaC8 = 0
    somaC9 = 0
    QtGui.QApplication.processEvents() # para não travar usar antes de loops
    for line in csv1:        
        line_aux0 = str(line[c1])
        line_aux1 = edit_data(line_aux0)       
        line_aux0 = str(line[c2])
        line_aux2  = edit_data(line_aux0)        
        line_aux0 = str(line[c3])
        line_aux3 = edit_data(line_aux0)        
        line_aux0 = str(line[c4])
        line_aux4 = edit_data(line_aux0)        
        line_aux0 = str(line[c5])
        line_aux5 = edit_data(line_aux0)        
        line_aux0 = str(line[c6])
        line_aux6 = edit_data(line_aux0)        
        line_aux0 = str(line[c7])
        line_aux7 = edit_data(line_aux0)        
        line_aux0 = str(line[c8])
        line_aux8 = edit_data(line_aux0)        
        line_aux0 = str(line[c9])
        line_aux9 = edit_data(line_aux0)
        line_aux = line_aux1+","+line_aux2+","+line_aux3+","+line_aux4+","+line_aux5+","+line_aux6+","+line_aux7+","+line_aux8+","+line_aux9        
        list_out.append(line_aux+","+str(line[c10-1])+"\n")        
        # para verificar se coluna có contém 0
        if not line[c1].isalpha(): #para pular primeira linha que é alfa
            somaC1 = somaC1+float(line[c1])
            somaC2 = somaC2+float(line[c2])
            somaC3 = somaC3+float(line[c3])
            somaC4 = somaC4+float(line[c4])
            somaC5 = somaC5+float(line[c5])
            somaC6 = somaC6+float(line[c6])
            somaC7 = somaC7+float(line[c7]) 
            somaC8 = somaC8+float(line[c8])    
            somaC9 = somaC9+float(line[c9])             
    

    # Open new csv file
    diretorio ="./adjustmentFunctions/"
    fo2 =  open(diretorio+"prep_data.csv","w")    
    # Looping through list_out
    for line in list_out:
        fo2.write(line)        
    fo2.close()
    if (somaC1 == 0) or (somaC2 == 0) or (somaC3 == 0) or (somaC4 == 0) or (somaC5 == 0) or (somaC6 == 0) or (somaC7 == 0) or (somaC8 == 0) or (somaC9 == 0):
        return True
    else:
        return False
#------------------------------------------------------------------------------
def prep_11_col_csv_file(file_in,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11):
    """Function to preparate csv file"""   
    # Set up empty list
    list_out = []    
    csv1 = retornaArquivo(file_in)    
    # Looping through data
    somaC1 = 0
    somaC2 = 0
    somaC3 = 0
    somaC4 = 0
    somaC5 = 0
    somaC6 = 0
    somaC7 = 0
    somaC8 = 0
    somaC9 = 0
    somaC10 = 0
    QtGui.QApplication.processEvents() # para não travar usar antes de loops
    for line in csv1:        
        line_aux0 = str(line[c1])
        line_aux1 = edit_data(line_aux0)       
        line_aux0 = str(line[c2])
        line_aux2  = edit_data(line_aux0)        
        line_aux0 = str(line[c3])
        line_aux3 = edit_data(line_aux0)        
        line_aux0 = str(line[c4])
        line_aux4 = edit_data(line_aux0)        
        line_aux0 = str(line[c5])
        line_aux5 = edit_data(line_aux0)        
        line_aux0 = str(line[c6])
        line_aux6 = edit_data(line_aux0)        
        line_aux0 = str(line[c7])
        line_aux7 = edit_data(line_aux0)        
        line_aux0 = str(line[c8])
        line_aux8 = edit_data(line_aux0)        
        line_aux0 = str(line[c9])
        line_aux9 = edit_data(line_aux0)        
        line_aux0 = str(line[c10])
        line_aux10 = edit_data(line_aux0)
        line_aux = line_aux1+","+line_aux2+","+line_aux3+","+line_aux4+","+line_aux5+","+line_aux6+","+line_aux7+","+line_aux8+","+line_aux9+","+line_aux10        
        list_out.append(line_aux+","+str(line[c11-1])+"\n")        
        # para verificar se coluna có contém 0
        if not line[c1].isalpha(): #para pular primeira linha que é alfa
            somaC1 = somaC1+float(line[c1])
            somaC2 = somaC2+float(line[c2])
            somaC3 = somaC3+float(line[c3])
            somaC4 = somaC4+float(line[c4])
            somaC5 = somaC5+float(line[c5])
            somaC6 = somaC6+float(line[c6])
            somaC7 = somaC7+float(line[c7]) 
            somaC8 = somaC8+float(line[c8])    
            somaC9 = somaC9+float(line[c9])
            somaC10 = somaC10+float(line[c10])                

    # Open new csv file
    diretorio ="./adjustmentFunctions/"
    fo2 =  open(diretorio+"prep_data.csv","w")    
    # Looping through list_out
    QtGui.QApplication.processEvents() # para não travar usar antes de loops
    for line in list_out:
        fo2.write(line)        
    fo2.close()
    if (somaC1 == 0) or (somaC2 == 0) or (somaC3 == 0) or (somaC4 == 0) or (somaC5 == 0) or (somaC6 == 0) or (somaC7 == 0) or (somaC8 == 0) or (somaC9 == 0) or (somaC10 == 0):
        return True
    else:
        return False
#=============================================================================
def get_number_of_cols(csv_file_in):
    """Function to get the number of columns in a CSV file"""
    
    # Import libraries
    import csv
    import sys
    
    # Try to open CSV file
    try:
        fo1 = open(csv_file_in,"r")
        csv1 = csv.reader(fo1)
    except IOError:
        sys.exit("IOError! I can't find "+csv_file_in+" file!.")
    
    # Get the number of columns
    QtGui.QApplication.processEvents() # para não travar usar antes de loops
    for line in csv1:
        n_cols = len(line)
        break
    return n_cols
  
  
def edit_data(s1):
    """Function to carry out some editing"""
    
    line_aux1 = s1.replace("[","")
    line_aux2 = line_aux1.replace("]","")
    line_aux3 = line_aux2.replace("\"","")
    line_aux4 = line_aux3.replace("\'","")
    
    return line_aux4

def retornaArquivo(arquivo): 
        # Try to open file
    try:
        fo1 = open(arquivo,"r")
        csv1 = csv.reader(fo1)
    except IOError:
        sys.exit("I can't find "+arquivo+" file! Finishing execution!!")
    
    return csv1