@echo off
title Industral Monitoring System
cd /d "%~dp0"

rem --- check venv ---
if not exist ".venv\Scripts\python.exe" (
  echo [ERROR] Python venv not found: .venv\Scripts\python.exe
  echo Please install dependencies first.
  pause
  exit /b 1
)

set "PATH=%~dp0.venv\Scripts;%PATH%"

echo ==========================================================
echo   Industral Monitoring System
echo   URL : http://127.0.0.1:8000/
echo   API : http://127.0.0.1:8000/docs
echo   A server window will open - close it to stop the system.
echo ==========================================================

start "IMS-Server" cmd /k ".venv\Scripts\python.exe -m uvicorn src.backend.main:app --host 127.0.0.1 --port 8000"

timeout /t 4 /nobreak >nul
start "" "http://127.0.0.1:8000/"
pause
