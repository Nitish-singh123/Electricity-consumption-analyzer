@echo off
rem Runs one test case end to end:  run_testcase.bat 1     (or 2, 3, all)
cd /d "%~dp0"
if "%~1"=="" (
    echo usage: run_testcase.bat ^<1^|2^|3^|all^>
    pause >nul
    exit /b 2
)
python testcases.py %1
echo.
echo Done. Press any key to close this window.
pause >nul