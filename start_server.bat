@echo off
rem Always run from this script's folder, so "python server.py" works from anywhere.
cd /d "%~dp0"
title Electricity Consumption Analyzer - SERVER
echo Starting the server (press Ctrl+C to stop)...
echo.
python server.py %*
echo.
echo The server has stopped.
pause >nul