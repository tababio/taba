#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import interfaceCaixaTexto

from PyQt4 import QtGui  # Import the PyQt4 module we'll need

class textos(QtGui.QMainWindow, interfaceCaixaTexto.Ui_Dialog):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setFixedSize(900,660)
        self.window11 = None

    
    