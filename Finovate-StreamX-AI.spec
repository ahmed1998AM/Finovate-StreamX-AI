# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/workspace/main.py'],
    pathex=[],
    binaries=[],
    datas=[('/workspace/ui', 'ui'), ('/workspace/assets', 'assets'), ('/workspace/core', 'core'), ('/workspace/database', 'database')],
    hiddenimports=['PySide6', 'aiohttp', 'aiosqlite', 'requests', 'langchain'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'test', 'pip'],
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
    name='Finovate-StreamX-AI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['/workspace/assets/icon.ico'],
)
