# coding=utf-8
def cria_dicionario(vet1,vet2):
# CC CN  CO  CS  CP  CF  CBR CCL CI  CAT
    # NN  NO  NS  NP  NF  NBR NCL NI  NAT
        # OO  OS  OP  OF  OBR OCL OI  OAT
            # SS  SP  SF  SBR SCL SI  SAT

    #Nao vai usar HOH   
    #listaDic = {'CC':'','CN':'','CO':'','CS':'','CP':'','CF':'','CBr':'','CCl':'','CI':'','CAt':'','NN':'','NO':'','NS':'','NP':'','NF':'','NBr':'','NCl':'','NI':'','NAt':'','OO':'','OS':'','OP':'','OF':'','OBr':'','OCl':'','OI':'','OAt':'','SS':'','SP':'','SF':'','SBr':'','SCl':'','SI':'','SAt':'','NHOHN':'','NHOHO':'','NHOHS':'','NHOHP':'','NHOHF':'','NHOHBR':'','NHOHCL':'','NHOHI':'','NHOHAT':'','OHOHO':'','OHOHS':'','OHOHP':'','OHOHF':'','OHOHBR':'','OHOHCL':'','OHOHI':'','OHOHAT':''}
    listaDic = {'CC':'','CN':'','CO':'','CS':'','CP':'','CF':'','CBr':'','CCl':'','CI':'','CAt':'','NN':'','NO':'','NS':'','NP':'','NF':'','NBr':'','NCl':'','NI':'','NAt':'','OO':'','OS':'','OP':'','OF':'','OBr':'','OCl':'','OI':'','OAt':'','SS':'','SP':'','SF':'','SBr':'','SCl':'','SI':'','SAt':''}    
    a= vet1.__len__()
    for i in range(a):
# CC  CN  CO  CS  CP  CF  CBR CCL CI  CAT
        if vet2[i]=="CC":
            listaDic['CC']=vet1[i] 
        if vet2[i]=="CN":
            listaDic['CN']=vet1[i]                     
        if vet2[i]=="CO":
            listaDic['CO']=vet1[i]          
        if vet2[i]=="CS":
            listaDic['CS']=vet1[i] 
        if vet2[i]=="CP":
            listaDic['CP']=vet1[i]                                 
        if vet2[i]=="CF":
            listaDic['CF']=vet1[i] 
        if vet2[i]=="CBr":
            listaDic['CBr']=vet1[i]                   
        if vet2[i]=="CCl":
            listaDic['CCl']=vet1[i]        
        if vet2[i]=="CI":
            listaDic['CI']=vet1[i]         
        if vet2[i]=="CAt":
            listaDic['CAt']=vet1[i]        
# NN  NO  NS  NP  NF  NBR NCL NI  NAT
        if vet2[i]=="NN":
            listaDic['NN']=vet1[i] 
        if vet2[i]=="NO":
            listaDic['NO']=vet1[i]         
        if vet2[i]=="NS":
            listaDic['NS']=vet1[i]   
        if vet2[i]=="NP":
            listaDic['NP']=vet1[i]                     
        if vet2[i]=="NF":
            listaDic['NF']=vet1[i] 
        if vet2[i]=="NBr":
            listaDic['NBr']=vet1[i]             
        if vet2[i]=="NCl":
            listaDic['NCl']=vet1[i]        
        if vet2[i]=="NI":
            listaDic['NI']=vet1[i]           
        if vet2[i]=="NAt":
            listaDic['NAt']=vet1[i]                              
# OO  OS  OP  OF  OBR OCL OI  OAT
        if vet2[i]=="OO":
            listaDic['OO']=vet1[i]                  
        if vet2[i]=="OS":
            listaDic['OS']=vet1[i]      
        if vet2[i]=="OP":
            listaDic['OP']=vet1[i]             
        if vet2[i]=="OF":
            listaDic['OF']=vet1[i]
        if vet2[i]=="OBr":
            listaDic['OBr']=vet1[i]                    
        if vet2[i]=="OCl":
            listaDic['OCl']=vet1[i]            
        if vet2[i]=="OI":
            listaDic['OI']=vet1[i]          
        if vet2[i]=="OAt":
            listaDic['OAt']=vet1[i]                                                                    
# SS  SP  SF  SBR SCL SI  SAT
        if vet2[i]=="SS":
            listaDic['SS']=vet1[i]
        if vet2[i]=="SP":
            listaDic['SP']=vet1[i]         
        if vet2[i]=="SF":
            listaDic['SF']=vet1[i]
        if vet2[i]=="SBr":
            listaDic['SBr']=vet1[i]            
        if vet2[i]=="SCl":
            listaDic['SCl']=vet1[i]           
        if vet2[i]=="SI":
            listaDic['SI']=vet1[i]           
        if vet2[i]=="SAt":
            listaDic['SAt']=vet1[i] 
# NHOHN  NHOHO  NHOHS  NHOHP  NHOHF  NHOHBR NHOHCL NHOHI  NHOHAT  ** para pontes de agua
#        if vet2[i]=="NHOHN":
#            listaDic['NHOHN']=vet1[i] 
#        if vet2[i]=="NHOHO":
#            listaDic['NHOHO']=vet1[i] 
#        if vet2[i]=="NHOHS":
#            listaDic['NHOHS']=vet1[i] 
#        if vet2[i]=="NHOHP":
#            listaDic['NHOHP']=vet1[i] 
#        if vet2[i]=="NHOHF":
#            listaDic['NHOHF']=vet1[i] 
#        if vet2[i]=="NHOHBR":
#            listaDic['NHOHBR']=vet1[i] 
#        if vet2[i]=="NHOHCL":
#            listaDic['NHOHCL']=vet1[i] 
#        if vet2[i]=="NHOHI":
#            listaDic['NHOHI']=vet1[i] 
#        if vet2[i]=="NHOHAT":
#            listaDic['NHOHAT']=vet1[i] 
        
# OHOHO  OHOHS  OHOHP  OHOHF  OHOHBR OHOHCL OHOHI  OHOHAT                                                                           
#        if vet2[i]=="OHOHO":
#            listaDic['OHOHO']=vet1[i]
#        if vet2[i]=="OHOHS":
#            listaDic['OHOHS']=vet1[i]   
#        if vet2[i]=="OHOHP":
#            listaDic['OHOHP']=vet1[i]   
#        if vet2[i]=="OHOHF":
#            listaDic['OHOHF']=vet1[i]   
#        if vet2[i]=="OHOHBR":
#            listaDic['OHOHBR']=vet1[i]   
#        if vet2[i]=="OHOHCL":
#            listaDic['OHOHCL']=vet1[i]   
#        if vet2[i]=="OHOHI":
#            listaDic['OHOHI']=vet1[i] 
#        if vet2[i]=="OHOHAT":
#            listaDic['OHOHAT']=vet1[i]         
    return listaDic