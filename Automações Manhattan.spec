# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['interface.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('C:\\Users\\2905043620\\Documents\\App_Manhattan\\automation_mht\\icons\\github.ico', 'icons'),
        ('C:\\Users\\2905043620\\Documents\\App_Manhattan\\automation_mht\\icons\\help.ico', 'icons'),
        ('C:\\Users\\2905043620\\Documents\\App_Manhattan\\automation_mht\\icons\\linkedin_1.ico', 'icons'),
        ('C:\\Users\\2905043620\\Documents\\App_Manhattan\\automation_mht\\icons\\mini_icon.ico', 'icons')
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
    name='Automações Manhattan',
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
    icon=['icons\\mini_icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Automações Manhattan',
)
