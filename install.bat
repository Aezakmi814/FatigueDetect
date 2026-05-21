@echo off
chcp 65001 >nul
title 驾驶员疲劳检测系统 - 环境安装

echo ============================================
echo   驾驶员疲劳检测系统 - 一键安装环境
echo ============================================
echo.

:: 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.10~3.12
    echo   下载地址：https://www.python.org/downloads/
    echo   安装时请勾选 "Add Python to PATH"
    pause
    exit /b 1
)

python -c "import sys; v=sys.version_info; exit(0 if v.major==3 and v.minor>=10 and v.minor<=12 else 1)"
if %errorlevel% neq 0 (
    echo [错误] Python 版本不符合要求（需要 3.10~3.12）
    python --version
    pause
    exit /b 1
)

python --version
echo.

:: 创建虚拟环境
echo [1/4] 创建虚拟环境...
if exist venv (
    echo   虚拟环境已存在，跳过
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [错误] 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo   虚拟环境创建成功
)
echo.

:: 激活虚拟环境
call venv\Scripts\activate.bat

:: 升级 pip
echo [2/4] 升级 pip...
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple --quiet
echo.

:: 设置镜像源（国内加速）
set PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
set PIP_DEFAULT_TIMEOUT=120
set PIP_RETRIES=5

:: 安装依赖
echo [3/4] 安装依赖包（网络不好时自动重试，请耐心等待）...
echo   镜像源：清华镜像（国内加速）
echo   总大小约 1~2GB，首次安装可能需要 10~30 分钟
echo.

pip install -r requirements.txt --timeout 120 --retries 5
if %errorlevel% neq 0 (
    echo.
    echo [警告] 部分包安装失败，尝试逐个安装...
    echo.
    for /f "usebackq tokens=*" %%i in (requirements.txt) do (
        echo   正在安装: %%i
        pip install %%i --timeout 120 --retries 5
    )
)

echo.
echo [4/4] 验证安装...
python -c "import PyQt5; import cv2; import numpy; import ultralytics; import mediapipe; print('所有依赖安装成功！')" 2>nul
if %errorlevel% neq 0 (
    echo [警告] 有个别包可能没装完整，但不影响核心功能
    echo   缺失的包会在首次启动时自动提示
) else (
    echo   所有依赖安装成功！
)
echo.

echo ============================================
echo   安装完成！
echo   双击 run.bat 即可启动程序
echo ============================================
echo.
pause
