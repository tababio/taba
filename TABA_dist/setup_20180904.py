# -*- coding: utf-8 -*-
# setup para Taba sin64
# No terminal digitar 'python setup.py bdist_msi'
#instalar o PyQt4 que est� no download
# utilizar cx_freeze 6 -> https://pypi.org/project/cx_Freeze/6.0b1/#files
# primeiro instala python 3.5 depois o Miniconda
# usar versoes mais atuais de scipy, numpy e sklearn
# vai ajustando lisbs at� acertar
# instalar a vers�o correta do Microsoft Visual C++
# alterar windist.py ->linha 62 usando 'TARGETDIR" no �ltimo NONE ->https://github.com/anthony-tuininga/cx_Freeze/issues/48
# gera instalador para windows 64 bits
# primeiro instala python 3.5 depois o Miniconda
#setup.py
#18_03_2018 - falta incluir pastas, ver permissoes diretorio
# nao pode ter arquivos com espaco em branco as vezes eh lixo esquecido
#renomear imagens com caractere estranho
#'packages': ["os","idna","sys","ctypes","win32con","encodings","asyncio"]
#pip install -U scikit-learn[alldeps] -> necessario para atualizar as vezes
#then the cKDTree.*.pyd will not be copied but the ckdtree.*.pyd 
#is kept in the lib\scipy\spatial of the build folder -> estou excluindo para nao ter que trocar
#para o shortcut apontar certo, editar em Miniconda3/Lib/.../cx_freeze -> windist.py Lines 58-62 (colocando no ultimo none "TARGETDIR"

from cx_Freeze import setup, Executable

#import os, numpy, scipy
import os,sys, numpy
import shutil
from pathlib import Path 
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')
#------------------------------------------------------------------------------------------------------------
#### As pastas copiadas devem ter apenas o arquivo null texto,
#    exceto a pasta inputFiles que dever� ter o arquivo config.csv(ver padr�o de vari�veis), ml.in e pdbsProteina.txt
#>>>>>>>>>>>>>>>>>>>>>>>>>>> verificar codigo
# +++++++++ se copiar a pasta scipy para a pasta taba funciona
#--------------------------------------------------------------------------------------------------------------
home = str(Path.home())
home = "'homepath'/Taba"
#--------------------------------------------------------------------------------------------------------------
if os.path.isdir("dist"):
	shutil.rmtree("dist", ignore_errors=True)
if os.path.isdir("build"):
	shutil.rmtree("build", ignore_errors=True)
#--------------------------------------------------------------------------------------------------------------
productName = "Taba"
#'C:\\Program Files\' -> falta permissao
if 'bdist_msi' in sys.argv:
    sys.argv += ['--initial-target-dir', 'C:\\' + productName]

#if 'bdist_msi' in sys.argv:
#    sys.argv += ['--initial-target-dir',r'C:\\Users\%USERNAME%\Taba'] #pasta inicial para instalar
#--------------------------------------------------------------------------------------------------------------

os.environ['TCL_LIBRARY'] = r'C:\Users\amaur\Miniconda3\tcl\tcl8.6'

os.environ['TK_LIBRARY'] = r'C:\Users\amaur\Miniconda3\tcl\tk8.6'
#--------------------------------------------------------------------------------------------------------------
#additional_mods = ['numpy.core._methods', 'numpy.lib.format', 'scipy.sparse.csgraph._validation','matplotlib.backends.backend_qt4agg','csv','pandas','matplotlib','numpy']

additional_mods = ['numpy.lib.format',
    'scipy.sparse.csgraph._validation',
    'csv',
    'pandas',
    'matplotlib.backends.backend_tkagg'
]
#-------------------------------------------------------------------
#
excluir = ["scipy.spatial.cKDTree",
	     "PyQt4.QtSql", "sqlite3", 
             "scipy.lib.lapack.flapack",
             "PyQt4.QtNetwork",
             "PyQt4.QtScript",
             "numpy.core._dotblas", 
             "PyQt5"]

target = Executable(
    script="taba.py",
    base="Win32GUI",
    #base = None,
    icon="beagleIco.ico",
    shortcutName="Taba",
    shortcutDir="DesktopFolder",
    )
pacotes = ["encodings","asyncio","os","idna","sys","ctypes","win32con","numpy","sklearn", "tkinter","matplotlib"]
#para copiar pasta tem que ter no Minimo 1 arquivo:pode ser nulo
arquivos = ['models','outputFiles','inputFiles',
            'adjustmentFunctions','ki',
            'logs','pdbs','setsExperiments','img',
            r'C:\Users\amaur\Miniconda3\Lib\site-packages\scipy',
os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
]
#--------------------------------------------------------------------------------------------------------------
setup(
    name = "TabaWin64",
    version = "2.0.15",
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

########################################################
'''
padrao de variaveis para o arquivo config.csv
<descricaoDataset>,novaVersao
<tipoAfinidade>,Ki
<quantidadeProteinas>,null
<quantidadeInicialProteinas>,null
<spearman>,null
<melhorEquacao>,null
<tipoMedia>,null
<comentarios>,novaVersao
<nomeExperimento>,null
<comentarios>,null
<seed35>,null
<seed45>,null
<seed60>,null
<seed75>,null
<seed90>,null 
<outlier>,no
'''