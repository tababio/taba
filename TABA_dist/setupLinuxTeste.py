#setup.py
# no terminal digitar 'python setupLinux.py build'
from cx_Freeze import setup, Executable
from distutils.dir_util import copy_tree
# packages'numpy','scipy','sklearn','matplotlib',
# Dependencies are automatically detected, but some modules need help.
#'numpy','scipy','sklearn','matplotlib','matplotlib.backends.backend_tkagg'
buildOptions = dict(
    packages = ['numpy','scipy','sklearn','matplotlib','matplotlib.backends.backend_tkagg'],
    excludes = ['PyQt5'],
    # We can list binary includes here if our target environment is missing them.
    bin_includes = ['libpython3.6m.so.1.0','libc.so.6'],
    include_files = ['img',],
    
  )

executables = [
    Executable(
        'tabaTeste.py',
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
copy_tree('/home/amauri/eclipse-workspace/TABA2/img', '/home/amauri/eclipse-workspace/TABA2/build/exe.linux-x86_64-3.6/img')
