@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" goto :no_venv

".venv\Scripts\python.exe" main.py
set "exit_code=%ERRORLEVEL%"

if not "%exit_code%"=="0" goto :run_error
exit /b 0

:no_venv
echo Virtual environment not found (.venv\Scripts\python.exe).
echo Please run install.bat first.
pause
exit /b 1

:run_error
echo.
echo Dashboard exited with error code: %exit_code%
pause
exit /b %exit_code%

