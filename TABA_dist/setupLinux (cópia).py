#setup.py
# no terminal digitar 'python setup.py bdist_msi'
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but some modules need help.
buildOptions = dict(
    packages = ['numpy','matplotlib.backends.backend_tkagg' ],
    excludes = [],
    # We can list binary includes here if our target environment is missing them.
    bin_includes = [
        'libcrypto.so.1.0.0',
        'libcrypto.so.10',
        'libgssapi_krb5.so.2',
        'libk5crypto.so.3',
        'libkeyutils.so.1',
        'libssl.so.1.0.1e',
        'libssl.so.10',
        'libpython3.6m.so.1.0',
        'GLIBC_2.25'

    ]
  )

executables = [
    Executable(
        'taba.py',
        base = None,
        targetName = 'Taba',
        #copyDependentFiles = True,
        #compress = True
    )
]

setup(
    name='Taba',
    version = '0.1',
    description = 'taba linux 64',
    options = dict(build_exe = buildOptions),
    executables = executables
)
