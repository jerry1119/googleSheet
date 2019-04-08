# -*- mode: python -*-

block_cipher = None


a = Analysis(['1208_AutoUpload.py'],
             pathex=['C:\\Users\\1\\AppData\\Local\\Programs\\Python\\Python36-32\\Lib', 'C:\\Users\\shopfloornb4.F2-QCMC\\PycharmProjects\\11.1'],
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
          name='1208_AutoUpload',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
