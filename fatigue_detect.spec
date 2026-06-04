# -*- mode: python ; coding: utf-8 -*-
"""
FatigueDetect - PyInstaller 打包配置文件
驾驶员疲劳检测系统 (PyQt5 + YOLOv8 + MediaPipe)

构建命令:
    pyinstaller fatigue_detect.spec

输出目录:
    dist/FatigueDetect/
       ├── FatigueDetect.exe   ← 主程序（启动入口）
       └── _internal/          ← 依赖库/DLL/模型文件

使用方法:
    把整个 FatigueDetect/ 文件夹分发给用户
    用户双击 FatigueDetect.exe 即可运行
"""

import os
import sys

# 项目根目录
ROOT = os.path.abspath(SPECPATH)

# 模型文件列表: (源路径, 目标子目录)
# PyInstaller 会把它们拷贝到 dist/FatigueDetect/_internal/ 下
MODEL_FILES = [
    (os.path.join(ROOT, 'eyesyawn.pt'), '.'),                     # YOLO 检测模型
    (os.path.join(ROOT, 'models', 'face_landmarker.task'), 'models'),  # MediaPipe 关键点模型
]

a = Analysis(
    ['main.pyw'],           # 入口脚本
    pathex=[ROOT],
    binaries=[],
    datas=MODEL_FILES,

    # 隐式导入（PyInstaller 自动扫描不到的动态导入）
    hiddenimports=[
        'ultralytics',
        'ultralytics.nn.tasks',
        'ultralytics.models.yolo.detect.train',
        'ultralytics.models.yolo.detect.val',
        'ultralytics.models.yolo.detect.predict',
        'ultralytics.models.yolo.classify',
        'ultralytics.models.yolo.segment',
        'torch',
        'torchvision',
        'mediapipe',
        'cv2',
        'PIL',
        'PIL.Image',
        'PIL.ImageFilter',
    ],

    hookspath=[],
    hooksconfig={},

    # 排除不必要的模块（减小打包体积）
    excludes=[
        'torch.cuda',            # 只用 CPU 推理
        'torch.backends.cuda',
        'torch.backends.cudnn',
        'IPython', 'jupyter',    # 开发工具
        'matplotlib',            # 绘图库（未使用）
        'pytest', 'unittest',    # 测试框架
        'sphinx',                # 文档生成
        'tensorboard',           # 训练可视化
    ],

    noarchive=[],
)

pyz = PYZ(a.pure)

# 可执行文件（兼容 onedir 模式）
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
    console=False,               # GUI 模式，不显示控制台
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# COLLECT 将依赖文件收集到同一目录（onedir 模式）
# 用户分发整个 FatigueDetect/ 文件夹即可
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FatigueDetect',
)
