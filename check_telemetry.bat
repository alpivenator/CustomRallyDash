@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found (.venv\Scripts\python.exe).
    echo Please run install.bat first.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" telemetry_check.py %*
set "exit_code=%ERRORLEVEL%"

if not "%exit_code%" == "0" (
    echo.
    pause
)

exit /b %exit_code%
