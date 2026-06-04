@echo off
chcp 65001 >nul
title FatigueDetect 打包工具
echo ============================================
echo   FatigueDetect - PyInstaller 打包脚本
echo ============================================
echo.

:: 检查虚拟环境
if exist venv\Scripts\python.exe (
    echo [1/4] 使用虚拟环境 Python...
    set PYTHON=venv\Scripts\python.exe
) else (
    echo [1/4] 使用系统 Python...
    set PYTHON=python
)

echo [2/4] 检查 PyInstaller...
%PYTHON% -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo   PyInstaller 未安装，正在安装...
    %PYTHON% -m pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple
)

echo [3/4] 清理旧构建...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

echo [4/4] 开始打包...
echo   使用配置文件: fatigue_detect.spec
echo   输出目录: dist/FatigueDetect/
echo.
%PYTHON% -m PyInstaller fatigue_detect.spec

if errorlevel 1 (
    echo.
    echo [错误] 打包失败！请检查上方错误信息。
    pause
    exit /b 1
)

echo.
echo ============================================
echo   ✅ 打包成功！
echo   可执行文件位于: dist/FatigueDetect/FatigueDetect.exe
echo ============================================
echo.
echo 注意：
echo - 需要把 dist/FatigueDetect/ 整个目录分发给用户
echo - 用户双击 FatigueDetect.exe 即可运行
echo - 首次运行可能需要添加 Windows Defender 排除项
echo.
echo 发布到 GitHub Releases:
echo   1. git tag v1.0
echo   2. git push origin v1.0
echo   3. 等待 GitHub Actions 自动构建并发布
echo.
pause
