#setup.py
# no terminal digitar 'python setupLinux.py build'
# para debug ver gdb
from cx_Freeze import setup, Executable
from distutils.dir_util import copy_tree
# packages: 'numpy','scipy','sklearn','matplotlib', 'PyQt4','tkinter','matplotlib.backends.backend_tkagg' -> devem estar presentes se nao deverao estar instalados na maquina do usuario
# Dependencies are automatically detected, but some modules need help.
#'numpy','scipy','sklearn','matplotlib','matplotlib.backends.backend_tkagg'
# includes'libpython3.5m.so.1.0','libc.so.6' -> dár erro de fragmentação tem que apagar depois
buildOptions = dict(
    packages = ['numpy','scipy','sklearn','matplotlib', 'PyQt4','tkinter','matplotlib.backends.backend_tkagg'],
    excludes = ['PyQt5'],
    # We can list binary includes here if our target environment is missing them.
    bin_includes = [], # deve apagar antes de distribuir para nao dar erro de fragmentacao
    include_files = ['img',],
    
  )

executables = [
    Executable(
        'taba.py',
        base = None,
        targetName = 'Taba',
    )
]

setup(
    name='Taba',
    version = '0.1',
    description = 'taba linux 64',
    options = dict(build_exe = buildOptions),
    executables = executables
)
#copy_tree('/home/amauri/eclipse-workspace/TABA2/img', '/home/amauri/eclipse-workspace/TABA2/build/exe.linux-x86_64-3.6/img')
