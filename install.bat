@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>&1
if errorlevel 1 (
    echo Python Launcher bulunamadi. Python 3.12'yi python.org adresinden kurun.
    pause
    exit /b 1
)

py -3.12 -c "import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 12) else 1)"
if errorlevel 1 (
    echo Python 3.12 bulunamadi. Python 3.12 x64 kurun ve tekrar deneyin.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Sanal ortam olusturuluyor...
    py -3.12 -m venv .venv
    if errorlevel 1 goto :error
)

echo Python paketleri kuruluyor...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :error
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo Ilk kurulum sihirbazi baslatiliyor...
".venv\Scripts\python.exe" setup_wizard.py
if errorlevel 1 goto :error

echo.
echo Kurulum tamamlandi. Programi run_dash.bat ile baslatabilirsiniz.
pause
exit /b 0

:error
echo.
echo Kurulum tamamlanamadi. Yukaridaki hata mesajini kontrol edin.
pause
exit /b 1
