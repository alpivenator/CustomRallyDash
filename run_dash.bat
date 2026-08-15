@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Sanal ortam bulunamadi. Once install.bat dosyasini calistirin.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" main.py
set "exit_code=%ERRORLEVEL%"

if not "%exit_code%" == "0" (
    echo.
    echo Dashboard hata koduyla kapandi: %exit_code%
    pause
)

exit /b %exit_code%
