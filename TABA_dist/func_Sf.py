# coding=utf-8
from PyQt4 import QtGui  # Import the PyQt4 module we'll need
def calc_RMSE(y_obs,y_pred):
    """Function to calculate root-mean squared error(RMSE)"""
    # Import library
    import numpy as np

    # Get the length of the array    
    n = len(y_obs)
    
    # Make sure we have arrays
    yo = np.array(y_obs)
    yp = np.array(y_pred)
    
    # Get the mean of experimental activities
    yo_mean = np.mean(yo)
    
    # Looping through arrays
    rmse0 = 0.0
    for i in range(n):
        rmse0 = (yp[i] - yo_mean)**2

    # Calculate RMSE    
    rmse = np.sqrt(rmse0/(n-1))
    
    return rmse

def calc_chi2(y_obs,y_pred):
    """Function to calculate chi-squared"""
    
    # Import library
    import numpy as np

    # Get the length of the array    
    n = len(y_obs)
    
    # Make sure we have arrays
    yo = np.array(y_obs)
    yp = np.array(y_pred)

    # Looping through arrays
    chi2 = 0.0
    for i in range(n):
        if yp[i] != 0:
            chi2 += np.abs(((yo[i]-yp[i])**2)/yp[i])
        
    return chi2
        
def cross_validated_LOO_r2(n,method_in):
    """Function to call SF for LOO files"""
    import numpy as np
    
    # Set uo empty list
    q = []
    
    # Looping through CSV files
    for i in range(1000):
        # Fix the number of characters
        my_str_3_char = str(i)
        if len(my_str_3_char)< 4:
            my_str_lig = str((3-len(my_str_3_char) )*"0")+my_str_3_char
            my_str = my_str_lig # We must have three columns
        else:
            my_str = my_str_3_char
        
        # Try to open
        diretorio = "./adjustmentFunctions/"
        try:
            csv_file_in = diretorio+"loo_file_"+my_str+".csv"
            fo1 = open(csv_file_in,"r")
            fo1.close()
            
            # Call SF() to get q2 values
            q.append(SF_CV(csv_file_in,n,method_in))
            
        except IOError:
            break       # Break once finished
    
    q_array =  np.array(q)
    q2 = np.mean(q_array)        # It returns the mean we could easily change to minimum
    
    return q2   


def SF_CV(my_scoring_function_file,num_ind_var,my_mlr_method_in):
    """ Scoring function (SF) function and returns R2"""
    
    # Import libraries
    import scikit_regression_methods_v001z_works as reg_method001     
    import numpy as np
    
    # Calls function read_csv_4_SF()
    my_first_line, num_var, x,y = read_csv_4_SF(my_scoring_function_file,num_ind_var)
    
    # Calls filter_data_4_SF
    my_indep_variables,z = filter_data_4_SF(x,y,num_var)

    # Creates regression model (return self.b, self.R2, self.R2adj,self.sd,self.F,self.Fpv)
    '''
    my_R_p -> p-value pearson
    my_rho_p -> p-value Spearman
    '''
    SF_model = reg_method001.Multvar_reg_modeling(num_var,y,z,'y',my_indep_variables,my_mlr_method_in)
         
    n_obs,my_model_coefs,my_R,my_R2,my_R_p_value,my_R2_adj,my_sd,my_rho,my_rho_p,\
    my_f_stat,my_errors,Q_factor,y_pred = SF_model.summary()
    #print("spearman 1---", my_rho)
    # Double my_errors values
    my_d_errors = np.zeros(len(my_errors) ,dtype=float)
    for i in range(len(my_errors)):
        my_d_errors[i] = 2*my_errors[i]    
    
    # Calls function to generate models
    p1,my_model_string0 = gen_model_4_SF(num_var,my_model_coefs,my_first_line,x,y) 
       
    # Return R
    return my_R2
    
def SF(my_scoring_function_file,num_ind_var,my_mlr_method_in):
    """ Scoring function (SF) function"""
    # Import libraries
    import scikit_regression_methods_v001z_works as reg_method001      
    import numpy as np
    
    # Append to SF.log file
    diretorio = "./outputFiles/"
    SF_log_fo = open(diretorio+"SF.log","w")
    SF_csv_fo = open(diretorio+"SF.csv","w")

    # Calls function read_csv_4_SF()
    my_first_line, num_var, x,y = read_csv_4_SF(my_scoring_function_file,num_ind_var)
    
    
    # Calls filter_data_4_SF
    my_indep_variables,z = filter_data_4_SF(x,y,num_var)
    #print("ind variavel", my_indep_variables,"\n",z)
    # Creates regression model (return self.b, self.R2, self.R2adj,self.sd,self.F,self.Fpv)

    
    SF_model = reg_method001.Multvar_reg_modeling(num_var,y,z,'y',my_indep_variables,my_mlr_method_in) 
    n_obs,my_model_coefs,my_R,my_R2,my_R_p_value,my_R2_adj,my_sd,my_rho,my_rho_p,\
    my_f_stat,my_errors,Q_factor,y_pred = SF_model.summary()
    #print("spearman 2---", my_rho)
    # Double my_errors values
    my_d_errors = np.zeros(len(my_errors),dtype=float)
    for i in range(len(my_errors)):
        my_d_errors[i] = 2*my_errors[i]    

    # Calls function to generate models
    p1,my_model_string0 = gen_model_4_SF(num_var,my_model_coefs,my_first_line,x,y) 
    # Call generate_LOO_files()
    #generate_LOO_files(z,y,my_mlr_method_in,my_first_line)
    
    # Clean my_model_string0
    
    my_model_string1 = my_model_string0.replace(" ","")
    my_model_string2 = my_model_string1.replace("++","+")
    my_model_string3 = my_model_string2.replace("+-","-")
    my_model_string4 = my_model_string3.replace("-"," - ")
    my_model_string5 = my_model_string4.replace("+"," + ")
    # Call cross_validated_LOO_r2()
    my_q2_loo = cross_validated_LOO_r2(num_ind_var,my_mlr_method_in)
    
    # Call calc_chi2()
    my_chi2 = calc_chi2(y,y_pred)
    
    # Call calc_RMSE()
    my_RMSE = calc_RMSE(y,y_pred)
    
    # Write results
    SF_log_fo.write("\n\n######################################### MODEL GENERATOR ###############################################\n")
    SF_log_fo.write("\n\nFile: "+my_scoring_function_file)
    SF_log_fo.write("\n\nRegression equation : \nPred. "+str(my_first_line[len(my_first_line)-1])+" = "+my_model_string5)
    for i in range(len(my_d_errors)):
        if i == 0:
            SF_log_fo.write('\nError for c(0)\t:% -5.3f  '%my_d_errors[i] )
        else:
            SF_log_fo.write('\nError for '+my_first_line[i-1]+'\t:% -5.3f  '%my_d_errors[i]  ) 
    SF_log_fo.write("\n\nBest fit equation between observed and predicted information:"+str(p1))
    SF_log_fo.write("\n\nN                    : "+str(n_obs))
    SF_log_fo.write('\nStandard deviation   :%6.5f'% my_sd)
    SF_log_fo.write('\nR                    :%6.5f' % my_R )
    SF_log_fo.write('\nR-squared            :%6.5f' % my_R2 )
    SF_log_fo.write('\np-value1              :%6.5f' % my_R_p_value) # pearson
    SF_log_fo.write('\nAdjusted R-square    :%6.5f' % my_R2_adj )
    SF_log_fo.write('\nSpearman correlation :%6.5f' % my_rho )
    SF_log_fo.write('\np-value2              :%6.5f' % my_rho_p ) # spearman
    SF_log_fo.write('\nQuality factor (Q)   :%6.5f' % Q_factor )
    SF_log_fo.write('\nq-squared for LOO    :%6.5f' % my_q2_loo )
    SF_log_fo.write('\nF-stat               :%6.5f' % my_f_stat )
    SF_log_fo.write('\nChi-squared          :%6.5f' % my_chi2 )
    SF_log_fo.write('\nRMSE                 :%6.5f' % my_RMSE )
    
    # Set up my_rho_p to 0.000 for  my_rho_p < 0.0001
    if my_rho_p < 0.0001:
        my_rho_p = 0.000
    SF_csv_fo.write(my_scoring_function_file+","+\
                          str(my_R2)+","+str(my_R2_adj)+","+str(my_sd)+","+\
                          str(my_rho)+","+str(my_rho_p)+"\n")
    
    
def read_csv_4_SF(my_scoring_function_file_in,num_ind_var_in):
    """Function to read CSV file"""
    # Import libraries
    import csv
    import numpy as np
    
    # Reads input file name and polynomial equation degree
    input_file_name = my_scoring_function_file_in
    var = num_ind_var_in
    # Reads first line to get headers
    csv_in = open(input_file_name,"r") 
    get_csv_lines = csv.reader(csv_in)
    
    # Reads CSV file first line only
    
    for line in get_csv_lines: 
        break
    csv_in.close()
    
    # Reads CSV file and skips first line
    csv = np.genfromtxt (input_file_name, delimiter=",", skip_header = 1) 
    # Gets each column from CSV file
    y = csv[:,var] 
    x = csv[:,0:var]
    return line,var, x,y
    
def filter_data_4_SF(x,y,var):
    """Function to filter data"""
    import numpy as np
    
    # Defines numbers of rows and columns 
    columns = var
    rows = len(y)

    # Sets up a matrix
    z = np.array([[0]*columns]*rows,float)           # np.array([[0]*column]*row,float)

    # looping through x to get independent variable columns
    for i in range(rows):
        for j in range(columns):
            z[i,j] = x[i,j]
        
    # Looping through to create a list with independent variables
    my_indep_variables = []
    for i in range(columns):
        my_indep_variables.append("x"+str(i+1))
 
    return my_indep_variables,z

def gen_model_4_SF(var,regression_coefs,first_line,x_in,y_in):
    """Function to generate models"""
    import numpy as np
    
    # Looping through to generate model
    p = 0
    total_variables = var + 1
    SF_model_string = ""
    QtGui.QApplication.processEvents() # para não travar
    for i in range(total_variables):
        
        if i == 0:
            p += regression_coefs[i]
            SF_model_string += str("%5.6f"%regression_coefs[i])+"+" 
        else:
            p += regression_coefs[i]*x_in[:,i-1]
            SF_model_string += str("+%5.6f"%regression_coefs[i])+"*("+first_line[i-1]+")"
    
    # Generate best fit line for experimental and computational model (least-squares polynomial fitting) 
    z = np.polyfit(y_in,p, 1)
    p1 = np.poly1d(z)
    return p1,SF_model_string   

# comentar proxima funcao
'''
def show_SF():
    """Function to show SF.log on screen"""
    
    # Import library
    import sys
    diretorio = "./outputFiles/"
    # Try to open SF.log
    try:
        fol = open(diretorio+"SF.log","r")
    except IOError:
        sys.exit("\nI can't find SF.log file! Finishing execution!(1)")
    
    # Looping through SF.log
    for line in fol:
        print(line)
    
    fol.close()
'''
def monta_SF():
    """Function para montar sf geral"""
    
    # Import library
    import sys
    diretorio = "./outputFiles/"
    # Try to open SF.log
    try:
        fo1 = open(diretorio+"SF.log","r")
    except IOError:
        sys.exit("\nI can't find SF.log file! Finishing execution!(1)")

    # Looping through SF.log
    linhaGeral = ""
    v1 = "Pred. Log(Ki) =" 
    v2 = "N                    :"
    v3 = "Standard deviation   :" 
    v4 = "R                    :"
    v5 = "R-squared            :"
    v6 = "p-value1              :"
    v7 = "Adjusted R-square    :"
    v8 = "Spearman correlation :"
    v9 = "p-value2              :" ## ha 2 p-value ?????
    v10 = "Quality factor (Q)   :"
    v11 = "q-squared for LOO    :"
    v12 = "F-stat               :"
    v13 = "Chi-squared          :"
    v14 = "RMSE                 :"
    for line in fo1:
        if (v1 in line):
            linhaGeral = linhaGeral+ line.replace(v1,"")+","
        if (v2 in line):
            linhaGeral = linhaGeral+ line.replace(v2,"")+","
        if (v3 in line):
            linhaGeral = linhaGeral+ line.replace(v3,"")+","
        if (v4 in line):
            linhaGeral = linhaGeral+ line.replace(v4,"")+","
        if (v5 in line):
            linhaGeral = linhaGeral+ line.replace(v5,"")+","
        if (v6 in line):
            linhaGeral = linhaGeral+ line.replace(v6,"")+","
        if (v7 in line):
            linhaGeral = linhaGeral+ line.replace(v7,"")+","
        if (v8 in line):
            linhaGeral = linhaGeral+ line.replace(v8,"")+","
        if (v9 in line):
            linhaGeral = linhaGeral+ line.replace(v9,"")+","
        if (v10 in line):
            linhaGeral = linhaGeral+ line.replace(v10,"")+","
        if (v11 in line):
            linhaGeral = linhaGeral+ line.replace(v11,"")+","
        if (v12 in line):
            linhaGeral = linhaGeral+ line.replace(v12,"")+","
        if (v13 in line):
            linhaGeral = linhaGeral+ line.replace(v13,"")+","
        if (v14 in line):
            linhaGeral = linhaGeral+ line.replace(v14,"")
    linhaGeral = linhaGeral.replace("\n","")                 
    
    fo1.close()
    return(linhaGeral+"\n")
    
       