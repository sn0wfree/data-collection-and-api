# -*- mode: python -*-

block_cipher = None


a = Analysis(['/Users/sn0wfree/Documents/python_projects/data_collection/API/Google_trend/test/untitled folder/gui.py'],
             pathex=['/Users/sn0wfree/Documents/python_projects/data_collection/API/Google_trend/Source'],
             binaries=[],
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
          name='gui',
          debug=False,
          strip=False,
          upx=True,
          console=True )
