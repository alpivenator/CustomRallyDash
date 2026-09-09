@echo off
setlocal
cd /d "%~dp0"

set "PY_CMD="

:: Check via Python Launcher (py -3.x) using findstr for reliable version matching
py -3.13 --version 2>nul | findstr /R /C:"^Python 3\.13" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=py -3.13"
    goto :found_py
)

py -3.12 --version 2>nul | findstr /R /C:"^Python 3\.12" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=py -3.12"
    goto :found_py
)

py -3.11 --version 2>nul | findstr /R /C:"^Python 3\.11" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=py -3.11"
    goto :found_py
)

:: Fallback: Check default python on PATH
python --version 2>nul | findstr /R /C:"^Python 3\.13" /C:"^Python 3\.12" /C:"^Python 3\.11" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=python"
    goto :found_py
)

:found_py
if "%PY_CMD%"=="" goto :no_py_supported

if exist ".venv\Scripts\python.exe" goto :venv_exists

echo.
echo [1/3] Creating virtual environment (.venv)...
%PY_CMD% -m venv .venv
if not exist ".venv\Scripts\python.exe" goto :error
goto :install_deps

:venv_exists
echo.
echo [1/3] Existing virtual environment found (.venv).

:install_deps
echo.
echo [2/3] Installing/updating Python dependencies...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :error
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo.
echo [3/3] Starting setup wizard...
".venv\Scripts\python.exe" tools\setup_wizard.py
if errorlevel 1 goto :error

echo.
pause
exit /b 0

:no_py_supported
echo.
echo Python 3.13, 3.12, or 3.11 x64 was not found. Please install a supported Python version and try again.
pause
exit /b 1

:error
echo.
echo Setup failed. Please check the error messages above.
pause
exit /b 1

