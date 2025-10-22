# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Пути к TCL/TK для tkinter
tcl_path = os.path.join(sys.prefix, 'tcl')
tk_path = os.path.join(sys.prefix, 'tcl')

# Добавляем TCL/TK файлы
datas_list = [('icon.ico', '.'), ('config.ini', '.')]
if os.path.exists(tcl_path):
    tcl_tk_path = os.path.join(sys.prefix, 'tcl', 'tcl8.6')
    tk_tk_path = os.path.join(sys.prefix, 'tcl', 'tk8.6')
    if os.path.exists(tcl_tk_path):
        datas_list.append((tcl_tk_path, 'tcl'))
    if os.path.exists(tk_tk_path):
        datas_list.append((tk_tk_path, 'tk'))

a = Analysis(
    ['OLED_Auto_Brightness.py'],
    pathex=[],
    binaries=[],
    datas=datas_list,
    hiddenimports=[
        'PIL._imaging',
        'PIL._imagingft',
        'PIL._imagingmath',
        'PIL._imagingmorph',
        'PIL.Image',
        'PIL.ImageTk',
        'PIL.ImageDraw',
        'PIL.ImageFilter',
        'PIL.ImageFont',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='OLED_AutoBrightness',
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
    icon='icon.ico',
)
