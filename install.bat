@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>&1
if errorlevel 1 (
    echo Python Launcher not found. Please install Python 3.12 from python.org.
    pause
    exit /b 1
)

py -3.12 -c "import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 12) else 1)"
if errorlevel 1 (
    echo Python 3.12 x64 was not found. Please install Python 3.12 x64 and try again.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo.
    echo [1/3] Creating virtual environment (.venv)...
    py -3.12 -m venv .venv
    if errorlevel 1 goto :error
) else (
    echo.
    echo [1/3] Existing virtual environment found (.venv).
)

echo.
echo [2/3] Installing/updating Python dependencies...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :error
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo.
echo [3/3] Starting setup wizard...
".venv\Scripts\python.exe" setup_wizard.py
if errorlevel 1 goto :error

echo.
pause
exit /b 0

:error
echo.
echo Setup failed. Please check the error messages above.
pause
exit /b 1

