@echo off
chcp 65001 >nul
title 驾驶员疲劳检测系统

echo 正在启动驾驶员疲劳检测系统...

:: 检查是否有虚拟环境
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

:: 启动程序
python main.pyw

:: 如果程序退出，暂停显示错误
if %errorlevel% neq 0 (
    echo.
    echo 程序异常退出，错误代码：%errorlevel%
    pause
)
