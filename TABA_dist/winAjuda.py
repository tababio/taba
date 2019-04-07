#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt4 import QtGui  # Import the PyQt4 module we'll need
import interfaceAjuda # This file holds our MainWindow and all design related things

class ajuda(QtGui.QMainWindow, interfaceAjuda.Ui_MainWindow):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setFixedSize(800,680)
    def funcao1(self):
        print("OK")
    def sair(self):
        self.close()
    def chamaOutra(self):
        print("chama outra")