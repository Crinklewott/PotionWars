# -*- mode: python -*-
a = Analysis(['PotionWars.py'],
             pathex=['/home/andrew2/SP_RPGS/PotionWars'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
data_tree = Tree('data', prefix='data')
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          data_tree,
          a.zipfiles,
          a.datas,
          name='PotionWars',
          debug=False,
          strip=None,
          upx=True,
          console=True )
