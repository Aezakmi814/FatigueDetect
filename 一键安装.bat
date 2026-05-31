@echo off
chcp 65001 >nul
title 疲劳检测系统 - 一键安装

echo ============================================
echo   驾驶员疲劳检测系统 - 一键部署
echo   全程离线安装，无需联网
echo ============================================
echo.

:: ======== 第1步：安装 Python ========
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [1/4] 正在安装 Python 3.12（自动静默安装）...
    echo   请稍候，约需 1~2 分钟...
    echo.
    start /wait python-3.12.9-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
    echo.
    echo   Python 安装完成，正在刷新环境变量...
    for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path') do set "PATH=%%b;%%PATH%"
    ping 127.0.0.1 -n 3 >nul
) else (
    echo [1/4] Python 已安装，跳过
    python --version
)
echo.

:: ======== 第2步：创建虚拟环境 ========
echo [2/4] 创建虚拟环境...
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

:: ======== 第3步：离线安装全部依赖 ========
call venv\Scripts\activate.bat

echo [3/4] 从 packages/ 离线安装依赖包...
echo   共 45 个包，约 400MB，请耐心等待...

pip install --no-index --find-links="packages" -r requirements.txt --timeout 120
if %errorlevel% neq 0 (
    echo.
    echo [提示] 批量安装未完成，尝试逐个安装...
    for /f "usebackq tokens=*" %%i in (requirements.txt) do (
        echo   安装: %%i
        pip install "%%i" --no-index --find-links="packages" --timeout 120
    )
)
echo.

:: ======== 第4步：验证 ========
echo [4/4] 验证安装...
python -c "import ultralytics; import mediapipe; import cv2; print(\"所有依赖安装成功！\")" 2>nul
if %errorlevel% eq 0 (
    echo   [成功] 所有依赖安装成功！
) else (
    echo   [警告] 部分包可能未装完整
    echo   缺失的包启动程序时会自动提示
)
echo.
echo ============================================
echo   安装完成！
echo   以后每次运行，打开 cmd 输入：
echo     D:
echo     cd D:\Pyqt5A
echo     venv\Scripts\activate
echo     python main.pyw
echo ============================================
echo.
pause