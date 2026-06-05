# -*- mode: python ; coding: utf-8 -*-
"""
FatigueDetect - PyInstaller 打包配置文件
基于 ONNX Runtime + GPU 推理，无 torch 依赖

构建命令:
    pyinstaller fatigue_detect.spec

输出:
    dist/FatigueDetect/FatigueDetect.exe  ← 双击运行
"""

import os
import sys

# ── 收集 mediapipe 所有文件 ──
from PyInstaller.utils.hooks import collect_submodules, collect_data_files, collect_dynamic_libs
MP_MODULES = collect_submodules('mediapipe')
MP_DATA    = collect_data_files('mediapipe')
MP_BINS    = collect_dynamic_libs('mediapipe')

ROOT = os.path.abspath(SPECPATH)

# 模型文件 + mediapipe 数据文件
ALL_DATA = [
    (os.path.join(ROOT, 'eyesyawn.onnx'), '.'),
    (os.path.join(ROOT, 'models', 'face_landmarker.task'), 'models'),
] + MP_DATA

ALL_BINARIES = MP_BINS

a = Analysis(
    ['main.pyw'],
    pathex=[ROOT],
    binaries=ALL_BINARIES,
    datas=ALL_DATA,

    hiddenimports=[
        # mediapipe 完整收集
    ] + MP_MODULES + [
        # PyQt5
        'PyQt5.sip',
        # 一般
        'cv2',
        'numpy',
        'PIL',
        'PIL.Image',
    ],

    hookspath=[],
    hooksconfig={},

    # 排除不必要的模块
    excludes=[
        # torch 全家桶（不再需要）
        'torch',
        'torchvision',
        'ultralytics',
        # DL 框架（完全没用）
        'paddle',
        'paddlepaddle',
        'tensorflow',
        'keras',
        # 科学计算（未使用）
        'scipy',
        'matplotlib',
        'pandas',
        # 开发工具
        'IPython',
        'jupyter',
        'jupyter_client',
        'jupyter_core',
        'notebook',
        # 测试
        'pytest',
        'unittest',
        # 文档
        'sphinx',
        # 系统
        'tkinter',
    ],

    noarchive=[],
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='FatigueDetect',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FatigueDetect',
)
