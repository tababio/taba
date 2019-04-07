# coding=utf-8
import sys


def correlation_coefficient2(listPrevisto,listExperimental): # lista1 = previsto lista2 = experimental
    """Calculates Spearman's rank correlation coeffcient between two lists"""
    #import scipy 
    from scipy.stats import spearmanr        
    from scipy.stats import pearsonr
    from scipy.stats import linregress
    #from sklearn.metrics import mean_squared_error
    from math import sqrt
    import numpy as np 
    len1 = len(listPrevisto) # previsto
    len2 = len(listExperimental) # experimental
    slope = 0 
    intercept = 0
    r_value = 0
    p_value = 0
    std_err = 0
    corr = 0
    pearson_cc = 0
    pearson_p = 0 
    std_deviation = 0   
    # Checks whether both lists have the same length
    if len1 != len2 :
        #print("\nError! Number of elements in listPrevisto != number of elements in listExperimental!")
        return None
    else:
        #rmse= str(sqrt(mean_squared_error(listPrevisto,listExperimental)))---> tem problemas no sklearn de deprecation isto faz aparecer uma nova tela de inicio do taba
        # para calcular RMSE
        previsto = np.array(listPrevisto) 
        experimental = np.array(listExperimental)
        rmse = np.sqrt(np.mean((previsto-experimental)**2))
        try:
            std_deviation = np.std(listPrevisto) # estava pegando listExperimental
        except:
            std_deviation = 0
        if std_deviation != 0:  # Avoids error message for lists where all elements are the same (standard deviation = 0)
            try:
                corr,pvalue = spearmanr(listPrevisto,listExperimental)
                corr = corr
                pvalue = pvalue
                
                try:
                    pearson_cc,pearson_p = pearsonr(listPrevisto,listExperimental)
                    slope, intercept, r_value, p_value, std_err = linregress(listPrevisto,listExperimental)
                   
                except:
                    pearson_cc = 10.0
                    pearson_p = 0
                    r_value = 0
            except:
                corr = 10.0
                pvalue = 0
                pearson_cc = 10.0
                pearson_p = 0
        else:
            corr = 10.0
            pvalue = 0
            pearson_cc = 10.0
            pearson_p = 0
        r2 = r_value**2
        ''' se for para calcular RMSE
        rms = sqrt(mean_squared_error(listPrevisto,listExperimental)) 
        print("rmse:",rms)
        from sklearn.metrics import mean_squared_error
        from math import sqrt
        '''
        return corr,pvalue,pearson_cc,pearson_p,r_value,r2, rmse, std_deviation

