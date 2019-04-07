# -*- coding: utf-8 -*-
# primeiro instala python 3.5 depois o anaconda
# usar versoes mais atuais de scipy, numpy e scklearn
# vai ajustando lisbs até acertar
#setup.py
#18_03_2018 - falta incluir pastas, ver permissoes diretorio
# nao pode ter arquivos com espaco em branco as vezes eh lixo esquecido
#renomear imagens com caractere estranho
# no terminal digitar 'python setup.py bdist_msi'
#'packages': ["os","idna","sys","ctypes","win32con","encodings","asyncio"]
#pip install -U scikit-learn[alldeps] -> necessario para atualizar as vezes
#then the cKDTree.*.pyd will not be copied but the ckdtree.*.pyd 
#is kept in the lib\scipy\spatial of the build folder -> estou excluindo para nao ter que trocar
#para o shortcut apontar certo, editar em Anaconda3/Lib/.../cx_freeze -> windist.py Lines 58-62 (colocando no ultimo none "TARGETDIR"

from cx_Freeze import setup, Executable
#import os, numpy, scipy
import os,sys, numpy, scipy
import shutil
from pathlib import Path 
#--------------------------------------------------------------------------------------------------------------
home = str(Path.home())
home = home+"\Taba"
#--------------------------------------------------------------------------------------------------------------
if os.path.isdir("dist"):
	shutil.rmtree("dist", ignore_errors=True)
if os.path.isdir("build"):
	shutil.rmtree("build", ignore_errors=True)
#--------------------------------------------------------------------------------------------------------------
if 'bdist_msi' in sys.argv:
    sys.argv += ['--initial-target-dir', home] #pasta inicial para instalar
#--------------------------------------------------------------------------------------------------------------
os.environ['TCL_LIBRARY'] = r'C:\Users\amaur\Anaconda3\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\amaur\Anaconda3\tcl\tk8.6'
#--------------------------------------------------------------------------------------------------------------
#additional_mods = ['numpy.core._methods', 'numpy.lib.format', 'scipy.sparse.csgraph._validation','matplotlib.backends.backend_qt4agg','csv','pandas','matplotlib','numpy']
additional_mods = ['numpy',
    'numpy.core._methods',
    'numpy.lib.format',
    'scipy.sparse.csgraph._validation',
    'matplotlib.backends.backend_qt4agg',
    'csv',
   'pandas',
   'matplotlib',
   'sklearn',
   'scipy']
#-------------------------------------------------------------------
excluir = ["tkinter",
    "PyQt4.QtSql",
    "sqlite3",
    "scipy.lib.lapack.flapack",
    "PyQt4.QtNetwork",
    "PyQt4.QtScript",
    "PyQt5",
    "scipy.spatial.cKDTree"
    ]
target = Executable(
    script="taba.py",
    base="Win32GUI",
    icon="beagleIco.ico",
    shortcutName="Taba",
    shortcutDir="DesktopFolder",
    )
pacotes = ["encodings","asyncio","os","idna","sys","ctypes","win32con","numpy","sklearn","scipy"]
arquivos = ['outputFiles','inputFiles','adjustmentFunctions','ki','logs','pdbs','setsExperiments','img']
#--------------------------------------------------------------------------------------------------------------

setup(
    name = "TabaWin64",
    version = "2.0.10",
    options = {"build_exe": {
        'packages': pacotes,   
	'includes': additional_mods,   
	'include_files': arquivos, 
	'excludes': excluir,
	"optimize": 2,
        'include_msvcr': True,
    }},
    executables = [target]
    )