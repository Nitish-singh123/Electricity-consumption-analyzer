@echo off
rem Runs the full automated test suite.
cd /d "%~dp0"
python -m unittest -v
echo.
echo Done. Press any key to close this window.
pause >nul