# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew, gstreamer
block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\KENG\\monthong\\monthong\\app'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['cv2', 'enchant'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += [('THSarabunNew.ttf','.\\fonts\THSarabunNew.ttf', "fonts")]
        
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins + gstreamer.dep_bins)],
          name='MonthongApp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='monthong.ico'
          )
