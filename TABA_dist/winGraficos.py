#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import interfaceGraficos
import sys

from PyQt4 import QtGui  # Import the PyQt4 module we'll need
import interfaceCorrelacao
from func_Gerais import get_arquivosSf, get_listaColunasDistancia,converteStringDeltaG, grava
from func_calculaCorrelacao import correlation_coefficient2 
from func_TestaEquacao import geraCalculoPelaFormula
from func_MelhorEquacao import melhor
from func_Gerais import grava, pegaConfig, gravaConfig, leCsvPulaLinha,pegaPosicaoExpPred
from func_manipulaArquivos import arquivosNaPastaModels, apagaArquivo
import numpy as np
import matplotlib.pyplot as plt
import csv


class graficos(QtGui.QMainWindow, interfaceGraficos.Ui_MainWindowGraficos):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setFixedSize(800,520)
        self.window11 = None
        self.reduzTeste = False;
        self.reduzTreino = False;
        self.lineEdit_minimoXTeste.setEnabled(False)
        self.lineEdit_maximoXTeste.setEnabled(False)
        self.lineEdit_minimoYTeste.setEnabled(False)
        self.lineEdit_maximoYTeste.setEnabled(False)   
        self.lineEdit_minimoXTreino.setEnabled(False)
        self.lineEdit_maximoXTreino.setEnabled(False)
        self.lineEdit_minimoYTreino.setEnabled(False)
        self.lineEdit_maximoYTreino.setEnabled(False)
    def geraGraficoTeste(self): 
        diretorio = "./outputFiles/"
        arq = diretorio+"resultadoTeste.csv"       
        inicioX = float(self.lineEdit_minimoXTeste.text())
        fimX = float(self.lineEdit_maximoXTeste.text())
        inicioY = float(self.lineEdit_minimoYTeste.text())
        fimY = float(self.lineEdit_maximoYTeste.text())
        titulo = "Test Set Plot"
        corPonto = 'green'
        corLinha = 'black'
        self.mostraGrafico(arq, inicioX, fimX, inicioY, fimY, titulo, corPonto, corLinha, self.reduzTeste)

    def geraGraficoTreino(self):  
        diretorio = "./outputFiles/"
        arq = diretorio+"resultadoTreino.csv"
        inicioX = float(self.lineEdit_minimoXTreino.text())
        fimX = float(self.lineEdit_maximoXTreino.text())
        inicioY = float(self.lineEdit_minimoYTreino.text())
        fimY = float(self.lineEdit_maximoYTreino.text())
        titulo = "Training Set Plot"
        corPonto = 'blue'
        corLinha = 'black'
        self.mostraGrafico(arq, inicioX, fimX, inicioY, fimY, titulo, corPonto, corLinha, self.reduzTreino)
    def mostraGrafico(self,arq, inicioX, fimX, inicioY, fimY, titulo, corPonto, corLinha, reduz):
        posPre,posExp = pegaPosicaoExpPred()
        with open(arq, "r") as fo:
            next(fo) # pula cabecalho
            data = [row for row in csv.reader(fo)]
            xd = [float(row[posExp]) for row in data]
            yd = [float(row[posPre]) for row in data]            
        # sort the data
        reorder = sorted(range(len(xd)), key = lambda ii: xd[ii])
        xd = [xd[ii] for ii in reorder]
        yd = [yd[ii] for ii in reorder]
        
        # make the scatter plot
        plt.rcParams['axes.facecolor'] = '#ffffff'

        plt.scatter(xd, yd, s=50, alpha=0.5, marker='o',color= corPonto)
        if reduz:
            minimoX = float(inicioX)    
            maximoX = float(fimX)
            minimoY = float(inicioY)  
            maximoY = float(fimY)
            plt.xlim(minimoX,maximoX)
            plt.ylim(minimoY,maximoY)
        # determine best fit line
        par = np.polyfit(xd, yd, 1, full=True)

        slope=par[0][0]
        intercept=par[0][1]
        xl = [min(xd), max(xd)]
        yl = [slope*xx + intercept  for xx in xl]
    
        # coefficient of determination, plot text
        variance = np.var(yd)
        residuals = np.var([(slope*xx + intercept - yy)  for xx,yy in zip(xd,yd)])
        Rsqr = np.round(1-residuals/variance, decimals=2)
        #plt.text(0.32*max(xd)+0.32*min(xd),0.001*max(yd)+0.001*min(yd),'R2 = %0.2f'% Rsqr, fontsize=12)
        plt.title(titulo,fontsize=20)
        
        plt.xlabel("Experimental Affinity("+'R2 = %0.2f'% Rsqr+")")
        plt.ylabel("Predicted Affinity")
 
        # error bounds
        #yerr = [abs(slope*xx + intercept - yy)  for xx,yy in zip(xd,yd)]
        #par = np.polyfit(xd, yerr, 2, full=True)
        #yerrUpper = [(xx*slope+intercept)+(par[0][0]*xx**2 + par[0][1]*xx + par[0][2]) for xx,yy in zip(xd,yd)]
        #yerrLower = [(xx*slope+intercept)-(par[0][0]*xx**2 + par[0][1]*xx + par[0][2]) for xx,yy in zip(xd,yd)]
        
        plt.plot(xl, yl, '-r', color= corLinha,linewidth = 1.5)
        #plt.plot(xd, yerrLower, '--r')
        #plt.plot(xd, yerrUpper, '--r')
        plt.grid(linestyle='-', linewidth = 0.5, color='grey')
      
        plt.show(block = True)
        fo.close()    

    def inclinacaoReta(self, arq):
        with open(arq, "r") as f:
            next(f) # pula cabecalho
            data = [row for row in csv.reader(f)]
            xd = [float(row[2]) for row in data]
            yd = [float(row[1]) for row in data]
        par = np.polyfit(xd, yd, 1, full=True)
        slope=par[0][0]
        f.close()
        return slope
    def habilitaReducaoTreino(self):
        diretorio = "./outputFiles/"
        arqTreino = diretorio+"resultadoTreino.csv"
        minimo, maximo = self.minimoMaximo(arqTreino, False, 'x')
        self.lineEdit_minimoXTreino.setText(str(minimo))
        self.lineEdit_maximoXTreino.setText(str(maximo))
        minimo, maximo = self.minimoMaximo(arqTreino, False, 'y')
        self.lineEdit_minimoYTreino.setText(str(minimo))
        self.lineEdit_maximoYTreino.setText(str(maximo))
        if self.radioButton_reduzTreino.isChecked():
            self.reduzTreino = True;
            self.lineEdit_minimoXTreino.setEnabled(True)
            self.lineEdit_maximoXTreino.setEnabled(True)
            self.lineEdit_minimoYTreino.setEnabled(True)
            self.lineEdit_maximoYTreino.setEnabled(True)      
        else:
            self.reduzTreino = False;  
            self.lineEdit_minimoXTreino.setEnabled(False)
            self.lineEdit_maximoXTreino.setEnabled(False)
            self.lineEdit_minimoYTreino.setEnabled(False)
            self.lineEdit_maximoYTreino.setEnabled(False)           
    def habilitaReducaoTeste(self):
        diretorio = "./outputFiles/"
        arqTeste = diretorio+"resultadoTeste.csv"
        minimo, maximo = self.minimoMaximo(arqTeste, False, 'x')
        self.lineEdit_minimoXTeste.setText(str(minimo))
        self.lineEdit_maximoXTeste.setText(str(maximo))
        minimo, maximo = self.minimoMaximo(arqTeste, False, 'y')
        self.lineEdit_minimoYTeste.setText(str(minimo))
        self.lineEdit_maximoYTeste.setText(str(maximo))
        if self.radioButton_reduzTeste.isChecked():
            self.reduzTeste = True;  
            self.lineEdit_minimoXTeste.setEnabled(True)
            self.lineEdit_maximoXTeste.setEnabled(True)
            self.lineEdit_minimoYTeste.setEnabled(True)
            self.lineEdit_maximoYTeste.setEnabled(True)           
        else:
            self.reduzTeste = False;      
            self.lineEdit_minimoXTeste.setEnabled(False)
            self.lineEdit_maximoXTeste.setEnabled(False)
            self.lineEdit_minimoYTeste.setEnabled(False)
            self.lineEdit_maximoYTeste.setEnabled(False)     

     
    def minimoMaximo(self,arq, rev,xy):
        arquivo = open(arq, 'r')
        reader = csv.reader(arquivo)
        list = [row for row in reader]
        ultimaPosicao = len(list[0])
        if xy == 'x':
            ind = ultimaPosicao-1
        elif xy == 'y':
            ind = ultimaPosicao-2
        lista = []
        for i in list[1:]:# pula cabecalho
            lista.append(float(i[ind])) # adiciona somente a coluna de x ou y

        lista.sort(key=lambda x: x, reverse=rev) 
        indUltimo = len(lista)-1
        minimo = np.round(lista[0], decimals=0)
        maximo = np.round(lista[indUltimo], decimals=0)
        arquivo.close()
        return minimo, maximo
 
    