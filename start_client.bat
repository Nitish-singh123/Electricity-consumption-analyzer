@echo off
rem Run the client in the correct folder. Pass a test case number if you like.
cd /d "%~dp0"
title Electricity Consumption Analyzer - CLIENT
set CASE=%1
if "%CASE%"=="" set CASE=1
python client.py --testcase %CASE%
echo.
echo Done. Press any key to close this window.
pause >nul