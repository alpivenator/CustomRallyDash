@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Error: Virtual environment not found. Please run install.bat first.
    pause
    exit /b 1
)

echo Starting Mock Telemetry Broadcaster...
echo Keep this window open and start your dashboard with run_dash.bat
echo.
".venv\Scripts\python.exe" tools\mock_telemetry.py
pause
