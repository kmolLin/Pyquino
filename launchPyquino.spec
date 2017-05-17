# -*- mode: python -*-

block_cipher = None


a = Analysis(['launchPyquino.py'],
             pathex=['C:\\Users\\Lin\\AppData\\Local\\Programs\\Python\\Python35\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'C:\\Users\\Lin\\Desktop\\Pyquino'],
             binaries=[('core/vrep_remoAPI/remoteApi.dll', '.')],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='launchPyquino',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='icons\\usb.ico')
