# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interfaceCaixaTexto.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(900, 660)
        self.textBrowser_treino = QtGui.QTextBrowser(Dialog)
        self.textBrowser_treino.setGeometry(QtCore.QRect(10, 180, 875, 140))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Bitstream Vera Sans Mono"))
        font.setPointSize(8)
        self.textBrowser_treino.setFont(font)
        self.textBrowser_treino.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.textBrowser_treino.setStyleSheet(_fromUtf8(""))
        self.textBrowser_treino.setAutoFormatting(QtGui.QTextEdit.AutoBulletList)
        self.textBrowser_treino.setObjectName(_fromUtf8("textBrowser_treino"))
        self.textBrowser_modelo = QtGui.QTextBrowser(Dialog)
        self.textBrowser_modelo.setGeometry(QtCore.QRect(10, 60, 875, 91))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.textBrowser_modelo.setFont(font)
        self.textBrowser_modelo.setObjectName(_fromUtf8("textBrowser_modelo"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 561, 17))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.textBrowser_teste = QtGui.QTextBrowser(Dialog)
        self.textBrowser_teste.setGeometry(QtCore.QRect(10, 350, 875, 140))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Bitstream Vera Sans Mono"))
        font.setPointSize(8)
        self.textBrowser_teste.setFont(font)
        self.textBrowser_teste.setStyleSheet(_fromUtf8(""))
        self.textBrowser_teste.setObjectName(_fromUtf8("textBrowser_teste"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 160, 211, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(_fromUtf8("color: rgb(0, 0, 214);"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 40, 67, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 330, 191, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(_fromUtf8("color: rgb(27, 107, 11);"))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(406, 622, 89, 25))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("img/fechar.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.textBrowser_informacoes = QtGui.QTextBrowser(Dialog)
        self.textBrowser_informacoes.setGeometry(QtCore.QRect(10, 520, 875, 91))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.textBrowser_informacoes.setFont(font)
        self.textBrowser_informacoes.setObjectName(_fromUtf8("textBrowser_informacoes"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(20, 500, 201, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Visualization", None))
        self.textBrowser_treino.setToolTip(_translate("Dialog", "You can copy and paste this data to a CSV file (ctrl + c, ctrl + v)", None))
        self.label.setText(_translate("Dialog", "Visualization", None))
        self.textBrowser_teste.setToolTip(_translate("Dialog", "You can copy and paste this data to a CSV file (ctrl + c, ctrl + v)", None))
        self.label_2.setText(_translate("Dialog", "Binding Affinity Training Set", None))
        self.label_4.setText(_translate("Dialog", "Model", None))
        self.label_3.setText(_translate("Dialog", "Binding Affinity Test Set", None))
        self.pushButton.setToolTip(_translate("Dialog", "Close this model view", None))
        self.pushButton.setStatusTip(_translate("Dialog", "Close this model view", None))
        self.pushButton.setWhatsThis(_translate("Dialog", "Close this model view", None))
        self.pushButton.setText(_translate("Dialog", "&Close", None))
        self.label_5.setText(_translate("Dialog", "Experiment Informations", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

