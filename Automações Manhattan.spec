# -*- mode: python ; coding: utf-8 -*-
# Build onedir do app: dist\Automações Manhattan\ (exe + _internal).
# Rodar via build.py (gera também o instalador) ou:
#   venv\Scripts\pyinstaller.exe --noconfirm --clean "Automações Manhattan.spec"

import os

# SPECPATH é definido pelo PyInstaller = pasta deste .spec (raiz do projeto)
ROOT = SPECPATH
exec(open(os.path.join(ROOT, 'version.py'), encoding='utf-8').read())  # APP_NAME, VERSION

a = Analysis(
    ['interface.py'],
    pathex=[ROOT],
    binaries=[],
    datas=[
        # interface.py lê estes arquivos da raiz de _internal (get_resource_path / basedir)
        (os.path.join(ROOT, 'github.png'), '.'),
        (os.path.join(ROOT, 'linkedin.png'), '.'),
        (os.path.join(ROOT, 'help.png'), '.'),
        (os.path.join(ROOT, 'icone.png'), '.'),
        (os.path.join(ROOT, 'mini_icon.ico'), '.'),
        # pasta icons completa (mantida como nas versões anteriores)
        (os.path.join(ROOT, 'icons', 'github.ico'), 'icons'),
        (os.path.join(ROOT, 'icons', 'help.ico'), 'icons'),
        (os.path.join(ROOT, 'icons', 'linkedin_1.ico'), 'icons'),
        (os.path.join(ROOT, 'icons', 'mini_icon.ico'), 'icons'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[os.path.join(ROOT, 'icons', 'mini_icon.ico')],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=APP_NAME,
)
