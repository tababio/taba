# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interfaceAjuda.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.resize(800, 680)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("img/beagle3.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setIconSize(QtCore.QSize(32, 32))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(90, 0, 711, 77))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        self.horizontalLayoutWidget_2.setFont(font)
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.horizontalLayout_2.setMargin(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.horizontalLayout_2.addItem(spacerItem)
        self.toolButton_exit = QtGui.QToolButton(self.horizontalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(52)
        sizePolicy.setVerticalStretch(65)
        sizePolicy.setHeightForWidth(self.toolButton_exit.sizePolicy().hasHeightForWidth())
        self.toolButton_exit.setSizePolicy(sizePolicy)
        self.toolButton_exit.setMinimumSize(QtCore.QSize(52, 65))
        self.toolButton_exit.setMaximumSize(QtCore.QSize(80, 65))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        self.toolButton_exit.setFont(font)
        self.toolButton_exit.setAccessibleDescription(_fromUtf8(""))
        self.toolButton_exit.setAutoFillBackground(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("img/exit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_exit.setIcon(icon1)
        self.toolButton_exit.setIconSize(QtCore.QSize(35, 35))
        self.toolButton_exit.setAutoRepeatDelay(300)
        self.toolButton_exit.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButton_exit.setAutoRaise(False)
        self.toolButton_exit.setObjectName(_fromUtf8("toolButton_exit"))
        self.horizontalLayout_2.addWidget(self.toolButton_exit)
        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(0, 70, 800, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        self.line_2.setFont(font)
        self.line_2.setFrameShadow(QtGui.QFrame.Raised)
        self.line_2.setLineWidth(4)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.textBrowser = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(15, 100, 770, 531))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.label_27 = QtGui.QLabel(self.centralwidget)
        self.label_27.setGeometry(QtCore.QRect(0, 0, 90, 65))
        self.label_27.setMaximumSize(QtCore.QSize(90, 65))
        self.label_27.setText(_fromUtf8(""))
        self.label_27.setPixmap(QtGui.QPixmap(_fromUtf8("img/TabaComLetras.png")))
        self.label_27.setScaledContents(True)
        self.label_27.setObjectName(_fromUtf8("label_27"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.toolButton_exit, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.sair)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Tool Help", None))
        self.toolButton_exit.setToolTip(_translate("MainWindow", "<html><head/><body><p>Exit this window</p></body></html>", None))
        self.toolButton_exit.setStatusTip(_translate("MainWindow", "Exit information", None))
        self.toolButton_exit.setWhatsThis(_translate("MainWindow", "Exit", None))
        self.toolButton_exit.setAccessibleName(_translate("MainWindow", "Save", None))
        self.toolButton_exit.setText(_translate("MainWindow", "&Exit", None))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:20pt; font-weight:600;\">Help</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-size:20pt; font-weight:600;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-size:8pt; font-style:italic;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:14pt; font-weight:600;\">The Science</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">The basic idea behind the Taba is that the determinant structural features responsible for ligand-binding affinity are already somehow imprinted in the three-dimensional structures of protein-ligand complexes. When we consider an ensemble of crystallographic structures, for which ligand-binding information data is available, we have the raw data that can be used by the program Taba to generate a target-based polynomial scoring function. To build this target-based polynomial scoring function, Taba reads all structures available for a biological system of interest and calculates the average distances for each type of pair of atoms. For instance, consider intermolecular Carbon-Carbon distances, where one Carbon belongs to the protein and the second one is in the ligand. Taba calculates the average intermolecular distance for Carbon-Carbon pair. Taba considers this length as the equilibrium distance for a Carbon-Carbon pair, taking an analogy with a mass-spring system. For a given structure, displacement from this equilibrium distance generates an increase in the energy of the system. Again, we consider this naïve analogy with the mass-spring system. We modeled our protein-ligand interactions as illustrated in the figure below. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-size:8pt; font-style:italic;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\"./img/proteinaMola.png\" width=\"450\" height=\"250\" /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:8pt; font-style:italic;\">Protein-ligand as a mass-spring system. We used the atomic coordinates for the complex CDK2-roscovitine (PDB: 2A4L)(De Azevedo et al., 1997).</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\"><br />For each pair of atoms, Taba calculates the average intermolecular distances. These distances are considered the equilibrium distance for each pair of atoms. We have an equilibrium distance for Carbon-Carbon pair, another for Carbon-Oxygen pair, and so on. </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">As we previously highlighted, to apply Taba we need to have an ensemble of crystallographic structures for which ligand-binding affinity is known. This set of structures is used to train our model. In the first round, Taba calculates the average distance for each pair of atoms. On a second round, Taba applies supervised machine learning techniques to determine the relative weights of each type of pair of atoms. Taba considers intermolecular distances for each pair of atoms as explanatory variables. The response variable is the log of binding affinity, for instance, log(Ki), where Ki is the inhibition constant. Taba considers the following atoms from the protein structure: C, N, O, S, and P. For the ligands, Tabas uses the following atoms: C, N, O, S, F, Cl, Br, I,  and P.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:14pt; font-weight:600;\">The Experiment</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-size:12pt; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">For the use of the Taba, we adopt a specific concept of experiment. For the Taba, the experiment is a set of files in the Protein Data Bank (PDB) format (Berman et al., 2000), data with PDB access codes, ligand-binding information file, configuration file, transformed files for regression, and resulting files. In this way, when we refer to an experiment, we are seeing to a set of data generated for a set of PDBs of a particular protein family and their associated records. Every experiment has a specific folder with the name given by the user.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:14pt; font-weight:600;\">The tool</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-size:12pt; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">The Taba has of the main screen, where you can select the desired task and six other screens with various functionalities. In addition to the feature screens, we have a screen with help and another overall information about the Taba. To run an experiment, you should follow the order in which the buttons are on the main screen, from left to right.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:14pt; font-weight:600;\">Important</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">Most of the time there are tooltips for buttons and labels. It is quite useful to guide the user. To show tooltips, hover over the button or label.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:14pt; font-weight:600;\">The main features of the Taba</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-size:12pt; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-weight:600;\">Experiment Management: </span><span style=\" font-family:\'Ubuntu\';\">Before starting any experiment, you will need to trigger this functionality that allows us to save the current experiment, open an existing experiment or even delete the current experiment. When erasing an experiment, check the need to save it first.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-weight:600;\">Downloading PDB files: </span><span style=\" font-family:\'Ubuntu\';\">This feature allows the user to download data from the rcsb.org site (Berman et al., 2000). Taba can download two types of files: the PDB file with the atomic coordinates and the second one with the binding-affinity information. This binding affinity can be the inhibition constant (Ki),  half-maximal inhibitory concentration (IC50), half-maximal effective concentration (EC50), and dissociation constant (Kd). </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">The codes obtained on the rcsb.org site, following user-defined search criteria, must be pasted into the appropriate box on the download screen. Before this, the user must use the cleaning button to clear the code field and also the name of the experiment. After pasting the PDB file codes, the user must fill in the field with the name of the experiment using the save option. Then you can select the download button. When the physical progress bar is 100%, you may close this screen. Always when the download screen opens, the PDB codes of the current experiment will be loaded.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-weight:600;\">Generate files for regression: </span><span style=\" font-family:\'Ubuntu\';\">This functionality is essential for the generation of machine-learning models. Taba makes use of the scikit-learn library to implement supervised-machine learning techniques (Pedregosa et al., 2011). The user can select the maximum distance. Taba will consider the intermolecular distance between an atom of a ligand and the protein. The allowed values ​​in Angstroms are the following: 3.5, 4.5, 6.0, 7.5, and 9 Å. This feature will randomly generate two file sets, one for training and another for testing. For this, the user can select the seed that will generate this randomness. For each dataset (training and test) four files will be generated to be selected later for regression. Taba uses the binding information from three other databases: PDBbind (Wang et al., 2004), BindingDB( Liu et al., 2007), and Binding MOAD (Hu et al., 2005). The fourth file type groups these three together.  </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:14pt; font-weight:600;\">Recommendation</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">When you use a different version of taba, new experiments should be generated. Old experiments can generate errors.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">Sometimes, when we select a larger number of variables to compose the regression equation, linear regression methods may not return results. In this case, we must select a smaller number of variables.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">The choice of many variables to compose the regression equation may require a very long processing time. This processing time can reach tens of hours in some cases.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-size:14pt; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:14pt; font-weight:600;\">Use</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">You have to use the buttons in sequence, from the second button (&quot;PDB&quot;) to the sixth button (&quot;Experiment&quot;). This way, you will prepare the data and execute the experiment.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">The icon below means something is in progress and you have to wait:</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\"./img/gifTempo.gif\" width=\"50\" height=\"50\" /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">The icon below means a good result:</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\"./img/setaCima.png\" width=\"50\" height=\"50\" /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">The icon below means a bad result:</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\"./img/setaBaixo.png\" width=\"50\" height=\"50\" /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">The icon below shows the expected duration of execution of the method. From 50%, the evolution is much faster in each method:</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\"./img/tempo.png\" width=\"50\" height=\"50\" /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\"./img/beagle.png\" width=\"360\" height=\"300\" /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:12pt; font-weight:600;\">References</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-size:12pt; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">Berman, H.M.; Westbrook, J.; Feng, Z.; Gilliland, G.; Bhat, T.N.; Weissig, H.; Shindyalov, I.N.; Bourne, P.E. The Protein Data Bank. Nucleic Acids Res., 2000, 28(1), 235-242.   </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">Hu, L.; Benson, M.L.; Smith, R.D.; Lerner, M.G.; Carlson, H.A. Binding MOAD (Mother Of All Databases). Proteins: Struct. Funct. Genet., 2005, 60(3):333-340.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">De Azevedo WF, Leclerc S, Meijer L, Havlicek L, Strnad M, Kim SH. Inhibition of cyclin-dependent kinases by purine analogues: crystal structure of human cdk2 complexed with roscovitine. Eur J Biochem. 1997; 243(1-2): 518-26. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">Liu, T.; Lin, Y.; Wen, X.; Jorrisen, R.N.; Gilson, M.K. BindingDB: a web-accessible database of experimentally determined protein-ligand binding affinities. Nucleic Acids Res., 2007, 35(Database issue), D198-201.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">Pedregosa F, Varoquaux G, Gramfort A, Michel V, Thirion B, Grisel O, Blondel M, Prettenhofer P, Weiss R, Dubourg V, Verplas J, Passos A, Cournapeau D, Brucher M, Perrot M, Duchesnay E. Scikit-learn: Machine Learning in Python. J Mach Learn Res. 2011; 12: 2825-2830.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\';\">Wang, R.; Fang, X.; Lu, Y.; Wang, S. The PDBbind Database: Collection of Binding Affinities for Protein-Ligand Complexes with Known Three-Dimensional Structures. J. Med. Chem., 2004, 47(12), 2977-2980.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\';\"><br /></p></body></html>", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

