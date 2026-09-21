# -*- mode: python ; coding: utf-8 -*-
# Empacota o instalador (installer\setup_app.py) em um único exe:
#   dist\Automações Manhattan_setup_<VERSION>.exe
# Pré-requisito: build_installer\app.zip e build_installer\version_info.txt (gerados pelo build.py).

import os

ROOT = os.path.dirname(SPECPATH)  # SPECPATH = pasta installer\ ; ROOT = raiz do projeto
BUILD_DIR = os.path.join(ROOT, 'build_installer')
exec(open(os.path.join(ROOT, 'version.py'), encoding='utf-8').read())  # APP_NAME, VERSION

a = Analysis(
    [os.path.join(SPECPATH, 'setup_app.py')],
    pathex=[ROOT],  # para "from version import ..." ser encontrado
    binaries=[],
    datas=[
        (os.path.join(BUILD_DIR, 'app.zip'), '.'),
        (os.path.join(ROOT, 'readme.txt'), '.'),
        (os.path.join(ROOT, 'LICENSE.txt'), '.'),
        (os.path.join(ROOT, 'mini_icon.ico'), '.'),
        (os.path.join(ROOT, 'version.py'), '.'),
    ],
    hiddenimports=['win32com.client', 'win32com', 'pythoncom', 'pywintypes'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # o instalador não precisa das libs do app; excluir reduz o exe e o tempo de abertura
    excludes=['pandas', 'numpy', 'selenium', 'PIL', 'ttkbootstrap', 'openpyxl', 'pyautogui', 'pywinauto'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=f'{APP_NAME}_setup_{VERSION}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[os.path.join(ROOT, 'mini_icon.ico')],
    version=os.path.join(BUILD_DIR, 'version_info.txt'),
    uac_admin=False,  # manifesto asInvoker: não pede UAC nos PCs corporativos
)
