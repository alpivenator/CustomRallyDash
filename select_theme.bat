@echo off
setlocal
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo Error: Virtual environment not found. Please run install.bat first.
    pause
    exit /b 1
)

"venv\Scripts\python.exe" tools\theme_selector.py
pause
