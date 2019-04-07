#! /usr/bin/python
# Program to generate a scatter plot, and find the best fit polynommial equation.
# Data for arrays x and y are read from a CSV file  

import numpy as np
import matplotlib.pyplot as plt
from func_Gerais import grava, gravaConfig
import csv
def tuning():
    diret = "./outputFiles/"
    #print("Reading resultadoTreino.csv...")
    fo1 = open(diret+"resultadoTreino.csv","r")
    # Get data
    primeira_linha = fo1.readline()
    listaLinha = primeira_linha.split(",")
    quantidadeColunas = len(listaLinha)    
    fo1.close()
    
    # Reads CSV file to get predicted and experimental data
    my_csv = np.genfromtxt (diret+'resultadoTreino.csv', delimiter=",", skip_header = 1)
    
    # Gets each column from CSV file
    colExp = quantidadeColunas-2# posicao coluna valor experimental
    colPre = quantidadeColunas-1 # posicao coluna valor predicted
    y = my_csv[:,colPre]
    x = my_csv[:,colExp]
    
    
    #Least-squares polynomial fitting 
    z = np.polyfit(x,y, 1)
    #p = np.poly1d(z)
    
    # Equation y = ax + b
    # z array has the coefficients a = z[0] and b = z[1] 
    '''
    print("a = ",z[0])
    print("b = ",z[1])
    print("Best fit polynomial equation: ",p)
    '''
    a = z[0]
    b = z[1]
    
   
    #################################
    # Read equation
    fo3 = open(diret+"melhorEquacao.csv","r")
    for line0 in fo3:
        break
    
    # Get b
    b0 = ""
    for line0 in fo3:
        for line2 in line0[17:]:
            b0 += str(line2)
        break
    coef1 = pegaPrimeiroCoef(b0)
    b0 = b0.replace(coef1,"") # retira coeficiente
    b0 = b0.replace("\n","")
    b0 = "("+b0+")"
    constante = "("+str(a)+"*"+coef1+"+"+str(b)+")"
    melhorEquacaoAjustada = constante+"+"+str(a)+"*"+str(b0)
    melhorEquacaoAjustada = melhorEquacaoAjustada.replace("+-","-")
    melhorEquacaoAjustada = melhorEquacaoAjustada.replace("\n","")
    melhorEquacaoAjustada = resolveEquacaoTuning(melhorEquacaoAjustada)
    fo4 = open(diret+"melhorEquacao.csv","r")
    texto = ""
    for line in fo4:
        line_aux = line
        if "[melhor Equacao]" in line_aux:
            line_aux ="[melhor Equacao],"+melhorEquacaoAjustada+"\n"
            
        texto = texto+line_aux
    texto = texto+"\n"+"[tuned],yes"
    diretorio = "./outputFiles/"
    grava(texto, diretorio+"melhorEquacao.csv")
    gravaConfig("melhorEquacao", melhorEquacaoAjustada)
    fo3.close()
    fo4.close()
    return True

def pegaPrimeiroCoef(equ):
    sinal = equ[0]
    equ_aux = equ.replace("-","#")
    equ_aux = equ_aux.replace("+","#")
    equList = equ_aux.split("#")
    equList = [x for x in equList if x != ''] # retira brancos
    coef = sinal+equList[0]
    return coef
def resolveEquacaoTuning(equacao): # simplifica primeira parte da equacao transformando em um unico numero
    constante = extraiConstante(equacao)
    parteVariavel = extraiParteVareiaveis(equacao, constante)
    parteVariavelResolvida = resolveParteVariavel(parteVariavel, constante)
    parteFixaResolvida = resolveParteFixa(equacao)
    eq = parteVariavelResolvida+parteFixaResolvida
    texto = posicionaConstante(eq)
    return (texto)
def extraiConstante(equacao):
    listEq = equacao.split("*")
    constante = listEq[0].replace("(","")
    return constante
def extraiParteVareiaveis(equacao,constante):
    pv = equacao.replace("("+constante,"")
    pv = pv.replace(constante+"*","#")
    pvList = pv.split("#")
    pv = pvList[1]
    return(pv)
def resolveParteVariavel(equacao,constante):
    eq = "("+equacao
    eq = eq.replace("((","")
    eq = eq.replace("))","")
    eq = eq.replace(")","#")
    listEq = eq.split("#")
    novaEq = ""
    for i in listEq:
        val = i.replace("*(","#")
        listVal = val.split("#")
        valorTermo = float(listVal[0])*float(constante)
        valorTermo = round(valorTermo,6)
        val = str(valorTermo)
        novaEq = novaEq+val+"*("+listVal[1]+")"
        novaEq = novaEq.replace(")-", "<")
        novaEq = novaEq.replace(")", ")+")
        novaEq = novaEq.replace("<", ")-")
        novaEq = novaEq.replace("++", "+")
        novaEq = novaEq.replace("+-", "-")
        novaEq = novaEq[:-1]
    return novaEq
def resolveParteFixa(equacao):
    eq = equacao.replace("(","<")
    eq = eq.replace(")","#")
    eqList = eq.split("#")
    st = (eqList[0]).replace("<","")
    valor = round(eval(st),6)
    result = str(valor)
    return result
def posicionaConstante(equacao): # posiciona constante na frente
    listEq = equacao.split(")")
    if not ("-" in listEq[0]):
        listEq[0] = "+"+listEq[0]
    tamList = len(listEq)
    texto = listEq[tamList-1]
    for i in range(tamList-1):
        texto = texto+str(listEq[i])+")"
    return texto
        
    
     
    
        
        
    1

