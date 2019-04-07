# Regression methods available in scikit.learn
#
# To include Machine Learning (scikit.learn)
# Import libraries
from numpy import sqrt, diagonal, average
from scipy import c_, ones, dot, stats
import sys
from scipy.linalg import inv 
import logging
logging.basicConfig(filename='logs.log', filemode='w', level=logging.DEBUG)
'''
[03/02/2018] este import estava causando erro e nao e utilizado
#from oauthlib.oauth2.rfc6749 import catch_errors_and_unavailability
[25/01/2018] alteradas linhas 120 - 119
'''
class Multvar_reg_modeling:
    """
    Class for multiple variable regression
    """
    def __init__(self,num_indep_var,y,x,y_varnm = 'y',x_varnm = '',selected_method_in="LinearRegression"):
        """
        Initializing the Multvar_reg_modeling class. 
        """
        logging.debug('entrou scikit_regress->M24')
        self.num_indep_var = num_indep_var
        #self.num_indep_var = 3
        logging.debug('entrou scikit_regress->M25')
        self.y = y
        self.x = c_[ones(x.shape[0]),x]
        logging.debug('entrou scikit_regress->M28')
        self.y_varnm = y_varnm
        self.selected_method_in = selected_method_in 
        logging.debug('entrou scikit_regress->M31')
        if not isinstance(x_varnm,list): 
            self.x_varnm = ['const'] + list(x_varnm)
            logging.debug('entrou scikit_regress->M44')
        else:
            self.x_varnm = ['const'] + x_varnm
            logging.debug('entrou scikit_regress->M37')
        # length of vector y
        self.num_elements = len(self.y)
        
        # Estimate model using OLS
        logging.debug('entrou scikit_regress->M38')
        self.basic_statistical_analysis()
        logging.debug('entrou scikit_regress->M39')
    
    def calc_ESS(self):
        """Method to calculate Explained Sum of Squares (ESS)"""
        # Import library
        import numpy as np
        logging.debug('entrou scikit_regress->M46')
        # Get number of data points
        n = len(self.y_in)
        
        # Set up array with zeros
        aux = np.zeros(n,dtype=float)
        
        # Calculate mean self.y_in
        mean_y_in = np.mean(self.y_in)
        
        # Looping through data points (self.y_in) and self.y_pred
        for i in range(n):
                aux[i] = (self.y_pred[i] - mean_y_in)**2
        
        # Calculates Explained Sum of Squares (ESS)
        self.ess = np.sum(aux)
        logging.debug('entrou scikit_regress->M62')
    
    def calc_RSS(self):
        """Function to calculate Residual Sum of Squares (RSS)"""
        # Import library
        import numpy as np
        logging.debug('entrou scikit_regress->M68')
        # Get number of data points
        n = len(self.y_in)
        
        # Set up array with zeros
        aux = np.zeros(n,dtype=float)
        
        # Looping through data points (self.y_in) and self.y_pred
        for i in range(n):
                aux[i] = (self.y_in[i] - self.y_pred[i])**2
        
        # Calculates Residual Sum of Squares (RSS)
        self.rss = np.sum(aux)
        logging.debug('entrou scikit_regress->M81')
    def stat_analysis_of_reg_models(self):
        """Function to carry out statistical analysis of regression models"""
        # import libraries
        logging.debug('entrou scikit_regress->M85')
        from scipy.stats import spearmanr, pearsonr
        import numpy as np
        logging.debug('entrou scikit_regress->M88')
        # Set up empty list   
        data_list = []
        
        # Looping through self.y_in to get elements for list
        for i in range(len(self.y_in)):
                aux = float(self.y_in[i][0])
                data_list.append(aux)
        
        # Get Spearman's rank and Person correlation coefficient and p-value         
        self.corr_s,self.pvalue_s = spearmanr(data_list,self.y_pred)
        self.corr_p,self.pvalue_p = pearsonr(data_list,self.y_pred)
        
        # To avoid "nan"
        if str(self.corr_s) == "nan":
            self.corr_s,self.pvalue_s = 0.0,1.0
            
        # Call calc_RSS
        self.calc_RSS()
        
        # Call calc_ess
        self.calc_ESS()
                
        # Basic statistics 
        logging.debug('entrou scikit_regress->M112')
        n = len(self.y_in)                              # Number of data points
        #p = 3                                           # Number of explanatory variables
        p = self.num_indep_var
        self.r2S = self.corr_p*self.corr_p              # R-squares
        self.s_dev = np.sqrt(self.rss/(n-p-1))          # Standard deviation
        self.f_stat = (self.ess/p)*( (n-p-1)/self.rss ) # Calculate F-stat                
        logging.debug('entrou scikit_regress->M117')
    def calc_SE_M(self):
        """Function to calculate standard error (SE) Equations taken from http://zip2002.psy.unipd.it/index.php?page=sbcs"""
        # Import library
        import numpy as np
        logging.debug('entrou scikit_regress->M123')
        # Get number of rows and columns
        n = len(self.x_in)
        row = n        
        column = len(self.x_in[0])

        # Set up matrices and vectors
        # a = np.array([[0]*column]*row,float)          # A matrix row(3) x column(
        x = np.array([[0]*(column+1)]*row,float)        # A matrix row x column
        beta = np.zeros(column+1,float)                 # A vector with column elements
        self.se = np.zeros(column+1,float)              # A vector with column+1 elements
        logging.debug('entrou scikit_regress->M134')
        # Beta coefficients
        for i in range(column):
                beta[i] = self.b[i]
        
        # Looping x_in to build x matrix
        for i in range(n):
                x[i][0] = 1.0
                for j in range(column):
                        x[i][j+1] = self.x_in[i][j]
        logging.debug('entrou scikit_regress->M144')       
        # Calculate transposes
        xt = np.transpose(x)
        yt = np.transpose(self.y_in)
        
        # Calculate [xt]*[x]
        xtx = np.dot(xt,x)
        
        # Calculate inverse of xtx
        xtx_inv = inv(xtx) 
        
        # Calculate ms_res
        aux1 = np.dot(yt,self.y_in)
        aux2 = np.dot(beta,xt)
        aux3 = np.dot(aux2,self.y_in)
        epe = aux1 - aux3
        ms_res = epe/(n-column-1)
        logging.debug('entrou scikit_regress->M161')
        # looping through standard errors
        for i in range(column+1):
                if ms_res*xtx_inv[i][i]  >= 0:
                        self.se[i] = np.sqrt( ms_res*xtx_inv[i][i] )
                else:
                        self.se[i] = np.sqrt( np.abs( ms_res*xtx_inv[i][i] ) )
        
        logging.debug('entrou scikit_regress->M169')
    def gen_modelMultD2(self):
        """Function to generate model (y_pred)"""
        self.y_pred = []
    
        columns =  len(self.b) - 1  
    
        # Looping through data to generate y_pred 
        for i in range(len(self.x_in)):
            aux1 = self.b[0]
            for j in range(columns):
                aux1 += self.b[j+1]*self.x_in[i][j]
            self.y_pred.append(aux1)
            aux1 = 0
            
    def prep_y1(self):
        """Method to prepare y for scikit"""
        self.y_in = []
        for line in self.y:
            aux_list = []
            aux_list.append(line)
            self.y_in.append(aux_list)
    
    def prep_x1(self):
        """Method to prepare x for scikit"""
        self.x_in = []
        for line in self.x:
            aux_list = []
            for aux1 in line[1:]:
                aux_list.append(aux1)
            self.x_in.append(aux_list)

    def scikit_LinearRegression(self):
        """Function to generate a multiple regression model sklearn.linear_model.LinearRegression"""
        logging.debug('entrou scikit_regress->M203')
        # import libraries
        try:
            logging.debug('entrou scikit_regress->M210')
            from sklearn import linear_model
            logging.debug('entrou scikit_regress->M212')
        except  Exception:            
            #mens = str('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            import traceback
            logging.debug('entrou scikit_regress erro->M214 :'+traceback.format_exc())
            
        import numpy as np
        logging.debug('entrou scikit_regress->M216')
        import csv
        logging.debug('entrou scikit_regress->M218')
        # Try to open ml.in
        diretorio = "./inputFiles/"
        try:
            logging.debug('entrou scikit_regress->M224')
            fo = open(diretorio+"ml.in","r")
            my_csv = csv.reader(fo)
            logging.debug('entrou scikit_regress->M227')
        except IOError:
            logging.debug('entrou scikit_regress->M229:'+IOError.args)
            sys.exit("I can't find ml.in file")
        
        # Looping through data
        for line in my_csv:
            if line[0] == "LinearRegression":
                if line[1] == "True":
                    fit_in = True
                else:
                    fit_in = False
                
                if line[2] == "True":
                    norm_in = True
                else:
                    norm_in =  False
                
                if line[3] == "True":
                    copy_in = True
                else:
                    copy_in = False
                    
                break
        
        # Close file
        fo.close()

        # Set up string with regression method
        self.reg_method = "LinearRegression"

        # Get a model
        model = linear_model.LinearRegression(fit_intercept=fit_in, normalize=norm_in, copy_X=copy_in, n_jobs=-1)
        model.fit(self.x_in, self.y_in)
                
        # Generate string with regression equation
        columns = len(self.x_in[0])
        self.reg_model = str("y = %8.3f"%float(model.intercept_))
        for i in range(columns):
            aux_string = str(  " + %8.3f"%float(model.coef_[0][i])+"x"+str(i+1)  )
            self.reg_model += aux_string
        
        # Get Multiple model 
        alphas = []
        columns = len(self.x_in[0])
        alphas.append(float(model.intercept_))
        for i in range(columns):
            alphas.append(model.coef_[0][i])
    
        self.b = np.array(alphas)
        
    def scikit_Lasso(self):
        """Function to generate a multiple regression model sklearn.linear_model.Lasso"""
        
        # import library
        from sklearn import linear_model
        import numpy as np
        import csv
        import sys
        diretorio = "./inputFiles/"
        # Try to open ml.in
        try:
            fo =  open(diretorio+"ml.in","r")
            my_csv = csv.reader(fo)
        except IOError:
            sys.exit("I can't find ml.in file! Finishing program execution!")
        
        # Looping through my_csv
        #print("\nRegression parameters read from ml.in")
        for line in my_csv:
            if line[0] == "Lasso" and line[0] != "LassoCV":
                
                # For alpha_in
                alpha_in = float(line[1])
                
                # For fit_in
                if line[2] == "True":
                    fit_in = True           # True
                elif line[2] == "False":
                    fit_in = False
                else:
                    print("Problem!")
                
                # For norm_in
                if line[3] == "True":
                    norm_in = True           # True
                elif line[3] == "False":
                    norm_in = False
                else:
                    print("Problem!")
                
                # For pre_in
                if line[4] == "True":
                    pre_in = True           
                elif line[4] == "False":    # False
                    pre_in = False
                else:
                    print("Problem!")
                
                # For copy_in
                if line[5] == "True":
                    copy_in = True           # True
                elif line[5] == "False":
                    copy_in = False
                else:
                    print("Problem!")
        
                # For max_in and tol_in
                max_in = int(line[6])       # True
                tol_in = float(line[7])   
                
                # For warm_in
                if line[8] == "True":
                    warm_in = True           # True
                elif line[8] == "False":
                    warm_in = False
                else:
                    print("Problem!")
                
                # For pos_in
                if line[9] == "True":
                    pos_in = True           
                elif line[9] == "False":    # False
                    pos_in = False
                else:
                    print("Problem!")
                                    
                # For sel_in
                sel_in = str(line[10])
                
                # For rand_in
                rand_in = int(line[11])
                
                # Finish loop
                break
        
        # Close file
        fo.close()
        
        #print("Regression method: ",line[0])
        '''
        print("Alpha = %6.3f"%alpha_in)
        print("Fit intercept? "+line[2])
        print("Normalize? "+line[3])
        print("Pre compute? "+line[4])
        print("Copy x array? "+line[5])  
        print("Maximum number of iterations: %6.3e"%max_in)  
        print("Tolerance for the optimization: %6.3e"%tol_in)  
        print("Reuse the solution of the previous call to fit? "+line[8] )
        print("Force the coefficients to be positive? "+line[9])  
        print("Method for coefficients: "+line[10])
        print("Random seed: "+str(rand_in))
        '''         
        # Set up alpha_array
        alpha_array =  np.linspace(0.9*alpha_in, 1.1*alpha_in, num=3)
        
        # Set up empty list
        residuals = []
        
        # Looping through alpha_array
        for i in alpha_array:
            # Create and fit the model
            model = linear_model.Lasso( alpha = i,          # Constant that multiplies the L1 term. 
                    fit_intercept = fit_in,    # Whether to calculate the intercept for this model.
                    normalize = norm_in,       # If True, the regressors X will be normalized before regression. 
                    precompute = pre_in,       # Whether to use a precomputed Gram matrix to speed up calculations. 
                    copy_X = copy_in,          # If True, X will be copied; else, it may be overwritten.
                    max_iter = max_in,         # The maximum number of iterations.
                    tol = tol_in,              # The tolerance for the optimization:
                    warm_start = warm_in,      # When set to True, reuse the solution of the previous call to fit
                                               # as initialization.
                    positive = pos_in,         # When set to True, forces the coefficients to be positive.
                    selection = sel_in,        # If set to random, a random coefficient is updated every iteration
                                               # rather than looping over features sequentially by default. 
                    random_state = rand_in     # The seed of the pseudo random number generator that selects a
                                               # random feature to update. 
                                    ) 
            model.fit(self.x_in, self.y_in)
            residuals.append(np.mean((model.predict(self.x_in)- self.y_in)** 2) )
        
        # Get model for minimum residual
        my_min = np.min(residuals)
        y_index = residuals.index(my_min)
        model = linear_model.Lasso(alpha=alpha_array[y_index] )
        model.fit(self.x_in, self.y_in)
        
        # Generate string with regression equation
        columns = len(self.x_in[0])
        self.reg_model = str("y = %8.3f"%float(model.intercept_))
        for i in range(columns):
                aux_string = str(  " + %8.3f"%float(model.coef_[i])+"x"+str(i+1)  )
                self.reg_model += aux_string
        
        # Get Multiple model 
        alphas = []
        alphas.append(float(model.intercept_))
        for i in range(columns):
            alphas.append(model.coef_[i])
        
        # Set up array with coefficients
        self.b = np.array(alphas)   
    
    def scikit_LassoCV(self):
        """Function to generate a multiple regression model using iterated sklearn.linear_model.Lasso to
        optimize alpha"""
    
        # import library
        from sklearn import linear_model
        import numpy as np
        import csv
        import sys
        
        # Try to open ml.in
        diretorio = "./inputFiles/"
        try:
            fo =  open(diretorio+"ml.in","r")
            my_csv = csv.reader(fo)
        except IOError:
            sys.exit("I can't find ml.in file! Finishing program execution!")
        
        # Looping through my_csv
        #print("\nRegression parameters read from ml.in")
        for line in my_csv:
            if line[0] == "LassoCV":
                
                # For alpha_in
                alpha_in = float(line[1])
                
                # For fit_in
                if line[2] == "True":
                    fit_in = True           # True
                elif line[2] == "False":
                    fit_in = False
                else:
                    print("Problem!")
                
                # For norm_in
                if line[3] == "True":
                    norm_in = True           # True
                elif line[3] == "False":
                    norm_in = False
                else:
                    print("Problem!")
                
                # For pre_in
                if line[4] == "True":
                    pre_in = True           
                elif line[4] == "False":    # False
                    pre_in = False
                else:
                    print("Problem!")
                
                # For copy_in
                if line[5] == "True":
                    copy_in = True           # True
                elif line[5] == "False":
                    copy_in = False
                else:
                    print("Problem!")
        
                # For max_in and tol_in
                max_in = int(line[6])       # True
                tol_in = float(line[7])   
                
                # For warm_in
                if line[8] == "True":
                    warm_in = True           # True
                elif line[8] == "False":
                    warm_in = False
                else:
                    print("Problem!")
                
                # For pos_in
                if line[9] == "True":
                    pos_in = True           
                elif line[9] == "False":    # False
                    pos_in = False
                else:
                    print("Problem!")
                                    
                # For sel_in
                sel_in = str(line[10])
                
                # For rand_in
                rand_in = int(line[11])
                
                # Finish loop
                break
        
        # Close file
        fo.close()
        
        #print("Regression method: ",line[0])
        '''
        print("Alpha = %6.3f"%alpha_in)
        print("Fit intercept? "+line[2])
        print("Normalize? "+line[3])
        print("Pre compute? "+line[4])
        print("Copy x array? "+line[5])  
        print("Maximum number of iterations: %6.3e"%max_in)  
        print("Tolerance for the optimization: %6.3e"%tol_in)  
        print("Reuse the solution of the previous call to fit? "+line[8] )
        print("Force the coefficients to be positive? "+line[9])  
        print("Method for coefficients: "+line[10])
        print("Random seed: "+str(rand_in))
        '''
        # Set up alpha_array
        alpha_array =  np.linspace(0.1, 1.0, num=101)
        
        # Set up empty list
        residuals = []
        
        # Looping through alpha_array
        for i in alpha_array:
            # Create and fit the model
            model = linear_model.Lasso( alpha = i,          # Constant that multiplies the L1 term. 
                    fit_intercept = fit_in,    # Whether to calculate the intercept for this model.
                    normalize = norm_in,       # If True, the regressors X will be normalized before regression. 
                    precompute = pre_in,       # Whether to use a precomputed Gram matrix to speed up calculations. 
                    copy_X = copy_in,          # If True, X will be copied; else, it may be overwritten.
                    max_iter = max_in,         # The maximum number of iterations.
                    tol = tol_in,              # The tolerance for the optimization:
                    warm_start = warm_in,      # When set to True, reuse the solution of the previous call to fit
                                               # as initialization.
                    positive = pos_in,         # When set to True, forces the coefficients to be positive.
                    selection = sel_in,        # If set to ‘random, a random coefficient is updated every iteration
                                               # rather than looping over features sequentially by default. 
                    random_state = rand_in     # The seed of the pseudo random number generator that selects a
                                               # random feature to update. 
                                    ) 
            model.fit(self.x_in, self.y_in)
            residuals.append(np.mean((model.predict(self.x_in)- self.y_in)** 2) )
        
        # Get model for minimum residual
        my_min = np.min(residuals)
        y_index = residuals.index(my_min)
        model = linear_model.Lasso(alpha=alpha_array[y_index] )
        model.fit(self.x_in, self.y_in)
        
        # Generate string with regression equation
        columns = len(self.x_in[0])
        self.reg_model = str("y = %8.3f"%float(model.intercept_))
        for i in range(columns):
                aux_string = str(  " + %8.3f"%float(model.coef_[i])+"x"+str(i+1)  )
                self.reg_model += aux_string
        
        # Get Multiple model 
        alphas = []
        alphas.append(float(model.intercept_))
        for i in range(columns):
            alphas.append(model.coef_[i])
        
        # Set up array with coefficients
        self.b = np.array(alphas)
        
    def scikit_Ridge(self):
        """Function to generate multiple regression model using sklearn.linear_model.Ridge"""
        
        # Import library
        from sklearn import linear_model
        import numpy as np 
        import csv
        import sys
        diretorio = "./inputFiles/"
        # Try to open ml.in
        try:
            fo =  open(diretorio+"ml.in","r")
            my_csv = csv.reader(fo)
        except IOError:
            sys.exit("I can't find ml.in file! Finishing program execution!")
        
        # Looping through my_csv
        #print("\nRegression parameters read from ml.in")
        for line in my_csv:
            if line[0] == "Ridge" and line[0] != "RidgeCV":
                
                # For alpha_in
                alpha_in = float(line[1])   # Regularization strength; must be a positive float. It can be > 1.0
                
                # For fit_in
                if line[2] == "True":
                    fit_in = True           # True
                elif line[2] == "False":
                    fit_in = False
                else:
                    print("Problem!")
                
                # For norm_in
                if line[3] == "True":
                    norm_in = True           # True
                elif line[3] == "False":
                    norm_in = False
                else:
                    print("Problem!")
                                
                # For copy_in
                if line[4] == "True":
                    copy_in = True           # True
                elif line[4] == "False":
                    copy_in = False
                else:
                    print("Problem!")
        
                # For max_in
                if line[5] == "None":
                    max_in = None
                else:
                    max_in = int(line[5])
                
                # For tol_in
                tol_in = float(line[6])   
                
                # For solver_in
                solver_in = line[7] # It can be ‘auto’, ‘svd’, ‘cholesky’, ‘lsqr’, ‘sparse_cg’, ‘sa'
                
                # Finish loop
                break
        
        # Close file
        fo.close()
        
        #print("Regression method: ",line[0])
        '''
        print("Alpha = %6.3f"%alpha_in)
        print("Fit intercept? "+line[2])
        print("Normalize? "+line[3])
        print("Copy x array? "+line[4])  
        print("Maximum number of iterations: ",max_in)  
        print("Tolerance for the optimization: %6.3e"%tol_in)  
        print("Solver: ",solver_in)
        '''    
        # Get a model
        model = linear_model.Ridge(alpha=alpha_in, fit_intercept = fit_in, normalize = norm_in, copy_X = copy_in, 
                                     max_iter = max_in, tol = tol_in, solver = solver_in )
        model.fit(self.x_in, self.y_in)
                
        # Generate string with regression equation
        columns = len(self.x_in[0])
        self.reg_model = str("y = %8.3f"%float(model.intercept_))
        for i in range(columns):
            aux_string = str(  " + %8.3f"%float(model.coef_[0][i])+"x"+str(i+1)  )
            self.reg_model += aux_string
                
        # Get Multiple model 
        alphas = []
        columns = len(self.x_in[0])
        alphas.append(float(model.intercept_))
        for i in range(columns):
            alphas.append(model.coef_[0][i])
    
        # Set up array with coefficients
        self.b = np.array(alphas)  
    
    def scikit_RidgeCV(self):
        """Function to generate a multiple regression model using iterated sklearn.linear_model.Ridge"""
        
        # import library
        from sklearn import linear_model
        import numpy as np
        import csv
        import sys
        diretorio = "./inputFiles/"
        # Try to open ml.in
        try:
            fo =  open(diretorio+"ml.in","r")
            my_csv = csv.reader(fo)
        except IOError:
            sys.exit("I can't find ml.in file! Finishing program execution!")
        
        # Looping through my_csv
        #print("\nRegression parameters read from ml.in")
        for line in my_csv:
            if line[0] == "RidgeCV":
                
                # For alpha_in1
                alpha_in1 = float(line[1])   # Regularization strength; must be a positive float. It can be > 1.0
                
                # For alpha_in2
                alpha_in2 = float(line[2])   # Regularization strength; must be a positive float. It can be > 1.0
                
                # For delta_alpha
                delta_alpha = float(line[3])
                
                # For fit_in
                if line[4] == "True":
                    fit_in = True           # True
                elif line[4] == "False":
                    fit_in = False
                else:
                    print("Problem!")
                
                # For norm_in
                if line[5] == "True":
                    norm_in = True           # True
                elif line[5] == "False":
                    norm_in = False
                else:
                    print("Problem!")
                                
                # For copy_in
                if line[6] == "True":
                    copy_in = True           # True
                elif line[6] == "False":
                    copy_in = False
                else:
                    print("Problem!")
        
                # For max_in
                if line[7] == "None":
                    max_in = None
                else:
                    max_in = int(line[7])
                
                # For tol_in
                tol_in = float(line[8])   
                
                # For solver_in
                solver_in = line[9] # It can be ‘auto’, ‘svd’, ‘cholesky’, ‘lsqr’, ‘sparse_cg’, ‘sa'
                
                # Finish loop
                break
        
        # Close file
        fo.close()
        
        #print("Regression method: ",line[0])
        '''
        print("Minimum alpha = %6.3f"%alpha_in1)
        print("Maximum alpha = %6.3f"%alpha_in2)
        print("Delta alpha = %8.4e"%delta_alpha)  
        print("Fit intercept? "+line[4])
        print("Normalize? "+line[5])
        print("Copy x array? "+line[6])  
        print("Maximum number of iterations: ",max_in)  
        print("Tolerance for the optimization: %6.3e"%tol_in)  
        print("Solver: ",solver_in)
        '''
        # Set up alpha_array
        alpha_array =  np.arange(alpha_in1,alpha_in2,delta_alpha)
        
        # Set up empty list
        residuals = []
        
        # Looping through alpha_array
        for i in alpha_array:
            # Create and fit the model
            model = linear_model.Ridge(alpha=i,copy_X = copy_in, fit_intercept = fit_in, max_iter = max_in,
                                    normalize = norm_in, solver = solver_in, tol = tol_in)  
            model.fit(self.x_in, self.y_in)
            residuals.append(np.mean((model.predict(self.x_in)- self.y_in)** 2) )
        
        # Get model for minimum residual
        my_min = np.min(residuals)
        y_index = residuals.index(my_min)
        model = linear_model.Ridge(alpha=alpha_array[y_index],copy_X = copy_in, fit_intercept = fit_in, 
                                    max_iter = max_in, normalize = norm_in, solver = solver_in, tol = tol_in )
        model.fit(self.x_in, self.y_in)
        
        
        # Generate string with regression equation
        columns = len(self.x_in[0])
        self.reg_model = str("y = %8.3f"%float(model.intercept_))
        for i in range(columns):
            aux_string = str(  " + %8.3f"%float(model.coef_[0][i])+"x"+str(i+1)  )
            self.reg_model += aux_string
                
        # Get Multiple model 
        alphas = []
        columns = len(self.x_in[0])
        alphas.append(float(model.intercept_))
        for i in range(columns):
            alphas.append(model.coef_[0][i])
                    
        # Set up array with coefficients
        self.b = np.array(alphas)
        
    def scikit_ElasticNet(self):
        """Function to generate a multiple regression model sklearn.linear_model.ElasticNet"""
        
        # import library
        from sklearn import linear_model
        import numpy as np
        import csv
        import sys
        
        # Try to open ml.in
        diretorio = "./inputFiles/"
        try:
            fo =  open(diretorio+"ml.in","r")
            my_csv = csv.reader(fo)
        except IOError:
            sys.exit("I can't find ml.in file! Finishing program execution!")
        
        # Looping through my_csv
        #print("\nRegression parameters read from ml.in")
        for line in my_csv:
            if line[0] == "ElasticNet" and line[0] != "ElasticNetCV":
                
                # For alpha_in
                alpha_in = float(line[1])
                
                # For l1_ratio_in
                l1_ratio_in = float(line[2])
                
                # For fit_in
                if line[3] == "True":
                    fit_in = True           # True
                elif line[3] == "False":
                    fit_in = False
                else:
                    print("Problem!")
                
                # For norm_in
                if line[4] == "True":
                    norm_in = True           # True
                elif line[4] == "False":
                    norm_in = False
                else:
                    print("Problem!")
                
                # For pre_in
                if line[5] == "True":
                    pre_in = True           
                elif line[5] == "False":    # False
                    pre_in = False
                else:
                    print("Problem!")
                
                # For max_in 
                max_in = int(line[6])       # True
                
                # For copy_in
                if line[7] == "True":
                    copy_in = True           # True
                elif line[7] == "False":
                    copy_in = False
                else:
                    print("Problem!")
                
                # For tol_in
                tol_in = float(line[8]) 
                  
                # For warm_in
                if line[9] == "True":
                    warm_in = True           # True
                elif line[9] == "False":
                    warm_in = False
                else:
                    print("Problem!")
                
                # For pos_in
                if line[10] == "True":
                    pos_in = True           
                elif line[10] == "False":    # False
                    pos_in = False
                else:
                    print("Problem!")
                
                # For rand_in
                if line[11] == "None":
                    rand_in = None
                else:
                    rand_in = int(line[11])
                    
                # For sel_in
                sel_in = str(line[12])
                
                # Finish loop
                break
        
        # Close file    
        fo.close()
        
        #print("Regression method: ",line[0])
        '''
        print("Alpha = %6.3f"%alpha_in)
        print("L1 ratio %6.3f"%l1_ratio_in)
        print("Fit intercept? "+line[3])
        print("Normalize? "+line[4])
        print("Pre compute? "+line[5])
        print("Maximum number of iterations: %6.3e"%max_in)   
        print("Copy x array? "+line[7])  
        print("Tolerance for the optimization: %6.3e"%tol_in)  
        print("Reuse the solution of the previous call to fit? "+line[9] )
        print("Force the coefficients to be positive? "+line[10])  
        print("Random seed: "+str(rand_in))
        print("Method for coefficients: ",sel_in)
        '''                
        # Get a model
        model = linear_model.ElasticNet(alpha = alpha_in, l1_ratio = 0.7, fit_intercept= fit_in, 
                                    normalize = norm_in, precompute = pre_in, 
                                    max_iter = max_in, copy_X = copy_in, tol = tol_in,
                                    warm_start = warm_in, positive = pos_in, random_state = rand_in,
                                    selection = sel_in )
        model.fit(self.x_in, self.y_in)
        
        
        # Generate string with regression equation
        columns = len(self.x_in[0])
        self.reg_model = str("y = %8.3f"%float(model.intercept_))
        for i in range(columns):
                aux_string = str(  " + %8.3f"%float(model.coef_[i])+"x"+str(i+1)  )
                self.reg_model += aux_string
        
        # Get Multiple model 
        alphas = []
        alphas.append(float(model.intercept_))
        for i in range(columns):
            alphas.append(model.coef_[i])
        
        # Set up array with coefficients
        self.b = np.array(alphas)    

    def scikit_ElasticNetCV(self):
        """Function to generate a multiple regression model using iterated sklearn.linear_model.ElasticNet to
        optimize alpha"""
    
        # import library
        from sklearn import linear_model
        import numpy as np
        import csv
        import sys
        diretorio = "./inputFiles/"
        # Try to open ml.in
        try:
            fo =  open(diretorio+"ml.in","r")
            my_csv = csv.reader(fo)
        except IOError:
            sys.exit("I can't find ml.in file! Finishing program execution!")
        
        # Looping through my_csv
        #print("\nRegression parameters read from ml.in")
        for line in my_csv:
            if line[0] == "ElasticNetCV":
                
                # For alpha_in1
                alpha_in1 = float(line[1])
                
                # For alpha_in2
                alpha_in2 = float(line[2])
                
                # For step_in
                step_in = int(line[3])
                
                # For l1_ratio_in
                l1_ratio_in = float(line[4])
                
                # For fit_in
                if line[5] == "True":
                    fit_in = True           # True
                elif line[5] == "False":
                    fit_in = False
                else:
                    print("Problem!")
                
                # For norm_in
                if line[6] == "True":
                    norm_in = True           # True
                elif line[6] == "False":
                    norm_in = False
                else:
                    print("Problem!")
                
                # For pre_in
                if line[7] == "True":
                    pre_in = True           
                elif line[7] == "False":    # False
                    pre_in = False
                else:
                    print("Problem!")
                
                # For max_in 
                max_in = int(line[8])       # True
                
                # For copy_in
                if line[9] == "True":
                    copy_in = True           # True
                elif line[9] == "False":
                    copy_in = False
                else:
                    print("Problem!")
                
                # For tol_in
                tol_in = float(line[10]) 
                  
                # For warm_in
                if line[11] == "True":
                    warm_in = True           # True
                elif line[11] == "False":
                    warm_in = False
                else:
                    print("Problem!")
                
                # For pos_in
                if line[12] == "True":
                    pos_in = True           
                elif line[12] == "False":    # False
                    pos_in = False
                else:
                    print("Problem!")
                
                # For rand_in
                if line[13] == "None":
                    rand_in = None
                else:
                    rand_in = int(line[13])
                    
                # For sel_in
                sel_in = str(line[14])
                
                # Finish loop
                break
        
        # Close file    
        fo.close()
        
        #print("Regression method: ",line[0])
        '''
        print("Minimum alpha = %6.3f"%alpha_in1)
        print("Maximum alpha = %6.3f"%alpha_in2)
        print("Steps = %4d"%step_in)
        print("L1 ratio = %6.3f"%l1_ratio_in)
        print("Fit intercept? "+line[5])
        print("Normalize? "+line[6])
        print("Pre compute? "+line[7])
        print("Maximum number of iterations = %6.3e"%max_in)   
        print("Copy x array? "+line[9])  
        print("Tolerance for the optimization = %6.3e"%tol_in)  
        print("Reuse the solution of the previous call to fit? "+line[11] )
        print("Force the coefficients to be positive? "+line[12])  
        print("Random seed = "+str(rand_in))
        print("Method for coefficient: ",sel_in)
        '''
        # Set up alpha_array
        alpha_array =  np.linspace(alpha_in1, alpha_in2, num = step_in)
        
        # Set up empty list
        residuals = []
        
        # Looping through alpha_array
        for i in alpha_array:
            # Create and fit the model
            model = linear_model.ElasticNet(alpha = i, l1_ratio = l1_ratio_in, fit_intercept= fit_in, 
                                    normalize = norm_in, precompute = pre_in, 
                                    max_iter = max_in, copy_X = copy_in, tol = tol_in,
                                    warm_start = warm_in, positive = pos_in, random_state = rand_in,
                                    selection = sel_in )     
            model.fit(self.x_in, self.y_in)
            residuals.append(np.mean((model.predict(self.x_in)- self.y_in)** 2) )
        
        # Get model for minimum residual
        my_min = np.min(residuals)
        y_index = residuals.index(my_min)
        model = linear_model.ElasticNet(alpha=alpha_array[y_index],l1_ratio = l1_ratio_in, fit_intercept= fit_in, 
                                    normalize = norm_in, precompute = pre_in, 
                                    max_iter = max_in, copy_X = copy_in, tol = tol_in,
                                    warm_start = warm_in, positive = pos_in, random_state = rand_in,
                                    selection = sel_in )   
        model.fit(self.x_in, self.y_in)
        
        # Generate string with regression equation
        columns = len(self.x_in[0])
        self.reg_model = str("y = %8.3f"%float(model.intercept_))
        for i in range(columns):
                aux_string = str(  " + %8.3f"%float(model.coef_[i])+"x"+str(i+1)  )
                self.reg_model += aux_string
        
        # Get Multiple model 
        alphas = []
        alphas.append(float(model.intercept_))
        for i in range(columns):
            alphas.append(model.coef_[i])
        
        # Set up array with coefficients
        self.b = np.array(alphas)

    def scikit_Lars(self):
        """Function to generate a multiple regression model sklearn.linear_model.Lars"""
        
        # import libraries
        from sklearn import linear_model
        import numpy as np
                
        # Get a model
        columns = len(self.x_in[0])
        model = linear_model.Lars(n_nonzero_coefs=columns,eps = 1e-17)
        model.fit(self.x_in, self.y_in)

        # Generate string with regression equation
        self.reg_model = str("y = %8.3f"%float(model.intercept_))
        for i in range(columns):
                aux_string = str(  " + %8.3f"%float(model.coef_[i])+"x"+str(i+1)  )
                self.reg_model += aux_string
        
        # Get Multiple model 
        alphas = []
        alphas.append(float(model.intercept_))
        for i in range(columns):
            alphas.append(model.coef_[i])
        
        # Set up array with coefficients
        self.b = np.array(alphas)
        
    def scikit_SGDRegressor(self):
        """Function to generate a multiple regression model sklearn.linear_model.SGDRegressor"""
        
        # import libraries
        from sklearn import linear_model
        import numpy as np
        
        y = []
        for line in self.y_in:
            y.append(line[0])
                
        # Create and fit the model
        columns = len(self.x_in[0])
        model = linear_model.SGDRegressor(n_iter=1e8, power_t = 0.1)
        model.fit(self.x_in, y)

        # Generate string with regression equation
        self.reg_model = str("y = %8.3f"%float(model.intercept_))
        for i in range(columns):
                aux_string = str(  " + %8.3f"%float(model.coef_[i])+"x"+str(i+1)  )
                self.reg_model += aux_string
        
        
        # Get Multiple model 
        alphas = []
        alphas.append(float(model.intercept_))
        for i in range(columns):
            alphas.append(model.coef_[i])
        
        # Set up array with coefficients
        self.b = np.array(alphas)
        
    def scikit_SVR(self):
        """Function to generate a multiple regression SVR"""
        
        # import libraries
        from sklearn.svm import SVR  
        import numpy as np

        # Generate y for SVR
        y = []
        for line in self.y_in:
            y.append(line[0])
        
        # Create and fit the model
        model = SVR(kernel="linear", C=1.0, max_iter = -1)
        model.fit(self.x_in, y)
        
        # Generate string with regression equation
        columns = len(self.x_in[0])
        self.reg_model = str("y = %8.3f"%float(model.intercept_))
        for i in range(columns):
                aux_string = str(  " + %8.3f"%float(model.coef_[0][i])+"x"+str(i+1)  )
                self.reg_model += aux_string
        
        # Get Multiple model 
        alphas = []
        alphas.append(float(model.intercept_))
        for i in range(columns):
            alphas.append(model.coef_[0][i])
        
        # Set up array with coefficients
        self.b = np.array(alphas)  
    
    
       
    def basic_statistical_analysis(self):
        """Method to carry out basic statistical calculation"""
        logging.debug('entrou scikit_regress->M1190')
        # Prepare arrays for scikit-learn
        self.prep_y1()
        self.prep_x1()
        logging.debug('entrou scikit_regress->M1194')
        # Select regression method
        if self.selected_method_in == "LinearRegression":
            logging.debug('entrou scikit_regress->M1197')
            self.scikit_LinearRegression()
            logging.debug('entrou scikit_regress->M1199')
        elif self.selected_method_in == "Lasso":
            self.scikit_Lasso()
        elif self.selected_method_in == "LassoCV":  
            self.scikit_LassoCV()
        elif self.selected_method_in == "Ridge":
            self.scikit_Ridge() 
        elif self.selected_method_in == "RidgeCV":
            self.scikit_RidgeCV()
        elif self.selected_method_in == "ElasticNet":
            self.scikit_ElasticNet()
        elif self.selected_method_in == "ElasticNetCV":
            self.scikit_ElasticNetCV()
        elif self.selected_method_in == "Lars":
            self.scikit_Lars()
        elif self.selected_method_in == "SGDRegressor":
            self.scikit_SGDRegressor()
        elif self.selected_method_in == "SVR":  
            self.scikit_SVR()        
        else:
            print("Error! No such regression method!")
            return None
        logging.debug('entrou scikit_regress->M1215')
        self.gen_modelMultD2()
        logging.debug('entrou scikit_regress->M1217')
        self.calc_SE_M()
        logging.debug('entrou scikit_regress->M1219')
        
        self.nobs = self.y.shape[0]                     # Number of observations
        self.stat_analysis_of_reg_models()
        logging.debug('entrou scikit_regress->M1223')
        # estimating coefficients, and basic stats
        self.inv_xx = inv(dot(self.x.T,self.x))
        logging.debug('entrou scikit_regress->M1226')
        #xy = dot(self.x.T,self.y)
        #self.b = dot(self.inv_xx,xy)                   # Estimate coefficients
        
        # Former statistical formulas
        #self.nobs = self.y.shape[0]                     # Number of observations
        self.ncoef = self.x.shape[1]                    # Number of coefficients
        self.df_e = self.nobs - self.ncoef              # Degrees of freedom, error 
        self.df_r = self.ncoef - 1                      # Degrees of freedom, regression 
        
        try:
            self.e = self.y - dot(self.x,self.b)        # Residuals
        except:
            self.e = 1.0
    
        self.sse = dot(self.e,self.e)/self.df_e         # SSE
        
        try:
            self.se1 = sqrt(diagonal(self.sse*self.inv_xx)) # Coefficient of standard errors
            logging.debug('entrou scikit_regress->M1245')
        except:
            logging.debug('entrou scikit_regress->M1247')
            print("sqrt error:",self.sse,self.inv_xx)
        
        self.t = self.b / self.se1                      # Coefficient of  t-statistics
        self.p = (1-stats.t.cdf(abs(self.t),self.df_e))*2   # Coefficient of  p-values

        # Looping through to calculate RSS (Residual Sum of Squares) and TSS (Total Sum of Squares)
        self.rss1 = 0
        self.tss = 0
        self.aver_y = average(self.y)
        for i in range(len(self.y)):
            try:
                self.rss1 += (self.e[i])**2
            except:
                self.rss1 += 1.0
            self.tss += (self.y[i] - self.aver_y)**2 
        logging.debug('entrou scikit_regress->M1263')
        self.R2 = self.corr_p*self.corr_p                                        # model R-squared
        self.R2adj = 1-(1-self.R2)*((self.nobs-1)/(self.nobs-self.ncoef))       # adjusted R-square
        self.F = (self.R2/self.df_r) / ((1-self.R2)/self.df_e)                  # model F-statistic
        self.Fpv = 1-stats.f.cdf(self.F, self.df_r, self.df_e)                  # F-statistic p-value
        self.sd = (self.rss1/( len(self.y) - self.num_indep_var - 1 ) )**0.5    # Calculates standard deviation 
        self.Q = self.corr_p/self.sd                                            # Quality factor
    
    def summary(self):
        """ Method for returning statistical analysis to screen"""
        if str(self.corr_s) == "nan":
            self.corr_s,self.pvalue_s = 0.0,1.0
        
        # Return basic statistical analysis of regression model   
       
        return self.nobs,self.b,self.corr_p,self.R2,self.pvalue_p,self.R2adj,self.sd,self.corr_s,\
            self.pvalue_s,self.f_stat,self.se1,self.Q, self.y_pred
            