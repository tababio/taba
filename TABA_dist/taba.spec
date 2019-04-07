# -*- mode: python -*-
# gera executavel para linux
# para executar pyinstaller --onefile taba.spec 
# problema do Gtk não mostrar corretamente os botões: sudo apt-get install build-essential linux-headers-`uname -r`
#apagar manualmente pastas dist e build quando "ignoring icon, platform not capable"
from distutils.dir_util import copy_tree
block_cipher = None

a = Analysis(['taba.py'], 
             pathex=['/home/amauri/ENV_Taba32/TABAdistLinux'],
             binaries=[],
             datas=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
	     hiddenimports=['scipy._lib.messagestream'])
a.datas += [('beagle3.png','/home/amauri/ENV_Taba32/TABAdistLinux/img/beagle3.png','DATA'),
            ('beagleIco.ico','/home/amauri/ENV_Taba32/TABAdistLinux/beagleIco.ico','DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Taba',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True,
          icon='//home//amauri//ENV_Taba32//TABAdistLinux//beagleAzul.ico')

#------------- Copia pastas e arquivos necessarios ----------------------
copy_tree('/home/amauri/ENV_Taba32/TABAdistLinux/outputFiles', '/home/amauri/ENV_Taba32/TABAdistLinux/dist/outputFiles')
copy_tree('/home/amauri/ENV_Taba32/TABAdistLinux/inputFiles', '/home/amauri/ENV_Taba32/TABAdistLinux/dist/inputFiles')
copy_tree('/home/amauri/ENV_Taba32/TABAdistLinux/adjustmentFunctions', '/home/amauri/ENV_Taba32/TABAdistLinux/dist/adjustmentFunctions')
copy_tree('/home/amauri/ENV_Taba32/TABAdistLinux/ki', '/home/amauri/ENV_Taba32/TABAdistLinux/dist/ki')
copy_tree('/home/amauri/ENV_Taba32/TABAdistLinux/logs', '/home/amauri/ENV_Taba32/TABAdistLinux/dist/logs')
copy_tree('/home/amauri/ENV_Taba32/TABAdistLinux/pdbs', '/home/amauri/ENV_Taba32/TABAdistLinux/dist/pdbs')
copy_tree('/home/amauri/ENV_Taba32/TABAdistLinux/setsExperiments', '/home/amauri/ENV_Taba32/TABAdistLinux/dist/setsExperiments')
copy_tree('/home/amauri/ENV_Taba32/TABAdistLinux/img', '/home/amauri/ENV_Taba32/TABAdistLinux/dist/img')
copy_tree('/home/amauri/ENV_Taba32/TABAdistLinux/models', '/home/amauri/ENV_Taba32/TABAdistLinux/dist/models')
copy_tree('/home/amauri/ENV_Taba32/TABAdistLinux/results', '/home/amauri/ENV_Taba32/TABAdistLinux/dist/results')
